#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：strategies.py
@Author  ：david
@Date    ：2025-08-11 23:39 
"""
import asyncio
# utils/api_tools/executors/strategies.py
import time
from abc import ABC, abstractmethod
from typing import Union

from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult, CasesConfig


class ExecutorStrategy(ABC):
    """执行器策略抽象基类"""

    @abstractmethod
    def execute(self, context: ExecutorContext,
                config: Union[SetupConfig, TeardownConfig, CasesConfig]) -> ExecutorResult:
        """执行具体逻辑"""
        pass

    def validate_config(self, config: Union[SetupConfig, TeardownConfig]) -> bool:
        """验证配置"""
        return True

    def _measure_execution_time(self, func, *args, **kwargs):
        """测量执行时间的装饰器方法"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        if hasattr(result, 'execution_time'):
            result.execution_time = execution_time
        return result


class WaitTimeExecutor(ExecutorStrategy):
    """等待时间执行器"""

    async def execute(self, context: ExecutorContext, config: Union[SetupConfig, TeardownConfig]) -> ExecutorResult:
        start_time = time.time()
        try:
            wait_time = getattr(config, 'wait_time', 0)
            if wait_time <= 0:
                return ExecutorResult(success=True, message="无需等待")

            # 方式1: 真正阻塞等待（会阻塞整个事件循环）
            time.sleep(wait_time / 1000)

            # 方式2: 如果需要在线程池中执行阻塞操作（推荐）
            # loop = asyncio.get_event_loop()
            # await loop.run_in_executor(None, time.sleep, wait_time / 1000)

            execution_time = time.time() - start_time

            return ExecutorResult(
                success=True,
                message=f"等待{wait_time / 1000}秒完成",
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutorResult(
                success=False,
                error=f"等待执行失败: {str(e)}",
                execution_time=execution_time
            )
