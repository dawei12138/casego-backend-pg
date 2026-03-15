#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：extract_variable_executor.py
@Author  ：david
@Date    ：2025-08-14 15:40 
"""
import re
import xml.etree.ElementTree as ET
from jsonpath import jsonpath
from lxml import etree
import asyncio

from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel, Cache_dataQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from utils.api_tools.executors.strategies import ExecutorStrategy
import time
from typing import Union
from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult

import time
import json
from typing import Union, Dict, Any
from jsonpath import jsonpath

from utils.api_tools.regular_control import advanced_template_parser


class ExtractVariableExecutor(ExecutorStrategy):
    """变量提取执行器"""

    async def execute(self, context: ExecutorContext, config: Union[SetupConfig, TeardownConfig]) -> ExecutorResult:
        start_time = time.time()
        exec_log = {}
        try:
            # 获取配置参数
            original_jsonpath = getattr(config, 'jsonpath', '')
            # 构造查询对象用于缓存变量查询
            query_object = Cache_dataQueryModel(
                environment_id=context.env_id,
                user_id=str(context.user_id)
            )
            # 替换缓存变量
            jsonpath_expr = await advanced_template_parser(original_jsonpath, context.redis_obj, query_object, variables_dict=context.parameterization)

            # 添加日志输出
            if original_jsonpath != jsonpath_expr:
                print(f"[变量提取] JSONPath 替换:")
                print(f"  原始表达式: {original_jsonpath}")
                print(f"  替换后: {jsonpath_expr}")
                print(f"  参数化变量: {context.parameterization}")

            variable_name = getattr(config, 'variable_name', '')
            extract_method = getattr(config, 'extract_variable_method', 'response_json')
            regular_expression = getattr(config, 'regular_expression', '')
            xpath_expression = getattr(config, 'xpath_expression', '')
            response_header = getattr(config, 'response_header', '')
            response_cookie = getattr(config, 'response_cookie', '')

            # JSONPath索引提取参数（仅JSON使用）
            extract_index = getattr(config, 'extract_index', None)
            extract_index_is_run = getattr(config, 'extract_index_is_run', False)

            # 参数验证
            if not variable_name:
                return ExecutorResult(
                    success=False,
                    error="变量名为空"
                )

            if not context.response:
                return ExecutorResult(
                    success=False,
                    error="响应对象为空，无法提取变量"
                )

            # 根据提取方法获取数据源 - 异步执行
            source_data = await asyncio.to_thread(
                self._get_source_data, context, extract_method
            )

            if source_data is None:
                return ExecutorResult(
                    success=False,
                    error=f"无法从 {extract_method} 获取数据源"
                )

            # 根据不同的提取方法进行提取 - 异步执行
            extracted_value = await asyncio.to_thread(
                self._extract_value,
                source_data,
                extract_method,
                jsonpath_expr,
                regular_expression,
                xpath_expression,
                response_header,
                response_cookie,
                extract_index,
                extract_index_is_run
            )

            # 保存到缓存
            await self._save_to_cache(context, variable_name, extracted_value)
            exec_log.update({variable_name: extracted_value})
            execution_time = time.time() - start_time

            return ExecutorResult(
                success=True,
                message=f"变量 {variable_name} 提取成功，值为: {extracted_value}",
                log=exec_log,
                variables={variable_name: extracted_value},
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutorResult(
                success=False,
                error=f"变量提取失败: {str(e)}",
                log=exec_log,
                execution_time=execution_time
            )

    def _get_source_data(self, context: ExecutorContext, extract_method: str) -> Any:
        """根据提取方法获取数据源"""
        try:
            if extract_method == 'response_json':
                # 响应JSON数据
                if hasattr(context.response, 'response_body') and context.response.response_body:
                    return context.response.response_body
                return {}

            elif extract_method == 'response_text':
                # 响应文本数据 (返回原始文本字符串)
                if hasattr(context.response, 'response_body'):
                    body = context.response.response_body
                    if isinstance(body, str):
                        return body
                    elif isinstance(body, dict):
                        return json.dumps(body, ensure_ascii=False)
                    else:
                        return str(body)
                return ""

            elif extract_method == 'response_xml':
                # 响应XML数据 (返回原始XML字符串)
                if hasattr(context.response, 'response_body'):
                    body = context.response.response_body
                    if isinstance(body, str):
                        return body
                    else:
                        return str(body)
                return ""

            elif extract_method == 'response_header':
                # 响应头数据 (返回响应头对象)
                if hasattr(context.response, 'response_headers') and context.response.response_headers:
                    return context.response.response_headers
                return {}

            elif extract_method == 'response_cookie':
                # 响应Cookie数据 (返回cookie对象)
                if hasattr(context.response, 'response_cookies') and context.response.response_cookies:
                    return context.response.response_cookies
                return {}

            else:
                raise ValueError(f"不支持的提取方法: {extract_method}")

        except Exception as e:
            print(f"获取数据源失败: {str(e)}")
            return None

    def _extract_value(self, source_data: Any, extract_method: str, jsonpath_expr: str = '',
                       regular_expression: str = '', xpath_expression: str = '',
                       response_header: str = '', response_cookie: str = '',
                       extract_index: int = None, extract_index_is_run: bool = False) -> str:
        """根据提取方法和表达式提取数据"""
        try:
            if extract_method == 'response_json':
                # JSON数据使用JSONPath提取，支持索引
                if not jsonpath_expr:
                    return ""
                return self._extract_value_with_jsonpath(source_data, jsonpath_expr, extract_index,
                                                         extract_index_is_run)

            elif extract_method == 'response_text':
                # 文本数据使用正则表达式提取，不使用索引
                if not regular_expression:
                    return source_data if isinstance(source_data, str) else str(source_data)
                return self._extract_value_with_regex(source_data, regular_expression)

            elif extract_method == 'response_xml':
                # XML数据使用XPath表达式提取，不使用索引
                if not xpath_expression:
                    return source_data if isinstance(source_data, str) else str(source_data)
                return self._extract_value_with_xpath(source_data, xpath_expression)

            elif extract_method == 'response_header':
                # 响应头使用键名直接提取，不使用索引
                if not response_header:
                    return ""
                return self._extract_value_from_headers(source_data, response_header)

            elif extract_method == 'response_cookie':
                # Cookie使用键名直接提取，不使用索引
                if not response_cookie:
                    return ""
                return self._extract_value_from_cookies(source_data, response_cookie)

            else:
                return ""

        except Exception as e:
            print(f"数据提取失败: {str(e)}")
            return ""

    def _extract_value_with_jsonpath(self, source_data: Any, jsonpath_expr: str,
                                     extract_index: int = None, extract_index_is_run: bool = False) -> str:
        """使用JSONPath提取数据，支持索引提取"""
        try:
            # 添加调试日志
            # print(f"[JSONPath 提取]")
            # print(f"  表达式: {jsonpath_expr}")
            print(f"  源数据类型: {type(source_data)}")
            if isinstance(source_data, dict):
                print(f"  源数据键: {list(source_data.keys())}")

            # 使用jsonpath提取数据
            result = jsonpath(source_data, jsonpath_expr)

            print(f"  提取结果: {result}")
            # print(f"  结果类型: {type(result)}")

            if result:
                # 检查是否需要进行索引提取
                if extract_index_is_run and extract_index is not None:
                    # 验证索引的有效性
                    if 0 <= extract_index < len(result):
                        extracted_value = result[extract_index]
                    else:
                        # 索引超出范围，返回空或第一个值
                        print(f"JSONPath索引 {extract_index} 超出范围 [0, {len(result) - 1}]，使用第一个值")
                        extracted_value = result[0] if result else ""
                else:
                    # 不使用索引提取，取第一个匹配的值
                    extracted_value = result[0]

                # 转换为字符串
                final_value = str(extracted_value) if extracted_value is not None else ""
                print(f"  最终值: {final_value}")
                return final_value
            else:
                # 没有匹配到数据
                print(f"  ⚠️ 未匹配到任何数据")
                return ""

        except Exception as e:
            print(f"❌ JSONPath提取失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return ""

    def _extract_value_with_regex(self, source_data: str, pattern: str) -> str:
        """使用正则表达式提取数据，不使用索引"""
        try:
            if not isinstance(source_data, str):
                source_data = str(source_data)

            # 使用search查找第一个匹配项
            match = re.search(pattern, source_data, re.DOTALL)
            if match:
                # 如果有分组，返回第一个分组，否则返回整个匹配
                if match.groups():
                    return match.group(1)
                else:
                    return match.group(0)
            else:
                return ""

        except Exception as e:
            print(f"正则表达式提取失败: {str(e)}")
            return ""

    def _extract_value_with_xpath(self, source_data: str, xpath_expr: str) -> str:
        """使用XPath表达式提取XML数据，不使用索引"""
        try:
            if not isinstance(source_data, str):
                source_data = str(source_data)

            # 尝试使用lxml解析XML
            try:
                # 解析XML
                root = etree.fromstring(source_data.encode('utf-8'))
                # 使用XPath查询
                result = root.xpath(xpath_expr)

                if result:
                    # 取第一个匹配的结果
                    selected_result = result[0]

                    # 处理不同类型的结果
                    if isinstance(selected_result, etree._Element):
                        # 如果是元素，返回文本内容
                        return selected_result.text or ""
                    elif isinstance(selected_result, (str, int, float, bool)):
                        # 如果是基本类型，直接转换为字符串
                        return str(selected_result)
                    else:
                        return str(selected_result)
                else:
                    return ""

            except etree.XMLSyntaxError:
                # 如果lxml解析失败，尝试使用标准库
                root = ET.fromstring(source_data)
                # 标准库的XPath支持有限，这里做简化处理
                elements = root.findall(xpath_expr.replace('//', './/'))
                if elements:
                    return elements[0].text or ""
                else:
                    return ""

        except Exception as e:
            print(f"XPath提取失败: {str(e)}")
            return ""

    def _extract_value_from_headers(self, headers: Any, header_key: str) -> str:
        """从响应头中使用键名直接提取数据"""
        try:
            if isinstance(headers, dict):
                # 直接通过键名获取值，支持大小写不敏感
                for key, value in headers.items():
                    if key.lower() == header_key.lower():
                        return str(value)
                # 如果没找到，返回空
                return ""
            else:
                # 如果headers不是字典，尝试转换为字符串进行搜索
                headers_str = str(headers)
                # 使用正则表达式查找 key: value 模式
                pattern = rf"{re.escape(header_key)}\s*:\s*([^\r\n]+)"
                match = re.search(pattern, headers_str, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                return ""

        except Exception as e:
            print(f"响应头提取失败: {str(e)}")
            return ""

    def _extract_value_from_cookies(self, cookies: Any, cookie_key: str) -> str:
        """从Cookie中使用键名直接提取数据"""
        try:
            if isinstance(cookies, dict):
                # 直接通过键名获取值
                return str(cookies.get(cookie_key, ""))
            else:
                # 如果cookies不是字典，尝试解析cookie字符串
                cookies_str = str(cookies)
                # 使用正则表达式查找 key=value 模式
                pattern = rf"{re.escape(cookie_key)}\s*=\s*([^;]+)"
                match = re.search(pattern, cookies_str, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                return ""

        except Exception as e:
            print(f"Cookie提取失败: {str(e)}")
            return ""

    async def _save_to_cache(self, context: ExecutorContext, variable_name: str, cache_value: str):
        """保存变量到缓存"""
        try:
            # 构造缓存查询模型
            query = Cache_dataPageQueryModel(
                cache_key=variable_name,
                environment_id=context.env_id,
                user_id=context.user_id,
                cache_value=cache_value
            )

            # 保存到Redis缓存
            await Cache_dataService.add_cache_data_services(context.redis_obj, query)

            # # 更新上下文变量
            # if not hasattr(context, 'variables') or context.variables is None:
            #     context.variables = {}
            # context.variables[variable_name] = cache_value

        except Exception as e:
            print(f"保存到缓存失败: {str(e)}")
            # 即使缓存保存失败，也不影响提取结果
            pass

    def get_supported_methods(self) -> list:
        """获取支持的提取方法列表"""
        return [
            'response_json',  # JSON数据，使用JSONPath + 索引
            'response_text',  # 文本数据，使用正则表达式
            'response_xml',  # XML数据，使用XPath
            'response_header',  # 响应头，使用键名直接获取
            'response_cookie'  # Cookie，使用键名直接获取
        ]

    async def validate_config(self, config: Union[SetupConfig, TeardownConfig]) -> bool:
        """验证配置参数 - 异步版本"""
        return await asyncio.to_thread(self._validate_config_sync, config)

    def _validate_config_sync(self, config: Union[SetupConfig, TeardownConfig]) -> bool:
        """验证配置参数 - 同步版本"""
        variable_name = getattr(config, 'variable_name', '')
        extract_method = getattr(config, 'extract_variable_method', 'response_json')
        extract_index = getattr(config, 'extract_index', None)
        extract_index_is_run = getattr(config, 'extract_index_is_run', False)

        # 变量名必填
        if not variable_name:
            return False

        # 检查提取方法是否支持
        if extract_method not in self.get_supported_methods():
            return False

        # 根据不同的提取方法验证对应的表达式/键名
        if extract_method == 'response_json':
            jsonpath_expr = getattr(config, 'jsonpath', '')
            if not jsonpath_expr:
                return False

            # 验证索引提取参数（仅JSON支持索引）
            if extract_index_is_run:
                # 如果启用了索引提取，索引必须是非负整数
                if extract_index is None or not isinstance(extract_index, int) or extract_index < 0:
                    return False

        elif extract_method == 'response_text':
            # 文本提取的正则表达式是可选的
            pass

        elif extract_method == 'response_xml':
            # XML提取的XPath表达式是可选的
            pass

        elif extract_method == 'response_header':
            response_header = getattr(config, 'response_header', '')
            if not response_header:
                return False

        elif extract_method == 'response_cookie':
            response_cookie = getattr(config, 'response_cookie', '')
            if not response_cookie:
                return False

        return True

    # 如果需要同时保留同步版本的接口，可以添加这个方法
    def validate_config_sync(self, config: Union[SetupConfig, TeardownConfig]) -> bool:
        """同步版本的验证配置参数方法"""
        return self._validate_config_sync(config)


# 使用示例：
"""
# 创建执行器实例
executor = ExtractVariableExecutor()

# 配置示例
config_examples = {
    # JSONPath 提取示例（支持索引）
    'json_extraction': {
        'variable_name': 'user_id',
        'extract_variable_method': 'response_json',
        'jsonpath': '$.data[*].id',  # 提取所有用户ID
        'extract_index': 2,          # 取第3个用户的ID (索引从0开始)
        'extract_index_is_run': True # 启用索引提取
    },

    # 正则表达式提取示例（不使用索引，返回第一个匹配）
    'regex_extraction': {
        'variable_name': 'phone_number',
        'extract_variable_method': 'response_text',
        'regular_expression': r'(\d{11})'  # 匹配11位手机号，返回第一个
    },

    # XPath 提取示例（不使用索引，返回第一个匹配）
    'xpath_extraction': {
        'variable_name': 'product_name',
        'extract_variable_method': 'response_xml',
        'xpath_expression': '//product/name/text()'  # 提取产品名称，返回第一个
    },

    # Header 提取示例（使用键名直接获取）
    'header_extraction': {
        'variable_name': 'content_type',
        'extract_variable_method': 'response_header',
        'response_header': 'Content-Type'  # 直接通过键名获取header值
    },

    # Cookie 提取示例（使用键名直接获取）
    'cookie_extraction': {
        'variable_name': 'session_id',
        'extract_variable_method': 'response_cookie',
        'response_cookie': 'JSESSIONID'  # 直接通过键名获取cookie值
    }
}

# 异步调用
async def main():
    result = await executor.execute(context, config)
    print(result)

# 运行
import asyncio
asyncio.run(main())"""
