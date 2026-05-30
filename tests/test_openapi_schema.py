from copy import deepcopy
import asyncio
from pathlib import Path
import sys

_original_argv = sys.argv[:]
sys.argv = [sys.argv[0]]
from server import app, custom_redoc_html, enrich_openapi_schema
sys.argv = _original_argv


def _contains_type_null(value):
    if isinstance(value, dict):
        if value.get('type') == 'null':
            return True
        return any(_contains_type_null(child) for child in value.values())
    if isinstance(value, list):
        return any(_contains_type_null(child) for child in value)
    return False


def _json_response():
    return {
        '200': {
            'description': 'Successful Response',
            'content': {'application/json': {'schema': {}}},
        }
    }


def test_enrich_openapi_schema_converts_openapi_31_nullable_schemas():
    schema = {
        'openapi': '3.1.0',
        'info': {'title': 'CaseGo', 'version': 'test'},
        'paths': {
            '/items': {
                'get': {
                    'summary': 'List items',
                    'parameters': [
                        {
                            'name': 'keyword',
                            'in': 'query',
                            'schema': {
                                'anyOf': [{'type': 'string'}, {'type': 'null'}],
                                'title': 'Keyword',
                            },
                        }
                    ],
                    'responses': _json_response(),
                }
            }
        },
        'components': {'schemas': {}},
    }

    enriched = enrich_openapi_schema(deepcopy(schema))

    parameter_schema = enriched['paths']['/items']['get']['parameters'][0]['schema']
    assert enriched['openapi'] == '3.0.3'
    assert parameter_schema['type'] == 'string'
    assert parameter_schema['nullable'] is True
    assert not _contains_type_null(enriched)


def test_enrich_openapi_schema_adds_common_contract_and_auth_errors():
    schema = {
        'openapi': '3.1.0',
        'info': {'title': 'CaseGo', 'version': 'test'},
        'paths': {
            '/public': {
                'get': {
                    'summary': 'Public endpoint',
                    'responses': _json_response(),
                }
            },
            '/secure': {
                'get': {
                    'summary': 'Secure endpoint',
                    'security': [{'OAuth2PasswordBearer': []}],
                    'responses': _json_response(),
                }
            },
        },
        'components': {'schemas': {}, 'securitySchemes': {'OAuth2PasswordBearer': {'type': 'oauth2'}}},
    }

    enriched = enrich_openapi_schema(deepcopy(schema))

    components = enriched['components']
    secure_responses = enriched['paths']['/secure']['get']['responses']
    public_responses = enriched['paths']['/public']['get']['responses']
    assert 'CaseGoResponse' in components['schemas']
    assert 'UnauthorizedError' in components['responses']
    assert 'ForbiddenError' in components['responses']
    assert secure_responses['401']['$ref'] == '#/components/responses/UnauthorizedError'
    assert secure_responses['403']['$ref'] == '#/components/responses/ForbiddenError'
    assert '401' not in public_responses
    assert '业务' in secure_responses['200']['description']


def test_enrich_openapi_schema_marks_streaming_and_download_endpoints():
    schema = {
        'openapi': '3.1.0',
        'info': {'title': 'CaseGo', 'version': 'test'},
        'paths': {
            '/workflow/workflow/exec': {
                'post': {
                    'summary': 'Exec Workflow Stream',
                    'security': [{'OAuth2PasswordBearer': []}],
                    'responses': _json_response(),
                }
            },
            '/system/user/export': {
                'post': {
                    'summary': 'Export System User List',
                    'security': [{'OAuth2PasswordBearer': []}],
                    'responses': _json_response(),
                }
            },
        },
        'components': {'schemas': {}, 'securitySchemes': {'OAuth2PasswordBearer': {'type': 'oauth2'}}},
    }

    enriched = enrich_openapi_schema(deepcopy(schema))

    stream_content = enriched['paths']['/workflow/workflow/exec']['post']['responses']['200']['content']
    export_content = enriched['paths']['/system/user/export']['post']['responses']['200']['content']
    assert list(stream_content) == ['text/event-stream']
    assert stream_content['text/event-stream']['schema']['type'] == 'string'
    assert list(export_content) == ['application/octet-stream']
    assert export_content['application/octet-stream']['schema']['format'] == 'binary'


def test_enrich_openapi_schema_adds_request_and_response_examples():
    schema = {
        'openapi': '3.1.0',
        'info': {'title': 'CaseGo', 'version': 'test'},
        'paths': {
            '/sample': {
                'post': {
                    'summary': 'Create sample',
                    'security': [{'OAuth2PasswordBearer': []}],
                    'requestBody': {
                        'required': True,
                        'content': {
                            'application/json': {
                                'schema': {'$ref': '#/components/schemas/SampleRequest'}
                            }
                        },
                    },
                    'responses': _json_response(),
                }
            }
        },
        'components': {
            'schemas': {
                'SampleRequest': {
                    'type': 'object',
                    'required': ['userName', 'password'],
                    'properties': {
                        'userName': {'type': 'string', 'description': '用户账号'},
                        'password': {'type': 'string', 'description': '用户密码'},
                        'enabled': {'type': 'boolean', 'description': '是否启用'},
                    },
                }
            },
            'securitySchemes': {'OAuth2PasswordBearer': {'type': 'oauth2'}},
        },
    }

    enriched = enrich_openapi_schema(deepcopy(schema))

    operation = enriched['paths']['/sample']['post']
    request_content = operation['requestBody']['content']['application/json']
    response_content = operation['responses']['200']['content']['application/json']
    properties = enriched['components']['schemas']['SampleRequest']['properties']
    assert request_content['example'] == {'userName': 'admin', 'password': 'admin123', 'enabled': True}
    assert response_content['example']['code'] == 200
    assert properties['userName']['example'] == 'admin'
    assert properties['password']['example'] == 'admin123'


def test_generated_openapi_schema_is_compatible_and_documents_key_contracts():
    app.openapi_schema = None
    schema = app.openapi()

    login_content = schema['paths']['/login']['post']['requestBody']['content']['application/x-www-form-urlencoded']
    assert schema['openapi'] == '3.0.3'
    assert not _contains_type_null(schema)
    assert schema['components']['schemas']['CaseGoResponse']['properties']['code']['example'] == 200
    assert schema['paths']['/getInfo']['get']['responses']['401']['$ref'] == '#/components/responses/UnauthorizedError'
    workflow_exec_response = schema['paths']['/workflow/workflow/exec']['post']['responses']['200']['content']
    user_export_response = schema['paths']['/system/user/export']['post']['responses']['200']['content']
    assert workflow_exec_response['text/event-stream']['schema']['type'] == 'string'
    assert user_export_response['application/octet-stream']['schema']['format'] == 'binary'
    assert login_content['example']['username'] == 'admin'
    assert login_content['example']['password'] == 'admin123'


def test_redoc_html_uses_existing_static_bundle():
    redoc_bundle = Path('CaseGo/download_path/redoc/bundles/redoc.standalone.js')

    response = asyncio.run(custom_redoc_html())
    html = response.body.decode('utf-8')

    assert redoc_bundle.is_file()
    assert '/static/redoc/bundles/redoc.standalone.js' in html
