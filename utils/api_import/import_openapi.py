#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : fast_api_admin
@File    : import_openapi.py
@Author  : Claude
@Date    : 2025-12-05
@Description : OpenAPI/Swagger 规范导入工具
支持 OpenAPI 3.0、3.1 和 Swagger 2.0 格式
支持 JSON 和 YAML 文件格式
"""

import json
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Union, Tuple
from urllib.parse import urljoin

import requests
import yaml
from pydantic import BaseModel, Field, ConfigDict

from config.enums import Request_method, Request_Type
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesModel
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataModel
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersModel
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsModel
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesAllParamsQueryModel


class OpenAPIRequestModel(Test_casesAllParamsQueryModel):
    """OpenAPI解析后的请求模型"""
    model_config = ConfigDict(populate_by_name=True)

    operation_id: Optional[str] = Field(default=None, description='操作ID')
    tags: Optional[List[str]] = Field(default=[], description='标签列表')
    summary: Optional[str] = Field(default=None, description='接口摘要')
    deprecated: Optional[bool] = Field(default=False, description='是否已废弃')
    security: Optional[List[Dict]] = Field(default=None, description='安全配置')


class OpenAPIFilterConfig(BaseModel):
    """OpenAPI解析过滤配置"""
    allowed_methods: Optional[List[str]] = Field(default=None, description='允许的HTTP方法，None表示全部')
    include_tags: Optional[List[str]] = Field(default=None, description='只包含的标签，None表示全部')
    exclude_tags: Optional[List[str]] = Field(default=None, description='排除的标签')
    path_patterns: Optional[List[str]] = Field(default=None, description='路径正则匹配模式，None表示全部')
    include_deprecated: bool = Field(default=False, description='是否包含已废弃的接口')


class OpenAPIInfo(BaseModel):
    """OpenAPI基本信息"""
    title: str = Field(description='API标题')
    version: str = Field(description='API版本')
    description: Optional[str] = Field(default=None, description='API描述')
    openapi_version: str = Field(description='OpenAPI规范版本')
    base_url: Optional[str] = Field(default=None, description='基础URL')


class OpenAPIParseResult(BaseModel):
    """OpenAPI解析结果"""
    info: OpenAPIInfo = Field(description='API基本信息')
    requests: List[OpenAPIRequestModel] = Field(default=[], description='请求列表')
    tags: Dict[str, int] = Field(default={}, description='标签统计')
    methods: Dict[str, int] = Field(default={}, description='方法统计')


def detect_openapi_version(spec: Dict) -> str:
    """
    检测OpenAPI规范版本

    Args:
        spec: OpenAPI规范字典

    Returns:
        版本字符串: 'swagger2', 'openapi3.0', 'openapi3.1'
    """
    if 'swagger' in spec:
        return 'swagger2'
    elif 'openapi' in spec:
        version = spec['openapi']
        if version.startswith('3.1'):
            return 'openapi3.1'
        elif version.startswith('3.0'):
            return 'openapi3.0'
        else:
            return f'openapi{version}'
    return 'unknown'


def load_spec_from_url(url: str, timeout: int = 30) -> Dict:
    """
    从URL加载OpenAPI规范

    Args:
        url: OpenAPI规范URL
        timeout: 请求超时时间（秒）

    Returns:
        解析后的规范字典
    """
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()

    content_type = response.headers.get('Content-Type', '').lower()

    # 尝试JSON解析
    if 'json' in content_type or url.endswith('.json'):
        return response.json()

    # 尝试YAML解析
    if 'yaml' in content_type or 'yml' in content_type or url.endswith(('.yaml', '.yml')):
        return yaml.safe_load(response.text)

    # 自动检测
    try:
        return response.json()
    except json.JSONDecodeError:
        return yaml.safe_load(response.text)


def load_spec_from_file(file_path: str) -> Dict:
    """
    从文件加载OpenAPI规范

    Args:
        file_path: 文件路径

    Returns:
        解析后的规范字典
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    content = path.read_text(encoding='utf-8')

    # 根据扩展名判断格式
    if path.suffix.lower() == '.json':
        return json.loads(content)
    elif path.suffix.lower() in ('.yaml', '.yml'):
        return yaml.safe_load(content)
    else:
        # 自动检测
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return yaml.safe_load(content)


def get_base_url(spec: Dict, version: str) -> Optional[str]:
    """
    获取API基础URL

    Args:
        spec: OpenAPI规范
        version: 规范版本

    Returns:
        基础URL或None
    """
    if version == 'swagger2':
        # Swagger 2.0: host + basePath + schemes
        host = spec.get('host', '')
        base_path = spec.get('basePath', '')
        schemes = spec.get('schemes', ['https'])
        if host:
            scheme = schemes[0] if schemes else 'https'
            return f"{scheme}://{host}{base_path}"
    else:
        # OpenAPI 3.x: servers
        servers = spec.get('servers', [])
        if servers:
            return servers[0].get('url', '')
    return None


def resolve_ref(spec: Dict, ref: str) -> Dict:
    """
    解析$ref引用

    Args:
        spec: 完整规范
        ref: 引用路径，如 '#/components/schemas/User'

    Returns:
        解析后的对象
    """
    if not ref.startswith('#/'):
        return {}

    parts = ref[2:].split('/')
    result = spec

    for part in parts:
        if isinstance(result, dict) and part in result:
            result = result[part]
        else:
            return {}

    return result if isinstance(result, dict) else {}


def extract_schema_example(spec: Dict, schema: Dict) -> Any:
    """
    从schema提取示例值

    Args:
        spec: 完整规范
        schema: schema定义

    Returns:
        示例值
    """
    # 处理$ref
    if '$ref' in schema:
        schema = resolve_ref(spec, schema['$ref'])

    # 直接有example
    if 'example' in schema:
        return schema['example']

    # 有默认值
    if 'default' in schema:
        return schema['default']

    # 根据类型生成示例
    schema_type = schema.get('type', 'string')

    if schema_type == 'object':
        result = {}
        properties = schema.get('properties', {})
        for prop_name, prop_schema in properties.items():
            result[prop_name] = extract_schema_example(spec, prop_schema)
        return result
    elif schema_type == 'array':
        items = schema.get('items', {})
        return [extract_schema_example(spec, items)]
    elif schema_type == 'string':
        format_type = schema.get('format', '')
        if format_type == 'date':
            return '2024-01-01'
        elif format_type == 'date-time':
            return '2024-01-01T00:00:00Z'
        elif format_type == 'email':
            return 'user@example.com'
        elif format_type == 'uuid':
            return '00000000-0000-0000-0000-000000000000'
        elif 'enum' in schema:
            return schema['enum'][0] if schema['enum'] else ''
        return ''
    elif schema_type == 'integer':
        return 0
    elif schema_type == 'number':
        return 0.0
    elif schema_type == 'boolean':
        return False

    return None


def parse_request_body_v3(spec: Dict, request_body: Dict) -> Tuple[Request_Type, Any, List[FormdataModel]]:
    """
    解析OpenAPI 3.x请求体

    Args:
        spec: 完整规范
        request_body: requestBody定义

    Returns:
        (request_type, json_data, formdata)
    """
    # 处理$ref
    if '$ref' in request_body:
        request_body = resolve_ref(spec, request_body['$ref'])

    content = request_body.get('content', {})

    request_type = Request_Type.NONE
    json_data = None
    formdata = []

    # JSON
    if 'application/json' in content:
        request_type = Request_Type.JSON
        schema = content['application/json'].get('schema', {})
        example = content['application/json'].get('example')
        json_data = example if example else extract_schema_example(spec, schema)

    # Form Data (multipart)
    elif 'multipart/form-data' in content:
        request_type = Request_Type.Form_Data
        schema = content['multipart/form-data'].get('schema', {})
        if '$ref' in schema:
            schema = resolve_ref(spec, schema['$ref'])
        properties = schema.get('properties', {})
        for prop_name, prop_schema in properties.items():
            value = extract_schema_example(spec, prop_schema)
            formdata.append(FormdataModel(
                key=prop_name,
                value=str(value) if value is not None else ''
            ))

    # URL Encoded
    elif 'application/x-www-form-urlencoded' in content:
        request_type = Request_Type.x_www_form_urlencoded
        schema = content['application/x-www-form-urlencoded'].get('schema', {})
        if '$ref' in schema:
            schema = resolve_ref(spec, schema['$ref'])
        properties = schema.get('properties', {})
        for prop_name, prop_schema in properties.items():
            value = extract_schema_example(spec, prop_schema)
            formdata.append(FormdataModel(
                key=prop_name,
                value=str(value) if value is not None else ''
            ))

    # XML
    elif 'application/xml' in content or 'text/xml' in content:
        request_type = Request_Type.XML
        mime = 'application/xml' if 'application/xml' in content else 'text/xml'
        example = content[mime].get('example', '')
        json_data = example

    # Raw text
    elif 'text/plain' in content:
        request_type = Request_Type.Raw
        json_data = content['text/plain'].get('example', '')

    # Binary
    elif 'application/octet-stream' in content:
        request_type = Request_Type.Binary
        json_data = ''

    return request_type, json_data, formdata


def parse_request_body_v2(spec: Dict, consumes: List[str], parameters: List[Dict]) -> Tuple[Request_Type, Any, List[FormdataModel]]:
    """
    解析Swagger 2.0请求体

    Args:
        spec: 完整规范
        consumes: 内容类型列表
        parameters: 参数列表

    Returns:
        (request_type, json_data, formdata)
    """
    request_type = Request_Type.NONE
    json_data = None
    formdata = []

    # 查找body参数
    body_params = [p for p in parameters if p.get('in') == 'body']
    form_params = [p for p in parameters if p.get('in') == 'formData']

    if body_params:
        body_param = body_params[0]
        schema = body_param.get('schema', {})

        if 'application/json' in consumes:
            request_type = Request_Type.JSON
            json_data = extract_schema_example(spec, schema)
        elif 'application/xml' in consumes:
            request_type = Request_Type.XML
            json_data = extract_schema_example(spec, schema)

    elif form_params:
        if 'multipart/form-data' in consumes:
            request_type = Request_Type.Form_Data
        elif 'application/x-www-form-urlencoded' in consumes:
            request_type = Request_Type.x_www_form_urlencoded

        for param in form_params:
            value = param.get('default', param.get('example', ''))
            formdata.append(FormdataModel(
                key=param.get('name', ''),
                value=str(value) if value is not None else ''
            ))

    return request_type, json_data, formdata


def parse_parameters(spec: Dict, parameters: List[Dict], version: str) -> Tuple[List[ParamsModel], List[HeadersModel], List[CookiesModel], Dict[str, str]]:
    """
    解析参数列表

    Args:
        spec: 完整规范
        parameters: 参数列表
        version: 规范版本

    Returns:
        (query_params, headers, cookies, path_params)
    """
    query_params = []
    headers = []
    cookies = []
    path_params = {}

    for param in parameters:
        # 处理$ref
        if '$ref' in param:
            param = resolve_ref(spec, param['$ref'])

        param_in = param.get('in', 'query')
        param_name = param.get('name', '')

        # 获取默认值或示例值
        if version.startswith('openapi'):
            # OpenAPI 3.x
            schema = param.get('schema', {})
            if '$ref' in schema:
                schema = resolve_ref(spec, schema['$ref'])
            value = param.get('example', schema.get('default', schema.get('example', '')))
        else:
            # Swagger 2.0
            value = param.get('default', param.get('example', param.get('x-example', '')))

        value_str = str(value) if value is not None else ''

        if param_in == 'query':
            query_params.append(ParamsModel(key=param_name, value=value_str))
        elif param_in == 'header':
            headers.append(HeadersModel(key=param_name, value=value_str))
        elif param_in == 'cookie':
            cookies.append(CookiesModel(key=param_name, value=value_str))
        elif param_in == 'path':
            path_params[param_name] = value_str

    return query_params, headers, cookies, path_params


def replace_path_params(path: str, path_params: Dict[str, str]) -> str:
    """
    替换路径参数占位符

    Args:
        path: 原始路径，如 /users/{id}
        path_params: 路径参数字典

    Returns:
        替换后的路径，保留{param}格式作为占位符
    """
    # 保留原始路径格式，供变量替换使用
    return path


def parse_openapi_to_requests(
    spec: Dict,
    filter_config: Optional[OpenAPIFilterConfig] = None,
    base_url_override: Optional[str] = None
) -> OpenAPIParseResult:
    """
    解析OpenAPI规范为请求模型列表

    Args:
        spec: OpenAPI规范字典
        filter_config: 过滤配置
        base_url_override: 覆盖基础URL

    Returns:
        OpenAPIParseResult: 解析结果
    """
    if filter_config is None:
        filter_config = OpenAPIFilterConfig()

    version = detect_openapi_version(spec)
    base_url = base_url_override or get_base_url(spec, version) or ''

    # 提取基本信息
    info = spec.get('info', {})
    api_info = OpenAPIInfo(
        title=info.get('title', 'Unknown API'),
        version=info.get('version', '1.0.0'),
        description=info.get('description'),
        openapi_version=spec.get('openapi', spec.get('swagger', 'unknown')),
        base_url=base_url
    )

    requests_list = []
    tags_count = {}
    methods_count = {}

    paths = spec.get('paths', {})

    # 全局参数（Swagger 2.0）
    global_consumes = spec.get('consumes', ['application/json'])

    for path, path_item in paths.items():
        # 路径级别参数
        path_level_params = path_item.get('parameters', [])

        for method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
            if method not in path_item:
                continue

            operation = path_item[method]
            method_upper = method.upper()

            # 过滤：方法
            if filter_config.allowed_methods and method_upper not in filter_config.allowed_methods:
                continue

            # 过滤：标签
            tags = operation.get('tags', ['未分类'])
            if filter_config.include_tags:
                if not any(tag in filter_config.include_tags for tag in tags):
                    continue
            if filter_config.exclude_tags:
                if any(tag in filter_config.exclude_tags for tag in tags):
                    continue

            # 过滤：路径模式
            if filter_config.path_patterns:
                if not any(re.search(pattern, path) for pattern in filter_config.path_patterns):
                    continue

            # 过滤：废弃接口
            deprecated = operation.get('deprecated', False)
            if deprecated and not filter_config.include_deprecated:
                continue

            # 合并参数（路径级别 + 操作级别）
            all_params = path_level_params + operation.get('parameters', [])

            # 解析参数
            query_params, headers, cookies, path_params = parse_parameters(spec, all_params, version)

            # 解析请求体
            if version.startswith('openapi'):
                # OpenAPI 3.x
                request_body = operation.get('requestBody', {})
                request_type, json_data, formdata = parse_request_body_v3(spec, request_body)
            else:
                # Swagger 2.0
                consumes = operation.get('consumes', global_consumes)
                request_type, json_data, formdata = parse_request_body_v2(spec, consumes, all_params)

            # 构建请求名称
            operation_id = operation.get('operationId', '')
            summary = operation.get('summary', '')
            request_name = summary or operation_id or f"{method_upper} {path}"

            # 构建完整路径
            full_path = path if not base_url else urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))

            # 创建请求模型
            req_model = OpenAPIRequestModel(
                name=request_name,
                path=full_path,
                method=Request_method(method_upper),
                request_type=request_type,
                json_data=json_data,
                cookies_list=cookies,
                headers_list=headers,
                params_list=query_params,
                formdata=formdata,
                operation_id=operation_id,
                tags=tags,
                summary=summary,
                deprecated=deprecated,
                security=operation.get('security'),
                description=operation.get('description', '')
            )

            requests_list.append(req_model)

            # 统计
            methods_count[method_upper] = methods_count.get(method_upper, 0) + 1
            for tag in tags:
                tags_count[tag] = tags_count.get(tag, 0) + 1

    return OpenAPIParseResult(
        info=api_info,
        requests=requests_list,
        tags=tags_count,
        methods=methods_count
    )


def import_from_url(
    url: str,
    filter_config: Optional[OpenAPIFilterConfig] = None,
    base_url_override: Optional[str] = None,
    timeout: int = 30
) -> OpenAPIParseResult:
    """
    从URL导入OpenAPI规范

    Args:
        url: OpenAPI规范URL
        filter_config: 过滤配置
        base_url_override: 覆盖基础URL
        timeout: 请求超时时间（秒）

    Returns:
        OpenAPIParseResult: 解析结果
    """
    spec = load_spec_from_url(url, timeout)
    return parse_openapi_to_requests(spec, filter_config, base_url_override)


def import_from_file(
    file_path: str,
    filter_config: Optional[OpenAPIFilterConfig] = None,
    base_url_override: Optional[str] = None
) -> OpenAPIParseResult:
    """
    从文件导入OpenAPI规范

    Args:
        file_path: 文件路径（支持JSON和YAML）
        filter_config: 过滤配置
        base_url_override: 覆盖基础URL

    Returns:
        OpenAPIParseResult: 解析结果
    """
    spec = load_spec_from_file(file_path)
    return parse_openapi_to_requests(spec, filter_config, base_url_override)


def import_openapi(
    source: str,
    filter_config: Optional[OpenAPIFilterConfig] = None,
    base_url_override: Optional[str] = None,
    timeout: int = 30
) -> OpenAPIParseResult:
    """
    统一导入接口，自动判断URL或文件

    Args:
        source: URL或文件路径
        filter_config: 过滤配置
        base_url_override: 覆盖基础URL
        timeout: 请求超时时间（秒）

    Returns:
        OpenAPIParseResult: 解析结果
    """
    if source.startswith(('http://', 'https://')):
        return import_from_url(source, filter_config, base_url_override, timeout)
    else:
        return import_from_file(source, filter_config, base_url_override)


def print_parse_summary(result: OpenAPIParseResult):
    """打印解析摘要"""
    print("=" * 60)
    print(f"API 标题: {result.info.title}")
    print(f"API 版本: {result.info.version}")
    print(f"OpenAPI 版本: {result.info.openapi_version}")
    print(f"基础 URL: {result.info.base_url or 'N/A'}")
    if result.info.description:
        print(f"描述: {result.info.description[:100]}...")
    print("=" * 60)

    print(f"\n总接口数: {len(result.requests)}")

    print("\nHTTP 方法统计:")
    for method, count in sorted(result.methods.items(), key=lambda x: x[1], reverse=True):
        print(f"  {method:8s}: {count}")

    print("\n标签统计 (Top 10):")
    sorted_tags = sorted(result.tags.items(), key=lambda x: x[1], reverse=True)[:10]
    for tag, count in sorted_tags:
        print(f"  {tag:30s}: {count}")


if __name__ == '__main__':
    # 测试URL导入
    print("\n" + "=" * 60)
    print("测试从URL导入 OpenAPI")
    print("=" * 60)

    try:
        url = "http://127.0.0.1:9099/openapi.json"
        # url = "http://106.14.151.162:9902/v2/api-docs?group=%E6%89%80%E6%9C%89API%E6%8E%A5%E5%8F%A3"
        result = import_from_url(url)
        print_parse_summary(result)

        # 打印前5个接口
        print("\n前5个接口:")
        for idx, req in enumerate(result.requests[:5], 1):
            print(f"\n--- 接口 {idx} ---")
            print(f"名称: {req.name}")
            print(f"方法: {req.method.value}")
            print(f"路径: {req.path}")
            print(f"标签: {req.tags}")
            print(f"请求类型: {req.request_type.value}")
            if req.params_list:
                print(f"Query参数: {[p.key for p in req.params_list]}")
            if req.headers_list:
                print(f"Headers: {[h.key for h in req.headers_list]}")
            if req.json_data:
                print(f"JSON数据: {json.dumps(req.json_data, ensure_ascii=False)[:100]}...")
            if req.formdata:
                print(f"表单数据: {[f.key for f in req.formdata]}")
    except Exception as e:
        print(f"URL导入测试失败: {e}")

    # 测试过滤
    print("\n" + "=" * 60)
    print("测试过滤功能")
    print("=" * 60)

    try:
        # 只要POST方法
        config = OpenAPIFilterConfig(allowed_methods=['POST'])
        result = import_from_url(url, filter_config=config)
        print(f"POST接口数: {len(result.requests)}")

        # 只要包含login的路径
        config = OpenAPIFilterConfig(path_patterns=[r'login'])
        result = import_from_url(url, filter_config=config)
        print(f"包含'login'路径的接口数: {len(result.requests)}")
    except Exception as e:
        print(f"过滤测试失败: {e}")

    # 测试文件导入
    print("\n" + "=" * 60)
    print("测试从文件导入")
    print("=" * 60)
    result = import_from_file(r'D:\code\project\fast_api_admin\utils\api_import\openapi.json')
    # 示例：从本地文件导入
    # result = import_from_file("path/to/openapi.json")
    # result = import_from_file("path/to/openapi.yaml")
    print("使用示例:")
    print("  result = import_from_file('path/to/openapi.json')")
    print("  result = import_from_file('path/to/openapi.yaml')")
    print("  result = import_openapi('http://example.com/openapi.json')")
    print("  result = import_openapi('/local/path/spec.yaml')")
