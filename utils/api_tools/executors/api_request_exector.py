#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：api_case_single_executor_with_setup.py
@Author  ：david
@Date    ：2025-08-11
"""
import asyncio
import json
import re
import time
import ssl

from typing import Dict, Any, Optional, Union, Tuple
from datetime import datetime
from urllib.parse import urljoin

import aiofiles
import aiohttp
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel

from config.enums import DataTypeEnum, Request_Type
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel
from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsConfig
from module_admin.api_testing.api_environments.service.environments_service import EnvironmentsService
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FileConfig
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import APIResponse
from utils.api_tools.executors.models import RequestInfo
from utils.common_util import ensure_path_sep
from utils.log_util import logger


class APIExecutor:
    """API接口执行器"""

    def __init__(self, test_case, context):
        self.context = context  # 保存完整的 context 引用
        self.user_id = context.user_id
        self.case_id = context.case_id
        self.env_id = context.env_id

        self.query_db = context.mysql_obj
        self.redis = context.redis_obj

        self.variables = {}  # 存储运行时变量
        self.parameterization = context.parameterization  # 参数化变量，比环境变量优先级更高
        self.test_case = test_case
        self.session = context.session
        self.env_config = context.env_config

    async def execute(self) -> APIResponse:
        """
        执行接口测试

        Returns:
            APIResponse: 接口执行结果
        """
        request_info = None
        try:
            # 1. 优先从 context 获取预构建的请求参数，否则现场构建
            if self.context and self.context.request_info:
                request_info = self.context.request_info
            else:
                request_info = await self.build_request_info()

        except Exception as e:
            # 请求构建阶段出错
            error_msg = f"请求构建失败: {type(e).__name__} - {str(e)}"
            logger.exception(error_msg)
            return self._build_error_response(request_info, error_msg)

        try:
            # 2. 发送请求（异常已在 _send_request_with_info 内部处理）
            response = await self._send_request_with_info(request_info)

            # 3. 如果响应已经包含错误，直接补充请求信息后返回
            if not response.is_success and response.error_message:
                return self._build_response(response, request_info)

            # 4. 构建正常响应对象
            return self._build_response(response, request_info)

        except Exception as e:
            # 响应处理阶段出错
            error_msg = f"响应处理失败: {type(e).__name__} - {str(e)}"
            logger.exception(error_msg)
            return self._build_error_response(request_info, error_msg)

    @classmethod
    async def _type_to_params(cls, value, data_type: DataTypeEnum, file_config: FileConfig = None):
        _type_map = {
            DataTypeEnum.STRING: str,
            DataTypeEnum.INTEGER: int,
            DataTypeEnum.BOOLEAN: bool,
            DataTypeEnum.NUMBER: float,
            DataTypeEnum.ARRAY: list,
            # DataTypeEnum.FILE: dict,
        }
        try:
            res = _type_map.get(data_type, str)(value)
        except:
            res = value
        return res

    async def build_request_info(self) -> RequestInfo:
        """构建请求参数信息（公共方法，可在外部调用）"""
        start_time = time.time()

        url = await self._build_url()
        time2 = time.time()
        # logger.warning(f"接口URL构建耗时{time2 - start_time}")

        headers = await self._build_headers()
        time3 = time.time()
        # logger.warning(f"接口header构建耗时{time3 - time2}")

        params = await self._build_params()
        time4 = time.time()
        # logger.warning(f"接口拼接参数构建耗时{time4 - time3}")

        cookies = await self._build_cookies()
        time5 = time.time()
        # logger.warning(f"接口cookie构建耗时{time5 - time4}")

        body = await self._build_request_body()
        time6 = time.time()
        # logger.warning(f"接口请求body构建耗时{time6 - time5}")

        # 构建 RequestInfo 对象
        request_info = RequestInfo(
            url=url,
            method=self.test_case.method.value.upper(),
            headers=headers or {},
            params=params,
            cookies=cookies,
            body=body,
            allow_redirects=True
        )

        # 根据请求类型设置具体的请求体字段
        if self.test_case.request_type == Request_Type.JSON and body is not None:
            request_info.json_body = body

        elif self.test_case.request_type == Request_Type.Form_Data and body is not None:
            if isinstance(body, dict):
                form_data = aiohttp.FormData(quote_fields=False)  # 禁用字段名的URL编码
                for key, value in body.items():
                    if isinstance(value, list):
                        # 这里处理文件上传
                        for config in value:
                            try:
                                async with aiofiles.open(ensure_path_sep(config.file_path), "rb") as f:
                                    content = await f.read()

                                form_data.add_field(
                                    name=key,  # 后端接收参数名（多个文件可以用同名字段）
                                    value=content,
                                    filename=config.file_name,
                                    content_type="application/octet-stream"
                                )
                            except FileNotFoundError:
                                pass
                    else:
                        form_data.add_field(key, str(value))
                request_info.data = form_data
            else:
                request_info.data = body
            # 移除Content-Type，让aiohttp自动设置
            if request_info.headers and 'Content-Type' in request_info.headers:
                del request_info.headers['Content-Type']

        elif self.test_case.request_type == Request_Type.x_www_form_urlencoded and body is not None:
            request_info.data = body
            if not request_info.headers:
                request_info.headers = {}
            request_info.headers["Content-Type"] = "application/x-www-form-urlencoded"

        elif self.test_case.request_type in [Request_Type.XML, Request_Type.Raw] and body is not None:
            request_info.data = body

        elif self.test_case.request_type == Request_Type.Binary:
            if hasattr(self.test_case, 'case_file_config') and self.test_case.case_file_config:

                case_file_config = self.test_case.case_file_config
                try:
                    async with aiofiles.open(ensure_path_sep(case_file_config.file_path), "rb") as f:
                        content = await f.read()
                    request_info.data = content
                    request_info.headers["Content-Type"] = "binary/octet-stream"
                    if request_info.params:
                        request_info.params["filename"] = case_file_config.file_name
                    else:
                        request_info.params = {"filename": case_file_config.file_name}
                    request_info.headers["X-Filename"] = case_file_config.file_name
                except FileNotFoundError:
                    pass

        time7 = time.time()
        # logger.warning(f"接口请求参数准备耗时{time7 - time6}")

        return request_info

    async def _send_request_with_info(self, request_info: RequestInfo) -> APIResponse:
        """使用构建好的请求信息发送HTTP请求

        Args:
            request_info: RequestInfo 对象，包含请求参数

        Returns:
            APIResponse: 响应对象，包含成功的响应或错误信息
        """
        method = request_info.method
        url = request_info.url or 'Unknown URL'

        # 从 RequestInfo 的具体字段构建 aiohttp 请求参数
        kwargs = {
            'url': request_info.url,
            'headers': request_info.headers,
            'params': request_info.params,
            'allow_redirects': request_info.allow_redirects
        }

        # 处理cookies：合并session自动管理的cookies和手动配置的cookies
        # 从session的cookie jar中提取现有cookies（上一个请求返回的Set-Cookie）
        session_cookies = {}
        for cookie in self.session.cookie_jar:
            if cookie.key and cookie.value:
                session_cookies[cookie.key] = cookie.value
                # 记录详细的cookie信息用于调试
                logger.debug(f"Cookie jar中的cookie: {cookie.key}={cookie.value}, domain={cookie.get('domain')}, path={cookie.get('path')}")

        # 如果有手动配置的cookies，合并它们（手动配置的优先级更高）
        if request_info.cookies:
            merged_cookies = {**session_cookies, **request_info.cookies}
            logger.info(f"[Cookie合并] Session cookies: {session_cookies}")
            logger.info(f"[Cookie合并] 手动配置cookies: {request_info.cookies}")
            logger.info(f"[Cookie合并] 合并后发送: {merged_cookies}")
            kwargs['cookies'] = merged_cookies
            # 更新 request_info.cookies 为合并后的完整 cookies，以便记录到请求信息中
            request_info.cookies = merged_cookies
        else:
            # 没有手动cookies时，不传递cookies参数，让session的CookieJar自动管理
            # 这样aiohttp会自动从cookie jar读取并发送匹配的cookies
            if session_cookies:
                logger.info(f"[Cookie自动] Session中有{len(session_cookies)}个cookies，由aiohttp自动管理: {list(session_cookies.keys())}")
                # 将 session cookies 记录到 request_info.cookies，以便记录到请求信息中
                request_info.cookies = session_cookies.copy()
            else:
                logger.info(f"[Cookie自动] 没有cookies，首次请求")

        # 根据请求体类型设置对应参数
        if request_info.json_body is not None:
            kwargs['json'] = request_info.json_body
        elif request_info.data is not None:
            kwargs['data'] = request_info.data

        request_start_time = time.time()
        try:
            async with self.session.request(method, **kwargs) as response:
                response_time = time.time() - request_start_time
                logger.warning(f"接口发送获取响应阶段耗时{response_time}")

                # 记录服务器设置的cookies（用于调试cookie传递）
                set_cookie_headers = response.headers.getall('Set-Cookie', [])
                if set_cookie_headers:
                    logger.info(f"[响应Set-Cookie] 服务器返回了{len(set_cookie_headers)}个Set-Cookie header:")
                    for sc in set_cookie_headers:
                        logger.info(f"  -> {sc}")

                if response.cookies:
                    logger.info(f"[响应Cookies] aiohttp解析的cookies: {dict(response.cookies)}")

                # 记录当前cookie jar的状态
                logger.info(f"[Cookie Jar状态] 当前cookie jar中有{len(self.session.cookie_jar)}个cookies")

                # 获取Content-Type和Content-Length
                content_type = response.headers.get('content-type', '').lower()
                content_length = response.headers.get('content-length')

                # 根据Content-Type决定如何处理响应体
                response_body = await self._process_response_body(response, content_type, content_length)

                response_copy = APIResponse(
                    response_status_code=response.status,
                    response_headers=dict(response.headers),
                    response_body=response_body,
                    response_cookies=response.cookies,
                    is_success=200 <= response.status < 300
                )

                request_info.response_time = response_time
                return response_copy

        except aiohttp.ClientConnectorError as e:
            # 连接错误（如端口错误、主机不可达等）
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"连接失败 [{url}]: {type(e).__name__} - {str(e)}"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": "ClientConnectorError", "detail": str(e)},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except aiohttp.ServerTimeoutError as e:
            # 服务器超时
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"请求超时 [{url}]: {type(e).__name__} - {str(e)}"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": "ServerTimeoutError", "detail": str(e)},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except aiohttp.ClientResponseError as e:
            # 客户端响应错误
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"响应错误 [{url}]: HTTP {e.status} - {e.message}"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=e.status,
                response_headers={},
                response_body={"error_type": "ClientResponseError", "detail": e.message},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except aiohttp.InvalidURL as e:
            # URL 格式错误
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"无效URL [{url}]: {type(e).__name__} - {str(e)}"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": "InvalidURL", "detail": str(e)},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except ssl.SSLError as e:
            # SSL/TLS 错误
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"SSL证书错误 [{url}]: {type(e).__name__} - {str(e)}"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": "SSLError", "detail": str(e)},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except aiohttp.ClientError as e:
            # 其他 aiohttp 客户端错误
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"请求失败 [{url}]: {type(e).__name__} - {str(e)}"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": type(e).__name__, "detail": str(e)},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except asyncio.TimeoutError as e:
            # asyncio 超时错误
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"请求超时 [{url}]: asyncio.TimeoutError"
            logger.error(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": "TimeoutError", "detail": "请求超时"},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

        except Exception as e:
            # 捕获其他未预期的异常
            response_time = time.time() - request_start_time
            request_info.response_time = response_time
            error_detail = f"未知错误 [{url}]: {type(e).__name__} - {str(e)}"
            logger.exception(error_detail)
            return APIResponse(
                response_status_code=0,
                response_headers={},
                response_body={"error_type": type(e).__name__, "detail": str(e)},
                response_cookies=None,
                is_success=False,
                error_message=error_detail
            )

    async def _process_response_body(self, response, content_type: str, content_length: str = None):
        """根据内容类型处理响应体"""

        # 检查文件大小，避免内存溢出
        max_size = 100 * 1024 * 1024  # 100MB限制
        if content_length and int(content_length) > max_size:
            return {"error": "文件过大，超过处理限制", "size": content_length}

        # JSON类型
        if 'application/json' in content_type:
            return await response.json()

        # 文本类型
        elif (content_type.startswith('text/') or
              'application/xml' in content_type or
              'application/javascript' in content_type or
              'application/x-www-form-urlencoded' in content_type):
            return await response.text()

        # 二进制类型（图片、音频、视频等）
        elif (content_type.startswith(('image/', 'audio/', 'video/')) or
              'application/pdf' in content_type or
              'application/zip' in content_type or
              'application/octet-stream' in content_type or
              'application/msword' in content_type or
              'application/vnd.ms-excel' in content_type or
              'application/vnd.openxmlformats' in content_type):

            # 对于二进制文件，可以选择：
            # 1. 返回字节数据（小文件）
            # 2. 返回文件信息而不是内容（大文件）
            # 3. 保存到临时文件并返回路径

            if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB以上
                return {
                    "type": "binary_file",
                    "content_type": content_type,
                    "size": content_length,
                    "message": "文件过大，未读取内容"
                }
            else:
                binary_data = await response.read()
                return {
                    "type": "binary_data",
                    "content_type": content_type,
                    "size": len(binary_data),
                    "data": binary_data  # 或者转换为base64
                }

        # 多部分类型
        elif content_type.startswith('multipart/'):
            # multipart数据需要特殊处理
            return {
                "type": "multipart",
                "content_type": content_type,
                "raw_data": await response.read()
            }

        # 未知类型，默认按二进制处理
        else:
            return {
                "type": "unknown",
                "content_type": content_type,
                "data": await response.read()
            }

    async def _parse_template(self, template: str, variables_dict: dict = None) -> str:
        """
                解析模板字符串，替换变量和函数
        :param template: 包含变量的模板字符串
        :return: 解析后的字符串
        """

        from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel
        from utils.api_tools.regular_control import advanced_template_parser

        start_time = time.time()
        if not template:
            return template

        # 创建查询对象用于缓存查询
        query_object = Cache_dataPageQueryModel(
            environment_id=self.env_id,
            user_id=str(self.user_id)
        )
        res = await advanced_template_parser(template, self.redis, query_object, variables_dict=variables_dict)
        # 使用提供的高级模板解析器
        # logger.warning(f"缓存替换耗时：{start_time - time.time()}")
        return res

    # async def _build_url(self) -> str:
    #     """构建完整的请求URL"""
    #     from module_admin.api_testing.api_services.service.services_service import ServicesService
    #
    #     # 解析路径中的变量
    #     path = await self._parse_template(self.test_case.path, self.parameterization)
    #     path = path.strip() if path else ""
    #     base_url = await ServicesService.services_default_services(self.query_db, self.env_id)
    #     base_url = base_url.strip() if base_url else ""
    #     # 确保base_url有协议头
    #     if base_url:
    #         if not base_url.startswith(('http://', 'https://')):
    #             base_url = f"http://{base_url}"
    #         if path is None or path == "":
    #             return base_url
    #         if path.startswith(('http://', 'https://')):
    #             return path
    #         full_path = urljoin(base_url, path)
    #
    #         return full_path
    #     else:
    #         base_url = f"http://"
    #         if path is None or path == "":
    #             return base_url
    #         if path.startswith(('http://', 'https://')):
    #             return path
    #         full_path = base_url + path
    #
    #         return full_path
    #     # 如果路径已经是完整URL，直接返回
    #
    #     # 使用urljoin拼接URL
    async def _build_url(self) -> str:
        """构建完整的请求URL"""
        from module_admin.api_testing.api_services.service.services_service import ServicesService

        # 解析路径中的变量
        path = await self._parse_template(self.test_case.path, self.parameterization)
        path = path.strip() if path else ""

        # 如果路径已经是完整URL,直接返回
        if path.startswith(('http://', 'https://')):
            return path

        base_url = await ServicesService.services_default_services(self.query_db, self.env_id)
        base_url = base_url.strip() if base_url else ""

        # 如果base_url为空
        if not base_url:
            if not path:
                return "http://"
            # path不为空时,确保有协议头
            if not path.startswith(('http://', 'https://')):
                return f"http://{path}"
            return path

        # 确保base_url有协议头
        if not base_url.startswith(('http://', 'https://')):
            base_url = f"http://{base_url}"

        # 如果path为空,返回base_url
        if not path:
            return base_url

        # 移除path开头的/,以便urljoin正确拼接
        path = path.lstrip('/')

        # 确保base_url以/结尾,以便urljoin正确拼接
        if not base_url.endswith('/'):
            base_url = f"{base_url}/"

        full_path = urljoin(base_url, path)
        return full_path
    async def _build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        headers = {}

        if self.test_case.headers_list:
            for header in self.test_case.headers_list:
                if header.key.strip() == '':
                    continue
                if header.is_run:
                    key = await self._parse_template(header.key, self.parameterization)
                    parse_value = await self._parse_template(header.value, self.parameterization)
                    # `不需要类型转换
                    # value = await APIExecutor._type_to_params(parse_value, header.data_type)
                    headers[key] = parse_value

        # 获取全局配置头，覆盖原有参数
        global_headers = self.env_config.global_headers if self.env_config.global_headers else None
        if global_headers:
            for header_glob in global_headers:
                isrun = header_glob.is_run if hasattr(header_glob, "is_run") else False
                if isrun:
                    key = await self._parse_template(header_glob.key, self.parameterization)
                    value = await self._parse_template(header_glob.value, self.parameterization)
                    headers[key] = value

        # 根据请求类型设置默认Content-Type（如果用户没有手动设置）
        if self.test_case.request_type and 'Content-Type' not in headers:
            content_type_map = {
                'JSON': 'application/json',
                'Form_Data': 'multipart/form-data',
                'x_www_form_urlencoded': 'application/x-www-form-urlencoded',
                'XML': 'application/xml',
                'Raw': 'text/plain',
                'Binary': 'application/octet-stream'
            }

            # 特殊处理：Form_Data类型不设置Content-Type，让aiohttp自动生成boundary
            if self.test_case.request_type == Request_Type.Form_Data:
                pass
            elif self.test_case.request_type in content_type_map:
                headers['Content-Type'] = content_type_map[self.test_case.request_type]

        return headers

    async def _build_params(self) -> Optional[Dict[str, str]]:
        """构建查询参数"""
        params = {}

        if self.test_case.params_list:
            for param in self.test_case.params_list:
                if param.key.strip() == '':
                    continue
                if param.is_run:
                    key = await self._parse_template(param.key, self.parameterization)
                    value = await self._parse_template(param.value, self.parameterization)
                    params[key] = value

        return params if params else None

    async def _build_cookies(self) -> Optional[Dict[str, str]]:
        """构建Cookies（包含环境级别的全局Cookies）"""
        cookies = {}

        # 1. 如果启用了 use_env_cookies，先加载环境级别的全局 cookies
        if self.context and self.context.use_env_cookies:
            global_cookies = self.env_config.global_cookies if self.env_config and self.env_config.global_cookies else None
            if global_cookies:
                for cookie_item in global_cookies:
                    is_run = cookie_item.is_run if hasattr(cookie_item, "is_run") else False
                    if is_run:
                        key = await self._parse_template(cookie_item.key, self.parameterization)
                        value = await self._parse_template(cookie_item.value, self.parameterization) if cookie_item.value else ""
                        cookies[key] = value
                logger.info(f"[环境Cookies] 加载了 {len(cookies)} 个环境级别的cookies: {list(cookies.keys())}")

        # 2. 加载用例级别的 cookies（优先级更高，会覆盖环境级别的同名 cookie）
        if self.test_case.cookies_list:
            for cookie in self.test_case.cookies_list:
                if cookie.key.strip() == '':
                    continue
                if cookie.is_run:
                    key = await self._parse_template(cookie.key, self.parameterization)
                    value = await self._parse_template(cookie.value, self.parameterization) if cookie.value else ""
                    cookies[key] = value

        return cookies if cookies else None

    async def _build_request_body(self) -> Union[str, Dict, None, bytes]:
        """构建请求体"""
        if not self.test_case.request_type or self.test_case.request_type == Request_Type.NONE:
            return None

        # JSON请求体
        if self.test_case.request_type == Request_Type.JSON and self.test_case.json_data:
            if isinstance(self.test_case.json_data, str):
                json_str = await self._parse_template(self.test_case.json_data,
                                                      self.parameterization)
            else:
                json_str = await self._parse_template(json.dumps(self.test_case.json_data, ensure_ascii=False), self.parameterization)

            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print(f"JSON解析失败: {e}, 使用原始字符串")
                return json_str

        # Form Data (multipart/form-data)
        if self.test_case.request_type == Request_Type.Form_Data:
            form_data = {}
            if self.test_case.formdata:
                for item in self.test_case.formdata:
                    if item.is_run and item.data_type == DataTypeEnum.FILE:
                        key = await self._parse_template(item.key, self.parameterization)
                        # 如果有文件，就传入文件配置
                        form_data[key] = item.form_file_config
                        continue
                    if item.is_run:
                        key = await self._parse_template(item.key, self.parameterization)
                        value = await self._parse_template(item.value, self.parameterization)
                        form_data[key] = value
            return form_data if form_data else None

        # URL Encoded Form Data
        if self.test_case.request_type == Request_Type.x_www_form_urlencoded:
            form_data = {}
            if self.test_case.formdata:
                for item in self.test_case.formdata:
                    if item.is_run and item.data_type == DataTypeEnum.FILE:
                        continue
                    if item.is_run:
                        key = await self._parse_template(item.key, self.parameterization)
                        value = await self._parse_template(item.value, self.parameterization)
                        form_data[key] = value
            return form_data if form_data else None

        # XML请求体
        if self.test_case.request_type == Request_Type.XML and self.test_case.json_data:
            xml_str = await self._parse_template(self.test_case.json_data, self.parameterization)
            return xml_str

        # Raw文本请求体
        if self.test_case.request_type == Request_Type.Raw and self.test_case.json_data:
            raw_str = await self._parse_template(self.test_case.json_data, self.parameterization)
            return raw_str

        # Binary文件上传
        if self.test_case.request_type == Request_Type.Binary:
            # 如果有文件，就传入文件配置
            return self.test_case.case_file_config.model_dump()

        return None

    def _build_response(
            self,
            response: APIResponse,
            request_info: RequestInfo,
    ) -> APIResponse:
        """构建API响应对象

        Args:
            response: 从请求获取的响应对象（可能包含错误信息）
            request_info: RequestInfo 对象

        Returns:
            APIResponse: 完整的响应对象
        """
        # 处理响应cookies - aiohttp的cookies是SimpleCookie对象
        # 标准方案：SimpleCookie.items() 返回 (key, Morsel) 对，提取完整的 cookie 信息
        response_cookies = {}
        if hasattr(response, 'response_cookies') and response.response_cookies:
            try:
                # 提取所有 cookie 的完整信息（包括 value 和所有属性）
                for key, morsel in response.response_cookies.items():
                    response_cookies[key] = {
                        'value': morsel.value,
                        'expires': morsel.get('expires', ''),
                        'path': morsel.get('path', ''),
                        'comment': morsel.get('comment', ''),
                        'domain': morsel.get('domain', ''),
                        'max-age': morsel.get('max-age', ''),
                        'secure': morsel.get('secure', ''),
                        'httponly': morsel.get('httponly', ''),
                        'version': morsel.get('version', ''),
                        'samesite': morsel.get('samesite', '')
                    }
            except (TypeError, ValueError, AttributeError) as e:
                logger.warning(f"Cookie解析失败: {e}, 使用空字典")
                response_cookies = {}

        # 安全获取 response_headers
        response_headers = {}
        if hasattr(response, 'response_headers') and response.response_headers:
            try:
                response_headers = dict(response.response_headers)
            except (TypeError, ValueError):
                response_headers = {}

        # 获取错误信息（如果有）
        error_message = getattr(response, 'error_message', None)

        return APIResponse(
            case_id=int(self.case_id),
            case_name=str(self.test_case.name),
            env_id=int(self.env_id),
            request_url=request_info.url or '',
            request_method=request_info.method or 'UNKNOWN',
            request_headers=request_info.headers or {},
            request_params=request_info.params,
            request_body=request_info.body,
            request_cookies=request_info.cookies,
            response_status_code=response.response_status_code,
            response_headers=response_headers,
            response_body=response.response_body,
            response_cookies=response_cookies,
            response_time=request_info.response_time or 0,
            execution_time=datetime.now(),
            is_success=response.is_success,
            error_message=error_message,
        )

    def _build_error_response(self, request_info: Optional[RequestInfo], error_message: str) -> APIResponse:
        """构建错误响应对象

        Args:
            request_info: RequestInfo 对象，可能为 None（当请求构建阶段就失败时）
            error_message: 错误信息

        Returns:
            APIResponse: 包含错误信息的响应对象
        """
        # 安全获取请求参数
        request_url = ""
        request_method = "UNKNOWN"
        request_headers = {}
        request_params = None
        request_body = None
        request_cookies = None

        if request_info is not None:
            request_url = request_info.url or ''
            request_method = request_info.method or 'UNKNOWN'
            request_headers = request_info.headers or {}
            request_body = request_info.body
            request_cookies = request_info.cookies
            request_params = request_info.params

        return APIResponse(
            case_id=int(self.case_id) if self.case_id else 0,
            case_name=str(self.test_case.name) if self.test_case and hasattr(self.test_case, 'name') else "Unknown",
            env_id=int(self.env_id) if self.env_id else 0,
            request_url=request_url,
            request_method=request_method,
            request_headers=request_headers,
            request_params=request_params,
            request_body=request_body,
            request_cookies=request_cookies,
            response_status_code=0,
            response_headers={},
            response_body=None,
            response_cookies=None,
            response_time=0,
            execution_time=datetime.now(),
            is_success=False,
            error_message=error_message,
        )
