#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：js_script_control.py.py
@Author  ：david
@Date    ：2025-08-13 21:47 
"""
import execjs
import os
import json
import requests
from typing import Dict, Any, Optional
from pathlib import Path
import pickle


class PostmanJSExecutor:
    """
    基于类方法的JavaScript执行器，支持Postman风格的环境变量和请求操作
    无需实例化，直接使用类方法
    支持持久化存储变量到文件
    """

    # 类级别的环境变量存储
    _environment_vars: Dict[str, str] = {}
    _collection_vars: Dict[str, str] = {}
    _storage_path: str = "postman_variables.pkl"  # 默认存储文件路径
    _auto_persist: bool = False  # 是否自动持久化
    _loaded: bool = False  # 是否已加载数据

    @classmethod
    def _create_pm_context(cls) -> str:
        """
        创建pm对象的JavaScript上下文，通过全局变量传递数据
        """
        # 将当前的变量状态序列化为JavaScript可用的格式
        env_vars_js = json.dumps(cls._environment_vars)
        collection_vars_js = json.dumps(cls._collection_vars)

        pm_context = f"""
        // 全局变量存储
        var __environment_vars = {env_vars_js};
        var __collection_vars = {collection_vars_js};
        var __request_results = {{}};

        var pm = {{
            environment: {{
                get: function(key) {{
                    return __environment_vars[key] || null;
                }},
                set: function(key, value) {{
                    __environment_vars[key] = String(value);
                }}
            }},
            variables: {{
                get: function(key) {{
                    return __collection_vars[key] || null;
                }},
                set: function(key, value) {{
                    __collection_vars[key] = String(value);
                }}
            }},
            sendRequest: function(url, callback) {{
                // 简化的请求模拟，实际应该调用Python的requests
                var response = {{
                    status: 200,
                    headers: {{}},
                    text: '{{"status": "simulated"}}',
                    json: function() {{
                        return JSON.parse(this.text);
                    }}
                }};

                // 存储URL以便Python端处理
                __request_results[url] = true;

                if (callback) {{
                    callback(null, response);
                }}
                return response;
            }}
        }};

        // 辅助函数：获取更新后的变量状态
        function __get_updated_vars() {{
            return {{
                environment: __environment_vars,
                collection: __collection_vars,
                requests: Object.keys(__request_results)
            }};
        }}
        """
        return pm_context

    @classmethod
    def _handle_request(cls, url: str) -> Dict[str, Any]:
        """
        处理HTTP请求
        """
        try:
            response = requests.get(url, timeout=10)
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'text': response.text,
                'json': response.json() if 'application/json' in response.headers.get('content-type', '') else None
            }
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'status': 0,
                'text': '',
                'json': None
            }

    @classmethod
    def execute(cls, js_code: str, entry_function: str = "main",
                store_env_var: Optional[str] = None) -> Dict[str, Any]:
        """
        执行JavaScript代码

        :param js_code: JavaScript代码
        :param entry_function: 入口函数名
        :param store_env_var: 可选，将结果存储到环境变量
        :return: 执行结果
        """
        try:
            # 自动加载数据（如果还未加载）
            if not cls._loaded:
                cls.load_variables()

            # 创建完整的JavaScript上下文
            full_js_code = cls._create_pm_context() + "\n" + js_code + f"""

            // 在执行完用户代码后，返回结果和更新的变量
            function __execute_with_vars() {{
                var result = {entry_function}();
                var updated_vars = __get_updated_vars();
                return {{
                    result: result,
                    updated_vars: updated_vars
                }};
            }}
            """

            # 编译并执行JavaScript代码
            context = execjs.compile(full_js_code)

            # 执行并获取结果
            execution_result = context.call("__execute_with_vars")

            # 处理变量更新
            updated_vars = execution_result.get("updated_vars", {})

            # 更新环境变量
            if "environment" in updated_vars:
                for key, value in updated_vars["environment"].items():
                    cls._environment_vars[key] = str(value)
                    os.environ[key] = str(value)

            # 更新集合变量
            if "collection" in updated_vars:
                cls._collection_vars.update(updated_vars["collection"])

            # 处理HTTP请求
            if "requests" in updated_vars:
                for url in updated_vars["requests"]:
                    cls._handle_request(url)

            # 自动持久化
            if cls._auto_persist:
                cls.save_variables()

            # 存储到环境变量
            result = execution_result.get("result")
            if store_env_var:
                cls.set_env_variable(store_env_var, str(result))

            return {
                "success": True,
                "result": result,
                "environment_vars": cls._environment_vars.copy(),
                "collection_vars": cls._collection_vars.copy()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "environment_vars": cls._environment_vars.copy(),
                "collection_vars": cls._collection_vars.copy()
            }

    @classmethod
    def set_env_variable(cls, key: str, value: str) -> None:
        """设置环境变量"""
        if not cls._loaded:
            cls.load_variables()
        cls._environment_vars[key] = str(value)
        os.environ[key] = str(value)
        if cls._auto_persist:
            cls.save_variables()

    @classmethod
    def get_env_variable(cls, key: str) -> Optional[str]:
        """获取环境变量"""
        if not cls._loaded:
            cls.load_variables()
        return cls._environment_vars.get(key) or os.getenv(key)

    @classmethod
    def set_collection_variable(cls, key: str, value: str) -> None:
        """设置集合变量"""
        if not cls._loaded:
            cls.load_variables()
        cls._collection_vars[key] = str(value)
        if cls._auto_persist:
            cls.save_variables()

    @classmethod
    def get_collection_variable(cls, key: str) -> Optional[str]:
        """获取集合变量"""
        if not cls._loaded:
            cls.load_variables()
        return cls._collection_vars.get(key)

    @classmethod
    def save_variables(cls, file_path: Optional[str] = None) -> bool:
        """
        保存变量到文件

        :param file_path: 文件路径，默认使用类设置的路径
        :return: 是否保存成功
        """
        try:
            path = file_path or cls._storage_path
            data = {
                "environment": cls._environment_vars,
                "collection": cls._collection_vars
            }

            # 确保目录存在
            Path(path).parent.mkdir(parents=True, exist_ok=True)

            # 使用pickle进行序列化存储
            with open(path, 'wb') as f:
                pickle.dump(data, f)

            return True
        except Exception as e:
            print(f"保存变量失败: {e}")
            return False

    @classmethod
    def load_variables(cls, file_path: Optional[str] = None) -> bool:
        """
        从文件加载变量

        :param file_path: 文件路径，默认使用类设置的路径
        :return: 是否加载成功
        """
        try:
            path = file_path or cls._storage_path

            if not os.path.exists(path):
                cls._loaded = True
                return True

            with open(path, 'rb') as f:
                data = pickle.load(f)

            cls._environment_vars = data.get("environment", {})
            cls._collection_vars = data.get("collection", {})

            # 同时设置到系统环境变量
            for key, value in cls._environment_vars.items():
                os.environ[key] = str(value)

            cls._loaded = True
            return True

        except Exception as e:
            print(f"加载变量失败: {e}")
            cls._loaded = True  # 即使失败也标记为已加载，避免重复尝试
            return False

    @classmethod
    def set_storage_config(cls, file_path: str = "postman_variables.pkl",
                           auto_persist: bool = False) -> None:
        """
        设置存储配置

        :param file_path: 存储文件路径
        :param auto_persist: 是否自动持久化
        """
        cls._storage_path = file_path
        cls._auto_persist = auto_persist

    @classmethod
    def clear_variables(cls, also_clear_file: bool = False) -> None:
        """
        清空所有变量

        :param also_clear_file: 是否同时删除存储文件
        """
        cls._environment_vars.clear()
        cls._collection_vars.clear()

        if also_clear_file and os.path.exists(cls._storage_path):
            try:
                os.remove(cls._storage_path)
            except Exception as e:
                print(f"删除存储文件失败: {e}")

    @classmethod
    def export_variables_json(cls, file_path: str) -> bool:
        """
        导出变量为JSON格式

        :param file_path: JSON文件路径
        :return: 是否导出成功
        """
        try:
            if not cls._loaded:
                cls.load_variables()

            data = {
                "environment": cls._environment_vars,
                "collection": cls._collection_vars
            }

            # 确保目录存在
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"导出JSON失败: {e}")
            return False

    @classmethod
    def import_variables_json(cls, file_path: str) -> bool:
        """
        从JSON文件导入变量

        :param file_path: JSON文件路径
        :return: 是否导入成功
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            cls._environment_vars.update(data.get("environment", {}))
            cls._collection_vars.update(data.get("collection", {}))

            # 设置到系统环境变量
            for key, value in cls._environment_vars.items():
                os.environ[key] = str(value)

            cls._loaded = True

            # 自动保存
            if cls._auto_persist:
                cls.save_variables()

            return True
        except Exception as e:
            print(f"导入JSON失败: {e}")
            return False

    @classmethod
    def get_all_variables(cls) -> Dict[str, Dict[str, str]]:
        """获取所有变量"""
        if not cls._loaded:
            cls.load_variables()
        return {
            "environment": cls._environment_vars.copy(),
            "collection": cls._collection_vars.copy()
        }

    @classmethod
    def send_request(cls, url: str, method: str = "GET",
                     headers: Optional[Dict] = None,
                     data: Optional[Any] = None) -> Dict[str, Any]:
        """
        发送HTTP请求的Python方法

        :param url: 请求URL
        :param method: 请求方法
        :param headers: 请求头
        :param data: 请求数据
        :return: 响应结果
        """
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {"error": f"不支持的请求方法: {method}"}

            try:
                json_data = response.json()
            except:
                json_data = None

            return {
                "status": response.status_code,
                "headers": dict(response.headers),
                "text": response.text,
                "json": json_data,
                "success": 200 <= response.status_code < 300
            }

        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status": 0,
                "text": "",
                "json": None,
                "success": False
            }

    @classmethod
    def reset_storage(cls) -> None:
        """
        重置存储状态，用于调试
        """
        cls._loaded = False
        cls._environment_vars.clear()
        cls._collection_vars.clear()


def execute_js_script_simple(script_content: str, entry_function: str = "main") -> Dict[str, Any]:
    """
    简化的JavaScript脚本执行接口，用于公共脚本库

    Args:
        script_content: JavaScript脚本内容
        entry_function: 入口函数名，默认为 "main"

    Returns:
        统一格式的执行结果:
        {
            "success": bool,
            "result": Any,
            "logs": str,
            "error": str | None
        }
    """
    try:
        exec_result = PostmanJSExecutor.execute(script_content, entry_function=entry_function)

        return {
            "success": exec_result.get("success", False),
            "result": exec_result.get("result"),
            "logs": json.dumps(exec_result.get("environment_vars", {}), ensure_ascii=False),
            "error": exec_result.get("error")
        }
    except Exception as e:
        return {
            "success": False,
            "result": None,
            "logs": "",
            "error": f"{type(e).__name__}: {str(e)}"
        }


# 使用示例
if __name__ == "__main__":
    # 配置持久化存储
    PostmanJSExecutor.set_storage_config("my_postman_vars.pkl", auto_persist=True)

    # 示例1: 基本的环境变量操作（会自动持久化）
    js_code1 = """
    function main() {
        pm.environment.set("api_key", "ab88888883");
        pm.variables.set("user_id", "1238888888888845");

        var apiKey = pm.environment.get("api_key");
        var userId = pm.variables.get("user_id");

        return {
            apiKey: apiKey,
            userId: userId,
            message: "Variables set and retrieved successfully"
        };
    }
    """

    print("=== 示例1: 环境变量操作（持久化） ===")
    result1 = PostmanJSExecutor.execute(js_code1)
    print(json.dumps(result1, indent=2, ensure_ascii=False))
    #
    # # 示例2: 手动保存和加载
    # print("\n=== 示例2: 手动保存 ===")
    # PostmanJSExecutor.set_env_variable("manual_var", "manual_value")
    # save_success = PostmanJSExecutor.save_variables()
    # print(f"保存成功: {save_success}")
    #
    # # 清空内存变量，然后重新加载
    # PostmanJSExecutor._environment_vars.clear()
    # PostmanJSExecutor._loaded = False
    #
    # # 重新加载
    # load_success = PostmanJSExecutor.load_variables()
    # print(f"加载成功: {load_success}")
    #
    # # 验证数据是否恢复
    # manual_var = PostmanJSExecutor.get_env_variable("manual_var")
    # print(f"恢复的变量: {manual_var}")
    #
    # # 示例3: JSON导出导入
    # print("\n=== 示例3: JSON导出导入 ===")
    # PostmanJSExecutor.export_variables_json("variables.json")
    # print("变量已导出为JSON")
    #
    # # 查看导出的JSON文件内容
    # try:
    #     with open("variables.json", "r", encoding='utf-8') as f:
    #         exported_data = json.load(f)
    #     print("导出的数据:", json.dumps(exported_data, indent=2, ensure_ascii=False))
    # except Exception as e:
    #     print(f"读取JSON文件失败: {e}")

    # 示例4: 发送HTTP请求
    print("\n=== 示例4: 发送HTTP请求 ===")
    js_code4 = """
    function main() {
        pm.environment.set("base_url", "https://jsonplaceholder.typicode.com");
        var baseUrl = pm.environment.get("base_url");

        // 模拟发送请求
        pm.sendRequest(baseUrl + "/posts/1", function(err, response) {
            // 这里是回调函数
        });

        return {
            message: "Request sent",
            url: baseUrl + "/posts/1"
        };
    }
    """

    result4 = PostmanJSExecutor.execute(js_code4)
    print(json.dumps(result4, indent=2, ensure_ascii=False))

    # # 示例5: Python直接发送请求
    # print("\n=== 示例5: Python直接发送请求 ===")
    # request_result = PostmanJSExecutor.send_request("https://jsonplaceholder.typicode.com/posts/1")
    # print(f"状态码: {request_result.get('status')}")
    # print(f"成功: {request_result.get('success')}")
    # if request_result.get('json'):
    #     print(f"标题: {request_result['json'].get('title', 'N/A')}")

    # 示例6: 获取所有变量
    print("\n=== 所有变量 ===")
    all_vars = PostmanJSExecutor.get_all_variables()
    print(json.dumps(all_vars, indent=2, ensure_ascii=False))