#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：api_case_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：API测试用例执行器
"""
import time
from typing import Dict, Any

from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import Task_config
from utils.api_tools.executors.api_single_all_executor import api_single_all_executor
from utils.api_tools.executors.models import ExecutorContext, SingleExecutorResult
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.log_util import logger


class APICaseExecutor(BaseTaskExecutor):
    """
    API测试用例执行器

    执行已保存的API测试用例，包括前置脚本、接口请求、后置脚本和断言。
    """

    async def execute(self, task_config: Task_config) -> SingleExecutorResult:
        """
        执行API测试用例

        Args:
            task_config: 任务配置，包含:
                - api_id: 测试用例ID
                - case_id: 测试用例ID (备用字段)

        Returns:
            SingleExecutorResult: 包含完整的执行结果
        """
        start_time = time.time()

        try:
            # 获取用例ID
            case_id = task_config.api_id or task_config.case_id
            if not case_id:
                logger.error("API测试用例ID为空")
                return SingleExecutorResult(
                    response=None,
                    setup_results=[],
                    teardown_results=[],
                    assersion_result=None,
                    log="API测试用例ID为空"
                )

            logger.info(f"开始执行API测试用例，ID: {case_id}")

            # 创建执行上下文
            context = ExecutorContext(
                user_id=self.executor_ctx.user_id,
                env_id=self.executor_ctx.env_id,
                case_id=case_id,
                mysql_obj=self.executor_ctx.mysql_obj,
                redis_obj=self.executor_ctx.redis_obj,
                variables=self.executor_ctx.variables.copy() if self.executor_ctx.variables else {},
                parameterization=self.executor_ctx.parameterization.copy() if self.executor_ctx.parameterization else {},
                session=self.executor_ctx.session
            )

            # 确认session对象的传递
            logger.info(f"[Session传递] 使用session对象ID: {id(context.session)}, cookie jar中有{len(context.session.cookie_jar) if context.session else 0}个cookies")

            # 执行测试用例
            res = await api_single_all_executor(context)
            # res.response.case_name =
            execution_time = time.time() - start_time
            logger.info(f"API测试用例执行完成，ID: {case_id}，耗时: {execution_time:.3f}s")

            # 更新上下文变量（如果用例执行中产生了新变量）
            if context.variables:
                self.executor_ctx.variables.update(context.variables)

            return res

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"API测试用例执行异常: {str(e)}")

            # 返回一个失败的结果
            from utils.api_tools.executors.models import ExecutorResult
            from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import APIResponse

            error_response = APIResponse(
                is_success=False,
                error_message=f"执行异常: {str(e)}",
                execution_time=execution_time
            )

            return SingleExecutorResult(
                response=error_response,
                setup_results=[],
                teardown_results=[],
                assersion_result=ExecutorResult(
                    success=False,
                    error=str(e)
                ),
                log=f"API测试用例执行异常: {str(e)}"
            )

    def validate(self, task_config: Task_config) -> bool:
        """
        验证API测试用例配置

        Args:
            task_config: 任务配置

        Returns:
            验证是否通过
        """
        case_id = task_config.api_id or task_config.case_id
        if not case_id:
            logger.warning("API测试用例ID为空")
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
