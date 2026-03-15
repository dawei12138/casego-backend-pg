#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：base_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：任务执行器基类
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union

from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import (
    NodeConfigModel,
    WorknodesModelWithChildren,
    Task_config,
)
from utils.api_tools.executors.models import ExecutorContext, SingleExecutorResult, ExecutorResult
from utils.api_workflow_tools.models import StreamingExecutionContext


class BaseTaskExecutor(ABC):
    """
    任务执行器基类

    所有类型的任务执行器都需要继承此类，并实现 execute 和 validate 方法。
    """

    def __init__(
        self,
        config: NodeConfigModel,
        context: StreamingExecutionContext,
        node: WorknodesModelWithChildren,
        executor_ctx: ExecutorContext
    ):
        """
        初始化任务执行器

        Args:
            config: 节点配置信息
            context: 流式执行上下文
            node: 工作节点信息（包含子节点）
            executor_ctx: 执行器上下文
        """
        self.config = config
        self.context = context
        self.node = node
        self.executor_ctx = executor_ctx

    @abstractmethod
    async def execute(self, task_config: Task_config) -> Union[Dict[str, Any], SingleExecutorResult, ExecutorResult, str]:
        """
        执行任务

        Args:
            task_config: 任务配置参数

        Returns:
            执行结果，可以是字典、SingleExecutorResult 或 ExecutorResult
        """
        pass

    @abstractmethod
    def validate(self, task_config: Task_config) -> bool:
        """
        验证任务配置

        Args:
            task_config: 任务配置参数

        Returns:
            验证是否通过
        """
        return True

    def pre_execute(self, task_config: Task_config) -> bool:
        """
        执行前置处理

        Args:
            task_config: 任务配置参数

        Returns:
            前置处理是否成功
        """
        return True

    def post_execute(self, result: Union[Dict[str, Any], SingleExecutorResult, ExecutorResult]) -> Union[Dict[str, Any], SingleExecutorResult, ExecutorResult]:
        """
        执行后置处理

        Args:
            result: 执行结果

        Returns:
            处理后的执行结果
        """
        return result

    def get_task_type_name(self) -> str:
        """
        获取任务类型名称

        Returns:
            任务类型的可读名称
        """
        return self.__class__.__name__.replace("Executor", "")
