#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：custom_script_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：自定义脚本执行器
"""
import asyncio
import json
import time
from typing import Dict, Any

from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import Task_config
from utils.api_tools.executors.models import ExecutorResult
from utils.api_tools.executors.py_script_control import execute_async_py_script
from utils.api_tools.executors.js_script_control import PostmanJSExecutor
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.log_util import logger


class CustomScriptExecutor(BaseTaskExecutor):
    """
    自定义脚本执行器

    支持执行 Python 和 JavaScript 脚本。
    根据脚本内容自动识别脚本类型，或通过配置指定。
    """

    async def execute(self, task_config: Task_config) -> ExecutorResult:
        """
        执行自定义脚本

        Args:
            task_config: 任务配置，包含 custom_script（脚本内容）

        Returns:
            执行结果
        """
        start_time = time.time()
        exec_logs = {}

        try:
            script = task_config.custom_script
            if not script:
                return ExecutorResult(
                    success=False,
                    error="自定义脚本内容为空"
                )

            exec_logs["script"] = script

            # 检测脚本类型（简单判断，可以根据需要扩展）
            # script_type = self._detect_script_type(script)
            script_type = 'python'
            exec_logs["script_type"] = script_type

            logger.info(f"开始执行自定义脚本，类型: {script_type}")

            # if script_type == "python":
            #     result = await self._execute_python_script(script, exec_logs)
            # elif script_type == "javascript":
            #     result = await self._execute_javascript_script(script, exec_logs)
            # else:
            #     # 默认当作 Python 脚本执行
            result = await self._execute_python_script(script, exec_logs)

            execution_time = time.time() - start_time
            result.execution_time = execution_time

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"自定义脚本执行异常: {str(e)}")
            return ExecutorResult(
                success=False,
                error=f"自定义脚本执行失败: {str(e)}",
                log=exec_logs,
                execution_time=execution_time
            )

    async def _execute_python_script(self, script: str, exec_logs: Dict[str, Any]) -> ExecutorResult:
        """
        执行 Python 脚本

        Args:
            script: Python 脚本内容
            exec_logs: 执行日志字典

        Returns:
            执行结果
        """
        try:
            # 准备执行环境参数
            exec_params = {
                'env_id': self.executor_ctx.env_id,
                'user_id': self.executor_ctx.user_id,
                'context': self.executor_ctx,
                'variables': self.executor_ctx.variables,
                'parameterization': self.executor_ctx.parameterization,
            }

            # 在线程池中执行脚本
            result = await asyncio.to_thread(
                execute_async_py_script,
                script,
                extra_paths=["/utils"],
                **exec_params
            )

            exec_logs.update(result)

            if result.get('success'):
                # 尝试序列化日志，失败则使用字符串表示
                try:
                    logs_str = json.dumps(exec_logs, indent=2, ensure_ascii=False)
                except Exception:
                    logs_str = str(exec_logs)

                return ExecutorResult(
                    success=True,
                    message=f"Python 脚本执行成功\n执行日志：\n{logs_str}",
                    log=exec_logs,
                    data=result.get('output')
                )
            else:
                return ExecutorResult(
                    success=False,
                    error=f"Python 脚本执行失败: {result.get('error')}",
                    message=f"Python 脚本执行失败: {result.get('error')}",
                    log=exec_logs
                )

        except Exception as e:
            return ExecutorResult(
                success=False,
                error=f"Python 脚本执行异常: {str(e)}",
                message=f"Python 脚本执行异常: {str(e)}",
                log=exec_logs
            )

    async def _execute_javascript_script(self, script: str, exec_logs: Dict[str, Any]) -> ExecutorResult:
        """
        执行 JavaScript 脚本

        Args:
            script: JavaScript 脚本内容
            exec_logs: 执行日志字典

        Returns:
            执行结果
        """
        try:
            # 在线程池中执行 JS 脚本
            result = await asyncio.to_thread(
                PostmanJSExecutor.execute,
                script
            )

            exec_logs["result"] = result
            logs_str = json.dumps(exec_logs, indent=2, ensure_ascii=False)

            return ExecutorResult(
                success=True,
                message="JavaScript 脚本执行成功",
                log=logs_str,
                data=result
            )

        except Exception as e:
            return ExecutorResult(
                success=False,
                error=f"JavaScript 脚本执行失败: {str(e)}",
                log=exec_logs
            )

    def _detect_script_type(self, script: str) -> str:
        """
        检测脚本类型

        Args:
            script: 脚本内容

        Returns:
            脚本类型: "python", "javascript"
        """
        script_lower = script.strip().lower()

        # JavaScript 特征检测
        js_patterns = [
            'function ',
            'const ',
            'let ',
            'var ',
            'console.log',
            '=>',
            'async function',
            'pm.',  # Postman 特有
            'require(',
        ]

        # Python 特征检测
        py_patterns = [
            'def ',
            'import ',
            'from ',
            'print(',
            'async def',
            'class ',
            'if __name__',
        ]

        js_score = sum(1 for pattern in js_patterns if pattern in script_lower)
        py_score = sum(1 for pattern in py_patterns if pattern in script_lower)

        if js_score > py_score:
            return "javascript"
        else:
            return "python"

    def validate(self, task_config: Task_config) -> bool:
        """
        验证自定义脚本配置

        Args:
            task_config: 任务配置

        Returns:
            验证是否通过
        """
        if not task_config.custom_script:
            logger.warning("自定义脚本内容为空")
            return False
        return True
