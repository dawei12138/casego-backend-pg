#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：py_exector.py
@Author  ：david
@Date    ：2025-08-12 23:39
"""
import asyncio
import json
import time
from typing import Union
from utils.api_tools.executors.models import SetupConfig, ExecutorContext, ExecutorResult, TeardownConfig
from utils.api_tools.executors.py_script_control import execute_async_py_script
from utils.api_tools.executors.strategies import ExecutorStrategy


class PythonScriptExecutor(ExecutorStrategy):
    """Python脚本执行器"""

    async def execute(self, context: ExecutorContext, config: Union[SetupConfig, TeardownConfig]) -> ExecutorResult:
        start_time = time.time()
        exec_logs = {}

        try:
            script = getattr(config, 'script', '')
            exec_logs.update({"script": script})

            if not script:
                return ExecutorResult(success=False, error="脚本内容为空")

            # 准备执行环境参数
            exec_params = {
                'env_id': context.env_id,
                'user_id': context.user_id,
                'context': context,
                'config': config,
                'variables': context.variables,
                'response': context.response,
            }

            # 在事件循环中运行同步的 execute_async_py_script 函数
            import asyncio
            # 包装成任务并且执行
            result = await asyncio.to_thread(
                execute_async_py_script,
                script,
                extra_paths=["/utils"],
                **exec_params
            )
            exec_logs.update(result)

            execution_time = time.time() - start_time
            logs = json.dumps(exec_logs, indent=2, ensure_ascii=False)
            # 根据执行结果返回相应的 ExecutorResult
            if result['success']:
                return ExecutorResult(
                    success=True,
                    log=logs,
                    # data=exec_logs,
                    message=f"PYTHON-{config.name}执行成功",
                    variables={},  # 如果需要返回变量，可以从 result 中提取
                    execution_time=execution_time
                )
            else:
                return ExecutorResult(
                    success=False,
                    error=f"PYTHON-{config.name}执行失败: {result['error']}",
                    message=f"PYTHON-{config.name}执行失败: {result['error']}",
                    log=exec_logs,
                    execution_time=execution_time
                )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutorResult(
                success=False,
                error=f"PYTHON-{config.name}执行异常: {str(e)}{exec_logs}",
                message=f"PYTHON-{config.name}执行异常: {str(e)}{exec_logs}",
                execution_time=execution_time
            )
