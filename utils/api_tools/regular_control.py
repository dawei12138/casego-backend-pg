import ast
import json
import re
import datetime
import random
import importlib
from datetime import date, timedelta, datetime
from typing import Union, Dict, Any
from fastapi import Request
from jsonpath import jsonpath
from faker import Faker

from config.get_db import get_db
from config.get_redis import RedisUtil
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel, \
    Cache_dataQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from utils.api_tools.regular_faker_data import Context
from utils.api_tools import custom_faker
from utils.log_util import logger


def get_custom_faker_module():
    """获取并刷新 custom_faker 模块"""
    try:
        importlib.reload(custom_faker)
    except Exception as e:
        logger.warning(f"刷新 custom_faker 模块失败: {e}")
    return custom_faker


async def advanced_template_parser(
        template: str,
        redis,
        query_object: Cache_dataQueryModel,
        context: Union[Context, None] = None,
        variables_dict: Union[Dict[str, Any], None] = None,
        max_iterations: int = 50
) -> str:
    """
    增强版模板解析器（支持带参函数、缓存变量替换、变量赋值和嵌套解析，支持中文变量名和函数名）
    :param redis: Redis连接
    :param query_object: 查询对象，用于缓存查询
    :param template: 输入模板，支持以下格式：
        - {{variable}} : 从传入字典或缓存获取变量（优先级：字典 > redis > 保持原样）
        - {{function()}} : 执行函数
        - {{variable=function()}} : 执行函数并将结果存储到缓存变量中
        - {{中文变量}} : 支持中文变量名
        - {{中文函数()}} : 支持中文函数名
        - 支持嵌套: {{func({{inner_func()}})}} : 从内到外依次解析
    :param context: 可复用的Context实例
    :param variables_dict: 优先查找的键值对字典
    :param max_iterations: 最大迭代次数，防止无限循环（默认50）
    :return: 解析后的字符串
    """
    if not template:
        return template

    ctx = context or Context()
    var_dict = variables_dict or {}

    def parse_arguments(args_str: str) -> tuple:
        """ 安全解析函数参数（支持int/float/list/dict/str等基本类型） """
        if not args_str.strip():
            return ()
        try:
            # 处理参数字符串，确保能正确解析
            args_str = args_str.strip()
            # 确保解析结果总是元组（单参数时 ast.literal_eval('(8)') 返回 int，需要转换）
            # 添加尾逗号确保始终返回元组
            result = ast.literal_eval(f'({args_str},)')
            return result
        except (SyntaxError, ValueError) as e:
            print(f"参数解析错误: {args_str}, 错误: {e}")
            return ()

    async def execute_function(function_name: str, args_str: str = "") -> str:
        """
        执行函数调用
        :param function_name: 函数名
        :param args_str: 参数字符串
        :return: 函数执行结果
        """
        try:
            args = parse_arguments(args_str)

            # 1. 尝试 Context 类方法调用
            if hasattr(Context, function_name):
                method = getattr(Context, function_name)
                if isinstance(method, classmethod):
                    # return str()
                    value = method(*args)
                    return json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else str(value)
            # 2. 尝试 Context 实例方法调用
            if hasattr(ctx, function_name) and callable(getattr(ctx, function_name)):
                method = getattr(ctx, function_name)
                # return str()
                value = method(*args)
                return json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else str(value)
            # 3. 尝试从 custom_faker 模块中查找函数
            custom_module = get_custom_faker_module()
            if hasattr(custom_module, function_name):
                func = getattr(custom_module, function_name)
                if callable(func):
                    value = func(*args)
                    return json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else str(value)
            print(f"未找到函数: {function_name}")
            return f"{{{{{function_name}({args_str})}}}}"

        except Exception as e:
            print(f"函数调用错误 {function_name}({args_str}): {e}")
            return f"{{{{{function_name}({args_str})}}}}"

    async def save_to_cache(cache_key: str, cache_value: str) -> None:
        """
        将值保存到缓存中
        :param cache_key: 缓存键
        :param cache_value: 缓存值
        """
        try:
            cache_query = Cache_dataPageQueryModel(
                cache_key=cache_key,
                environment_id=query_object.environment_id,
                user_id=query_object.user_id,
                cache_value=cache_value
            )
            await Cache_dataService.add_cache_data_services(redis, cache_query)
            logger.info(f"已保存到缓存: {cache_key} = {cache_value}")
        except Exception as e:
            logger.info(f"保存缓存错误 {cache_key}: {e}")

    async def get_variable_value(cache_key: str) -> str:
        """
        获取变量值，优先级：字典 > redis > 保持原样
        :param cache_key: 变量键
        :return: 变量值或原模板
        """
        # 第一优先级：从传入的字典中获取
        if cache_key in var_dict:
            value = var_dict[cache_key]
            # print(f"从字典中获取变量: {cache_key} = {value}")
            return str(value)

        # 第二优先级：从redis缓存中获取
        try:
            cache_query = Cache_dataPageQueryModel(
                cache_key=cache_key,
                environment_id=query_object.environment_id,
                user_id=query_object.user_id
            )

            cache_data = await Cache_dataService.get_cachedata_by_key(
                redis=redis,
                query_object=cache_query
            )

            if cache_data is not None:
                # print(f"从Redis缓存中获取变量: {cache_key} = {cache_data}")
                return str(cache_data)
            else:
                # print(f"字典和缓存中均未找到key: {cache_key}，保持原样")
                return f"{{{{{cache_key}}}}}"

        except Exception as e:
            print(f"缓存查询错误 {cache_key}: {e}")
            return f"{{{{{cache_key}}}}}"

    async def process_single_match(variable_name: str = None, identifier: str = "", args_str: str = None) -> str:
        """
        处理单个匹配项
        :param variable_name: 变量名（用于赋值操作）
        :param identifier: 标识符（函数名或变量名）
        :param args_str: 参数字符串（如果有的话）
        :return: 处理结果
        """
        # 情况1: 变量赋值操作 {{var=func()}} 或 {{var=func(args)}}
        if variable_name is not None:
            if args_str is not None:
                # 执行函数调用
                result = await execute_function(identifier, args_str)
                # 保存到缓存
                await save_to_cache(variable_name, result)
                return result
            else:
                # 如果没有括号，说明格式错误
                print(f"赋值操作格式错误: {{variable=function()}} 中function必须有括号")
                return f"{{{{{variable_name}={identifier}}}}}"

        # 情况2: 函数调用 {{func()}} 或 {{func(args)}}
        elif args_str is not None:
            return await execute_function(identifier, args_str)

        # 情况3: 变量获取 {{variable}}
        else:
            return await get_variable_value(identifier)

    # 修改正则表达式以支持中文变量名和函数名，并支持嵌套解析
    # \u4e00-\u9fff 是中文字符的Unicode范围，涵盖绝大部分常用中文字符
    # 关键：[^{}]* 匹配不包含 { 或 } 的内容，确保匹配最内层的模板
    # 匹配格式：
    # - {{variable}} : 获取变量（支持中文）
    # - {{function()}} : 执行函数（支持中文）
    # - {{variable=function()}} : 执行函数并赋值给变量（支持中文）
    # 嵌套示例：{{func({{inner()}})}} 会先解析 {{inner()}}，再解析外层

    # 匹配最内层的 {{ }} （括号内不包含 { 或 } 的）
    inner_pattern = re.compile(r'\{\{(?:([\w\u4e00-\u9fff]+)=)?([\w\u4e00-\u9fff]+)(?:\(([^{}]*)\))?\}\}')

    result = template
    iteration = 0

    # 循环处理，每次只处理第一个匹配项，确保按照从上到下的顺序执行
    while iteration < max_iterations:
        match = inner_pattern.search(result)
        if not match:
            break

        iteration += 1
        previous_result = result  # 记录本轮开始前的结果

        # 处理第一个匹配项
        variable_name = match.group(1)  # 变量名（如果是赋值操作）
        identifier = match.group(2)  # 函数名或变量名
        args_str = match.group(3)  # 参数字符串

        # 处理匹配项
        replacement = await process_single_match(variable_name, identifier, args_str)

        # 替换原字符串
        result = result[:match.start()] + replacement + result[match.end():]

        # 如果本轮没有任何变化（变量未找到，保持原样），退出循环避免无限循环
        if result == previous_result:
            break

    if iteration >= max_iterations:
        logger.warning(f"模板解析达到最大迭代次数 {max_iterations}，可能存在无法解析的模板: {result}")

    return result


# 添加一个同步版本的解析器（用于不需要缓存的场景）
def sync_template_parser(
        template: str,
        context: Union[Context, None] = None,
        variables_dict: Union[Dict[str, Any], None] = None,
        max_iterations: int = 50
) -> str:
    """
    同步版本的模板解析器（仅支持函数调用和字典变量替换，不支持缓存变量和赋值，支持中文变量名和函数名，支持嵌套解析）
    :param template: 输入模板
    :param context: Context实例
    :param variables_dict: 变量字典
    :param max_iterations: 最大迭代次数，防止无限循环（默认50）
    :return: 解析后的字符串
    """
    if not template:
        return template

    ctx = context or Context()
    var_dict = variables_dict or {}

    def parse_arguments(args_str: str) -> tuple:
        if not args_str.strip():
            return ()
        try:
            # 确保解析结果总是元组（单参数时 ast.literal_eval('(8)') 返回 int，需要转换）
            result = ast.literal_eval(f'({args_str},)')
            return result
        except (SyntaxError, ValueError):
            return ()

    def process_function_call(identifier: str, args_str: str) -> str:
        try:
            args = parse_arguments(args_str)

            # 1. 尝试 Context 类方法调用
            if hasattr(Context, identifier):
                method = getattr(Context, identifier)
                if isinstance(method, classmethod):
                    return str(method(*args))

            # 2. 尝试 Context 实例方法调用
            if hasattr(ctx, identifier) and callable(getattr(ctx, identifier)):
                method = getattr(ctx, identifier)
                return str(method(*args))

            # 3. 尝试从 custom_faker 模块中查找函数
            custom_module = get_custom_faker_module()
            if hasattr(custom_module, identifier):
                func = getattr(custom_module, identifier)
                if callable(func):
                    return str(func(*args))

            return f"{{{{{identifier}({args_str})}}}}"

        except Exception as e:
            print(f"函数调用错误 {identifier}({args_str}): {e}")
            return f"{{{{{identifier}({args_str})}}}}"

    def get_variable_value(var_name: str) -> str:
        if var_name in var_dict:
            return str(var_dict[var_name])
        return f"{{{{{var_name}}}}}"  # 保持原样

    # 匹配最内层的 {{ }} （括号内不包含 { 或 } 的）
    # 支持变量 {{var}} 和函数调用 {{func(args)}}
    inner_pattern = re.compile(r'\{\{([\w\u4e00-\u9fff]+)(?:\(([^{}]*)\))?\}\}')

    result = template
    iteration = 0

    # 循环处理，每次只处理第一个匹配项，确保按照从上到下的顺序执行
    while iteration < max_iterations:
        match = inner_pattern.search(result)
        if not match:
            break

        iteration += 1
        previous_result = result  # 记录本轮开始前的结果

        # 处理第一个匹配项
        identifier = match.group(1)  # 函数名或变量名
        args_str = match.group(2)  # 参数字符串（可能为 None）

        if args_str is not None:
            # 函数调用 {{func(args)}}
            replacement = process_function_call(identifier, args_str)
        else:
            # 变量获取 {{variable}}
            replacement = get_variable_value(identifier)

        # 替换原字符串
        result = result[:match.start()] + replacement + result[match.end():]

        # 如果本轮没有任何变化（变量未找到，保持原样），退出循环避免无限循环
        if result == previous_result:
            break

    if iteration >= max_iterations:
        logger.warning(f"同步模板解析达到最大迭代次数 {max_iterations}，可能存在无法解析的模板: {result}")

    return result


if __name__ == '__main__':
    import asyncio


    async def main():
        db = await RedisUtil.create_redis_pool()
        try:
            # 添加测试缓存数据
            query1 = Cache_dataQueryModel(
                cache_key="test_key2",
                environment_id=1,
                user_id="1",
                cache_value="80多岁的"
            )
            await Cache_dataService.add_cache_data_services(db, query1)

            # 创建查询对象
            query = Cache_dataPageQueryModel(
                cache_key="",
                environment_id=1,
                user_id="1"
            )

            # 测试字典数据（包含中文键）
            test_dict = {
                "name": "张三",
                "age": 25,
                "city": "北京",
                "test_key1": "字典中的值111111",  # 这个会优先于Redis中的值
                "中文变量": "这是中文变量的值",
                "用户姓名": "李四",
                "年龄": 30,
                "min_val": 10,
                "max_val": 50
            }

            # 测试模板字符串（包含中文变量和函数）
            test_templates = [
                # 基本功能测试（优先从字典获取）
                "姓名: {{999}}，年龄: {{age}}，城市: {{city}}",
                "优先级测试: {{test_key3}}（应该显示字典中的值）",

                # 中文变量测试
                "中文变量测试: {{中文变量}}",
                "中文用户: {{用户姓名}}，年龄: {{年龄}}",

                # 混合测试（字典变量 + 函数调用）
                "用户{{name}}，年龄{{age}}，随机邮箱: {{get_email()}}",

                # 变量赋值测试（不受字典影响）
                "生成随机年龄: {{new_age=random_int(20,60)}}",
                "生成随机邮箱: {{user_email=get_email()}}",

                # 中文变量赋值测试
                "中文赋值: {{中文结果=random_int(1,100)}}",
                "保存中文变量: {{用户信息=get_email()}}",

                # 混合使用测试
                "字典中的姓名{{name}}，新生成的年龄{{new_age=random_int(25,45)}}岁",
                "之前保存的年龄: {{new_age}}，邮箱: {{user_email}}",
                "中文变量{{中文变量}}，中文结果: {{中文结果}}",

                # 不存在的变量测试
                "不存在的变量: {{nonexistent_var}}",
                "不存在的中文变量: {{不存在的中文变量}}",
            ]

            print("=== 异步模板解析测试（支持字典优先级和中文变量/函数）===")
            for i, template_str in enumerate(test_templates, 1):
                print(f"\n测试 {i}:")
                print(f"原始模板: {template_str}")
                result = await advanced_template_parser(template_str, db, query, variables_dict=test_dict)
                print(f"解析结果: {result}")

            # ====== 嵌套解析测试 ======
            print("\n" + "=" * 60)
            print("=== 嵌套模板解析测试 ===")
            print("=" * 60)

            nested_templates = [
                # 简单嵌套：内层函数结果作为外层参数
                ("简单嵌套", "{{random_int({{random_int(1, 10)}}, 100)}}"),

                # 变量嵌套：变量值作为函数参数
                ("变量嵌套", "{{random_int({{min_val}}, {{max_val}})}}"),

                # 双层嵌套
                ("双层嵌套", "{{random_int(0, {{random_int(50, {{random_int(80, 100)}})}})}}" ),

                # 三层嵌套（类似用户示例）
                ("三层嵌套", "{{random_int({{random_int({{random_int(0, 10)}}, 50)}}, 100)}}"),

                # 多个嵌套在同一模板中
                ("多嵌套混合", "最小值: {{random_int({{min_val}}, 30)}}，最大值: {{random_int(50, {{max_val}})}}"),

                # 嵌套赋值（外层赋值，内层计算）
                ("嵌套赋值", "{{result=random_int({{random_int(1, 10)}}, 100)}}"),

                # 中文嵌套
                ("中文嵌套", "年龄范围: {{random_int({{年龄}}, 100)}}"),
            ]

            for name, template_str in nested_templates:
                print(f"\n【{name}】")
                print(f"  原始模板: {template_str}")
                result = await advanced_template_parser(template_str, db, query, variables_dict=test_dict)
                print(f"  解析结果: {result}")

            # ====== 同步解析器嵌套测试 ======
            print("\n" + "=" * 60)
            print("=== 同步模板解析器嵌套测试 ===")
            print("=" * 60)

            sync_nested_templates = [
                ("简单嵌套", "{{random_int({{random_int(1, 10)}}, 100)}}"),
                ("变量嵌套", "{{random_int({{min_val}}, {{max_val}})}}"),
                ("双层嵌套", "{{random_int(0, {{random_int(50, {{random_int(80, 100)}})}})}}"),
            ]

            for name, template_str in sync_nested_templates:
                print(f"\n【{name}】")
                print(f"  原始模板: {template_str}")
                result = sync_template_parser(template_str, variables_dict=test_dict)
                print(f"  解析结果: {result}")

        except Exception as e:
            print(f"发生错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await db.close()


    asyncio.run(main())