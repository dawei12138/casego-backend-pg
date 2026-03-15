import json
from typing import Any, Dict, List, Set, Union
import jsonschema
from collections import defaultdict


def generate_json_schema(json_object: Any, strict_required: bool = False) -> Dict[str, Any]:
    """
    将JSON对象转换为JSON Schema

    Args:
        json_object: 要转换的JSON对象
        strict_required: 是否严格要求所有字段（默认False，更宽松）
    """

    def merge_schemas(schemas: List[Dict[str, Any]]) -> Dict[str, Any]:
        """合并多个schema，处理类型不一致的情况"""
        if not schemas:
            return {}

        if len(schemas) == 1:
            return schemas[0]

        # 收集所有可能的类型
        types = set()
        for schema in schemas:
            if "type" in schema:
                if isinstance(schema["type"], list):
                    types.update(schema["type"])
                else:
                    types.add(schema["type"])

        if len(types) == 1:
            return schemas[0]
        else:
            # 返回联合类型
            return {"type": list(types)}

    def infer_schema(value: Any) -> Dict[str, Any]:
        # 处理null值
        if value is None:
            return {"type": "null"}

        # 处理数组类型
        elif isinstance(value, list):
            if not value:
                # 空数组，允许任何类型的items
                return {
                    "type": "array",
                    "items": {}
                }

            # 分析所有元素的schema
            item_schemas = []
            for item in value:
                item_schemas.append(infer_schema(item))

            # 合并所有item的schema
            merged_items_schema = merge_schemas(item_schemas)

            return {
                "type": "array",
                "items": merged_items_schema
            }

        # 处理对象类型
        elif isinstance(value, dict):
            properties = {}
            for key, val in value.items():
                properties[key] = infer_schema(val)

            schema = {
                "type": "object",
                "properties": properties
            }

            # 根据strict_required参数决定是否添加required字段
            if strict_required:
                schema["required"] = list(properties.keys())

            return schema

        # 处理基础类型
        elif isinstance(value, bool):
            return {"type": "boolean"}
        elif isinstance(value, int):
            return {"type": "integer"}
        elif isinstance(value, float):
            return {"type": "number"}
        elif isinstance(value, str):
            return {"type": "string"}

        return {}

    return infer_schema(json_object)


def convert_json_to_schema(json_string: str, strict_required: bool = False) -> Dict[str, Any]:
    """
    将JSON字符串转换为JSON Schema

    Args:
        json_string: JSON字符串
        strict_required: 是否严格要求所有字段
    """
    try:
        json_object = json.loads(json_string)
        return generate_json_schema(json_object, strict_required)
    except json.JSONDecodeError as e:
        raise ValueError(f"无效的JSON格式: {e}")


def validate_json_with_schema(json_string: str, schema: Dict[str, Any], detailed_errors: bool = True) -> Dict[str, Any]:
    """
    校验JSON是否符合Schema，返回详细的校验结果

    Args:
        json_string: 要校验的JSON字符串
        schema: JSON Schema
        detailed_errors: 是否返回详细错误信息

    Returns:
        校验结果字典，包含is_valid, errors, error_count等信息
    """
    result = {
        "is_valid": False,
        "errors": [],
        "error_count": 0,
        "json_object": None
    }

    try:
        json_object = json.loads(json_string)
        result["json_object"] = json_object

        # 使用jsonschema进行校验
        validator = jsonschema.Draft7Validator(schema)
        errors = list(validator.iter_errors(json_object))

        if not errors:
            result["is_valid"] = True
            print("✅ 校验通过: JSON符合Schema规则")
        else:
            result["error_count"] = len(errors)

            if detailed_errors:
                for error in errors:
                    error_info = {
                        "path": " -> ".join([str(p) for p in error.absolute_path]) if error.absolute_path else "根节点",
                        "message": error.message,
                        "failed_value": error.instance,
                        "schema_path": " -> ".join([str(p) for p in error.schema_path]) if error.schema_path else "",
                        "validator": error.validator,
                        "validator_value": error.validator_value
                    }
                    result["errors"].append(error_info)

                    print(f"❌ 校验失败 #{len(result['errors'])}:")
                    print(f"   路径: {error_info['path']}")
                    print(f"   错误: {error_info['message']}")
                    print(f"   实际值: {error_info['failed_value']}")
                    print(f"   期望类型: {error_info['validator_value']}")
                    print()
            else:
                print(f"❌ 校验失败: 发现 {len(errors)} 个错误")
                for i, error in enumerate(errors, 1):
                    path = " -> ".join([str(p) for p in error.absolute_path]) if error.absolute_path else "根节点"
                    print(f"   {i}. {path}: {error.message}")

    except json.JSONDecodeError as e:
        result["errors"] = [{"message": f"JSON格式错误: {e}", "path": "解析阶段"}]
        result["error_count"] = 1
        print(f"❌ JSON格式错误: {e}")
    except Exception as e:
        result["errors"] = [{"message": f"校验过程出错: {e}", "path": "校验阶段"}]
        result["error_count"] = 1
        print(f"❌ 校验过程出错: {e}")

    return result


def analyze_multiple_json_samples(json_samples: List[str]) -> Dict[str, Any]:
    """
    分析多个JSON样本，生成更准确的Schema

    Args:
        json_samples: JSON字符串列表

    Returns:
        包含生成的schema和分析结果的字典
    """
    print(f"📊 分析 {len(json_samples)} 个JSON样本...")

    parsed_samples = []
    for i, sample in enumerate(json_samples):
        try:
            parsed = json.loads(sample)
            parsed_samples.append(parsed)
        except json.JSONDecodeError as e:
            print(f"⚠️  样本 {i + 1} JSON格式错误，跳过: {e}")

    if not parsed_samples:
        return {"schema": {}, "error": "没有有效的JSON样本"}

    # 为每个样本生成schema
    schemas = []
    for sample in parsed_samples:
        schema = generate_json_schema(sample, strict_required=False)
        schemas.append(schema)

    # 这里可以实现更复杂的schema合并逻辑
    # 简单起见，返回第一个schema
    final_schema = schemas[0]

    print(f"✅ 基于 {len(parsed_samples)} 个有效样本生成Schema")

    return {
        "schema": final_schema,
        "samples_analyzed": len(parsed_samples),
        "samples_total": len(json_samples),
        "individual_schemas": schemas
    }


# 使用示例
if __name__ == "__main__":
    # 示例1: 基本转换
    sample_json = r"""{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "caseId": 1,
    "name": "登录接口",
    "caseType": "1",
    "copyId": null,
    "parentCaseId": null,
    "parentSubmoduleId": 1,
    "projectId": null,
    "description": "",
    "path": "http://127.0.0.1:/dev-api/login",
    "method": "POST",
    "requestType": "Form_Data",
    "isRun": 1,
    "statusCode": 362,
    "sleep": 101,
    "createBy": "CpkFi9sWZq",
    "createTime": "2004-02-02T18:27:20",
    "updateBy": "admin",
    "updateTime": "2025-09-17T12:45:37",
    "remark": "CEoaptHJN0",
    "sortNo": 753.52,
    "delFlag": 0,
    "jsonData": "{\n  \"password\": \"123456\",\n  \"username\": \"david\"\n}",
    "caseFileConfig": {
      "fileId": 30,
      "fileName": "语音聊天对话流.png",
      "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_e5d786ff_613750.png",
      "fileSize": 89129,
      "mimeType": "image/png"
    },
    "cookiesList": [
      {
        "cookieId": 8,
        "caseId": 1,
        "key": "123",
        "value": "123",
        "domain": null,
        "path": null,
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-09T00:10:21",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 1,
        "delFlag": 0,
        "dataType": "integer"
      },
      {
        "cookieId": 50,
        "caseId": 1,
        "key": "",
        "value": "",
        "domain": null,
        "path": null,
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-22T03:55:45",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 2,
        "delFlag": 0,
        "dataType": "string"
      }
    ],
    "headersList": [
      {
        "headerId": 274,
        "caseId": 1,
        "key": "Content-Type",
        "value": "application/json",
        "isRun": 1,
        "isRequired": 0,
        "description": "JSON格式请求",
        "createBy": "",
        "createTime": "2025-08-29T02:29:57",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 1,
        "delFlag": 0,
        "dataType": "string"
      },
      {
        "headerId": 275,
        "caseId": 1,
        "key": "Accept",
        "value": "application/json",
        "isRun": 1,
        "isRequired": 0,
        "description": "接受JSON响应",
        "createBy": "",
        "createTime": "2025-08-29T02:29:57",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 2,
        "delFlag": 0,
        "dataType": "string"
      },
      {
        "headerId": 276,
        "caseId": 1,
        "key": "User-Agent",
        "value": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-29T02:29:57",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 3,
        "delFlag": 0,
        "dataType": "string"
      },
      {
        "headerId": 277,
        "caseId": 1,
        "key": "Authorization",
        "value": "123",
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-29T02:29:57",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 4,
        "delFlag": 0,
        "dataType": "string"
      }
    ],
    "paramsList": [
      {
        "paramId": 105,
        "caseId": 1,
        "key": "职位",
        "value": "{{随机职位()}}",
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-27T16:27:07",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 1,
        "delFlag": 0,
        "dataType": "string"
      },
      {
        "paramId": 106,
        "caseId": 1,
        "key": "随机测试用户",
        "value": "{{用户=随机测试用户()}}",
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-27T16:27:27",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 2,
        "delFlag": 0,
        "dataType": "string"
      },
      {
        "paramId": 107,
        "caseId": 1,
        "key": "随机测试订单",
        "value": "{{订单=随机测试订单()}}",
        "isRun": 1,
        "isRequired": 1,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-27T16:27:39",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 3,
        "delFlag": 0,
        "dataType": "string"
      },
      {
        "paramId": 108,
        "caseId": 1,
        "key": "上面存储的用户",
        "value": "{{用户}}",
        "isRun": 1,
        "isRequired": 0,
        "description": "",
        "createBy": "",
        "createTime": "2025-08-27T16:27:45",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "sortNo": 4,
        "delFlag": 0,
        "dataType": "string"
      }
    ],
    "setupList": [
      {
        "setupId": 1,
        "name": "后端查询",
        "caseId": 1,
        "setupType": "DB_CONNECTION",
        "dbConnectionId": 1,
        "script": "SELECT * FROM `ruoyi-fastapi`.`sys_oper_log` WHERE `oper_id` between 150 and 155 LIMIT 0,1000;",
        "extractVariables": [
          {
            "jsonpath": "$[?(@.oper_id> 153)]",
            "variable_name": "提取大于153的"
          },
          {
            "jsonpath": "$..oper_id",
            "variable_name": "id列表"
          }
        ],
        "jsonpath": "1",
        "variableName": "1",
        "waitTime": 0,
        "extractIndex": 0,
        "extractIndexIsRun": 1,
        "isRun": 0,
        "createBy": null,
        "createTime": null,
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 3,
        "delFlag": 0
      },
      {
        "setupId": 31,
        "name": "测试畅通",
        "caseId": 1,
        "setupType": "PYTHON_SCRIPT",
        "dbConnectionId": null,
        "script": "await set_cache(\"你是谁222\",\"感冒灵\")\nx = await get_cache(\"999感冒\")\nprint(x)\nimport requests\nres = requests.get(\"https://www.baidu.com\", verify=False)\n\nres .encoding = 'utf-8'  # 显式设置编码\n# print(res.text)",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "jsonpath": "",
        "variableName": "",
        "waitTime": 0,
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-13T06:05:36",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 2,
        "delFlag": 0
      },
      {
        "setupId": 34,
        "name": "111111",
        "caseId": 1,
        "setupType": "JS_SCRIPT",
        "dbConnectionId": null,
        "script": "    function main() {\n        pm.environment.set(\"api_key\", \"ab88888883\");\n        pm.variables.set(\"user_id\", \"1238888888888845\");\n\n        var apiKey = pm.environment.get(\"api_key\");\n        var userId = pm.variables.get(\"user_id\");\n\n        return {\n            apiKey: apiKey,\n            userId: userId,\n            message: \"Variables set and retrieved successfully\"\n        };\n    }",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "jsonpath": "",
        "variableName": "",
        "waitTime": 0,
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-13T06:40:12",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 5,
        "delFlag": 0
      },
      {
        "setupId": 35,
        "name": "等待1秒",
        "caseId": 1,
        "setupType": "WAIT_TIME",
        "dbConnectionId": null,
        "script": "",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "jsonpath": "",
        "variableName": "",
        "waitTime": 500,
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-14T09:05:13",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 4,
        "delFlag": 0
      },
      {
        "setupId": 286,
        "name": "打印返回值",
        "caseId": 1,
        "setupType": "PYTHON_SCRIPT",
        "dbConnectionId": null,
        "script": "print(response)",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "jsonpath": "",
        "variableName": "",
        "waitTime": 0,
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-29T01:24:52",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 1,
        "delFlag": 0
      }
    ],
    "teardownList": [
      {
        "teardownId": 23,
        "name": "python脚本",
        "caseId": 1,
        "teardownType": "PYTHON_SCRIPT",
        "extractVariableMethod": "response_json",
        "jsonpath": "",
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "variableName": "",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "regularExpression": "",
        "xpathExpression": "",
        "responseHeader": "",
        "responseCookie": "",
        "databaseId": null,
        "dbOperation": "await set_cache(\"999感冒\",\"感冒灵\")\nx = await get_cache(\"999感冒\")\nprint(x)\nimport requests\nres = requests.get(url=\"https://www.baidu.com\")\nprint(res.text)",
        "script": "await set_cache(\"test_cache_key\",\"123456789\")\nx = await get_cache(\"test_cache_key\")\nprint(x)\nimport requests\nres = requests.get(\"https://www.baidu.com\", verify=False)\n\nres .encoding = 'utf-8'  # 显式设置编码\nprint(res.text)",
        "waitTime": 0,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-13T06:32:26",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 2,
        "delFlag": 0
      },
      {
        "teardownId": 24,
        "name": "提取相应类型",
        "caseId": 1,
        "teardownType": "EXTRACT_VARIABLE",
        "extractVariableMethod": "response_json",
        "jsonpath": "$.token",
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "variableName": "fast_api_token",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "regularExpression": "",
        "xpathExpression": "",
        "responseHeader": "",
        "responseCookie": "",
        "databaseId": null,
        "dbOperation": "",
        "script": "",
        "waitTime": 0,
        "isRun": 1,
        "createBy": "",
        "createTime": "2025-08-13T06:43:20",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 3,
        "delFlag": 0
      },
      {
        "teardownId": 28,
        "name": "数据库操作",
        "caseId": 1,
        "teardownType": "DB_CONNECTION",
        "extractVariableMethod": "response_json",
        "jsonpath": "",
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "variableName": "",
        "extractVariables": [
          {
            "jsonpath": "$[?(@.oper_id> 158)]",
            "variable_name": "提取大于158的"
          },
          {
            "jsonpath": "$..oper_id",
            "variable_name": "id列表"
          },
          {
            "jsonpath": "123",
            "variable_name": "123"
          }
        ],
        "regularExpression": "",
        "xpathExpression": "",
        "responseHeader": "",
        "responseCookie": "",
        "databaseId": 1,
        "dbOperation": "SELECT * FROM `ruoyi-fastapi`.`sys_oper_log` WHERE `oper_id` between 157 and 2000 LIMIT 0,1000;",
        "script": "",
        "waitTime": 0,
        "isRun": 1,
        "createBy": "",
        "createTime": "2025-08-15T01:51:25",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 4,
        "delFlag": 0
      },
      {
        "teardownId": 29,
        "name": "等待时间",
        "caseId": 1,
        "teardownType": "WAIT_TIME",
        "extractVariableMethod": "response_json",
        "jsonpath": "",
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "variableName": "",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "regularExpression": "",
        "xpathExpression": "",
        "responseHeader": "",
        "responseCookie": "",
        "databaseId": null,
        "dbOperation": "",
        "script": "",
        "waitTime": 100,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-15T01:51:58",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 5,
        "delFlag": 0
      },
      {
        "teardownId": 31,
        "name": "js操作",
        "caseId": 1,
        "teardownType": "JS_SCRIPT",
        "extractVariableMethod": "response_json",
        "jsonpath": "",
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "variableName": "",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "regularExpression": "",
        "xpathExpression": "",
        "responseHeader": "",
        "responseCookie": "",
        "databaseId": null,
        "dbOperation": "",
        "script": "    function main() {\n        pm.environment.set(\"api_key\", \"ab88888883\");\n        pm.variables.set(\"user_id\", \"1238888888888845\");\n\n        var apiKey = pm.environment.get(\"api_key\");\n        var userId = pm.variables.get(\"user_id\");\n\n        return {\n            apiKey: apiKey,\n            userId: userId,\n            message: \"Variables set and retrieved successfully\"\n        };\n    }",
        "waitTime": 0,
        "isRun": 0,
        "createBy": "",
        "createTime": "2025-08-15T02:28:19",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 6,
        "delFlag": 0
      },
      {
        "teardownId": 337,
        "name": "返回值操作实例",
        "caseId": 1,
        "teardownType": "PYTHON_SCRIPT",
        "extractVariableMethod": "response_json",
        "jsonpath": "",
        "extractIndex": 0,
        "extractIndexIsRun": 0,
        "variableName": "",
        "extractVariables": [
          {
            "jsonpath": null,
            "variable_name": null
          }
        ],
        "regularExpression": "",
        "xpathExpression": "",
        "responseHeader": "",
        "responseCookie": "",
        "databaseId": null,
        "dbOperation": "",
        "script": "print(type(response))\nawait set_cache(f\"case_info{response.case_id}\",response.model_dump_json())\n",
        "waitTime": 0,
        "isRun": 1,
        "createBy": "",
        "createTime": "2025-08-29T01:26:16",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": null,
        "sortNo": 1,
        "delFlag": 0
      }
    ],
    "assertionList": [
      {
        "assertionId": 3,
        "caseId": 1,
        "jsonpath": "$.code",
        "jsonpathIndex": 0,
        "extractIndexIsRun": 0,
        "assertionMethod": "response_status",
        "value": "200",
        "assertType": "=",
        "isRun": 1,
        "createBy": "admin",
        "createTime": "2025-08-04T15:17:12",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": "chaxun",
        "sortNo": 1,
        "delFlag": 0
      },
      {
        "assertionId": 11,
        "caseId": 1,
        "jsonpath": "",
        "jsonpathIndex": 0,
        "extractIndexIsRun": 1,
        "assertionMethod": "response_text",
        "value": "登录成功",
        "assertType": "contain",
        "isRun": 1,
        "createBy": "",
        "createTime": "2025-08-15T01:54:33",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": "12312313",
        "sortNo": 2,
        "delFlag": 0
      }
    ],
    "formdata": [
      {
        "formdataId": 4,
        "caseId": 1,
        "key": "username",
        "value": "david",
        "isRun": 1,
        "isRequired": 1,
        "createBy": "",
        "createTime": "2025-08-08T09:41:40",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": "邮箱格式",
        "sortNo": 1,
        "delFlag": 0,
        "dataType": "string",
        "formFileConfig": null
      },
      {
        "formdataId": 5,
        "caseId": 1,
        "key": "password",
        "value": "123456",
        "isRun": 1,
        "isRequired": 1,
        "createBy": "",
        "createTime": "2025-08-08T09:41:40",
        "updateBy": "admin",
        "updateTime": "2025-09-17T12:45:37",
        "remark": null,
        "description": "邮箱格式",
        "sortNo": 2,
        "delFlag": 0,
        "dataType": "string",
        "formFileConfig": [
          {
            "fileId": 29,
            "fileName": "access.log",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_f3a57909_795681.log",
            "fileSize": 162674,
            "mimeType": null
          },
          {
            "fileId": 30,
            "fileName": "语音聊天对话流.png",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_e5d786ff_613750.png",
            "fileSize": 89129,
            "mimeType": "image/png"
          },
          {
            "fileId": 31,
            "fileName": "测试策略指南.pdf",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_6904c8c0_333556.pdf",
            "fileSize": 516226,
            "mimeType": "application/pdf"
          },
          {
            "fileId": 32,
            "fileName": "登录界面的测试用例.pdf",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_5a34cbcc_109598.pdf",
            "fileSize": 440739,
            "mimeType": "application/pdf"
          },
          {
            "fileId": 33,
            "fileName": "大模型RAG实战：RAG原理、应用与系统构建 (汪鹏, 谷清水, 卞龙鹏) (Z-Library).epub",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_93331f09_665111.epub",
            "fileSize": 50479921,
            "mimeType": "application/epub"
          },
          {
            "fileId": 34,
            "fileName": "基于大模型的RAG应用开发与优化——构建企业级LLM应用 (严灿平) (Z-Library).pdf",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_7eddb68c_317370.pdf",
            "fileSize": 28961284,
            "mimeType": "application/pdf"
          },
          {
            "fileId": 35,
            "fileName": "Python 3标准库 (道格·赫尔曼, 苏金国, 李璜) (Z-Library).pdf",
            "filePath": "/system/file/CaseGo/upload_path/files/2025/08/23/file_20250823152730_f7f46a61_669703.pdf",
            "fileSize": 33475919,
            "mimeType": "application/pdf"
          }
        ]
      }
    ]
  },
  "success": true,
  "time": "2025-09-17T15:50:21.372024"
}"""

    print("=== JSON到Schema转换示例 ===")
    schema = convert_json_to_schema(sample_json)
    print("生成的Schema:")
    print(json.dumps(schema, indent=2, ensure_ascii=False))
    result = validate_json_with_schema(sample_json, schema)
    # print("\n=== 校验示例 ===")
    # # 测试一个不符合schema的JSON
    # invalid_json = '''
    # {
    #     "name": "李四",
    #     "age": "二十五",
    #     "is_student": "no",
    #     "grades": ["A", "B", "C"],
    #     "address": {
    #         "city": "上海"
    #     }
    # }
    # '''
    #
    # result = validate_json_with_schema(invalid_json, schema)
    # print(f"校验结果: {'通过' if result['is_valid'] else '失败'}")
    # print(f"错误数量: {result['error_count']}")