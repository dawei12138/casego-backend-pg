import json

from datetime import datetime
from typing import Any, Optional, Dict

from fastmcp import Context
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from config.enums import Request_Type
from config.get_db import get_db

from module_admin.api_testing.api_test_cases.service.test_cases_service import Test_casesService
from module_fastmcp.tools.JsonToSchema import convert_json_to_schema
from utils.log_util import logger

# 导入MCP实例
from module_fastmcp.mcp_instance import mcp


#
@mcp.resource("config://server")
def load_config():
    """加载服务器配置"""
    return {
        "server_name": "MCP Development Server",
        "version": "1.0.0",
        "max_connections": 100,
        "timeout": 30,
        "analytics_enabled": True,
        "features": {
            "logging": True,
            "caching": True,
            "authentication": True
        },
        "updated_at": datetime.now().isoformat()
    }


@mcp.resource("template://api-test-best-practices")
def get_api_test_best_practices():
    """
    API 测试最佳实践指南
    """
    return {
        "title": "API 测试最佳实践",
        "version": "1.0",
        "updated_at": datetime.now().isoformat(),
        "practices": {
            "test_coverage": {
                "description": "测试覆盖度要求",
                "requirements": [
                    "所有必填字段必须有缺失测试",
                    "所有接口必须有正向和负向测试",
                    "关键业务逻辑必须有边界值测试",
                    "安全相关接口必须有安全测试（SQL注入、XSS等）",
                    "状态变更接口必须有状态转换测试"
                ],
                "coverage_target": "建议覆盖率 >= 80%"
            },
            "naming_convention": {
                "description": "测试用例命名规范",
                "format": "[场景]-[操作]-[预期结果]",
                "examples": [
                    "正常登录-使用有效账号密码-登录成功",
                    "异常登录-密码错误-返回401错误",
                    "边界测试-用户名为空-返回参数错误",
                    "安全测试-SQL注入攻击-返回400错误"
                ],
                "guidelines": [
                    "使用中文命名，清晰描述测试场景",
                    "避免使用测试1、测试2等无意义名称",
                    "名称应该让他人一眼看出测试目的"
                ]
            },
            "test_data_design": {
                "description": "测试数据设计原则",
                "principles": [
                    "真实性：使用符合实际业务的数据",
                    "多样性：覆盖各种可能的数据组合",
                    "独立性：测试数据之间不应相互依赖",
                    "可维护性：避免硬编码，使用变量和常量",
                    "安全性：敏感数据（密码等）使用测试专用数据"
                ],
                "examples": {
                    "valid_username": ["admin", "testuser", "user123"],
                    "invalid_username": ["", "a"*100, "<script>", "' OR '1'='1"],
                    "valid_password": ["Aa123456", "Pass@word123"],
                    "invalid_password": ["", "123", "a"*100]
                }
            },
            "assertion_design": {
                "description": "断言设计原则",
                "guidelines": [
                    "每个测试用例至少有一个断言",
                    "断言应该验证关键业务指标，而不仅是状态码",
                    "优先使用 JSON Path 断言验证响应结构",
                    "关键字段必须验证类型和值范围",
                    "错误场景必须验证错误码和错误信息"
                ],
                "common_assertions": [
                    "状态码断言：$.code == 200",
                    "数据存在性断言：$.data 不为空",
                    "字段类型断言：$.data.id 是整数",
                    "业务逻辑断言：$.data.status == 'success'",
                    "列表长度断言：$.data.list.length > 0"
                ]
            },
            "test_execution_order": {
                "description": "测试执行顺序",
                "order": [
                    "1. 前置条件准备（Setup）",
                    "2. 正向测试用例（验证核心功能）",
                    "3. 边界值测试",
                    "4. 异常/负向测试",
                    "5. 安全性测试",
                    "6. 后置清理（Teardown）"
                ]
            }
        }
    }


@mcp.resource("template://test-scenarios")
def get_test_scenarios_template():
    """
    常见测试场景模板
    """
    return {
        "title": "API 测试场景模板库",
        "version": "1.0",
        "scenarios": {
            "authentication": {
                "name": "认证授权类接口",
                "test_types": [
                    {
                        "type": "正常登录",
                        "description": "使用有效的用户名和密码",
                        "expected": "返回200，包含token"
                    },
                    {
                        "type": "密码错误",
                        "description": "正确的用户名，错误的密码",
                        "expected": "返回401，认证失败"
                    },
                    {
                        "type": "用户不存在",
                        "description": "不存在的用户名",
                        "expected": "返回401，用户不存在"
                    },
                    {
                        "type": "参数缺失",
                        "description": "用户名或密码为空",
                        "expected": "返回400，参数错误"
                    },
                    {
                        "type": "token过期",
                        "description": "使用过期的token访问",
                        "expected": "返回401，token过期"
                    }
                ]
            },
            "crud_operations": {
                "name": "CRUD操作类接口",
                "test_types": [
                    {
                        "type": "创建成功",
                        "description": "提供所有必填字段，数据有效",
                        "expected": "返回201，创建成功"
                    },
                    {
                        "type": "字段缺失",
                        "description": "缺少必填字段",
                        "expected": "返回400，参数错误"
                    },
                    {
                        "type": "数据重复",
                        "description": "唯一性约束冲突（如用户名已存在）",
                        "expected": "返回409，数据已存在"
                    },
                    {
                        "type": "查询成功",
                        "description": "提供有效的查询条件",
                        "expected": "返回200，数据列表"
                    },
                    {
                        "type": "查询为空",
                        "description": "查询条件不匹配任何数据",
                        "expected": "返回200，空列表"
                    },
                    {
                        "type": "更新成功",
                        "description": "更新已存在的记录",
                        "expected": "返回200，更新成功"
                    },
                    {
                        "type": "更新不存在",
                        "description": "更新不存在的记录",
                        "expected": "返回404，记录不存在"
                    },
                    {
                        "type": "删除成功",
                        "description": "删除已存在的记录",
                        "expected": "返回200，删除成功"
                    }
                ]
            },
            "data_validation": {
                "name": "数据验证类测试",
                "test_types": [
                    {
                        "type": "字段类型错误",
                        "description": "数字字段传入字符串，或反之",
                        "expected": "返回400，类型错误"
                    },
                    {
                        "type": "字段长度超限",
                        "description": "字符串字段超过最大长度",
                        "expected": "返回400，长度超限"
                    },
                    {
                        "type": "数值范围错误",
                        "description": "数值超出允许范围（最小/最大值）",
                        "expected": "返回400，数值超出范围"
                    },
                    {
                        "type": "格式错误",
                        "description": "如邮箱、电话、日期格式不正确",
                        "expected": "返回400，格式错误"
                    },
                    {
                        "type": "特殊字符",
                        "description": "包含不允许的特殊字符",
                        "expected": "返回400或过滤处理"
                    }
                ]
            },
            "security": {
                "name": "安全性测试",
                "test_types": [
                    {
                        "type": "SQL注入",
                        "description": "在参数中注入SQL语句",
                        "test_data": "admin' OR '1'='1",
                        "expected": "返回400，输入被过滤或拒绝"
                    },
                    {
                        "type": "XSS攻击",
                        "description": "注入JavaScript代码",
                        "test_data": "<script>alert('xss')</script>",
                        "expected": "返回400，或内容被转义"
                    },
                    {
                        "type": "路径穿越",
                        "description": "尝试访问系统文件",
                        "test_data": "../../etc/passwd",
                        "expected": "返回400，路径被拒绝"
                    },
                    {
                        "type": "未授权访问",
                        "description": "不带token访问需要认证的接口",
                        "expected": "返回401，未授权"
                    },
                    {
                        "type": "权限不足",
                        "description": "普通用户访问管理员接口",
                        "expected": "返回403，权限不足"
                    }
                ]
            },
            "business_logic": {
                "name": "业务逻辑测试",
                "test_types": [
                    {
                        "type": "状态转换",
                        "description": "测试状态流转是否符合业务规则",
                        "example": "订单：待支付->已支付->已发货->已完成"
                    },
                    {
                        "type": "并发操作",
                        "description": "同一资源的并发修改",
                        "expected": "使用锁机制或乐观锁控制"
                    },
                    {
                        "type": "重复提交",
                        "description": "防止重复创建相同的订单/记录",
                        "expected": "返回409或幂等性处理"
                    },
                    {
                        "type": "依赖关系",
                        "description": "测试资源间的依赖关系",
                        "example": "删除用户前必须先删除用户的所有订单"
                    }
                ]
            }
        }
    }


@mcp.resource("template://common-test-data")
def get_common_test_data():
    """
    常用测试数据库
    """
    return {
        "title": "常用测试数据库",
        "version": "1.0",
        "data_types": {
            "string": {
                "valid": {
                    "normal": ["test", "hello", "admin"],
                    "with_numbers": ["test123", "user001"],
                    "with_special_chars": ["test_user", "hello-world"],
                    "chinese": ["测试用户", "管理员"],
                    "mixed": ["Test用户123"]
                },
                "invalid": {
                    "empty": "",
                    "too_long": "a" * 100,
                    "sql_injection": "' OR '1'='1",
                    "xss": "<script>alert('xss')</script>",
                    "path_traversal": "../../etc/passwd",
                    "null_byte": "test\x00user",
                    "only_spaces": "   "
                },
                "boundary": {
                    "min_length": "a",
                    "typical_max": "a" * 255,
                    "unicode": "😀🎉💻",
                    "newline": "line1\nline2"
                }
            },
            "number": {
                "valid": {
                    "positive": [1, 100, 999],
                    "zero": 0,
                    "negative": [-1, -100],
                    "decimal": [0.5, 99.99, 3.14159]
                },
                "invalid": {
                    "string": "abc",
                    "infinity": float('inf'),
                    "nan": float('nan')
                },
                "boundary": {
                    "int_min": -2147483648,
                    "int_max": 2147483647,
                    "very_large": 999999999999
                }
            },
            "boolean": {
                "valid": [True, False, 1, 0, "true", "false"],
                "invalid": ["yes", "no", 2, -1, ""]
            },
            "email": {
                "valid": [
                    "test@example.com",
                    "user.name@domain.co.uk",
                    "user+tag@example.com"
                ],
                "invalid": [
                    "",
                    "notanemail",
                    "@example.com",
                    "user@",
                    "user @example.com",
                    "user@.com"
                ]
            },
            "phone": {
                "valid": [
                    "13800138000",
                    "18612345678",
                    "+86 138 0013 8000"
                ],
                "invalid": [
                    "",
                    "123",
                    "abcdefghijk",
                    "1234567890123456"
                ]
            },
            "password": {
                "valid": [
                    "Aa123456",
                    "Pass@word123",
                    "Test!2345"
                ],
                "weak": [
                    "123456",
                    "password",
                    "abc123"
                ],
                "invalid": [
                    "",
                    "123",
                    "a" * 100
                ]
            },
            "date": {
                "valid": [
                    "2024-01-01",
                    "2024-12-31T23:59:59",
                    "2024-06-15T12:00:00Z"
                ],
                "invalid": [
                    "",
                    "not-a-date",
                    "2024-13-01",
                    "2024-02-30",
                    "99999-99-99"
                ]
            },
            "url": {
                "valid": [
                    "http://example.com",
                    "https://www.example.com/path",
                    "https://api.example.com/v1/users?id=123"
                ],
                "invalid": [
                    "",
                    "not a url",
                    "ftp://invalid",
                    "javascript:alert('xss')"
                ]
            }
        }
    }


#
# @mcp.resource("user://{user_id}/profile")
# def get_user_profile(user_id: str):
#     """获取用户资料模板"""
#     return {
#         "user_id": user_id,
#         "profile": {
#             "display_name": f"User {user_id}",
#             "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={user_id}",
#             "preferences": {
#                 "theme": "dark",
#                 "language": "zh-CN",
#                 "notifications": True
#             }
#         },
#         "metadata": {
#             "last_updated": datetime.now().isoformat(),
#             "profile_version": "1.0"
#         }
#     }
#
#
# @mcp.resource("testcase://data/{case_id}")
# async def get_testcase_resource(case_id: int) -> dict:
#     """获取测试用例的信息"""
#     async for query_db in get_db():
#         test_cases_detail_result = await Test_casesService.test_cases_detail_services(query_db, case_id)
#         return test_cases_detail_result


# @mcp.resource("testcase-body://data/{case_id}")
# async def get_testcase_body_resource(case_id: int) -> str | Any:
#     """获取测试用例的请求体信息"""
#     caseid = int(case_id)
#     try:
#         async for query_db in get_db():
#             test_cases_detail_result = await Test_casesService.test_cases_detail_services(query_db, caseid)
#             jsondata = test_cases_detail_result.json_data
#             if jsondata:
#                 return jsondata
#             else:
#                 return f"查找失败: jsondata为空或者用例不存在{caseid}"
#     except Exception as e:
#         return f"查找失败，{e}"


class testcase_body_jsonschema(BaseModel):
    """
    jsonschema输出模型
    """

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    body_type: Optional[Any] = Field(default=None, description='请求体类型')
    # json_schema: Optional[Any] = Field(default=None, description='jsonschema')
    body: Optional[Any] = Field(default=None, description='请求体')


@mcp.resource("testcase-body-jsonschema://data/{case_id}")
async def get_testcase_jsonschema_resource(case_id: str, ctx: Context) -> dict[str, Any]:
    """获取测试用例的请求body和jsonschema信息，
    输入参数示例{"case_id": "1"}
    输出模型class testcase_body_jsonschema(BaseModel):

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    body_type: Optional[Any] = Field(default=None, description='请求体类型')
    # json_schema: Optional[Any] = Field(default=None, description='jsonschema')
    body: Optional[Any] = Field(default=None, description='请求体')

    """
    caseid = int(case_id)
    # content_list = await ctx.read_resource(f"testcase://data/{caseid}")
    # content = content_list[0].content
    # a = ctx.get_state(ctx.session_id)
    # ctx.set_state(ctx.session_id, "test_demo")
    # c = ctx.get_state(ctx.session_id)
    try:
        async for query_db in get_db():
            test_cases_detail_result = await Test_casesService.test_cases_detail_services(query_db, caseid)
            if test_cases_detail_result.request_type in [Request_Type.JSON, Request_Type.XML, Request_Type.Raw]:

                jsondata = test_cases_detail_result.json_data
                if jsondata:
                    schema_result = convert_json_to_schema(fr"{json.dumps(jsondata)}")
                    return jsondata
                    # return testcase_body_jsonschema(body=jsondata,
                    #                                 body_type=test_cases_detail_result.request_type.value)
                else:
                    return f"查找失败: jsondata为空或者用例不存在{caseid}"
            elif test_cases_detail_result.request_type in [Request_Type.Form_Data, Request_Type.x_www_form_urlencoded]:
                # data = {item.key: item.value for item in test_cases_detail_result.formdata}
                jsondata = {item.key: item.value for item in test_cases_detail_result.formdata}

                if jsondata:
                    schema_result = convert_json_to_schema(fr"{json.dumps(jsondata)}")
                    # return testcase_body_jsonschema(body=jsondata,
                    # body_type=test_cases_detail_result.request_type.value).model_dump()
                    return jsondata
                else:
                    return f"查找失败: jsondata为空或者用例不存在{caseid}"
            else:
                return None
    except Exception as e:
        return f"查找失败，{e}"

#
#
# @mcp.resource("system://status")
# def get_system_status():
#     """获取系统状态"""
#     return {
#         "status": "running",
#         "uptime": "2h 30m 45s",
#         "memory_usage": {
#             "used": "256MB",
#             "total": "1GB",
#             "percentage": 25.6
#         },
#         "active_connections": 12,
#         "last_check": datetime.now().isoformat()
#     }
