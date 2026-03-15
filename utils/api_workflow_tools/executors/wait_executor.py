#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：wait_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：等待任务执行器
"""
import asyncio
import time
from typing import Dict, Any

from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import Task_config
from utils.api_tools.executors.models import ExecutorResult
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.log_util import logger


class WaitTaskExecutor(BaseTaskExecutor):
    """
    等待任务执行器

    用于在工作流中实现等待/延时功能。
    """

    async def execute(self, task_config: Task_config) -> ExecutorResult:
        """
        执行等待逻辑

        Args:
            task_config: 任务配置，包含 wait_time（等待时间，单位毫秒）

        Returns:
            执行结果
        """
        start_time = time.time()

        try:
            # 获取等待时间（毫秒），默认为0
            wait_time_ms = task_config.wait_time or 0

            if wait_time_ms <= 0:
                return ExecutorResult(
                    success=True,
                    message="等待时间为0，跳过等待",
                    execution_time=0.0
                )

            # 转换为秒
            wait_time_seconds = wait_time_ms / 1000.0

            logger.info(f"开始等待 {wait_time_ms} 毫秒 ({wait_time_seconds} 秒)")

            # 使用异步等待
            # await asyncio.sleep(wait_time_seconds)
            time.sleep(wait_time_seconds)

            execution_time = time.time() - start_time

            logger.info(f"等待完成，实际耗时: {execution_time:.3f} 秒")

            return ExecutorResult(
                success=True,
                message=f"等待 {wait_time_ms} 毫秒完成",
                data={"wait_time_ms": wait_time_ms, "actual_time_s": execution_time},
                execution_time=execution_time
            )

        except asyncio.CancelledError:
            execution_time = time.time() - start_time
            logger.warning(f"等待任务被取消，已等待: {execution_time:.3f} 秒")
            return ExecutorResult(
                success=False,
                error="等待任务被取消",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"等待任务执行异常: {str(e)}")
            return ExecutorResult(
                success=False,
                error=f"等待任务执行失败: {str(e)}",
                execution_time=execution_time
            )

    def validate(self, task_config: Task_config) -> bool:
        """
        验证等待配置

        Args:
            task_config: 任务配置

        Returns:
            验证是否通过
        """
        # 等待时间可以为空或0，表示不等待
        wait_time = task_config.wait_time
        if wait_time is not None and wait_time < 0:
            logger.warning(f"等待时间不能为负数: {wait_time}")
            return False
        return True
