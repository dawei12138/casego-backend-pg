#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：factory.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：任务执行器工厂和管理器
"""
from typing import Dict, Any, Optional, Type, Union

from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import (
    NodeConfigModel,
    WorknodesModelWithChildren,
    Task_config,
    TaskTypeEnum,
)
from utils.api_tools.executors.models import ExecutorContext, SingleExecutorResult, ExecutorResult
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.api_workflow_tools.executors.wait_executor import WaitTaskExecutor
from utils.api_workflow_tools.executors.custom_script_executor import CustomScriptExecutor
from utils.api_workflow_tools.executors.public_script_executor import PublicScriptExecutor
from utils.api_workflow_tools.executors.db_operation_executor import DBOperationExecutor
from utils.api_workflow_tools.executors.api_case_executor import APICaseExecutor
from utils.api_workflow_tools.executors.api_executor import APIExecutor
from utils.api_workflow_tools.executors.web_case_executor import WebCaseExecutor
from utils.api_workflow_tools.models import StreamingExecutionContext
from utils.log_util import logger


class TaskExecutorFactory:
    """
    任务执行器工厂

    负责创建和管理不同类型的任务执行器。
    """

    # 执行器类型映射表
    _executor_classes: Dict[TaskTypeEnum, Type[BaseTaskExecutor]] = {
        TaskTypeEnum.WAIT: WaitTaskExecutor,
        TaskTypeEnum.CUSTOMSCRIPT: CustomScriptExecutor,
        TaskTypeEnum.PUBLICSCRIPT: PublicScriptExecutor,
        TaskTypeEnum.DB_OPERATION: DBOperationExecutor,
        TaskTypeEnum.APICASE: APICaseExecutor,
        TaskTypeEnum.API: APIExecutor,
        TaskTypeEnum.WEBCASE: WebCaseExecutor,
    }

    def __init__(
        self,
        config: NodeConfigModel,
        context: StreamingExecutionContext,
        node: WorknodesModelWithChildren,
        executor_ctx: ExecutorContext
    ):
        """
        初始化执行器工厂

        Args:
            config: 节点配置信息
            context: 流式执行上下文
            node: 工作节点信息
            executor_ctx: 执行器上下文
        """
        self.config = config
        self.context = context
        self.node = node
        self.executor_ctx = executor_ctx
        self._executors: Dict[TaskTypeEnum, BaseTaskExecutor] = {}
        self._register_executors()

    def _register_executors(self) -> None:
        """注册所有执行器实例"""
        for task_type, executor_class in self._executor_classes.items():
            self._executors[task_type] = executor_class(
                self.config,
                self.context,
                self.node,
                self.executor_ctx
            )

    def get_executor(self, task_type: TaskTypeEnum) -> Optional[BaseTaskExecutor]:
        """
        获取指定类型的执行器

        Args:
            task_type: 任务类型

        Returns:
            对应的执行器实例，如果不存在则返回 None
        """
        executor = self._executors.get(task_type)
        if not executor:
            logger.warning(f"未找到任务类型 {task_type} 的执行器")
        return executor

    def register_executor(
        self,
        task_type: TaskTypeEnum,
        executor: BaseTaskExecutor
    ) -> None:
        """
        动态注册执行器

        Args:
            task_type: 任务类型
            executor: 执行器实例
        """
        self._executors[task_type] = executor
        logger.info(f"已注册执行器: {task_type} -> {executor.__class__.__name__}")

    @classmethod
    def register_executor_class(
        cls,
        task_type: TaskTypeEnum,
        executor_class: Type[BaseTaskExecutor]
    ) -> None:
        """
        注册执行器类（全局注册）

        Args:
            task_type: 任务类型
            executor_class: 执行器类
        """
        cls._executor_classes[task_type] = executor_class
        logger.info(f"已注册执行器类: {task_type} -> {executor_class.__name__}")

    def get_supported_task_types(self) -> list:
        """
        获取支持的任务类型列表

        Returns:
            任务类型列表
        """
        return list(self._executors.keys())


class TaskExecutorManager:
    """
    任务执行器管理器

    负责协调任务执行器的创建和执行流程。
    """

    def __init__(
        self,
        config: NodeConfigModel,
        context: StreamingExecutionContext,
        node: WorknodesModelWithChildren,
        executor_ctx: ExecutorContext
    ):
        """
        初始化任务执行器管理器

        Args:
            config: 节点配置信息
            context: 流式执行上下文
            node: 工作节点信息
            executor_ctx: 执行器上下文
        """
        self.config = config
        self.context = context
        self.node = node
        self.executor_ctx = executor_ctx
        self.factory = TaskExecutorFactory(config, context, node, executor_ctx)

    async def execute_task(self) -> Union[Dict[str, Any], SingleExecutorResult, ExecutorResult]:
        """
        执行任务

        根据任务配置中的任务类型，获取对应的执行器并执行任务。

        Returns:
            执行结果

        Raises:
            ValueError: 当找不到对应的执行器或配置验证失败时
        """
        task_config = self.config.task_config
        if not task_config:
            raise ValueError("任务配置为空")

        task_type = task_config.task_type
        if not task_type:
            raise ValueError("任务类型为空")

        # 获取执行器
        executor = self.factory.get_executor(task_type)
        if not executor:
            raise ValueError(f"未找到任务类型 {task_type} 的执行器")

        # 验证配置
        if not executor.validate(task_config):
            raise ValueError(f"任务配置验证失败: {task_config}")

        # 执行前置处理
        executor.pre_execute(task_config)

        # 执行任务
        logger.info(f"开始执行任务，类型: {task_type}，节点: {self.node.name}")
        result = await executor.execute(task_config)

        # 执行后置处理
        result = executor.post_execute(result)

        logger.info(f"任务执行完成，类型: {task_type}，节点: {self.node.name}")

        return result

    async def execute_task_with_type(
        self,
        task_type: TaskTypeEnum,
        task_config: Task_config
    ) -> Union[Dict[str, Any], SingleExecutorResult, ExecutorResult]:
        """
        指定类型执行任务

        Args:
            task_type: 任务类型
            task_config: 任务配置

        Returns:
            执行结果
        """
        executor = self.factory.get_executor(task_type)
        if not executor:
            raise ValueError(f"未找到任务类型 {task_type} 的执行器")

        if not executor.validate(task_config):
            raise ValueError(f"任务配置验证失败: {task_config}")

        executor.pre_execute(task_config)
        result = await executor.execute(task_config)
        result = executor.post_execute(result)

        return result

    def get_supported_task_types(self) -> list:
        """
        获取支持的任务类型列表

        Returns:
            任务类型列表
        """
        return self.factory.get_supported_task_types()


# 使用示例
async def main():
    """使用示例"""
    from utils.api_workflow_tools.models import StreamingExecutionContext
    from utils.api_tools.executors.models import ExecutorContext

    # 创建执行上下文
    executor_ctx = ExecutorContext(
        user_id=1,
        env_id=1,
        mysql_obj=None,
        redis_obj=None,
        variables={},
        parameterization={},
        session=None
    )

    streaming_ctx = StreamingExecutionContext(
        executor_context=executor_ctx,
        workflow_id=1
    )

    # 创建节点配置
    task_config = Task_config(
        task_type=TaskTypeEnum.WAIT,
        wait_time=1000  # 等待1秒
    )

    node_config = NodeConfigModel(
        task_config=task_config
    )

    # 创建节点
    node = WorknodesModelWithChildren(
        node_id=1,
        name="测试等待节点"
    )

    # 创建管理器并执行
    manager = TaskExecutorManager(node_config, streaming_ctx, node, executor_ctx)
    result = await manager.execute_task()
    print(f"执行结果: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
