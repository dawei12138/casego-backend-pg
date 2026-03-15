#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：models.py
@Author  ：david
@Date    ：2025-08-11 23:38 
"""
# utils/api_tools/executors/models.py
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

from pydantic.alias_generators import to_camel

from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsConfig
from module_admin.api_testing.api_setup.entity.vo.setup_vo import SetupModel
from module_admin.api_testing.api_teardown.entity.vo.teardown_vo import TeardownModel
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesModel, \
    Test_casesAllParamsQueryModel, APIResponse


class ExecutorType(str, Enum):
    """执行器类型枚举"""
    PYTHON_SCRIPT = "PYTHON_SCRIPT"
    DB_CONNECTION = "DB_CONNECTION"
    JS_SCRIPT = "JS_SCRIPT"
    EXTRACT_VARIABLE = "EXTRACT_VARIABLE"
    WAIT_TIME = "WAIT_TIME"
    APIExecutor = "APIExecutor"


class RequestInfo(BaseModel):
    """请求信息模型 - 规范化请求参数"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    url: str = ""
    method: str = "GET"
    headers: Dict[str, str] = Field(default_factory=dict)
    params: Optional[Dict[str, str]] = None
    cookies: Optional[Dict[str, str]] = None
    body: Any = None  # 请求体（json/form/raw等）
    data: Any = None  # FormData 或其他 data 类型
    json_body: Any = None  # JSON 请求体（单独存储，用于 aiohttp json 参数）
    allow_redirects: bool = True
    response_time: Optional[float] = None  # 响应时间

    # ==================== Header 操作 ====================
    def set_header(self, key: str, value: str) -> "RequestInfo":
        """设置请求头（支持链式调用）"""
        if self.headers is None:
            self.headers = {}
        self.headers[key] = value
        return self

    def get_header(self, key: str, default: str = None) -> Optional[str]:
        """获取请求头"""
        if self.headers is None:
            return default
        return self.headers.get(key, default)

    def remove_header(self, key: str) -> "RequestInfo":
        """删除请求头（支持链式调用）"""
        if self.headers and key in self.headers:
            del self.headers[key]
        return self

    def has_header(self, key: str) -> bool:
        """检查请求头是否存在"""
        return self.headers is not None and key in self.headers

    # ==================== Param 操作 ====================
    def set_param(self, key: str, value: str) -> "RequestInfo":
        """设置查询参数（支持链式调用）"""
        if self.params is None:
            self.params = {}
        self.params[key] = value
        return self

    def get_param(self, key: str, default: str = None) -> Optional[str]:
        """获取查询参数"""
        if self.params is None:
            return default
        return self.params.get(key, default)

    def remove_param(self, key: str) -> "RequestInfo":
        """删除查询参数（支持链式调用）"""
        if self.params and key in self.params:
            del self.params[key]
        return self

    def has_param(self, key: str) -> bool:
        """检查查询参数是否存在"""
        return self.params is not None and key in self.params

    # ==================== Cookie 操作 ====================
    def set_cookie(self, key: str, value: str) -> "RequestInfo":
        """设置Cookie（支持链式调用）"""
        if self.cookies is None:
            self.cookies = {}
        self.cookies[key] = value
        return self

    def get_cookie(self, key: str, default: str = None) -> Optional[str]:
        """获取Cookie"""
        if self.cookies is None:
            return default
        return self.cookies.get(key, default)

    def remove_cookie(self, key: str) -> "RequestInfo":
        """删除Cookie（支持链式调用）"""
        if self.cookies and key in self.cookies:
            del self.cookies[key]
        return self

    def has_cookie(self, key: str) -> bool:
        """检查Cookie是否存在"""
        return self.cookies is not None and key in self.cookies

    # ==================== JSON Body 操作 ====================
    def set_json_field(self, key: str, value: Any) -> "RequestInfo":
        """设置JSON请求体字段（支持链式调用）

        支持点号分隔的嵌套路径，如 'user.name' 或 'data.items.0.id'
        """
        if self.json_body is None:
            self.json_body = {}
        if self.body is None:
            self.body = {}

        self._set_nested_value(self.json_body, key, value)
        self._set_nested_value(self.body, key, value)
        return self

    def get_json_field(self, key: str, default: Any = None) -> Any:
        """获取JSON请求体字段

        支持点号分隔的嵌套路径，如 'user.name' 或 'data.items.0.id'
        """
        if self.json_body is None:
            return default
        return self._get_nested_value(self.json_body, key, default)

    def remove_json_field(self, key: str) -> "RequestInfo":
        """删除JSON请求体字段（支持链式调用）

        支持点号分隔的嵌套路径
        """
        if self.json_body is not None:
            self._remove_nested_value(self.json_body, key)
        if self.body is not None and isinstance(self.body, dict):
            self._remove_nested_value(self.body, key)
        return self

    def has_json_field(self, key: str) -> bool:
        """检查JSON请求体字段是否存在"""
        if self.json_body is None:
            return False
        return self._get_nested_value(self.json_body, key, _MISSING) is not _MISSING

    # ==================== 批量操作 ====================
    def set_headers(self, headers: Dict[str, str]) -> "RequestInfo":
        """批量设置请求头（支持链式调用）"""
        if self.headers is None:
            self.headers = {}
        self.headers.update(headers)
        return self

    def set_params(self, params: Dict[str, str]) -> "RequestInfo":
        """批量设置查询参数（支持链式调用）"""
        if self.params is None:
            self.params = {}
        self.params.update(params)
        return self

    def set_cookies(self, cookies: Dict[str, str]) -> "RequestInfo":
        """批量设置Cookie（支持链式调用）"""
        if self.cookies is None:
            self.cookies = {}
        self.cookies.update(cookies)
        return self

    def set_json_body(self, body: Dict[str, Any]) -> "RequestInfo":
        """设置完整的JSON请求体（支持链式调用）"""
        self.json_body = body
        self.body = body
        return self

    # ==================== 内部辅助方法 ====================
    @staticmethod
    def _get_nested_value(obj: Any, path: str, default: Any = None) -> Any:
        """通过点号路径获取嵌套值"""
        keys = path.split('.')
        current = obj
        for key in keys:
            if isinstance(current, dict):
                if key not in current:
                    return default
                current = current[key]
            elif isinstance(current, list):
                try:
                    index = int(key)
                    if index < 0 or index >= len(current):
                        return default
                    current = current[index]
                except (ValueError, IndexError):
                    return default
            else:
                return default
        return current

    @staticmethod
    def _set_nested_value(obj: Any, path: str, value: Any) -> None:
        """通过点号路径设置嵌套值"""
        keys = path.split('.')
        current = obj
        for i, key in enumerate(keys[:-1]):
            if isinstance(current, dict):
                if key not in current:
                    # 判断下一个 key 是否是数字，决定创建 list 还是 dict
                    next_key = keys[i + 1]
                    current[key] = [] if next_key.isdigit() else {}
                current = current[key]
            elif isinstance(current, list):
                try:
                    index = int(key)
                    while len(current) <= index:
                        current.append({})
                    current = current[index]
                except ValueError:
                    return

        # 设置最终值
        final_key = keys[-1]
        if isinstance(current, dict):
            current[final_key] = value
        elif isinstance(current, list):
            try:
                index = int(final_key)
                while len(current) <= index:
                    current.append(None)
                current[index] = value
            except ValueError:
                pass

    @staticmethod
    def _remove_nested_value(obj: Any, path: str) -> None:
        """通过点号路径删除嵌套值"""
        keys = path.split('.')
        current = obj
        for key in keys[:-1]:
            if isinstance(current, dict):
                if key not in current:
                    return
                current = current[key]
            elif isinstance(current, list):
                try:
                    index = int(key)
                    if index < 0 or index >= len(current):
                        return
                    current = current[index]
                except (ValueError, IndexError):
                    return
            else:
                return

        # 删除最终值
        final_key = keys[-1]
        if isinstance(current, dict) and final_key in current:
            del current[final_key]
        elif isinstance(current, list):
            try:
                index = int(final_key)
                if 0 <= index < len(current):
                    current.pop(index)
            except ValueError:
                pass


# 用于检测字段是否存在的哨兵值
class _MissingSentinel:
    pass


_MISSING = _MissingSentinel()


class ExecutorContext(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    """执行器上下文 - 基础公共参数"""
    user_id: int
    env_id: int
    mysql_obj: Any = Field(default=None, exclude=True)  # 排除序列化
    redis_obj: Any = Field(default=None, exclude=True)  # 排除序列化
    session: Any = Field(default=None, exclude=True)  # 排除序列化

    # 接口执行上下文
    case_id: Optional[int] = None
    env_config: EnvironmentsConfig = Field(default=None)
    parameterization: Dict[str, Any] = {}
    parameterization_id: Optional[int] = Field(default=None)  # 参数化变量
    # sort: Optional[int] = Field(default=None)  # 参数化变量
    variables: Dict[str, Any] = {}  # 全局变量
    response: Optional[Any] = None  # API响应对象
    request_info: Optional["RequestInfo"] = Field(
        default_factory=lambda: RequestInfo(
            url="",
            method="GET",
            headers={},
            allow_redirects=True
        )
    )
    use_env_cookies: bool = Field(default=False, description='是否使用环境级别的Cookies（请求前加载、请求后存储）')


class CasesConfig(Test_casesAllParamsQueryModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    # APIExecutor: Optional[Any] = None  # 执行类型
    pass


class SetupConfig(SetupModel):
    """前置脚本配置"""
    pass


class TeardownConfig(TeardownModel):
    """后置脚本配置"""
    pass


class ExecutorResult(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    """执行器结果"""
    success: bool
    message: str = ""
    data: Any = None
    error: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None  # 新增的变量
    execution_time: Optional[float] = None  # 执行耗时(秒)
    log: Any = None  # 执行日志


class SingleExecutorResult(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    setup_results: Optional[List[ExecutorResult]] = Field(default=[])
    response: Optional[APIResponse] = Field(default=None)
    teardown_results: Optional[List[ExecutorResult]] = Field(default=[])
    assersion_result: Optional[ExecutorResult] = Field(default=None)
    context: Optional[ExecutorContext] = Field(default=None)
    log: Optional[str] = Field(default=None)  # 原始格式日志文本
