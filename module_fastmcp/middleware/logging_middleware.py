import json
import time
from datetime import datetime
from typing import Any, Dict, Optional, List

import mcp.types as mt
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.tools.tool import Tool, ToolResult
from fastmcp.resources.resource import Resource
from fastmcp.resources.template import ResourceTemplate
from fastmcp.prompts.prompt import Prompt
from utils.log_util import logger


class LoggingMiddleware(Middleware):
    """
    MCP 请求日志中间件
    记录工具调用、资源读取、Prompt 请求等的详细信息

    根据 FastMCP 官方文档编写，支持所有标准的中间件钩子
    """

    def __init__(
            self,
            log_level: str = "INFO",
            include_payloads: bool = True,
            max_payload_length: int = 1000,
            log_timing: bool = True,
            log_strategy: str = "specific"  # "specific", "general", "all"
    ):
        """
        初始化日志中间件

        Args:
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
            include_payloads: 是否包含请求/响应载荷
            max_payload_length: 载荷最大长度
            log_timing: 是否记录执行时间
            log_strategy: 日志策略
                - "specific": 只记录最具体的操作（推荐，避免重复）
                - "general": 只记录通用的 message/request 级别
                - "all": 记录所有级别（会有重复，用于调试）
        """
        super().__init__()
        self.log_level = log_level.upper()
        self.include_payloads = include_payloads
        self.max_payload_length = max_payload_length
        self.log_timing = log_timing
        self.log_strategy = log_strategy

    def _json_serializer(self, obj):
        """自定义 JSON 序列化器，处理特殊类型"""
        # 处理 datetime 对象
        if isinstance(obj, datetime):
            return obj.isoformat()

        # 处理 Pydantic 的 AnyUrl 和其他 URL 类型
        if hasattr(obj, '__str__') and hasattr(obj, 'scheme'):
            return str(obj)

        # 处理 Path 对象
        if hasattr(obj, '__fspath__'):
            return str(obj)

        # 处理 Pydantic 模型
        if hasattr(obj, 'model_dump'):
            return obj.model_dump()

        # 处理字典类型的对象
        if hasattr(obj, 'dict'):
            return obj.dict()

        # 其他情况转为字符串
        if hasattr(obj, '__str__'):
            return str(obj)

        return repr(obj)

    def _truncate_payload(self, data: Any) -> str:
        """截断过长的载荷数据"""
        try:
            json_str = json.dumps(data, ensure_ascii=False, default=self._json_serializer)
            if len(json_str) > self.max_payload_length:
                return json_str[:self.max_payload_length] + "...[truncated]"
            return json_str
        except Exception:
            str_data = str(data)
            if len(str_data) > self.max_payload_length:
                return str_data[:self.max_payload_length] + "...[truncated]"
            return str_data

    def _get_client_info(self, context: MiddlewareContext) -> Dict[str, Any]:
        """获取客户端信息"""
        client_info = {
            "source": context.source,
            "type": context.type,
            "method": context.method,
            "session_id": context.fastmcp_context.session_id,
            "request_id": context.fastmcp_context.request_id,
            "timestamp": context.timestamp.isoformat()
        }

        # 从 FastMCP 上下文获取认证信息
        if context.fastmcp_context and hasattr(context.fastmcp_context, 'claims'):
            claims = context.fastmcp_context.claims
            if claims:
                client_info['client_id'] = claims.get('client_id', 'Anonymous')
                client_info['scopes'] = claims.get('scopes', [])

        return client_info

    def _safe_get_attribute(self, obj: Any, attr_name: str, default: str = "unknown") -> str:
        """安全地获取对象属性，避免 AttributeError"""
        try:
            value = getattr(obj, attr_name, None)
            if value is not None:
                return str(value)
            else:
                # 尝试其他可能的属性名
                if attr_name == "uriTemplate":
                    # 尝试常见的其他属性名
                    for alt_attr in ["uri_template", "template", "pattern", "name"]:
                        alt_value = getattr(obj, alt_attr, None)
                        if alt_value is not None:
                            return str(alt_value)
                elif attr_name == "uri":
                    # 尝试其他可能的 URI 属性名
                    for alt_attr in ["url", "path", "location", "name"]:
                        alt_value = getattr(obj, alt_attr, None)
                        if alt_value is not None:
                            return str(alt_value)
                return default
        except Exception:
            return default

    def _safe_extract_list_info(self, items: List[Any], attr_name: str) -> List[str]:
        """安全地从对象列表中提取属性信息"""
        if not items:
            return []

        result = []
        for item in items:
            try:
                value = self._safe_get_attribute(item, attr_name)
                result.append(value)
            except Exception as e:
                # 如果单个项目提取失败，记录但继续处理其他项目
                logger.debug(f"Failed to extract {attr_name} from item: {e}")
                result.append(f"<error_extracting_{attr_name}>")

        return result

    def _log_request(self, context: MiddlewareContext, operation_type: str, extra_data: Dict = None):
        """记录请求信息"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "type": f"{operation_type}_REQUEST",
            "method": context.method,
            "client_info": self._get_client_info(context)
        }

        if extra_data:
            log_data.update(extra_data)

        if self.include_payloads:
            log_data["payload"] = self._truncate_payload(context.message)

        logger.info(
            f"[MCP] {operation_type}: {json.dumps(log_data, ensure_ascii=False, default=self._json_serializer)}")

    def _log_response(self, context: MiddlewareContext, operation_type: str, result: Any, duration_ms: float,
                      extra_data: Dict = None):
        """记录响应信息"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "type": f"{operation_type}_RESPONSE",
            "method": context.method,
            "client_info": self._get_client_info(context),
            "success": True
        }

        if self.log_timing:
            log_data["duration_ms"] = round(duration_ms, 2)

        if extra_data:
            log_data.update(extra_data)

        if self.include_payloads and result is not None:
            log_data["response"] = self._truncate_payload(result)

        logger.info(
            f"[MCP] {operation_type}_RESULT: {json.dumps(log_data, ensure_ascii=False, default=self._json_serializer)}")

    def _log_error(self, context: MiddlewareContext, operation_type: str, error: Exception, duration_ms: float):
        """记录错误信息"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "type": f"{operation_type}_ERROR",
            "method": context.method,
            "client_info": self._get_client_info(context),
            "success": False,
            "error": str(error),
            "error_type": type(error).__name__
        }

        if self.log_timing:
            log_data["duration_ms"] = round(duration_ms, 2)

        logger.error(
            f"[MCP] {operation_type}_ERROR: {json.dumps(log_data, ensure_ascii=False, default=self._json_serializer)}")

    async def on_message(self, context: MiddlewareContext, call_next):
        """记录所有 MCP 消息"""
        # 只在 general 或 all 策略下记录
        if self.log_strategy not in ["general", "all"]:
            return await call_next(context)

        start_time = time.perf_counter()

        self._log_request(context, "MESSAGE")

        try:
            result = await call_next(context)

            if self.log_timing:
                duration_ms = (time.perf_counter() - start_time) * 1000
                self._log_response(context, "MESSAGE", result, duration_ms)

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._log_error(context, "MESSAGE", e, duration_ms)
            raise

    async def on_request(self, context: MiddlewareContext, call_next):
        """记录 MCP 请求（期望响应的消息）"""
        # 只在 general 或 all 策略下记录
        if self.log_strategy not in ["general", "all"]:
            return await call_next(context)

        start_time = time.perf_counter()

        self._log_request(context, "REQUEST")

        try:
            result = await call_next(context)

            if self.log_timing:
                duration_ms = (time.perf_counter() - start_time) * 1000
                self._log_response(context, "REQUEST", result, duration_ms)

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._log_error(context, "REQUEST", e, duration_ms)
            raise

    async def on_notification(self, context: MiddlewareContext, call_next):
        """记录 MCP 通知（不期望响应的消息）"""
        self._log_request(context, "NOTIFICATION")

        try:
            result = await call_next(context)
            logger.info(f"[MCP] NOTIFICATION_PROCESSED: {context.method}")
            return result

        except Exception as e:
            self._log_error(context, "NOTIFICATION", e, 0)
            raise

    async def on_call_tool(self, context: MiddlewareContext, call_next):
        """记录工具调用"""
        start_time = time.perf_counter()
        tool_params = context.message

        extra_data = {
            "tool_name": getattr(tool_params, 'name', 'unknown'),
            "arguments": self._truncate_payload(tool_params.arguments) if hasattr(tool_params,
                                                                                  'arguments') and tool_params.arguments else {}
        }

        self._log_request(context, "TOOL_CALL", extra_data)

        try:
            result = await call_next(context)
            duration_ms = (time.perf_counter() - start_time) * 1000

            result_extra = {
                "tool_name": getattr(tool_params, 'name', 'unknown'),
                "is_error": getattr(result, 'isError', False)
            }

            self._log_response(context, "TOOL_CALL", result, duration_ms, result_extra)
            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._log_error(context, "TOOL_CALL", e, duration_ms)
            raise

    async def on_read_resource(self, context: MiddlewareContext, call_next):
        """记录资源读取"""
        start_time = time.perf_counter()
        resource_params = context.message

        extra_data = {"resource_uri": self._safe_get_attribute(resource_params, "uri")}
        self._log_request(context, "RESOURCE_READ", extra_data)

        try:
            result = await call_next(context)
            duration_ms = (time.perf_counter() - start_time) * 1000

            result_extra = {
                "resource_uri": self._safe_get_attribute(resource_params, "uri"),
                "contents_count": len(result.contents) if hasattr(result, 'contents') and result.contents else 0
            }

            self._log_response(context, "RESOURCE_READ", result, duration_ms, result_extra)
            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._log_error(context, "RESOURCE_READ", e, duration_ms)
            raise

    async def on_get_prompt(self, context: MiddlewareContext, call_next):
        """记录 Prompt 获取"""
        start_time = time.perf_counter()
        prompt_params = context.message

        extra_data = {
            "prompt_name": getattr(prompt_params, 'name', 'unknown'),
            "arguments": self._truncate_payload(prompt_params.arguments) if hasattr(prompt_params,
                                                                                    'arguments') and prompt_params.arguments else {}
        }

        self._log_request(context, "PROMPT_GET", extra_data)

        try:
            result = await call_next(context)
            duration_ms = (time.perf_counter() - start_time) * 1000

            result_extra = {
                "prompt_name": getattr(prompt_params, 'name', 'unknown'),
                "messages_count": len(result.messages) if hasattr(result, 'messages') and result.messages else 0
            }

            self._log_response(context, "PROMPT_GET", result, duration_ms, result_extra)
            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self._log_error(context, "PROMPT_GET", e, duration_ms)
            raise

    async def on_list_tools(self, context: MiddlewareContext, call_next):
        """记录工具列表请求"""
        self._log_request(context, "LIST_TOOLS")

        try:
            result = await call_next(context)

            result_extra = {
                "tools_count": len(result) if result else 0,
                "tool_names": self._safe_extract_list_info(result, "name") if result else []
            }

            self._log_response(context, "LIST_TOOLS", result, 0, result_extra)
            return result

        except Exception as e:
            self._log_error(context, "LIST_TOOLS", e, 0)
            raise

    async def on_list_resources(self, context: MiddlewareContext, call_next):
        """记录资源列表请求"""
        self._log_request(context, "LIST_RESOURCES")

        try:
            result = await call_next(context)

            result_extra = {
                "resources_count": len(result) if result else 0,
                "resource_uris": self._safe_extract_list_info(result, "uri") if result else []
            }

            self._log_response(context, "LIST_RESOURCES", result, 0, result_extra)
            return result

        except Exception as e:
            self._log_error(context, "LIST_RESOURCES", e, 0)
            raise

    async def on_list_resource_templates(self, context: MiddlewareContext, call_next):
        """记录资源模板列表请求"""
        self._log_request(context, "LIST_RESOURCE_TEMPLATES")

        try:
            result = await call_next(context)

            result_extra = {
                "templates_count": len(result) if result else 0,
                "template_patterns": self._safe_extract_list_info(result, "uriTemplate") if result else []
            }

            self._log_response(context, "LIST_RESOURCE_TEMPLATES", result, 0, result_extra)
            return result

        except Exception as e:
            self._log_error(context, "LIST_RESOURCE_TEMPLATES", e, 0)
            raise

    async def on_list_prompts(self, context: MiddlewareContext, call_next):
        """记录 Prompt 列表请求"""
        self._log_request(context, "LIST_PROMPTS")

        try:
            result = await call_next(context)

            result_extra = {
                "prompts_count": len(result) if result else 0,
                "prompt_names": self._safe_extract_list_info(result, "name") if result else []
            }

            self._log_response(context, "LIST_PROMPTS", result, 0, result_extra)
            return result

        except Exception as e:
            self._log_error(context, "LIST_PROMPTS", e, 0)
            raise