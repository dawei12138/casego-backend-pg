from haralyzer import HarParser
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
import json
import requests
from urllib.parse import urlparse

from config.enums import Request_method, Request_Type
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesModel
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataModel
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersModel
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsModel
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesAllParamsQueryModel
from utils.common_util import ensure_path_sep


class HarRequestModel(Test_casesAllParamsQueryModel):
    """HAR解析后的请求模型"""
    model_config = ConfigDict(populate_by_name=True)


class HarFilterConfig(BaseModel):
    """HAR解析过滤配置"""
    filter_static: bool = Field(default=True, description='过滤静态资源文件')
    allowed_methods: Optional[List[str]] = Field(default=None, description='允许的HTTP方法，None表示全部')
    include_domains: Optional[List[str]] = Field(default=None, description='只包含的域名，None表示全部')
    url_keywords: Optional[List[str]] = Field(default=None, description='URL必须包含的关键词，None表示全部')


# 静态资源扩展名和MIME类型
STATIC_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.css', '.js', '.woff', '.woff2', '.ttf', '.mp4',
               '.mp3'}
STATIC_MIMES = {'image/', 'text/css', 'javascript', 'font/', 'audio/', 'video/'}


def is_static_resource(url: str, mime_type: str) -> bool:
    """判断是否为静态资源"""
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in STATIC_EXTS) or any(mime in mime_type for mime in STATIC_MIMES)


def parse_formdata_params(params: List[dict]) -> List[FormdataModel]:
    """
    解析表单参数，处理嵌套的字典值

    Args:
        params: HAR文件中的params列表

    Returns:
        List[FormdataModel]: 表单数据模型列表
    """
    formdata = []
    for p in params:
        param_name = p.get('name', '')
        param_value = p.get('value', '')

        # 如果value是字典，需要展开
        if isinstance(param_value, dict):
            for key, val in param_value.items():
                formdata.append(FormdataModel(
                    key=key,
                    value=str(val) if not isinstance(val, str) else val
                ))
        # 如果value是列表，每个元素作为一个条目
        elif isinstance(param_value, list):
            for item in param_value:
                if isinstance(item, dict):
                    # 列表中的字典也需要展开
                    for key, val in item.items():
                        formdata.append(FormdataModel(key=key, value=str(val)))
                else:
                    formdata.append(FormdataModel(key=param_name, value=str(item)))
        # 普通字符串或其他类型
        else:
            formdata.append(FormdataModel(
                key=param_name,
                value=str(param_value) if param_value is not None else ''
            ))

    return formdata


def parse_request_type_and_body(post_data: dict) -> tuple:
    """
    解析请求体类型和数据

    Args:
        post_data: HAR文件中的postData字段

    Returns:
        tuple: (request_type, json_data, formdata)
    """
    mime = post_data.get('mimeType', '').lower()
    text = post_data.get('text', '')
    params = post_data.get('params', [])

    request_type = Request_Type.NONE
    json_data = None
    formdata = []

    # 1. JSON类型
    if 'application/json' in mime or 'json' in mime:
        request_type = Request_Type.JSON
        if text:
            try:
                json_data = json.loads(text)
            except json.JSONDecodeError:
                # 如果解析失败，保留原始字符串
                json_data = text
        else:
            json_data = {}

    # 2. Form Data (multipart/form-data)
    elif 'multipart/form-data' in mime:
        request_type = Request_Type.Form_Data
        formdata = parse_formdata_params(params)

    # 3. URL Encoded (application/x-www-form-urlencoded)
    elif 'x-www-form-urlencoded' in mime or 'urlencoded' in mime:
        request_type = Request_Type.x_www_form_urlencoded
        # 如果有params，使用params；否则尝试解析text
        if params:
            formdata = parse_formdata_params(params)
        elif text:
            # 手动解析URL编码的数据
            try:
                from urllib.parse import parse_qs
                parsed = parse_qs(text)
                formdata = [
                    FormdataModel(key=k, value=v[0] if v else '')
                    for k, v in parsed.items()
                ]
            except:
                # 解析失败，保留原始文本
                formdata = [FormdataModel(key='raw', value=text)]

    # 4. XML类型
    elif 'xml' in mime:
        request_type = Request_Type.XML
        json_data = text  # XML存储为字符串

    # 5. 纯文本或其他
    elif 'text/plain' in mime or text:
        request_type = Request_Type.Raw
        json_data = text

    # 6. Binary数据
    elif 'octet-stream' in mime or 'binary' in mime:
        request_type = Request_Type.Binary
        json_data = text

    return request_type, json_data, formdata


def parse_har_to_requests(har_file_path: str, filter_config: Optional[HarFilterConfig] = None) -> List[HarRequestModel]:
    """
    解析HAR文件为请求模型列表

    Args:
        har_file_path: HAR文件路径
        filter_config: 过滤配置，默认过滤静态资源

    Returns:
        List[HarRequestModel]: 请求模型列表
    """
    if filter_config is None:
        filter_config = HarFilterConfig()

    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_parser = HarParser(json.load(f))

    requests_list = []

    for entry in har_parser.har_data['entries']:
        request = entry['request']
        response = entry['response']
        url = request['url']
        method = request['method']
        mime_type = response['content'].get('mimeType', '')

        # 过滤逻辑
        if filter_config.filter_static and is_static_resource(url, mime_type):
            continue
        if filter_config.allowed_methods and method not in filter_config.allowed_methods:
            continue
        if filter_config.include_domains and urlparse(url).netloc not in filter_config.include_domains:
            continue
        if filter_config.url_keywords and not any(kw in url for kw in filter_config.url_keywords):
            continue

        # 解析基础数据
        query_params = [ParamsModel(key=p['name'], value=p['value']) for p in request.get('queryString', [])]
        headers = [HeadersModel(key=h['name'], value=h['value']) for h in request.get('headers', [])]
        cookies = [CookiesModel(key=c['name'], value=c['value']) for c in request.get('cookies', [])]

        # 解析请求体类型和数据
        post_data = request.get('postData', {})
        request_type, json_data, formdata = parse_request_type_and_body(post_data)

        # 提取请求名称（从URL路径的最后一部分）
        path_parts = url.split('/')[-1].split('?')
        request_name = path_parts[0] if path_parts[0] else 'request'

        req_model = HarRequestModel(
            name=request_name,
            path=url,
            method=Request_method(method),
            request_type=request_type,
            status_code=response['status'],
            cookies_list=cookies,
            headers_list=headers,
            params_list=query_params,
            json_data=json_data,
            formdata=formdata
        )

        requests_list.append(req_model)

    return requests_list


def execute_request(req_model: HarRequestModel) -> requests.Response:
    """根据模型执行HTTP请求"""
    kwargs = {
        'headers': {h.key: h.value for h in req_model.headers_list},
        'cookies': {c.key: c.value for c in req_model.cookies_list},
        'params': {p.key: p.value for p in req_model.params_list}
    }

    if req_model.request_type == Request_Type.JSON and req_model.json_data:
        kwargs['json'] = req_model.json_data
    elif req_model.request_type in [Request_Type.Form_Data, Request_Type.x_www_form_urlencoded]:
        kwargs['data'] = {f.key: f.value for f in req_model.formdata}
    elif req_model.request_type in [Request_Type.XML, Request_Type.Raw]:
        kwargs['data'] = req_model.json_data
    elif req_model.request_type == Request_Type.Binary:
        kwargs['data'] = req_model.json_data

    return requests.request(method=req_model.method.value, url=req_model.path, **kwargs)


if __name__ == '__main__':
    path = ensure_path_sep("/CaseGo/upload_path/files/2025/11/17/file_20251117181517_380fc2f1_291973.har")

    # 默认：过滤静态资源
    print("解析HAR文件...")
    har_requests = parse_har_to_requests(path)
    print(f"共解析 {len(har_requests)} 个API请求\n")

    # 只要POST请求
    config = HarFilterConfig(allowed_methods=['POST'])
    har_requests = parse_har_to_requests(path, config)
    print(f"POST请求: {len(har_requests)} 个\n")

    # 只要包含baidu.com的请求
    config = HarFilterConfig(url_keywords=['baidu.com'])
    har_requests = parse_har_to_requests(path, config)
    print(f"包含baidu.com的请求: {len(har_requests)} 个\n")

    # 打印前3个请求的详细信息
    for idx, req in enumerate(har_requests[:3], 1):
        print(f"\n========== 请求 {idx} ==========")
        print(f"请求名称: {req.name}")
        print(f"URL: {req.path}")
        print(f"方法: {req.method.value}")
        print(f"请求类型: {req.request_type.value}")
        print(f"状态码: {req.status_code}")

        if req.request_type == Request_Type.JSON:
            print(f"JSON数据: {json.dumps(req.json_data, ensure_ascii=False, indent=2)[:200]}...")
        elif req.request_type in [Request_Type.Form_Data, Request_Type.x_www_form_urlencoded]:
            print(f"表单数据: {[f'{f.key}={f.value}' for f in req.formdata[:3]]}")

        print(f"Headers数量: {len(req.headers_list)}")
        print(f"Cookies数量: {len(req.cookies_list)}")
        print(f"Query参数数量: {len(req.params_list)}")