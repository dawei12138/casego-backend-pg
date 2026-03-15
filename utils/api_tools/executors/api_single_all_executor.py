#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：example.py
@Author  ：david
@Date    ：2025-08-11 23:40 
"""
import base64
import time

from config.get_db import get_db
from config.get_redis import RedisUtil
from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsConfig
from module_admin.api_testing.api_environments.service.environments_service import EnvironmentsService
from module_admin.api_testing.api_test_cases.service.test_cases_service import Test_casesService
from utils.api_tools.executors.api_assersions_executor import AssertionExecutor
from utils.api_tools.executors.api_request_exector import APIExecutor
from utils.api_tools.executors.manager import ExecutorManager
from utils.api_tools.executors.models import CasesConfig, SingleExecutorResult, ExecutorContext
import json
from typing import List

from utils.log_util import logger
from utils.log_capture import async_capture_logs


async def api_single_all_executor(context: ExecutorContext) -> SingleExecutorResult:
    """执行单个用例全流程"""
    async with async_capture_logs() as capture:
        start1_time = time.time()
        # 1. 获取全局配置
        environments_config = EnvironmentsConfig(id=context.env_id)
        context.env_config = await EnvironmentsService.get_request_config_services(context.mysql_obj, environments_config)

        manager = ExecutorManager()
        # 2. 获取测试用例详情
        testcase_obj = await Test_casesService.test_cases_detail_services(query_db=context.mysql_obj,
                                                                          case_id=context.case_id)
        setup_configs = testcase_obj.setup_list
        teardown_configs = testcase_obj.teardown_list
        assertion_configs = testcase_obj.assertion_list

        # 3. 提前构建请求参数并放入上下文
        api_exector = APIExecutor(testcase_obj, context)
        context.request_info = await api_exector.build_request_info()

        # 4. 执行前置脚本（此时可以访问/修改 context.request_info）
        start2_time = time.time()
        setup_results = await manager.execute_setup_list(setup_configs, context)

        # 5. 执行 API 请求（使用上下文中预构建的请求参数）
        start3_time = time.time()
        response = await api_exector.execute()
        context.response = response

        start4_time = time.time()
        teardown_results = await manager.execute_teardown_list(teardown_configs, context)

        # 6.5 如果启用了 use_env_cookies，将响应的 cookies 保存到环境中
        if context.use_env_cookies and response.response_cookies:
            try:
                # 提取 cookies 的值（response_cookies 可能是 {key: {value: xxx, ...}} 格式）
                cookies_to_save = {}
                for key, cookie_data in response.response_cookies.items():
                    if isinstance(cookie_data, dict):
                        cookies_to_save[key] = cookie_data.get('value', '')
                    else:
                        cookies_to_save[key] = str(cookie_data)

                if cookies_to_save:
                    await EnvironmentsService.update_environment_cookies_services(
                        context.mysql_obj, context.env_id, cookies_to_save
                    )
                    logger.info(f"[环境Cookies] 已保存 {len(cookies_to_save)} 个cookies到环境: {list(cookies_to_save.keys())}")
            except Exception as e:
                logger.error(f"[环境Cookies] 保存cookies到环境失败: {str(e)}")

        # 7. 执行断言

        start5_time = time.time()
        assersion_executor = AssertionExecutor()
        assersion_result = await assersion_executor.execute(context, assertion_configs)

        start6_time = time.time()

        # 只有断言全部用过才算成功
        if not assersion_result.success:
            response.is_success = False

            response.error_message = response.error_message or ""
            response.error_message += f"🤔 {assersion_result.error}"
            for i in assersion_result.log.get("results"):
                if not i.get("success"):
                    response.error_message += f"\n {json.dumps(i)}"

            pass
        # logger.warning(f"🤔组装阶段{start2_time - start1_time}s")
        # logger.warning(f"🤔前置阶段{start3_time - start2_time}s")
        # logger.warning(f"🤔接口阶段{start4_time - start3_time}s")
        # logger.warning(f"🤔后置阶段{start5_time - start4_time}s")
        # logger.warning(f"🤔断言阶段{start6_time - start5_time}s")

        # 结果组装配置
        finish_res = SingleExecutorResult(
            setup_results=setup_results,
            response=response,
            teardown_results=teardown_results,
            assersion_result=assersion_result,
            log=capture.get_raw_logs()  # 原始格式日志文本
            # context=context
        )

        # 处理不同类型的响应体
        if hasattr(finish_res.response, "response_body") and isinstance(finish_res.response.response_body, dict):
            response_body = finish_res.response.response_body
            response_type = response_body.get('type')

            # 处理二进制数据类型（图片、文件等）
            if response_type == 'binary_data':
                content_type = response_body.get('content_type', 'application/octet-stream')
                binary_data = response_body.get('data')

                # 如果是图片类型且数据存在，直接返回二进制流
                if content_type.startswith('image/') and binary_data:
                    # return StreamingResponse(
                    #     io.BytesIO(binary_data),
                    #     media_type=content_type,
                    #     headers={
                    #         'Content-Length': str(response_body.get('size', len(binary_data))),
                    #         'Content-Disposition': 'inline'
                    #     }
                    # )
                    base64_data = base64.b64encode(binary_data).decode('utf-8')
                    finish_res.response.response_body = {
                        **response_body,
                        'data': base64_data,
                        'encoding': 'base64'
                    }

                # 其他二进制文件，可以选择返回base64编码或文件信息
                elif binary_data:
                    # 将二进制数据转换为base64以便在JSON中传输
                    base64_data = base64.b64encode(binary_data).decode('utf-8')
                    finish_res.response.response_body = {
                        **response_body,
                        'data': base64_data,
                        'encoding': 'base64'
                    }

            # 处理大型二进制文件类型
            elif response_type == 'binary_file':
                # 大文件只返回元信息，不返回实际内容
                pass  # 保持原有的响应体结构

            # 处理多部分数据类型
            elif response_type == 'multipart':
                raw_data = response_body.get('raw_data')
                if raw_data and isinstance(raw_data, bytes):
                    # 转换为base64编码
                    base64_data = base64.b64encode(raw_data).decode('utf-8')
                    finish_res['response_body'] = {
                        **response_body,
                        'raw_data': base64_data,
                        'encoding': 'base64'
                    }

            # 处理未知类型
            elif response_type == 'unknown':
                data = response_body.get('data')
                if data and isinstance(data, bytes):
                    # 尝试解码为文本，失败则转换为base64
                    try:
                        text_data = data.decode('utf-8')
                        finish_res['response_body'] = {
                            **response_body,
                            'data': text_data,
                            'encoding': 'utf-8'
                        }
                    except UnicodeDecodeError:
                        base64_data = base64.b64encode(data).decode('utf-8')
                        finish_res['response_body'] = {
                            **response_body,
                            'data': base64_data,
                            'encoding': 'base64'
                        }

        return finish_res


if __name__ == "__main__":
    import asyncio

    # 运行示例

    asyncio.run(api_single_all_executor())
    # example_custom_executor()
    # example_error_handling()

    print("\n=== 示例运行完成 ===")
