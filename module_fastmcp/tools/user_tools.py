import json
import time
from datetime import datetime
from typing import Optional, List, Any

from fastmcp import Context
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import AsyncSessionLocal
from config.enums import Request_Type
from config.get_db import get_db
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesPageQueryModel, CookiesModel
from module_admin.api_testing.api_formdata.dao.formdata_dao import FormdataDao
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataModel, FormdataPageQueryModel
from module_admin.api_testing.api_formdata.service.formdata_service import FormdataService
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersPageQueryModel, HeadersModel
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsPageQueryModel, ParamsModel
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesModel, \
    Test_casesAllParamsQueryModel
from module_admin.api_testing.api_test_cases.service.test_cases_service import Test_casesService
from utils.log_util import logger

# 导入MCP实例
from module_fastmcp.mcp_instance import mcp


# class UserResponse(BaseModel):
#     """用户响应模型"""
#     success: bool
#     message: str
#     user_id: Optional[int] = None
#
#
# class SessionData(BaseModel):
#     """会话数据模型"""
#     user_id: str
#     username: str
#     created_at: str
#     permissions: List[str] = Field(default_factory=lambda: ["read"])
#     session_id: str
#
#
# # 内存中的会话存储（生产环境应使用Redis等）
# _sessions = {}
#
#
# @mcp.tool()
# def create_user(username: str = "test_user") -> UserResponse:
#     """创建用户"""
#     try:
#         # 模拟用户创建逻辑
#         user_id = hash(username + str(datetime.now().timestamp())) % 100000
#
#         logger.info(f"创建用户: {username}, ID: {user_id}")
#
#         return UserResponse(
#             success=True,
#             message=f"用户 {username} 创建成功",
#             user_id=user_id
#         )
#     except Exception as e:
#         logger.error(f"def get_parent_redis(request: Request):
#     """获取父应用的 Redis 连接"""
#     return request.app.state.redis
#


@mcp.tool()
async def set_redis_cache(key: str, value: str, ctx: Context, ex=36000, nx=False, xx=False):
    """创建或者更新redis缓存，命名空间默认mcp_cache,也就是说你的缓存键名必须要以mcp_cache:开头，如果没有按照此要求会报错，默认过期时间是36000秒，无特殊需要不要修改默认参数"""
    try:
        # 从应用状态获取 Redis（如果需要）
        if key.startswith("mcp_cache:"):
            redis = ctx.request_context.request.app.state._state.get('redis')
            # name_key = f'{namespace}:{key}' if namespace else key
            await redis.set(key, value, ex=ex, nx=nx, xx=xx)
            redis.set(key, value)

            return f"创建或者更新缓存成功，缓存键:{key}"
        else:
            raise ValueError(f"输入 '{key}' 不是以mcp_cache:开头")
    except Exception as e:
        logger.error(f"创建或者更新缓存失败: {str(e)}")
        return f"创建或者更新缓存失败: {str(e)}"


@mcp.tool()
async def get_redis_cache(key: str, ctx: Context):
    """查询缓存，输入字符串格式的缓存键，返回缓存值，不存在的键会返回None"""
    try:
        # 从应用状态获取 Redis（如果需要）

        redis = ctx.request_context.request.app.state._state.get('redis')

        value = await redis.get(key)
        return f"{value}"
    except Exception as e:
        logger.error(f"查询缓存失败: {str(e)}")
        return f"查询缓存失败:  {str(e)}"


class FieldOperation(BaseModel):
    """
    字段操作配置
    支持的操作类型:
    - update: 更新/添加字段 (需要提供 data)
    - delete: 删除指定字段 (需要提供 keys_to_delete)
    - replace: 完全替换所有字段 (需要提供 data)
    - set_empty: 设置指定字段为空值 (需要提供 keys_to_empty)
    - clear: 清空所有字段

    支持的目标类型:
    - params: 查询参数 (URL参数)
    - headers: 请求头
    - cookies: Cookies
    - body: 请求体 (JSON 或 Form-Data，根据原用例的 request_type 自动识别)
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    operation: str = Field(description='操作类型: update/delete/replace/set_empty/clear')
    target: str = Field(description='操作目标: params/headers/cookies/body')
    data: Optional[dict] = Field(default=None, description='操作数据 (用于 update/replace)')
    keys_to_delete: Optional[List[str]] = Field(default=None, description='要删除的键列表 (用于 delete)')
    keys_to_empty: Optional[List[str]] = Field(default=None, description='要设置为空的键列表 (用于 set_empty)')


class TestCaseParams(BaseModel):
    """
    单个测试用例的参数配置
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    name: str = Field(description='测试用例名称')
    description: Optional[str] = Field(default=None, description='测试用例描述')
    operations: List[FieldOperation] = Field(description='字段操作列表，按顺序执行')


class GenerateTestCasesInput(BaseModel):
    """
    生成测试用例的输入模型
    """
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    case_id: Any = Field(description='原始测试用例ID')
    test_cases: List[TestCaseParams] = Field(description="要生成的测试用例列表")


# ==================== 辅助函数 ====================

async def _apply_field_operation(
    session: AsyncSession,
    test_case: Test_casesAllParamsQueryModel,
    operation: FieldOperation
) -> None:
    """
    应用字段操作到测试用例
    """
    target = operation.target.lower()
    op_type = operation.operation.lower()

    # 处理 params (查询参数)
    if target == "params":
        await _process_params_operation(session, test_case, operation)

    # 处理 headers (请求头)
    elif target == "headers":
        await _process_headers_operation(session, test_case, operation)

    # 处理 cookies
    elif target == "cookies":
        await _process_cookies_operation(session, test_case, operation)

    # 处理 body (请求体)
    elif target == "body":
        await _process_body_operation(session, test_case, operation)

    else:
        raise ValueError(f"不支持的目标类型: {target}")


async def _process_params_operation(
    session: AsyncSession,
    test_case: Test_casesAllParamsQueryModel,
    operation: FieldOperation
) -> None:
    """处理查询参数操作"""
    from module_admin.api_testing.api_params.dao.params_dao import ParamsDao
    from module_admin.api_testing.api_params.service.params_service import ParamsService

    case_id = test_case.case_id
    op_type = operation.operation.lower()

    if op_type == "clear":
        # 清空所有参数：将所有参数的 is_run 设为 0（软删除）
        params_list = test_case.params_list or []
        for param in params_list:
            param.is_run = 0
            await ParamsService.edit_params_services(session, param)

    elif op_type == "replace":
        # 完全替换：先将所有现有参数的 is_run 设为 0，再添加新参数（is_run=1）
        params_list = test_case.params_list or []
        for param in params_list:
            param.is_run = 0
            await ParamsService.edit_params_services(session, param)

        if operation.data:
            for key, value in operation.data.items():
                await ParamsService.add_params_services(session, ParamsModel(
                    key=str(key),
                    value=str(value),
                    case_id=case_id,
                    is_run=1  # 新增时设置 is_run=1
                ))

    elif op_type == "delete":
        # 删除指定键：将 is_run 设为 0（软删除），而不是真正删除
        if operation.keys_to_delete:
            for key in operation.keys_to_delete:
                params_list = test_case.params_list or []
                for param in params_list:
                    if param.key == key:
                        param.is_run = 0
                        await ParamsService.edit_params_services(session, param)

    elif op_type == "update":
        # 更新/添加参数
        if operation.data:
            params_list = test_case.params_list or []
            existing_keys = {param.key: param for param in params_list}

            for key, value in operation.data.items():
                if key in existing_keys:
                    # 更新现有参数：只更新 value，不修改 is_run
                    existing_param = existing_keys[key]
                    existing_param.value = str(value)
                    await ParamsService.edit_params_services(session, existing_param)
                else:
                    # 添加新参数：设置 is_run=1
                    await ParamsService.add_params_services(session, ParamsModel(
                        key=str(key),
                        value=str(value),
                        case_id=case_id,
                        is_run=1  # 新增时设置 is_run=1
                    ))

    elif op_type == "set_empty":
        # 设置指定键为空：设置值为空，确保 is_run=1
        if operation.keys_to_empty:
            params_list = test_case.params_list or []
            for param in params_list:
                if param.key in operation.keys_to_empty:
                    param.value = ""
                    param.is_run = 1  # 设置为空时确保 is_run=1
                    await ParamsService.edit_params_services(session, param)


async def _process_headers_operation(
    session: AsyncSession,
    test_case: Test_casesAllParamsQueryModel,
    operation: FieldOperation
) -> None:
    """处理请求头操作"""
    from module_admin.api_testing.api_headers.dao.headers_dao import HeadersDao
    from module_admin.api_testing.api_headers.service.headers_service import HeadersService

    case_id = test_case.case_id
    op_type = operation.operation.lower()

    if op_type == "clear":
        # 清空所有请求头：将所有请求头的 is_run 设为 0（软删除）
        headers_list = test_case.headers_list or []
        for header in headers_list:
            header.is_run = 0
            await HeadersService.edit_headers_services(session, header)

    elif op_type == "replace":
        # 完全替换：先将所有现有请求头的 is_run 设为 0，再添加新请求头（is_run=1）
        headers_list = test_case.headers_list or []
        for header in headers_list:
            header.is_run = 0
            await HeadersService.edit_headers_services(session, header)

        if operation.data:
            for key, value in operation.data.items():
                await HeadersService.add_headers_services(session, HeadersModel(
                    key=str(key),
                    value=str(value),
                    case_id=case_id,
                    is_run=1  # 新增时设置 is_run=1
                ))

    elif op_type == "delete":
        # 删除指定键：将 is_run 设为 0（软删除），而不是真正删除
        if operation.keys_to_delete:
            for key in operation.keys_to_delete:
                headers_list = test_case.headers_list or []
                for header in headers_list:
                    if header.key == key:
                        header.is_run = 0
                        await HeadersService.edit_headers_services(session, header)

    elif op_type == "update":
        # 更新/添加请求头
        if operation.data:
            headers_list = test_case.headers_list or []
            existing_keys = {header.key: header for header in headers_list}

            for key, value in operation.data.items():
                if key in existing_keys:
                    # 更新现有请求头：只更新 value，不修改 is_run
                    existing_header = existing_keys[key]
                    existing_header.value = str(value)
                    await HeadersService.edit_headers_services(session, existing_header)
                else:
                    # 添加新请求头：设置 is_run=1
                    await HeadersService.add_headers_services(session, HeadersModel(
                        key=str(key),
                        value=str(value),
                        case_id=case_id,
                        is_run=1  # 新增时设置 is_run=1
                    ))

    elif op_type == "set_empty":
        # 设置指定键为空：设置值为空，确保 is_run=1
        if operation.keys_to_empty:
            headers_list = test_case.headers_list or []
            for header in headers_list:
                if header.key in operation.keys_to_empty:
                    header.value = ""
                    header.is_run = 1  # 设置为空时确保 is_run=1
                    await HeadersService.edit_headers_services(session, header)


async def _process_cookies_operation(
    session: AsyncSession,
    test_case: Test_casesAllParamsQueryModel,
    operation: FieldOperation
) -> None:
    """处理 Cookies 操作"""
    from module_admin.api_testing.api_cookies.dao.cookies_dao import CookiesDao
    from module_admin.api_testing.api_cookies.service.cookies_service import CookiesService

    case_id = test_case.case_id
    op_type = operation.operation.lower()

    if op_type == "clear":
        # 清空所有 Cookies：将所有 Cookies 的 is_run 设为 0（软删除）
        cookies_list = test_case.cookies_list or []
        for cookie in cookies_list:
            cookie.is_run = 0
            await CookiesService.edit_cookies_services(session, cookie)

    elif op_type == "replace":
        # 完全替换：先将所有现有 Cookies 的 is_run 设为 0，再添加新 Cookies（is_run=1）
        cookies_list = test_case.cookies_list or []
        for cookie in cookies_list:
            cookie.is_run = 0
            await CookiesService.edit_cookies_services(session, cookie)

        if operation.data:
            for key, value in operation.data.items():
                await CookiesService.add_cookies_services(session, CookiesModel(
                    key=str(key),
                    value=str(value),
                    case_id=case_id,
                    is_run=1  # 新增时设置 is_run=1
                ))

    elif op_type == "delete":
        # 删除指定键：将 is_run 设为 0（软删除），而不是真正删除
        if operation.keys_to_delete:
            for key in operation.keys_to_delete:
                cookies_list = test_case.cookies_list or []
                for cookie in cookies_list:
                    if cookie.key == key:
                        cookie.is_run = 0
                        await CookiesService.edit_cookies_services(session, cookie)

    elif op_type == "update":
        # 更新/添加 Cookies
        if operation.data:
            cookies_list = test_case.cookies_list or []
            existing_keys = {cookie.key: cookie for cookie in cookies_list}

            for key, value in operation.data.items():
                if key in existing_keys:
                    # 更新现有 Cookie：只更新 value，不修改 is_run
                    existing_cookie = existing_keys[key]
                    existing_cookie.value = str(value)
                    await CookiesService.edit_cookies_services(session, existing_cookie)
                else:
                    # 添加新 Cookie：设置 is_run=1
                    await CookiesService.add_cookies_services(session, CookiesModel(
                        key=str(key),
                        value=str(value),
                        case_id=case_id,
                        is_run=1  # 新增时设置 is_run=1
                    ))

    elif op_type == "set_empty":
        # 设置指定键为空：设置值为空，确保 is_run=1
        if operation.keys_to_empty:
            cookies_list = test_case.cookies_list or []
            for cookie in cookies_list:
                if cookie.key in operation.keys_to_empty:
                    cookie.value = ""
                    cookie.is_run = 1  # 设置为空时确保 is_run=1
                    await CookiesService.edit_cookies_services(session, cookie)


async def _process_body_operation(
    session: AsyncSession,
    test_case: Test_casesAllParamsQueryModel,
    operation: FieldOperation
) -> None:
    """
    处理请求体操作（支持 JSON 和 Form-Data）

    注意：
    - JSON/XML/Raw 类型：没有 is_run 字段，直接修改 json_data
    - Form-Data 类型：有 is_run 字段，需要按照 is_run 规则处理
    """
    request_type = test_case.request_type
    case_id = test_case.case_id
    op_type = operation.operation.lower()

    # ==================== JSON/XML/Raw 类型的请求体（没有 is_run 字段）====================
    if request_type in [Request_Type.JSON, Request_Type.XML, Request_Type.Raw]:
        if op_type == "clear":
            test_case.json_data = {}

        elif op_type == "replace":
            test_case.json_data = operation.data or {}

        elif op_type == "delete":
            if operation.keys_to_delete and isinstance(test_case.json_data, dict):
                for key in operation.keys_to_delete:
                    test_case.json_data.pop(key, None)

        elif op_type == "update":
            if operation.data:
                if not isinstance(test_case.json_data, dict):
                    test_case.json_data = {}
                test_case.json_data.update(operation.data)

        elif op_type == "set_empty":
            if operation.keys_to_empty and isinstance(test_case.json_data, dict):
                for key in operation.keys_to_empty:
                    if key in test_case.json_data:
                        test_case.json_data[key] = ""

        # 保存更新
        await Test_casesService.edit_test_cases_services(session, test_case)

    # ==================== Form-Data 类型的请求体（有 is_run 字段）====================
    elif request_type in [Request_Type.Form_Data, Request_Type.x_www_form_urlencoded]:
        if op_type == "clear":
            # 清空所有表单数据：将所有表单项的 is_run 设为 0（软删除）
            formdata_list = test_case.formdata or []
            for form_item in formdata_list:
                form_item.is_run = 0
                await FormdataService.edit_formdata_services(session, form_item)

        elif op_type == "replace":
            # 完全替换：先将所有现有表单项的 is_run 设为 0，再添加新表单项（is_run=1）
            formdata_list = test_case.formdata or []
            for form_item in formdata_list:
                form_item.is_run = 0
                await FormdataService.edit_formdata_services(session, form_item)

            if operation.data:
                for key, value in operation.data.items():
                    await FormdataService.add_formdata_services(session, FormdataModel(
                        key=str(key),
                        value=str(value),
                        case_id=case_id,
                        is_run=1  # 新增时设置 is_run=1
                    ))

        elif op_type == "delete":
            # 删除指定键：将 is_run 设为 0（软删除），而不是真正删除
            if operation.keys_to_delete:
                for key in operation.keys_to_delete:
                    formdata_list = test_case.formdata or []
                    for form_item in formdata_list:
                        if form_item.key == key:
                            form_item.is_run = 0
                            await FormdataService.edit_formdata_services(session, form_item)

        elif op_type == "update":
            # 更新/添加表单数据
            if operation.data:
                formdata_list = test_case.formdata or []
                existing_keys = {form.key: form for form in formdata_list}

                for key, value in operation.data.items():
                    if key in existing_keys:
                        # 更新现有表单项：只更新 value，不修改 is_run
                        existing_form = existing_keys[key]
                        existing_form.value = str(value)
                        await FormdataService.edit_formdata_services(session, existing_form)
                    else:
                        # 添加新表单项：设置 is_run=1
                        await FormdataService.add_formdata_services(session, FormdataModel(
                            key=str(key),
                            value=str(value),
                            case_id=case_id,
                            is_run=1  # 新增时设置 is_run=1
                        ))

        elif op_type == "set_empty":
            # 设置指定键为空：设置值为空，确保 is_run=1
            if operation.keys_to_empty:
                formdata_list = test_case.formdata or []
                for form_item in formdata_list:
                    if form_item.key in operation.keys_to_empty:
                        form_item.value = ""
                        form_item.is_run = 1  # 设置为空时确保 is_run=1
                        await FormdataService.edit_formdata_services(session, form_item)


# ==================== 主工具函数 ====================

@mcp.tool()
async def generate_test_cases(params_test_case: Any, ctx: Context) -> str:
    """
    生成测试用例的函数方法 - 支持灵活的字段操作

    支持的操作类型:
    - update: 更新/添加字段
    - delete: 删除指定字段
    - replace: 完全替换所有字段
    - set_empty: 设置指定字段为空值
    - clear: 清空所有字段

    支持的目标类型:
    - params: 查询参数
    - headers: 请求头
    - cookies: Cookies
    - body: 请求体 (JSON 或 Form-Data)

    输入示例 1 - 查询参数验证:
    {
      "case_id": "123",
      "test_cases": [
        {
          "name": "查询参数验证-缺少参数key1",
          "description": "删除 key1 参数测试",
          "operations": [
            {
              "operation": "delete",
              "target": "params",
              "keys_to_delete": ["key1"]
            }
          ]
        },
        {
          "name": "查询参数验证-参数为空",
          "description": "清空所有查询参数",
          "operations": [
            {
              "operation": "clear",
              "target": "params"
            }
          ]
        }
      ]
    }

    输入示例 2 - 请求头验证:
    {
      "case_id": "123",
      "test_cases": [
        {
          "name": "请求头验证-缺少Authorization",
          "operations": [
            {
              "operation": "delete",
              "target": "headers",
              "keys_to_delete": ["Authorization"]
            }
          ]
        },
        {
          "name": "请求头验证-Content-Type错误",
          "operations": [
            {
              "operation": "update",
              "target": "headers",
              "data": {"Content-Type": "text/plain"}
            }
          ]
        }
      ]
    }

    输入示例 3 - JSON 请求体验证:
    {
      "case_id": "123",
      "test_cases": [
        {
          "name": "登录-密码为空",
          "operations": [
            {
              "operation": "set_empty",
              "target": "body",
              "keys_to_empty": ["password"]
            }
          ]
        },
        {
          "name": "登录-用户名错误",
          "operations": [
            {
              "operation": "update",
              "target": "body",
              "data": {"username": "wrong_user"}
            }
          ]
        }
      ]
    }

    输入示例 4 - Form-Data 请求体验证:
    {
      "case_id": "456",
      "test_cases": [
        {
          "name": "表单提交-缺少必填字段",
          "operations": [
            {
              "operation": "delete",
              "target": "body",
              "keys_to_delete": ["required_field"]
            }
          ]
        }
      ]
    }

    输入示例 5 - 多种操作组合:
    {
      "case_id": "789",
      "test_cases": [
        {
          "name": "综合测试-修改多个部分",
          "operations": [
            {
              "operation": "update",
              "target": "params",
              "data": {"page": "1", "size": "20"}
            },
            {
              "operation": "delete",
              "target": "headers",
              "keys_to_delete": ["X-Custom-Header"]
            },
            {
              "operation": "update",
              "target": "body",
              "data": {"status": "active"}
            }
          ]
        }
      ]
    }
    """
    logger.info(f"收到生成测试用例请求: {params_test_case}")

    # 参数验证和转换
    if isinstance(params_test_case, str):
        try:
            params_test_case = GenerateTestCasesInput.model_validate(json.loads(params_test_case))
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"JSON 解析失败: {str(e)}"
            }, ensure_ascii=False, indent=2)

    elif isinstance(params_test_case, dict):
        try:
            params_test_case = GenerateTestCasesInput.model_validate(params_test_case)
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": f"参数验证失败: {str(e)}"
            }, ensure_ascii=False, indent=2)

    elif not isinstance(params_test_case, GenerateTestCasesInput):
        return json.dumps({
            "success": False,
            "error": "不支持的参数类型"
        }, ensure_ascii=False, indent=2)

    start_time = time.time()
    generated_cases = []
    failed_cases = []

    for i, test_case_param in enumerate(params_test_case.test_cases):
        session = AsyncSessionLocal()

        try:
            # 1. 复制测试用例
            copy_test_cases = Test_casesModel(case_id=int(params_test_case.case_id))
            copy_test_cases.create_by = "mcp-llm"
            copy_test_cases.create_time = datetime.now()
            copy_test_cases.update_by = "mcp-llm"
            copy_test_cases.update_time = datetime.now()

            add_test_cases_result = await Test_casesService.test_cases_copy_services(
                session, copy_test_cases, is_copy_to_case=True
            )

            new_case_id = add_test_cases_result.get("caseId")
            await session.commit()

            # 2. 获取新用例的详细信息
            test_case_detail = await Test_casesService.test_cases_detail_services(
                session, new_case_id
            )

            if test_case_detail is None:
                failed_cases.append({
                    "name": test_case_param.name,
                    "error": f"无法找到创建的测试用例 (ID: {new_case_id})"
                })
                continue

            # 3. 更新基本信息
            test_case_detail.name = test_case_param.name
            if test_case_param.description:
                test_case_detail.description = test_case_param.description

            # 4. 保存基本信息更新（name, description）到数据库
            await Test_casesService.edit_test_cases_services(session, test_case_detail)

            # 5. 应用所有操作（每次操作后刷新用例数据以确保后续操作使用最新数据）
            for idx, operation in enumerate(test_case_param.operations):
                await _apply_field_operation(session, test_case_detail, operation)

                # 如果还有后续操作，刷新用例数据
                if idx < len(test_case_param.operations) - 1:
                    await session.commit()  # 先提交当前操作
                    # 重新获取用例详情，确保后续操作使用最新数据
                    test_case_detail = await Test_casesService.test_cases_detail_services(
                        session, new_case_id
                    )

            # 6. 最终提交
            await session.commit()

            generated_cases.append({
                "case_id": new_case_id,
                "name": test_case_param.name,
                "description": test_case_param.description,
                "operations_count": len(test_case_param.operations),
                "status": "created"
            })

            logger.info(f"成功生成测试用例 {i + 1}/{len(params_test_case.test_cases)}: {test_case_param.name}")

        except Exception as e:
            error_msg = f"处理测试用例 '{test_case_param.name}' 时出错: {str(e)}"
            logger.error(error_msg, exc_info=True)
            await session.rollback()
            failed_cases.append({
                "name": test_case_param.name,
                "error": str(e)
            })

        finally:
            await session.close()

    # 计算处理时间
    elapsed_time = time.time() - start_time

    result = {
        "success": len(failed_cases) == 0,
        "summary": {
            "total": len(params_test_case.test_cases),
            "success": len(generated_cases),
            "failed": len(failed_cases),
            "elapsed_time_seconds": round(elapsed_time, 2)
        },
        "generated_cases": generated_cases,
        "failed_cases": failed_cases if failed_cases else None
    }

    logger.info(f"测试用例生成完成: {result['summary']}")

    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_test_case_info(case_id: str, ctx: Context) -> str:
    """
    获取测试用例的完整信息，用于分析接口结构并生成测试用例

    参数:
        case_id: 测试用例ID

    返回:
        测试用例的完整信息（JSON格式），包括：
        - 接口路径、方法、请求类型
        - 请求参数/请求体
        - 断言配置
        - 前置/后置操作
    """
    try:
        caseid = int(case_id)
        session = AsyncSessionLocal()

        try:
            # 获取测试用例详情
            test_case = await Test_casesService.test_cases_detail_services(session, caseid)

            if not test_case:
                return json.dumps({
                    "success": False,
                    "error": f"测试用例 {case_id} 不存在"
                }, ensure_ascii=False, indent=2)

            # 构建返回信息（只包含关键信息，减少上下文）
            result = {
                "success": True,
                "case_id": test_case.case_id,
                "name": test_case.name,
                "path": test_case.path,
                "method": test_case.method.value if test_case.method else None,
                "request_type": test_case.request_type.value if test_case.request_type else None,
                "status_code": test_case.status_code,
                "description": test_case.description,

                # 请求参数信息
                "request_data": None,

                # 参数字段说明
                "fields": []
            }

            # 根据请求类型提取参数
            if test_case.request_type in [Request_Type.JSON, Request_Type.XML, Request_Type.Raw]:
                if test_case.json_data:
                    result["request_data"] = test_case.json_data
                    # 提取字段列表
                    result["fields"] = list(test_case.json_data.keys()) if isinstance(test_case.json_data, dict) else []

            elif test_case.request_type in [Request_Type.Form_Data, Request_Type.x_www_form_urlencoded]:
                if test_case.formdata:
                    result["request_data"] = {item.key: item.value for item in test_case.formdata}
                    result["fields"] = [item.key for item in test_case.formdata]

            # 添加断言信息（如果有）
            if test_case.assertion_list:
                result["assertions"] = [
                    {
                        "jsonpath": a.jsonpath,
                        "assert_type": a.assert_type,
                        "value": a.value
                    }
                    for a in test_case.assertion_list[:3]  # 只返回前3个断言作为参考
                ]

            return json.dumps(result, ensure_ascii=False, indent=2)

        finally:
            await session.close()

    except Exception as e:
        logger.error(f"获取测试用例信息失败: {str(e)}")
        return json.dumps({
            "success": False,
            "error": f"获取测试用例信息失败: {str(e)}"
        }, ensure_ascii=False, indent=2)
