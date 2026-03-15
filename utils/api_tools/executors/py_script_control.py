#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：py_script_control.py
@Author  ：david
@Date    ：2025-08-12 23:40 
"""
import time
from abc import ABC, abstractmethod
from typing import Union

from utils.api_tools.executors.strategies import ExecutorStrategy
from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult

import ast
import sys
import subprocess
import importlib
import importlib.util
import builtins
import os
import shutil
from io import StringIO
from types import ModuleType

from utils.common_util import ensure_path_sep


# ----------------------------
# 安全模块实现
# ----------------------------

class SafeOS(ModuleType):
    def __getattr__(self, name):
        forbidden_methods = ['remove', 'unlink', 'rmdir', 'removedirs']
        if name in forbidden_methods:
            raise PermissionError(f"os.{name} is disabled for security reasons")
        return super().__getattr__(name)


safe_os = SafeOS('os')
safe_os.__dict__.update(os.__dict__)  # 继承原始模块属性


class SafeShutil(ModuleType):
    def __getattr__(self, name):
        if name in ['rmtree', 'move']:
            raise PermissionError(f"shutil.{name} is disabled for security reasons")
        return super().__getattr__(name)


safe_shutil = SafeShutil('shutil')
safe_shutil.__dict__.update(shutil.__dict__)

# ----------------------------
# 导入拦截器
# ----------------------------
original_import = builtins.__import__


def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == 'os':
        return safe_os
    elif name == 'shutil':
        return safe_shutil
    return original_import(name, globals, locals, fromlist, level)


# ----------------------------
# 模块安装和检测
# ----------------------------
MODULE_PACKAGE_MAP = {
    'yaml': 'PyYAML',
    'bs4': 'beautifulsoup4',
    'sklearn': 'scikit-learn',
    'cv2': 'opencv-python',
}


def get_package_name(module_name):
    return MODULE_PACKAGE_MAP.get(module_name, module_name)


def install_module(module_name):
    package = get_package_name(module_name)
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package, '--no-cache-dir', '-i',
             'https://pypi.mirrors.ustc.edu.cn/simple'],
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


# ----------------------------
# AST解析获取导入模块
# ----------------------------
class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.modules = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.modules.add(alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.level == 0:
            self.modules.add(node.module.split('.')[0])
        self.generic_visit(node)


def get_imports(script):
    try:
        tree = ast.parse(script)
    except SyntaxError as e:
        return None, f"语法错误: {e}"

    visitor = ImportVisitor()
    try:
        visitor.visit(tree)
    except Exception as e:
        return None, f"分析导入失败: {e}"

    return visitor.modules, None


# ----------------------------
# 异步脚本模板生成器
# ----------------------------
def generate_async_script_template(user_script: str, **kwargs) -> str:
    """
    生成标准化的异步脚本模板
    用户脚本将在数据库连接上下文中执行
    """

    # 脚本初始化部分
    script_init = '''
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataQueryModel, Cache_dataPageQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from config.get_db import get_db
from config.get_redis import RedisUtil
from utils.log_util import logger
import asyncio

# print("=== 脚本执行环境初始化 ===")
print(f"传入的环境ID: {env_id}")
print(f"传入的用户ID: {user_id}")

try:
    print("成功导入动态模块")
except ImportError as e:
    print(f"导入错误: {e}")


async def set_cache(cache_key,cache_value):
    try:
        async with RedisUtil.get_redis_connection() as redis:
            query = Cache_dataQueryModel(cache_key=cache_key,
                                         environment_id=env_id, user_id=user_id,
                                         cache_value=cache_value)
            await Cache_dataService.add_cache_data_services(redis, query)
            return True
    except Exception as e:
        print(f"执行过程中发生错误: {type(e).__name__}: {str(e)}")    

async def get_cache(cache_key):
    try:
        async with RedisUtil.get_redis_connection() as redis:
            query = Cache_dataQueryModel(cache_key=cache_key,
                                         environment_id=env_id, user_id=user_id,
                                         )
            return await Cache_dataService.get_cachedata_by_key(redis, query)
    except Exception as e:
        print(f"执行过程中发生错误: {type(e).__name__}: {str(e)}")    

async def delete_cache(cache_key):
    try:
        async with RedisUtil.get_redis_connection() as redis:
            query = Cache_dataQueryModel(cache_key=cache_key,
                                         environment_id=env_id, user_id=user_id,
                                         )
            return await Cache_dataService.delete_cache_services(redis, query)
    except Exception as e:
        print(f"执行过程中发生错误: {type(e).__name__}: {str(e)}")    


async def main():
    # print("=== 开始异步主函数 ===")
    try:
        # print("Redis 连接池创建成功")
        # 获取数据库连接并在连接上下文中执行用户代码
        async for db in get_db():
            # print("数据库连接获取成功")
            print("=== 开始执行用户自定义代码 ===")
            redis = await RedisUtil.create_redis_pool()
            # ===========================================
            # 用户自定义代码将插入到这里
            # 在此上下文中，db 连接可用，redis 可用
            
'''

    # 脚本结尾部分
    script_end = '''
            # ===========================================
            break    

    except Exception as e:
        print(f"执行过程中发生错误: {type(e).__name__}: {str(e)}")
        import traceback
        print("详细错误信息:")
        traceback.print_exc()
    finally:
        print("=== 异步主函数执行完成 ===")


asyncio.run(main())
print("=== 脚本执行结束 ===")
'''

    # 处理用户脚本的缩进 - 用户代码需要在 async for db 循环内执行
    # 给用户脚本的每一行添加适当的缩进（12个空格，因为在 async for 循环内）
    user_lines = user_script.strip().split('\n')
    indented_user_script = '\n'.join(['            ' + line if line.strip() else '' for line in user_lines])

    # 组合完整脚本
    full_script = script_init + '\n' + indented_user_script + '\n' + script_end

    return full_script


# ----------------------------
# 执行器核心（异步版本）
# ----------------------------
def execute_async_py_script(user_script: str, extra_paths=None, **kwargs):
    """
    执行基于异步框架的用户脚本

    Args:
        user_script: 用户的自定义脚本代码
        extra_paths: 额外的模块搜索路径列表，用于找到项目中的自定义模块
        **kwargs: 传递给脚本的额外参数（如 env_id, user_id 等）
    """
    # 初始化执行环境
    output = StringIO()
    error_log = StringIO()
    result = {'success': False, 'logs': '', 'error': None}

    # 保存原始环境状态
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    original_builtins_import = builtins.__import__
    original_sys_path = sys.path.copy()

    # 重定向输出
    sys.stdout = output
    sys.stderr = error_log
    builtins.__import__ = safe_import

    try:
        # 处理额外路径 - 用于找到项目模块
        if extra_paths:
            # 将相对路径转换为绝对路径并添加到模块搜索路径
            absolute_paths = [ensure_path_sep(path) for path in extra_paths]
            sys.path.extend(absolute_paths)
            # print(f"添加模块搜索路径: {absolute_paths}")

        # 生成完整的异步脚本
        full_script = generate_async_script_template(user_script, **kwargs)

        # 解析依赖
        modules, err = get_imports(full_script)
        if err:
            raise RuntimeError(err)

        # 安装依赖
        if modules:
            for module in modules:
                if module in sys.builtin_module_names:
                    continue
                try:
                    importlib.import_module(module)
                except ImportError:
                    success, msg = install_module(module)
                    if not success:
                        raise RuntimeError(f"模块安装失败: {module}\n{msg}")

        # 准备安全环境
        original_builtins = builtins.__dict__.copy()
        original_builtins['__import__'] = safe_import
        original_builtins.pop('open', None)  # 禁用open函数

        safe_globals = {
            '__builtins__': original_builtins,
            'os': safe_os,
            'shutil': safe_shutil
        }

        # 添加额外的参数到全局命名空间
        safe_globals.update(kwargs)

        # 执行完整脚本
        exec(full_script, safe_globals)

    except Exception as e:
        result['error'] = f"{type(e).__name__}: {str(e)}"
    finally:
        # 恢复原始环境
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        builtins.__import__ = original_builtins_import
        sys.path = original_sys_path

        result['logs'] = output.getvalue() + error_log.getvalue()
        result['success'] = result['error'] is None

    return result


def _run_in_thread(script_content: str, env_id: int, user_id: int) -> dict:
    """在独立线程中执行脚本，避免事件循环冲突"""
    return execute_async_py_script(
        script_content,
        extra_paths=["/utils"],
        env_id=env_id,
        user_id=user_id,
        context=ExecutorContext(user_id=user_id, env_id=env_id)
    )


def execute_py_script_simple(script_content: str, env_id: int = 9999, user_id: int = 0) -> dict:
    """
    简化的Python脚本执行接口，用于公共脚本库

    Args:
        script_content: Python脚本内容
        env_id: 环境ID
        user_id: 用户ID

    Returns:
        统一格式的执行结果:
        {
            "success": bool,
            "result": Any,
            "logs": str,
            "error": str | None
        }
    """
    import concurrent.futures

    try:
        # 使用线程池执行，避免 asyncio.run() 在已有事件循环中的冲突
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_in_thread, script_content, env_id, user_id)
            exec_result = future.result(timeout=60)  # 60秒超时

        return {
            "success": exec_result.get("success", False),
            "result": None,
            "logs": exec_result.get("logs", ""),
            "error": exec_result.get("error")
        }
    except concurrent.futures.TimeoutError:
        return {
            "success": False,
            "result": None,
            "logs": "",
            "error": "脚本执行超时（60秒）"
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "logs": "",
            "error": f"{type(e).__name__}: {str(e)}"
        }


# ----------------------------
# 使用示例
# ----------------------------
if __name__ == "__main__":
    # 用户只需要编写在数据库连接上下文中执行的核心业务逻辑
    user_custom_script = """
# 用户的自定义业务逻辑代码
print(f"当前环境ID: {env_id}")
print(f"当前用户ID: {user_id}")

# 可以直接使用 db 连接
# 可以直接使用 redis 连接
# 可以使用所有已导入的服务和模型
# 示例：创建查询模型
query = Cache_dataQueryModel(cache_key=1111,
                                 environment_id=env_id, user_id=user_id,
                                 )
await Cache_dataService.get_cachedata_by_key(redis, query)
await set_cache(110,222)
print(await get_cache(110))
assert(1==2)
"""

    # 执行异步脚本
    # extra_paths 用于添加项目根目录到模块搜索路径
    result = execute_async_py_script(
        user_custom_script,
        extra_paths=[
            "/utils",  # 替换为你的项目根路径
        ],
        env_id=1,  # 传入环境 ID
        user_id=1,  # 传入用户 ID

    )

    print("\n" + "=" * 50)
    print("Execution Result:")
    print(f"Success: {result['success']}")
    print("=" * 50)
    print("Logs:")
    print(result['logs'])
    print("=" * 50)
    if result['error']:
        print(f"Error: {result['error']}")
        print("=" * 50)
