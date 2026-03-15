"""
cURL 命令解析工具

支持解析 cURL 命令为 API 测试用例格式
兼容 Bash 和 Windows CMD 两种格式
"""
import re
import json
import shlex
from typing import Optional, List, Tuple
from urllib.parse import urlparse, parse_qs, unquote
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel

from config.enums import Request_method, Request_Type
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesModel
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataModel
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersModel
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsModel
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesAllParamsQueryModel


class CurlRequestModel(Test_casesAllParamsQueryModel):
    """cURL解析后的请求模型"""
    model_config = ConfigDict(populate_by_name=True)


class CurlImportRequest(BaseModel):
    """cURL导入请求模型"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    curl_command: str = Field(..., description='cURL命令字符串')
    project_id: int = Field(..., description='项目ID')


class CurlImportResult(BaseModel):
    """cURL导入结果模型"""
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    success: bool = Field(default=True, description='是否成功')
    msg: str = Field(default='', description='消息')
    data: Optional[CurlRequestModel] = Field(default=None, description='解析后的请求数据')


def detect_curl_format(curl_command: str) -> str:
    """
    检测 cURL 命令格式（Bash 或 CMD）

    Args:
        curl_command: cURL 命令字符串

    Returns:
        'bash' 或 'cmd'
    """
    # Chrome CMD 格式特征：使用 ^" 作为引号转义
    # 例如: curl ^"http://example.com^" -H ^"Accept: */*^"
    if '^"' in curl_command:
        return 'cmd'

    # CMD 格式特征：使用 ^ 作为换行续行符
    if re.search(r'\^\s*\n', curl_command):
        return 'cmd'

    # Bash 格式特征：使用 \ 作为换行续行符，或使用单引号包裹参数
    if re.search(r'\\\s*\n', curl_command):
        return 'bash'

    # 检查引号风格
    single_quote_count = curl_command.count("'")
    double_quote_count = curl_command.count('"')

    # 如果有 $' 这样的 bash 语法
    if "$'" in curl_command:
        return 'bash'

    # 如果单引号多于双引号，倾向于 Bash
    if single_quote_count > double_quote_count:
        return 'bash'

    # 默认尝试 Bash
    return 'bash'


def normalize_cmd_curl(curl_command: str) -> str:
    """
    标准化 CMD 格式的 cURL 命令

    Chrome 的 "Copy as cURL (cmd)" 使用以下格式：
    - ^" 表示双引号
    - ^\^" 表示内嵌的转义双引号
    - 行尾 ^ 是续行符

    Args:
        curl_command: CMD 格式的 cURL 命令

    Returns:
        标准化后可被 shlex 解析的命令
    """
    # 去除首尾空白
    curl_command = curl_command.strip()

    # Step 1: 移除行尾续行符 ^ 和换行
    # 匹配: ^ 后跟可选空白和换行
    curl_command = re.sub(r'\^\s*\r?\n\s*', ' ', curl_command)

    # Step 2: 处理嵌套转义 ^\^" -> \"（CMD中表示字面引号）
    curl_command = curl_command.replace('^^', '\x00CARET\x00')  # 临时替换 ^^
    curl_command = curl_command.replace('^\\^"', '\\"')  # ^\^" -> \"

    # Step 3: 将 ^" 转换为普通 "
    curl_command = curl_command.replace('^"', '"')

    # Step 4: 移除其他 ^ 转义符（如 ^& -> &, ^| -> |）
    # 这些在 CMD 中用于转义特殊字符
    curl_command = re.sub(r'\^([&|<>()@^])', r'\1', curl_command)

    # Step 5: 恢复 ^^
    curl_command = curl_command.replace('\x00CARET\x00', '^')

    # 合并多余空白
    curl_command = re.sub(r'\s+', ' ', curl_command)

    return curl_command


def normalize_bash_curl(curl_command: str) -> str:
    """
    标准化 Bash 格式的 cURL 命令

    Args:
        curl_command: Bash 格式的 cURL 命令

    Returns:
        标准化后的单行命令
    """
    # 去除首尾空白
    curl_command = curl_command.strip()

    # 处理 Bash 格式的续行符 \
    curl_command = re.sub(r'\\\s*\r?\n\s*', ' ', curl_command)

    # 合并多余空白
    curl_command = re.sub(r'\s+', ' ', curl_command)

    return curl_command


def parse_curl_arguments(curl_command: str) -> List[str]:
    """
    解析 cURL 命令参数

    Args:
        curl_command: cURL 命令字符串

    Returns:
        参数列表
    """
    # 检测格式
    curl_format = detect_curl_format(curl_command)

    # 根据格式标准化
    if curl_format == 'cmd':
        normalized = normalize_cmd_curl(curl_command)
    else:
        normalized = normalize_bash_curl(curl_command)

    try:
        # 尝试使用 shlex 解析
        args = shlex.split(normalized, posix=True)
    except ValueError:
        # 如果解析失败，尝试非 POSIX 模式
        try:
            args = shlex.split(normalized, posix=False)
        except ValueError:
            # 最后尝试简单分割
            args = normalized.split()

    return args


def parse_header(header_str: str) -> Tuple[str, str]:
    """
    解析单个 Header 字符串

    Args:
        header_str: "Header-Name: Header-Value" 格式的字符串

    Returns:
        (header_name, header_value)
    """
    parts = header_str.split(':', 1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return header_str.strip(), ''


def parse_data_urlencode(data_str: str) -> List[Tuple[str, str]]:
    """
    解析 --data-urlencode 格式的数据

    Args:
        data_str: URL 编码的数据字符串

    Returns:
        [(key, value), ...] 列表
    """
    result = []

    # 检查是否是 key=value 格式
    if '=' in data_str:
        parts = data_str.split('=', 1)
        key = unquote(parts[0])
        value = unquote(parts[1]) if len(parts) > 1 else ''
        result.append((key, value))
    else:
        # 纯内容
        result.append(('', unquote(data_str)))

    return result


def detect_content_type(headers: List[HeadersModel], data: str) -> Request_Type:
    """
    根据 Headers 和数据内容检测请求类型

    Args:
        headers: Headers 列表
        data: 请求数据

    Returns:
        Request_Type
    """
    # 先从 Headers 中查找 Content-Type
    content_type = ''
    for h in headers:
        if h.key.lower() == 'content-type':
            content_type = h.value.lower()
            break

    if 'application/json' in content_type:
        return Request_Type.JSON
    elif 'multipart/form-data' in content_type:
        return Request_Type.Form_Data
    elif 'x-www-form-urlencoded' in content_type:
        return Request_Type.x_www_form_urlencoded
    elif 'xml' in content_type:
        return Request_Type.XML
    elif 'text/plain' in content_type:
        return Request_Type.Raw
    elif 'octet-stream' in content_type or 'binary' in content_type:
        return Request_Type.Binary

    # 如果没有 Content-Type，尝试从数据内容推断
    if data:
        data = data.strip()
        # 尝试解析为 JSON
        if (data.startswith('{') and data.endswith('}')) or \
           (data.startswith('[') and data.endswith(']')):
            try:
                json.loads(data)
                return Request_Type.JSON
            except json.JSONDecodeError:
                pass

        # 检查是否是 URL 编码格式
        if '=' in data and '&' in data:
            return Request_Type.x_www_form_urlencoded
        elif '=' in data:
            return Request_Type.x_www_form_urlencoded

        # 检查是否是 XML
        if data.startswith('<?xml') or data.startswith('<'):
            return Request_Type.XML

    return Request_Type.NONE


def parse_curl_command(curl_command: str) -> CurlImportResult:
    """
    解析 cURL 命令为请求模型

    Args:
        curl_command: cURL 命令字符串（支持 Bash 和 CMD 格式）

    Returns:
        CurlImportResult
    """
    try:
        # 解析参数
        args = parse_curl_arguments(curl_command)

        if not args:
            return CurlImportResult(success=False, msg='cURL命令为空')

        # 移除 'curl' 命令本身
        if args[0].lower() == 'curl':
            args = args[1:]

        # 初始化变量
        url = ''
        method = 'GET'
        headers: List[HeadersModel] = []
        cookies: List[CookiesModel] = []
        params: List[ParamsModel] = []
        formdata: List[FormdataModel] = []
        data_raw = ''
        is_form = False

        # 遍历参数
        i = 0
        while i < len(args):
            arg = args[i]

            # 处理 URL（没有 - 前缀的参数）
            if not arg.startswith('-') and ('http://' in arg or 'https://' in arg or '://' in arg):
                url = arg
                i += 1
                continue

            # -X, --request: 请求方法
            if arg in ('-X', '--request'):
                if i + 1 < len(args):
                    method = args[i + 1].upper()
                    i += 2
                    continue

            # -H, --header: 请求头
            if arg in ('-H', '--header'):
                if i + 1 < len(args):
                    header_name, header_value = parse_header(args[i + 1])

                    # 特殊处理 Cookie 头
                    if header_name.lower() == 'cookie':
                        # 解析 Cookie 字符串
                        cookie_pairs = header_value.split(';')
                        for pair in cookie_pairs:
                            pair = pair.strip()
                            if '=' in pair:
                                ck, cv = pair.split('=', 1)
                                cookies.append(CookiesModel(key=ck.strip(), value=cv.strip()))
                    else:
                        headers.append(HeadersModel(key=header_name, value=header_value))

                    i += 2
                    continue

            # -b, --cookie: Cookie
            if arg in ('-b', '--cookie'):
                if i + 1 < len(args):
                    cookie_str = args[i + 1]
                    cookie_pairs = cookie_str.split(';')
                    for pair in cookie_pairs:
                        pair = pair.strip()
                        if '=' in pair:
                            ck, cv = pair.split('=', 1)
                            cookies.append(CookiesModel(key=ck.strip(), value=cv.strip()))
                    i += 2
                    continue

            # -d, --data, --data-raw, --data-binary: 请求体
            if arg in ('-d', '--data', '--data-raw', '--data-binary'):
                if i + 1 < len(args):
                    data_raw = args[i + 1]
                    # 如果有 -d 参数但没有 -X，默认使用 POST
                    if method == 'GET':
                        method = 'POST'
                    i += 2
                    continue

            # --data-urlencode: URL 编码数据
            if arg == '--data-urlencode':
                if i + 1 < len(args):
                    parsed = parse_data_urlencode(args[i + 1])
                    for key, value in parsed:
                        if key:
                            formdata.append(FormdataModel(key=key, value=value))
                    is_form = True
                    if method == 'GET':
                        method = 'POST'
                    i += 2
                    continue

            # -F, --form: 表单数据 (multipart/form-data)
            if arg in ('-F', '--form'):
                if i + 1 < len(args):
                    form_item = args[i + 1]
                    if '=' in form_item:
                        key, value = form_item.split('=', 1)
                        # 处理文件上传 (@file)
                        if value.startswith('@'):
                            formdata.append(FormdataModel(key=key, value=value))
                        else:
                            formdata.append(FormdataModel(key=key, value=value))
                    is_form = True
                    if method == 'GET':
                        method = 'POST'
                    i += 2
                    continue

            # --compressed: 忽略
            if arg == '--compressed':
                i += 1
                continue

            # -k, --insecure: 忽略 SSL 验证（忽略）
            if arg in ('-k', '--insecure'):
                i += 1
                continue

            # -L, --location: 跟随重定向（忽略）
            if arg in ('-L', '--location'):
                i += 1
                continue

            # -v, --verbose: 详细输出（忽略）
            if arg in ('-v', '--verbose'):
                i += 1
                continue

            # -s, --silent: 静默模式（忽略）
            if arg in ('-s', '--silent'):
                i += 1
                continue

            # -o, --output: 输出文件（忽略）
            if arg in ('-o', '--output'):
                i += 2
                continue

            # -A, --user-agent: User-Agent
            if arg in ('-A', '--user-agent'):
                if i + 1 < len(args):
                    headers.append(HeadersModel(key='User-Agent', value=args[i + 1]))
                    i += 2
                    continue

            # -e, --referer: Referer
            if arg in ('-e', '--referer'):
                if i + 1 < len(args):
                    headers.append(HeadersModel(key='Referer', value=args[i + 1]))
                    i += 2
                    continue

            # -u, --user: 基础认证（暂不处理）
            if arg in ('-u', '--user'):
                i += 2
                continue

            # 其他未识别参数，尝试作为 URL
            if not arg.startswith('-') and not url:
                # 可能是 URL
                if '.' in arg or '/' in arg:
                    url = arg

            i += 1

        # 验证 URL
        if not url:
            return CurlImportResult(success=False, msg='未找到有效的URL')

        # 解析 URL 中的查询参数
        parsed_url = urlparse(url)
        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            for key, values in query_params.items():
                for value in values:
                    params.append(ParamsModel(key=key, value=value))
            # 移除 URL 中的查询字符串，保留 path
            url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        # 确定请求类型
        request_type = detect_content_type(headers, data_raw)

        # 处理请求数据
        json_data = None

        if request_type == Request_Type.JSON:
            try:
                json_data = json.loads(data_raw)
            except json.JSONDecodeError:
                json_data = data_raw
        elif request_type == Request_Type.x_www_form_urlencoded:
            # 解析 URL 编码的表单数据
            if data_raw and not is_form:
                pairs = data_raw.split('&')
                for pair in pairs:
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        formdata.append(FormdataModel(key=unquote(k), value=unquote(v)))
        elif request_type in (Request_Type.XML, Request_Type.Raw):
            json_data = data_raw
        elif request_type == Request_Type.NONE and data_raw:
            # 没有明确类型但有数据，尝试解析为 JSON
            try:
                json_data = json.loads(data_raw)
                request_type = Request_Type.JSON
            except json.JSONDecodeError:
                # 作为表单数据处理
                if '=' in data_raw:
                    pairs = data_raw.split('&')
                    for pair in pairs:
                        if '=' in pair:
                            k, v = pair.split('=', 1)
                            formdata.append(FormdataModel(key=unquote(k), value=unquote(v)))
                    request_type = Request_Type.x_www_form_urlencoded
                else:
                    json_data = data_raw
                    request_type = Request_Type.Raw

        # 处理 -F 表单数据
        if is_form and formdata:
            request_type = Request_Type.Form_Data

        # 验证请求方法
        try:
            method_enum = Request_method(method)
        except ValueError:
            method_enum = Request_method.GET

        # 提取请求名称
        path_parts = parsed_url.path.split('/')
        request_name = path_parts[-1] if path_parts[-1] else 'request'
        # 移除扩展名
        if '.' in request_name:
            request_name = request_name.rsplit('.', 1)[0]
        if not request_name:
            request_name = parsed_url.netloc or 'request'

        # 构建结果
        result = CurlRequestModel(
            name=request_name,
            path=url,
            method=method_enum,
            request_type=request_type,
            cookies_list=cookies,
            headers_list=headers,
            params_list=params,
            json_data=json_data,
            formdata=formdata
        )

        return CurlImportResult(
            success=True,
            msg='解析成功',
            data=result
        )

    except Exception as e:
        return CurlImportResult(
            success=False,
            msg=f'解析cURL命令失败: {str(e)}'
        )


if __name__ == '__main__':
    # 测试用例

    # Bash 格式测试
    curl_bash = '''
    curl 'https://api.example.com/users?page=1&size=10' \
      -H 'Accept: application/json' \
      -H 'Content-Type: application/json' \
      -H 'Cookie: session=abc123; token=xyz789' \
      -X POST \
      -d '{"name": "test", "email": "test@example.com"}'
    '''

    print("===== Bash 格式测试 =====")
    result = parse_curl_command(curl_bash)
    if result.success:
        print(f"请求名称: {result.data.name}")
        print(f"URL: {result.data.path}")
        print(f"方法: {result.data.method.value}")
        print(f"请求类型: {result.data.request_type.value}")
        print(f"Headers: {[(h.key, h.value) for h in result.data.headers_list]}")
        print(f"Cookies: {[(c.key, c.value) for c in result.data.cookies_list]}")
        print(f"Params: {[(p.key, p.value) for p in result.data.params_list]}")
        print(f"JSON数据: {result.data.json_data}")
    else:
        print(f"解析失败: {result.msg}")

    # Chrome CMD 格式测试（Copy as cURL (cmd)）
    curl_cmd_chrome = '''curl ^"http://localhost/dev-api/api_test_cases/test_cases/2236^" ^
  -H ^"Accept: application/json, text/plain, */*^" ^
  -H ^"Authorization: Bearer eyJtoken123^" ^
  -H ^"Content-Type: application/json^" ^
  -b ^"rememberMe=true; username=admin; token=abc123^"'''

    print("\n===== Chrome CMD 格式测试 =====")
    result = parse_curl_command(curl_cmd_chrome)
    if result.success:
        print(f"请求名称: {result.data.name}")
        print(f"URL: {result.data.path}")
        print(f"方法: {result.data.method.value}")
        print(f"Headers: {[(h.key, h.value) for h in result.data.headers_list]}")
        print(f"Cookies: {[(c.key, c.value) for c in result.data.cookies_list]}")
    else:
        print(f"解析失败: {result.msg}")

    # 简单 CMD 格式测试
    curl_cmd = '''
    curl "https://api.example.com/login" ^
      -H "Accept: application/json" ^
      -H "Content-Type: application/x-www-form-urlencoded" ^
      -X POST ^
      -d "username=admin&password=123456"
    '''

    print("\n===== 简单 CMD 格式测试 =====")
    result = parse_curl_command(curl_cmd)
    if result.success:
        print(f"请求名称: {result.data.name}")
        print(f"URL: {result.data.path}")
        print(f"方法: {result.data.method.value}")
        print(f"请求类型: {result.data.request_type.value}")
        print(f"FormData: {[(f.key, f.value) for f in result.data.formdata]}")
    else:
        print(f"解析失败: {result.msg}")

    # 简单格式测试
    curl_simple = 'curl https://api.example.com/health'

    print("\n===== 简单格式测试 =====")
    result = parse_curl_command(curl_simple)
    if result.success:
        print(f"请求名称: {result.data.name}")
        print(f"URL: {result.data.path}")
        print(f"方法: {result.data.method.value}")
    else:
        print(f"解析失败: {result.msg}")
