#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : fast_api_admin
@File : faker_config_controller.py
@Description : 自定义 Faker 函数配置管理
               提供文件内容的读取、保存、语法校验和函数测试功能
"""
import ast
import importlib
import os
from typing import Optional, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.service.login_service import LoginService
from utils.log_util import logger
from utils.response_util import ResponseUtil

# 自定义 faker 文件路径（基于项目根目录）
# 当前文件位置: module_admin/api_testing/api_faker_func/faker_config_controller.py
# 需要向上4层到达项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CUSTOM_FAKER_FILE = os.path.join(PROJECT_ROOT, 'utils', 'api_tools', 'custom_faker.py')

fakerConfigController = APIRouter(
    prefix='/api_testing/faker_config',
    dependencies=[Depends(LoginService.get_current_user)]
)


# ======================== 请求/响应模型 ========================

class FakerConfigModel(BaseModel):
    """Faker 配置内容"""
    content: str = Field(..., description="Python 代码内容")


class FakerFunctionInfo(BaseModel):
    """函数信息"""
    name: str = Field(..., description="函数名")
    doc: Optional[str] = Field(None, description="函数文档")
    params: List[str] = Field(default_factory=list, description="参数列表")


class FakerConfigResponse(BaseModel):
    """配置响应"""
    content: str = Field(..., description="文件内容")
    functions: List[FakerFunctionInfo] = Field(default_factory=list, description="已定义的函数列表")


class ValidateResultModel(BaseModel):
    """校验结果"""
    valid: bool = Field(..., description="是否有效")
    message: str = Field(..., description="校验消息")
    functions: List[FakerFunctionInfo] = Field(default_factory=list, description="解析出的函数列表")


class TestFunctionModel(BaseModel):
    """测试函数请求"""
    function_name: str = Field(..., description="函数名")
    args: List = Field(default_factory=list, description="参数列表")


class TestFunctionResultModel(BaseModel):
    """测试函数结果"""
    success: bool = Field(..., description="是否成功")
    result: Optional[str] = Field(None, description="执行结果")
    error: Optional[str] = Field(None, description="错误信息")


# ======================== 工具函数 ========================

def parse_functions_from_code(code: str) -> List[FakerFunctionInfo]:
    """从代码中解析函数信息"""
    functions = []
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 获取参数列表
                params = []
                for arg in node.args.args:
                    param_str = arg.arg
                    params.append(param_str)

                # 获取文档字符串
                doc = ast.get_docstring(node)

                functions.append(FakerFunctionInfo(
                    name=node.name,
                    doc=doc,
                    params=params
                ))
    except SyntaxError:
        pass
    return functions


def reload_custom_faker():
    """热重载自定义 faker 模块"""
    try:
        from utils.api_tools import custom_faker
        importlib.reload(custom_faker)
        logger.info("custom_faker 模块已重新加载")
        return True
    except Exception as e:
        logger.error(f"重新加载 custom_faker 模块失败: {e}")
        return False


# ======================== API 接口 ========================

@fakerConfigController.get(
    '/content',
    response_model=FakerConfigResponse,
    summary="获取自定义 Faker 配置",
    dependencies=[Depends(CheckUserInterfaceAuth('api_testing:faker_config:query'))]
)
async def get_faker_config():
    """获取 custom_faker.py 文件内容和已定义的函数列表"""
    try:
        if not os.path.exists(CUSTOM_FAKER_FILE):
            return ResponseUtil.failure(msg="配置文件不存在")

        with open(CUSTOM_FAKER_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        functions = parse_functions_from_code(content)

        return ResponseUtil.success(data=FakerConfigResponse(
            content=content,
            functions=functions
        ))
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f"读取配置失败: {str(e)}")


@fakerConfigController.post(
    '/validate',
    response_model=ValidateResultModel,
    summary="校验代码语法",
    dependencies=[Depends(CheckUserInterfaceAuth('api_testing:faker_config:query'))]
)
async def validate_faker_config(config: FakerConfigModel):
    """校验 Python 代码语法是否正确"""
    try:
        ast.parse(config.content)
        functions = parse_functions_from_code(config.content)

        return ResponseUtil.success(data=ValidateResultModel(
            valid=True,
            message="语法校验通过",
            functions=functions
        ))
    except SyntaxError as e:
        return ResponseUtil.success(data=ValidateResultModel(
            valid=False,
            message=f"语法错误: 第 {e.lineno} 行 - {e.msg}",
            functions=[]
        ))


@fakerConfigController.post(
    '/save',
    summary="保存自定义 Faker 配置",
    dependencies=[Depends(CheckUserInterfaceAuth('api_testing:faker_config:edit'))]
)
async def save_faker_config(config: FakerConfigModel):
    """
    保存配置到 custom_faker.py 文件
    1. 语法校验
    2. 写入文件
    3. 热重载模块
    """
    try:
        # 1. 语法校验
        try:
            ast.parse(config.content)
        except SyntaxError as e:
            return ResponseUtil.failure(msg=f"语法错误: 第 {e.lineno} 行 - {e.msg}")

        # 2. 备份原文件（可选）
        backup_file = CUSTOM_FAKER_FILE + '.bak'
        if os.path.exists(CUSTOM_FAKER_FILE):
            with open(CUSTOM_FAKER_FILE, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_file, 'w', encoding='utf-8') as f:
                f.write(backup_content)

        # 3. 写入新内容
        with open(CUSTOM_FAKER_FILE, 'w', encoding='utf-8') as f:
            f.write(config.content)

        # 4. 热重载模块
        if not reload_custom_faker():
            # 重载失败，恢复备份
            if os.path.exists(backup_file):
                with open(backup_file, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                with open(CUSTOM_FAKER_FILE, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                reload_custom_faker()
            return ResponseUtil.failure(msg="模块重载失败，已恢复原配置")

        # 5. 解析函数列表
        functions = parse_functions_from_code(config.content)

        logger.info(f"Faker 配置已保存，共 {len(functions)} 个函数")
        return ResponseUtil.success(
            msg="保存成功",
            data={"functions": [f.model_dump() for f in functions]}
        )

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f"保存失败: {str(e)}")


@fakerConfigController.post(
    '/test',
    response_model=TestFunctionResultModel,
    summary="测试执行函数",
    dependencies=[Depends(CheckUserInterfaceAuth('api_testing:faker_config:query'))]
)
async def test_faker_function(test_request: TestFunctionModel):
    """测试执行指定的 faker 函数（支持内置函数和自定义函数）"""
    try:
        function_name = test_request.function_name
        args = test_request.args
        func = None

        # 1. 先从 Context 类（内置函数）中查找
        from utils.api_tools.regular_faker_data import Context
        ctx = Context()

        # 从实例获取方法（实例方法和类方法都可以通过实例调用）
        if hasattr(ctx, function_name):
            method = getattr(ctx, function_name)
            if callable(method):
                func = method

        # 2. 再从 custom_faker 模块中查找
        if func is None:
            reload_custom_faker()
            from utils.api_tools import custom_faker
            if hasattr(custom_faker, function_name):
                method = getattr(custom_faker, function_name)
                if callable(method):
                    func = method

        # 3. 函数不存在
        if func is None:
            return ResponseUtil.success(data=TestFunctionResultModel(
                success=False,
                error=f"函数 '{function_name}' 不存在"
            ))

        # 执行函数
        result = func(*args)

        return ResponseUtil.success(data=TestFunctionResultModel(
            success=True,
            result=str(result)
        ))

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.success(data=TestFunctionResultModel(
            success=False,
            error=str(e)
        ))


@fakerConfigController.get(
    '/functions',
    summary="获取所有可用函数列表",
    dependencies=[Depends(CheckUserInterfaceAuth('api_testing:faker_config:query'))]
)
async def get_all_faker_functions():
    """
    获取所有可用的 faker 函数，包括：
    1. Context 类中的静态方法
    2. custom_faker 中的自定义函数
    """
    try:
        functions = []

        # 1. 从 Context 类获取方法
        from utils.api_tools.regular_faker_data import Context
        ctx = Context()
        for name in dir(ctx):
            if not name.startswith('_') and callable(getattr(ctx, name)):
                method = getattr(ctx, name)
                doc = method.__doc__ if hasattr(method, '__doc__') else None
                functions.append({
                    'name': name,
                    'doc': doc.strip() if doc else None,
                    'source': 'builtin'
                })

        # 2. 从 custom_faker 获取函数
        reload_custom_faker()
        from utils.api_tools import custom_faker
        for name in dir(custom_faker):
            if not name.startswith('_') and callable(getattr(custom_faker, name)):
                # 排除导入的模块
                obj = getattr(custom_faker, name)
                if hasattr(obj, '__module__') and 'custom_faker' in obj.__module__:
                    doc = obj.__doc__ if hasattr(obj, '__doc__') else None
                    functions.append({
                        'name': name,
                        'doc': doc.strip() if doc else None,
                        'source': 'custom'
                    })

        return ResponseUtil.success(data=functions)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f"获取函数列表失败: {str(e)}")
