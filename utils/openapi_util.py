OPENAPI_HTTP_METHODS = {'get', 'post', 'put', 'delete', 'patch', 'options', 'head', 'trace'}

OPENAPI_SERVERS = [
    {'url': '/', 'description': '本地后端直连或同源代理'},
    {'url': '/dev-api', 'description': '前端开发代理前缀，Vite 会转发到后端并去掉 /dev-api'},
]

OPENAPI_TESTING_NOTES = """

## 接口测试约定

- 前端开发环境可通过 `http://localhost/openapi.json` 获取文档，但业务接口调试建议使用
  `http://localhost/dev-api`，或直连后端 `http://127.0.0.1:9099`。
- 除登录、注册、验证码、WebSocket 调试状态等公开接口外，请求头需要携带
  `Authorization: Bearer <token>`。
- 登录接口是 `application/x-www-form-urlencoded`，常用字段为 `username`、`password`、`code`、`uuid`。
- 常规 JSON 响应采用统一结构：`code`、`msg`、`success`、`time`，业务数据通常在 `data` 或 `rows`。
- 当前系统部分业务异常会以 HTTP 200 返回，并通过响应体 `code` 区分结果；自动化断言应优先检查响应体
  `code` 和 `success`。
- 常见业务码：`200` 成功，`401` 未认证或 token 失效，`403` 无接口权限，`500` 服务异常，`601` 业务警告。
- 导出、下载接口返回二进制流；工作流执行和大模型对话相关接口使用 `text/event-stream`。
"""

OPENAPI_SUCCESS_DESCRIPTION = (
    'HTTP 200。常规接口返回统一响应体，业务是否成功请以响应体 code/success 为准；'
    '常见业务码：200 成功，401 未认证或 token 失效，403 无接口权限，500 服务异常，601 业务警告。'
)

OPENAPI_STREAM_ENDPOINTS = {
    ('post', '/workflow/workflow/exec'),
    ('post', '/chat/agent/completions'),
    ('post', '/chat/agent/answer'),
    ('get', '/chat/agent/stream/reconnect'),
}

OPENAPI_DOWNLOAD_PATHS = {
    '/common/download',
    '/common/download/resource',
    '/system/user/importTemplate',
    '/chat/workspace/files/download',
    '/tool/gen/batchGenCode',
}

MAX_EXAMPLE_PROPERTIES = 20


def _ref_name(ref):
    prefix = '#/components/schemas/'
    if isinstance(ref, str) and ref.startswith(prefix):
        return ref.removeprefix(prefix)
    return None


def _resolve_schema(schema, schemas):
    if not isinstance(schema, dict):
        return schema
    ref = _ref_name(schema.get('$ref'))
    if ref:
        return schemas.get(ref, schema)
    return schema


def _merge_all_of_schema(schema, schemas):
    merged = {}
    for item in schema.get('allOf', []):
        resolved = _resolve_schema(item, schemas)
        if not isinstance(resolved, dict):
            continue
        if resolved.get('properties'):
            merged.setdefault('properties', {}).update(resolved.get('properties', {}))
        if resolved.get('required'):
            merged.setdefault('required', []).extend(resolved.get('required', []))
        for key, value in resolved.items():
            if key not in {'properties', 'required'}:
                merged.setdefault(key, value)
    return merged or schema


def _first_schema_option(schema, schemas):
    for key in ('anyOf', 'oneOf'):
        options = schema.get(key)
        if isinstance(options, list):
            for option in options:
                resolved = _resolve_schema(option, schemas)
                if isinstance(resolved, dict) and resolved.get('nullable') is True:
                    continue
                if isinstance(resolved, dict) and not resolved.get('type') and not resolved.get('$ref'):
                    continue
                return resolved
    return schema


def _heuristic_string_example(field_name):
    name = field_name.replace('_', '').replace('-', '').lower()
    if name in {'username', 'useraccount', 'loginname'}:
        return 'admin'
    if name in {'password', 'oldpassword', 'newpassword', 'confirmpassword'}:
        return 'admin123'
    if name == 'granttype':
        return 'password'
    if name == 'code' or name.endswith('code'):
        return '1234'
    if name == 'uuid':
        return 'captcha-uuid'
    if 'email' in name:
        return 'tester@example.com'
    if 'phone' in name or 'mobile' in name:
        return '13800138000'
    if 'url' in name:
        return 'https://example.com'
    if name.endswith('path') or name == 'path':
        return '/example/path'
    if 'token' in name:
        return 'Bearer <token>'
    if name.endswith('name') or name in {'name', 'title'}:
        return '示例名称'
    if name in {'status', 'state', 'type', 'category'} or name.endswith('type'):
        return '0'
    return '示例值'


def _heuristic_number_example(field_name):
    name = field_name.replace('_', '').replace('-', '').lower()
    if name == 'pagenum':
        return 1
    if name == 'pagesize':
        return 10
    if name == 'sortno' or name.endswith('sort') or name.endswith('ordernum'):
        return 1
    return 1


def _example_for_schema(schema, field_name='', schemas=None, depth=0, seen=None):
    schemas = schemas or {}
    seen = seen or set()
    if depth > 4:
        return {}
    if not isinstance(schema, dict):
        return '示例值'

    if 'example' in schema:
        return schema['example']
    if 'examples' in schema and schema['examples']:
        examples = schema['examples']
        if isinstance(examples, list):
            return examples[0]
        if isinstance(examples, dict):
            first_example = next(iter(examples.values()))
            return first_example.get('value') if isinstance(first_example, dict) else first_example
    default = schema.get('default')
    if default is not None and default != '':
        return default
    if schema.get('enum'):
        return schema['enum'][0]

    ref = _ref_name(schema.get('$ref'))
    if ref:
        if ref in seen:
            return {}
        seen.add(ref)
        return _example_for_schema(schemas.get(ref, schema), field_name, schemas, depth + 1, seen)

    if schema.get('allOf'):
        return _example_for_schema(_merge_all_of_schema(schema, schemas), field_name, schemas, depth + 1, seen)
    if schema.get('anyOf') or schema.get('oneOf'):
        return _example_for_schema(_first_schema_option(schema, schemas), field_name, schemas, depth + 1, seen)

    schema_type = schema.get('type')
    schema_format = schema.get('format')

    if schema_format == 'binary':
        return '<binary file>'
    if schema_format == 'date-time':
        return '2026-05-30T00:00:00'
    if schema_format == 'date':
        return '2026-05-30'

    if schema_type == 'object' or schema.get('properties'):
        properties = schema.get('properties', {})
        required = schema.get('required', [])
        ordered_names = list(dict.fromkeys([*required, *properties.keys()]))[:MAX_EXAMPLE_PROPERTIES]
        return {
            name: _example_for_schema(properties[name], name, schemas, depth + 1, seen.copy())
            for name in ordered_names
            if name in properties
        }
    if schema_type == 'array':
        return [_example_for_schema(schema.get('items', {}), field_name, schemas, depth + 1, seen.copy())]
    if schema_type == 'boolean':
        return True
    if schema_type == 'integer':
        return _heuristic_number_example(field_name)
    if schema_type == 'number':
        return float(_heuristic_number_example(field_name))
    if schema_type == 'string':
        return _heuristic_string_example(field_name)
    return _heuristic_string_example(field_name)


def _convert_openapi_31_nullable_to_30(schema_part):
    """
    FastAPI/Pydantic v2 emits OpenAPI 3.1 nullable schemas as anyOf + type:null.
    The project serves OpenAPI 3.0.3 for the bundled Swagger UI, so normalize them.
    """
    if isinstance(schema_part, list):
        for item in schema_part:
            _convert_openapi_31_nullable_to_30(item)
        return

    if not isinstance(schema_part, dict):
        return

    any_of = schema_part.get('anyOf')
    if isinstance(any_of, list):
        non_null_schemas = []
        has_null_schema = False
        for item in any_of:
            if isinstance(item, dict) and item.get('type') == 'null':
                has_null_schema = True
            else:
                non_null_schemas.append(item)

        if has_null_schema and non_null_schemas:
            metadata = {key: value for key, value in schema_part.items() if key != 'anyOf'}
            if len(non_null_schemas) == 1:
                replacement = dict(non_null_schemas[0])
                if '$ref' in replacement and len(replacement) == 1:
                    schema_part.clear()
                    schema_part.update(metadata)
                    schema_part['allOf'] = [replacement]
                else:
                    schema_part.clear()
                    schema_part.update(replacement)
                    schema_part.update(metadata)
            else:
                schema_part['anyOf'] = non_null_schemas
            schema_part['nullable'] = True

    schema_type = schema_part.get('type')
    if isinstance(schema_type, list) and 'null' in schema_type:
        non_null_types = [item for item in schema_type if item != 'null']
        schema_part['nullable'] = True
        if len(non_null_types) == 1:
            schema_part['type'] = non_null_types[0]
        else:
            schema_part.pop('type', None)
            schema_part['anyOf'] = [{'type': item} for item in non_null_types]
    elif schema_type == 'null':
        schema_part.pop('type', None)
        schema_part['nullable'] = True

    for child in list(schema_part.values()):
        _convert_openapi_31_nullable_to_30(child)


def _add_casego_openapi_components(openapi_schema):
    components = openapi_schema.setdefault('components', {})
    schemas = components.setdefault('schemas', {})
    responses = components.setdefault('responses', {})

    schemas.setdefault(
        'CaseGoResponse',
        {
            'title': 'CaseGoResponse',
            'type': 'object',
            'description': 'CaseGo 统一 JSON 响应结构。部分接口会按业务需要增加 token、data、rows 等字段。',
            'properties': {
                'code': {'type': 'integer', 'description': '业务状态码', 'example': 200},
                'msg': {'type': 'string', 'description': '响应消息', 'example': '操作成功'},
                'success': {'type': 'boolean', 'description': '业务是否成功', 'example': True},
                'time': {'type': 'string', 'format': 'date-time', 'description': '响应时间'},
                'data': {'description': '业务数据，结构由具体接口决定', 'nullable': True},
                'rows': {
                    'type': 'array',
                    'description': '分页或列表数据',
                    'items': {},
                },
            },
        },
    )

    responses.setdefault(
        'UnauthorizedError',
        {
            'description': (
                '未认证或 token 失效。缺少 Authorization 时通常返回 HTTP 401；'
                '业务 token 校验失败时当前实现可能返回 HTTP 200 且响应体 code=401。'
            ),
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/CaseGoResponse'},
                    'example': {
                        'code': 401,
                        'msg': '用户token已失效，请重新登录',
                        'success': False,
                        'data': '',
                    },
                }
            },
        },
    )
    responses.setdefault(
        'ForbiddenError',
        {
            'description': (
                '当前用户无接口权限。当前实现通常返回 HTTP 200 且响应体 code=403，'
                '测试断言应以响应体 code/success 为准。'
            ),
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/CaseGoResponse'},
                    'example': {'code': 403, 'msg': '该用户无此接口权限', 'success': False},
                }
            },
        },
    )
    responses.setdefault(
        'ServiceError',
        {
            'description': '服务异常。当前实现通常返回 HTTP 200 且响应体 code=500。',
            'content': {
                'application/json': {
                    'schema': {'$ref': '#/components/schemas/CaseGoResponse'},
                    'example': {'code': 500, 'msg': '接口异常', 'success': False},
                }
            },
        },
    )


def _add_schema_property_examples(openapi_schema):
    schemas = openapi_schema.get('components', {}).get('schemas', {})
    for schema in schemas.values():
        for prop_name, prop_schema in schema.get('properties', {}).items():
            if isinstance(prop_schema, dict) and 'example' not in prop_schema and 'examples' not in prop_schema:
                prop_schema['example'] = _example_for_schema(prop_schema, prop_name, schemas)


def _add_request_body_examples(operation, schemas):
    request_body = operation.get('requestBody')
    if not isinstance(request_body, dict):
        return
    for content_schema in request_body.get('content', {}).values():
        if not isinstance(content_schema, dict):
            continue
        if 'example' in content_schema or 'examples' in content_schema:
            continue
        content_schema['example'] = _example_for_schema(content_schema.get('schema', {}), schemas=schemas)


def _add_response_examples(operation, schemas):
    for response in operation.get('responses', {}).values():
        if not isinstance(response, dict):
            continue
        for media_type, content_schema in response.get('content', {}).items():
            if media_type != 'application/json' or not isinstance(content_schema, dict):
                continue
            if 'example' in content_schema or 'examples' in content_schema:
                continue
            schema = content_schema.get('schema') or {'$ref': '#/components/schemas/CaseGoResponse'}
            example = _example_for_schema(schema, schemas=schemas)
            content_schema['example'] = example or _example_for_schema(
                {'$ref': '#/components/schemas/CaseGoResponse'},
                schemas=schemas,
            )


def _operation_requires_auth(operation):
    return bool(operation.get('security'))


def _is_stream_endpoint(method, path):
    return (method, path) in OPENAPI_STREAM_ENDPOINTS


def _is_download_endpoint(path):
    return path.endswith('/export') or path in OPENAPI_DOWNLOAD_PATHS


def _mark_stream_response(operation):
    responses = operation.setdefault('responses', {})
    responses['200'] = {
        'description': 'SSE 流式响应。每个事件为一行 `data: <json>`，结束事件通常为 `data: [DONE]`。',
        'content': {
            'text/event-stream': {
                'schema': {
                    'type': 'string',
                    'description': 'Server-Sent Events stream',
                },
                'example': 'data: {"type":"message","content":"..."}\\n\\ndata: [DONE]\\n\\n',
            }
        },
    }


def _mark_download_response(operation):
    responses = operation.setdefault('responses', {})
    responses['200'] = {
        'description': '二进制文件流响应。导出接口通常返回 Excel，下载接口按实际文件类型返回。',
        'content': {
            'application/octet-stream': {
                'schema': {
                    'type': 'string',
                    'format': 'binary',
                }
            }
        },
    }


def _enrich_operation(method, path, operation):
    schemas = operation.get('_casego_schemas', {})
    operation.pop('_casego_schemas', None)

    if not operation.get('description') and operation.get('summary'):
        operation['description'] = operation['summary']

    if _is_stream_endpoint(method, path):
        _mark_stream_response(operation)
    elif _is_download_endpoint(path):
        _mark_download_response(operation)
    else:
        response_200 = operation.setdefault('responses', {}).get('200')
        if response_200:
            response_200['description'] = OPENAPI_SUCCESS_DESCRIPTION

    operation['x-casego-response-contract'] = {
        'successCode': 200,
        'authExpiredCode': 401,
        'forbiddenCode': 403,
        'serviceErrorCode': 500,
        'warningCode': 601,
        'assertionHint': '优先断言响应体 code 和 success，HTTP 状态码仅表示传输层结果。',
    }

    if _operation_requires_auth(operation):
        operation['x-casego-auth'] = {
            'type': 'Bearer JWT',
            'header': 'Authorization',
            'format': 'Bearer <token>',
            'loginEndpoint': '/login',
        }
        responses = operation.setdefault('responses', {})
        responses.setdefault('401', {'$ref': '#/components/responses/UnauthorizedError'})
        responses.setdefault('403', {'$ref': '#/components/responses/ForbiddenError'})

    operation.setdefault('responses', {}).setdefault('500', {'$ref': '#/components/responses/ServiceError'})
    _add_request_body_examples(operation, schemas)
    _add_response_examples(operation, schemas)


def enrich_openapi_schema(openapi_schema):
    openapi_schema['openapi'] = '3.0.3'
    openapi_schema['servers'] = OPENAPI_SERVERS

    info = openapi_schema.setdefault('info', {})
    description = info.get('description') or ''
    if '## 接口测试约定' not in description:
        info['description'] = f'{description}{OPENAPI_TESTING_NOTES}'

    _add_casego_openapi_components(openapi_schema)
    _convert_openapi_31_nullable_to_30(openapi_schema)
    _add_schema_property_examples(openapi_schema)

    schemas = openapi_schema.get('components', {}).get('schemas', {})
    for path, path_item in openapi_schema.get('paths', {}).items():
        for method, operation in path_item.items():
            if method in OPENAPI_HTTP_METHODS:
                operation['_casego_schemas'] = schemas
                _enrich_operation(method, path, operation)

    return openapi_schema
