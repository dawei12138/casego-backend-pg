#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：api_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：API类型执行器（直接执行API请求）
"""
import time
from typing import Dict, Any

from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import Task_config
from utils.api_tools.executors.api_single_all_executor import api_single_all_executor
from utils.api_tools.executors.models import ExecutorContext, SingleExecutorResult, ExecutorResult
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.log_util import logger


class APIExecutor(BaseTaskExecutor):
    """
    API类型执行器

    执行API请求，与APICaseExecutor逻辑一致，但类型为API而非API_CASE。
    可用于直接配置的API请求节点。
    """

    async def execute(self, task_config: Task_config) -> SingleExecutorResult:
        """
        执行API请求

        Args:
            task_config: 任务配置，包含:
                - api_id: API用例ID

        Returns:
            SingleExecutorResult: 包含完整的执行结果
        """
        start_time = time.time()

        try:
            # 获取API ID（这里api_id就是用例ID）
            api_id = task_config.api_id
            if not api_id:
                logger.error("API ID为空")
                return self._create_error_result("API ID为空", time.time() - start_time)

            logger.info(f"开始执行API请求，ID: {api_id}")

            # 创建执行上下文
            context = ExecutorContext(
                user_id=self.executor_ctx.user_id,
                env_id=self.executor_ctx.env_id,
                case_id=api_id,  # API执行同样使用case_id
                mysql_obj=self.executor_ctx.mysql_obj,
                redis_obj=self.executor_ctx.redis_obj,
                variables=self.executor_ctx.variables.copy() if self.executor_ctx.variables else {},
                parameterization=self.executor_ctx.parameterization.copy() if self.executor_ctx.parameterization else {},
                session=self.executor_ctx.session
            )

            # 确认session对象的传递
            logger.info(f"[Session传递] 使用session对象ID: {id(context.session)}, cookie jar中有{len(context.session.cookie_jar) if context.session else 0}个cookies")

            # 执行API请求（复用api_single_all_executor）
            res = await api_single_all_executor(context)

            execution_time = time.time() - start_time
            logger.info(f"API请求执行完成，ID: {api_id}，耗时: {execution_time:.3f}s")

            # 更新上下文变量
            if context.variables:
                self.executor_ctx.variables.update(context.variables)

            # 更新参数化变量
            if context.parameterization:
                self.executor_ctx.parameterization.update(context.parameterization)

            return res

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"API请求执行异常: {str(e)}")
            return self._create_error_result(str(e), execution_time)

    def _create_error_result(self, error_msg: str, execution_time: float) -> SingleExecutorResult:
        """
        创建错误结果

        Args:
            error_msg: 错误信息
            execution_time: 执行耗时

        Returns:
            SingleExecutorResult: 错误结果
        """
        from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import APIResponse

        error_response = APIResponse(
            is_success=False,
            error_message=f"执行异常: {error_msg}",
            execution_time=execution_time
        )

        return SingleExecutorResult(
            response=error_response,
            setup_results=[],
            teardown_results=[],
            assersion_result=ExecutorResult(
                success=False,
                error=error_msg
            ),
            log=f"API请求执行异常: {error_msg}"
        )

    def validate(self, task_config: Task_config) -> bool:
        """
        验证API配置

        Args:
            task_config: 任务配置

        Returns:
            验证是否通过
        """
        if not task_config.api_id:
            logger.warning("API ID为空")
            return False
        return True

    def post_execute(self, result: SingleExecutorResult) -> SingleExecutorResult:
        """
        后置处理：更新流式上下文的统计信息

        Args:
            result: 执行结果

        Returns:
            处理后的执行结果
        """
        # 更新上下文统计信息
        if self.context:
            if result.response and result.response.is_success:
                self.context.increment_completed()
            else:
                self.context.increment_failed()

        return result
