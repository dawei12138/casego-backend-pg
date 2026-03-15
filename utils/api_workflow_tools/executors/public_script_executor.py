#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：public_script_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：公共脚本执行器
"""
import asyncio
import json
import time
from typing import Dict, Any

from module_admin.api_testing.api_script_library.service.script_library_service import Script_libraryService
from module_admin.api_testing.api_script_library.entity.vo.script_library_vo import ScriptTypeEnum
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import Task_config
from utils.api_tools.executors.models import ExecutorResult
from utils.api_tools.executors.py_script_control import execute_async_py_script
from utils.api_tools.executors.js_script_control import PostmanJSExecutor
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.log_util import logger


class PublicScriptExecutor(BaseTaskExecutor):
    """
    公共脚本执行器

    从公共脚本库中获取脚本并执行，支持 Python 和 JavaScript 脚本。
    """

    async def execute(self, task_config: Task_config) -> ExecutorResult:
        """
        执行公共脚本

        Args:
            task_config: 任务配置，包含 publicscript（公共脚本ID）

        Returns:
            执行结果
        """
        start_time = time.time()
        exec_logs = {}

        try:
            script_id = task_config.publicscript
            if not script_id:
                return ExecutorResult(
                    success=False,
                    error="公共脚本ID为空"
                )

            # 转换脚本ID
            try:
                script_id = int(script_id)
            except (ValueError, TypeError):
                return ExecutorResult(
                    success=False,
                    error=f"公共脚本ID格式错误: {script_id}"
                )

            exec_logs["script_id"] = script_id

            # 从数据库获取脚本详情
            logger.info(f"获取公共脚本，ID: {script_id}")
            script_info = await Script_libraryService.script_library_detail_services(
                query_db=self.executor_ctx.mysql_obj,
                script_id=script_id
            )

            if not script_info or not script_info.script_id:
                return ExecutorResult(
                    success=False,
                    error=f"未找到公共脚本，ID: {script_id}"
                )

            # 检查脚本状态
            if script_info.status == 0:
                return ExecutorResult(
                    success=False,
                    error=f"公共脚本已停用，ID: {script_id}"
                )

            script_content = script_info.script_content
            script_type = script_info.script_type
            script_name = script_info.script_name

            if not script_content:
                return ExecutorResult(
                    success=False,
                    error=f"公共脚本内容为空，ID: {script_id}"
                )

            exec_logs["script_name"] = script_name
            exec_logs["script_type"] = script_type
            exec_logs["script_content"] = script_content

            logger.info(f"开始执行公共脚本: {script_name}，类型: {script_type}")

            # 根据脚本类型执行
            if script_type == ScriptTypeEnum.PYTHON or script_type == "python":
                result = await self._execute_python_script(script_content, exec_logs)
            elif script_type == ScriptTypeEnum.JAVASCRIPT or script_type == "javascript":
                result = await self._execute_javascript_script(script_content, exec_logs)
            else:
                # 默认当作 Python 脚本执行
                result = await self._execute_python_script(script_content, exec_logs)

            execution_time = time.time() - start_time
            result.execution_time = execution_time

            logger.info(f"公共脚本执行完成: {script_name}，耗时: {execution_time:.3f}s")

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"公共脚本执行异常: {str(e)}")
            return ExecutorResult(
                success=False,
                error=f"公共脚本执行失败: {str(e)}",
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
                return ExecutorResult(
                    success=True,
                    message="Python 公共脚本执行成功",
                    log=json.dumps(exec_logs, indent=2, ensure_ascii=False),
                    data=result.get('output')
                )
            else:
                return ExecutorResult(
                    success=False,
                    error=f"Python 公共脚本执行失败: {result.get('error')}",
                    log=exec_logs
                )

        except Exception as e:
            return ExecutorResult(
                success=False,
                error=f"Python 公共脚本执行异常: {str(e)}",
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
                message="JavaScript 公共脚本执行成功",
                log=logs_str,
                data=result
            )

        except Exception as e:
            return ExecutorResult(
                success=False,
                error=f"JavaScript 公共脚本执行失败: {str(e)}",
                log=exec_logs
            )

    def validate(self, task_config: Task_config) -> bool:
        """
        验证公共脚本配置

        Args:
            task_config: 任务配置

        Returns:
            验证是否通过
        """
        if not task_config.publicscript:
            logger.warning("公共脚本ID为空")
            return False
        return True
