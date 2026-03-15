#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：api_assersions_control.py
@Author  ：david
@Date    ：2025-08-14 22:23 
"""
import re
import json
import time
import asyncio
import xml.etree.ElementTree as ET
from jsonpath import jsonpath
from lxml import etree
from typing import Any, Union, List
from utils.api_tools.executors.strategies import ExecutorStrategy
from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService


class AssertionExecutor(ExecutorStrategy):
    """断言执行器"""

    async def execute(self, context: ExecutorContext,
                      config_list: List[Union[SetupConfig, TeardownConfig]]) -> ExecutorResult:
        start_time = time.time()
        results = []

        for config in config_list:
            if not config.is_run:
                continue
            try:
                # 获取配置参数
                # 参数反了，注意下，前端传反了
                assertion_method = getattr(config, 'assert_type', '=')
                jsonpath_expr = getattr(config, 'jsonpath', '')
                jsonpath_index = getattr(config, 'jsonpath_index', None)
                extract_index_is_run = getattr(config, 'extract_index_is_run', False)
                assertion_type = getattr(config, 'assertion_method', "response_json")
                expected_value = getattr(config, 'value', '')

                # 提取实际值
                actual_value = await self._extract_actual_value(
                    context, assertion_type, jsonpath_expr, jsonpath_index, extract_index_is_run
                )

                # 执行断言比较
                assertion_result = self._compare_values(actual_value, expected_value, assertion_method)

                # 记录结果
                result_log = {
                    'assertion_type': assertion_type,
                    'actual_value': actual_value,
                    'expected_value': expected_value,
                    'assertion_method': assertion_method,
                    'success': assertion_result
                }
                results.append(result_log)

            except Exception as e:
                results.append({
                    'assertion_type': getattr(config, 'assertion_type', ''),
                    'error': str(e),
                    'success': False
                })

        execution_time = time.time() - start_time
        success_count = sum(1 for r in results if r.get('success', False))
        total_count = len(results)

        # 所有断言都成功才算成功
        overall_success = success_count == total_count

        log_data = {
            'total': total_count,
            'success': success_count,
            'failed': total_count - success_count,
            'results': results,
            'execution_time': execution_time
        }

        if overall_success:
            return ExecutorResult(
                success=True,
                message=f"断言执行成功 ({success_count}/{total_count})",
                log=log_data,
                execution_time=execution_time
            )
        else:
            return ExecutorResult(
                success=False,
                error=f"断言执行失败 ({success_count}/{total_count})",
                log=log_data,
                execution_time=execution_time
            )

    async def _extract_actual_value(self, context: ExecutorContext, assertion_type: str,
                                    jsonpath_expr: str, jsonpath_index: int = None,
                                    extract_index_is_run: bool = False) -> str:
        """根据断言类型提取实际值"""
        try:
            if assertion_type == 'response_json':
                source_data = context.response.response_body if hasattr(context.response, 'response_body') else {}
                return self._extract_with_jsonpath(source_data, jsonpath_expr, jsonpath_index, extract_index_is_run)

            elif assertion_type == 'response_text':
                if hasattr(context.response, 'response_body'):
                    body = context.response.response_body
                    source_data = body if isinstance(body, str) else json.dumps(body, ensure_ascii=False)
                else:
                    source_data = ""
                return self._extract_with_jsonpath(source_data, jsonpath_expr, jsonpath_index, extract_index_is_run)

            elif assertion_type == 'response_xml':
                if hasattr(context.response, 'response_body'):
                    body = context.response.response_body
                    source_data = body if isinstance(body, str) else str(body)
                else:
                    source_data = ""
                return self._extract_with_xpath(source_data, jsonpath_expr)

            elif assertion_type == 'response_header':
                source_data = context.response.response_headers if hasattr(context.response, 'response_headers') else {}
                return self._extract_with_jsonpath(source_data, jsonpath_expr, jsonpath_index, extract_index_is_run)

            elif assertion_type == 'response_cookie':
                source_data = context.response.response_cookies if hasattr(context.response, 'response_cookies') else {}
                return self._extract_with_jsonpath(source_data, jsonpath_expr, jsonpath_index, extract_index_is_run)

            elif assertion_type == 'response_status':
                return str(context.response.response_status_code) if hasattr(context.response,
                                                                             'response_status_code') else ""

            elif assertion_type == 'environment_cache':
                return await self._get_environment_variable(context, jsonpath_expr)

            else:
                return ""

        except Exception as e:
            print(f"提取实际值失败: {str(e)}")
            return ""

    def _extract_with_jsonpath(self, source_data: Any, jsonpath_expr: str,
                               jsonpath_index: int = None, extract_index_is_run: bool = False) -> str:
        """使用JSONPath提取数据"""
        try:
            if not jsonpath_expr:
                return str(source_data) if source_data is not None else ""

            result = jsonpath(source_data, jsonpath_expr)

            if result:
                if extract_index_is_run and jsonpath_index is not None:
                    if 0 <= jsonpath_index < len(result):
                        extracted_value = result[jsonpath_index]
                    else:
                        extracted_value = result[0] if result else ""
                else:
                    extracted_value = result[0]

                return str(extracted_value) if extracted_value is not None else ""
            else:
                return ""

        except Exception as e:
            print(f"JSONPath提取失败: {str(e)}")
            return ""

    def _extract_with_xpath(self, source_data: str, xpath_expr: str) -> str:
        """使用XPath表达式提取XML数据"""
        try:
            if not xpath_expr:
                return source_data if isinstance(source_data, str) else str(source_data)

            if not isinstance(source_data, str):
                source_data = str(source_data)

            try:
                root = etree.fromstring(source_data.encode('utf-8'))
                result = root.xpath(xpath_expr)

                if result:
                    selected_result = result[0]
                    if isinstance(selected_result, etree._Element):
                        return selected_result.text or ""
                    else:
                        return str(selected_result)
                else:
                    return ""

            except etree.XMLSyntaxError:
                root = ET.fromstring(source_data)
                elements = root.findall(xpath_expr.replace('//', './/'))
                if elements:
                    return elements[0].text or ""
                else:
                    return ""

        except Exception as e:
            print(f"XPath提取失败: {str(e)}")
            return ""

    async def _get_environment_variable(self, context: ExecutorContext, variable_name: str) -> str:
        """获取环境变量"""
        try:
            # 构造缓存查询模型
            query = Cache_dataPageQueryModel(
                cache_key=variable_name,
                environment_id=context.env_id,
                user_id=context.user_id,
            )

            result = await Cache_dataService.get_cachedata_by_key(context.redis_obj, query)
            return str(result) if result is not None else ""
        except Exception as e:
            print(f"获取环境变量失败: {str(e)}")
            return ""

    def _compare_values(self, actual_value: Any, expected_value: Any, compare_type: str) -> bool:
        """值比较函数"""
        # 空值判断
        if compare_type == "is_null":
            return actual_value is None or actual_value == ""

        if compare_type == "is_not_null":
            return actual_value is not None and actual_value != ""

        if compare_type == "exist":
            return actual_value is not None

        if compare_type == "not_exist":
            return actual_value is None

        if actual_value is None:
            return False

        # 先转换为字符串并去除空格
        actual_str = str(actual_value).strip()
        expected_str = str(expected_value).strip()

        # 等于/不等于比较 - 优先尝试数值比较
        if compare_type in ["=", "=="]:
            # 先尝试数值比较
            try:
                actual_num = float(actual_str)
                expected_num = float(expected_str)
                return actual_num == expected_num
            except (ValueError, TypeError):
                # 数值转换失败，使用字符串比较
                return actual_str == expected_str

        if compare_type == "!=":
            # 先尝试数值比较
            try:
                actual_num = float(actual_str)
                expected_num = float(expected_str)
                return actual_num != expected_num
            except (ValueError, TypeError):
                # 数值转换失败，使用字符串比较
                return actual_str != expected_str

        # 数值比较
        if compare_type in [">", ">=", "<", "<="]:
            try:
                actual_num = float(actual_str)
                expected_num = float(expected_str)
                if compare_type == ">":
                    return actual_num > expected_num
                elif compare_type == ">=":
                    return actual_num >= expected_num
                elif compare_type == "<":
                    return actual_num < expected_num
                elif compare_type == "<=":
                    return actual_num <= expected_num
            except (ValueError, TypeError):
                return False

        # 字符串操作
        if compare_type == "contain":
            return expected_str in actual_str

        if compare_type == "not_contain":
            return expected_str not in actual_str

        # 正则匹配
        if compare_type == "REGULAR_TYPE":
            try:
                return bool(re.search(expected_str, actual_str))
            except re.error:
                return False

        # 集合操作
        if compare_type == "belong_to_set":
            if isinstance(expected_value, (list, tuple, set)):
                return actual_value in expected_value
            return False

        if compare_type == "not_belong_to_set":
            if isinstance(expected_value, (list, tuple, set)):
                return actual_value not in expected_value
            return True

        return False


# 使用示例
"""
config_list = [
    {
        'assertion_type': 'response_status',
        'assertion_method': '=',
        'value': '200'
    },
    {
        'assertion_type': 'response_json',
        'jsonpath': '$.data.user_id',
        'assertion_method': '=',
        'value': '12345'
    },
    {
        'assertion_type': 'response_json',
        'jsonpath': '$.data.users[*].name',
        'jsonpath_index': 1,
        'extract_index_is_run': True,
        'assertion_method': 'contain',
        'value': 'test'
    }
]

async def main():
    executor = AssertionExecutor()
    result = await executor.execute(context, config_list)
    print(result)

asyncio.run(main())
"""
