#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：api_task_exectors.py
@Author  ：david
@Date    ：2025-10-23 13:38
@Desc    ：任务执行器模块（向后兼容入口）

此文件为向后兼容保留，所有执行器已重构到独立文件中。
建议直接从 utils.api_workflow_tools.executors 导入。
"""

# 从新的执行器模块导入所有内容，保持向后兼容
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.api_workflow_tools.executors.wait_executor import WaitTaskExecutor
from utils.api_workflow_tools.executors.custom_script_executor import CustomScriptExecutor
from utils.api_workflow_tools.executors.public_script_executor import PublicScriptExecutor
from utils.api_workflow_tools.executors.db_operation_executor import DBOperationExecutor
from utils.api_workflow_tools.executors.api_case_executor import APICaseExecutor
from utils.api_workflow_tools.executors.api_executor import APIExecutor
from utils.api_workflow_tools.executors.web_case_executor import WebCaseExecutor
from utils.api_workflow_tools.executors.factory import TaskExecutorFactory, TaskExecutorManager

# 导出所有类，保持向后兼容
__all__ = [
    "BaseTaskExecutor",
    "WaitTaskExecutor",
    "CustomScriptExecutor",
    "PublicScriptExecutor",
    "DBOperationExecutor",
    "APICaseExecutor",
    "APIExecutor",
    "WebCaseExecutor",
    "TaskExecutorFactory",
    "TaskExecutorManager",
]


# 使用示例
async def main():
    """使用示例"""
    from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import (
        NodeConfigModel,
        WorknodesModelWithChildren,
        Task_config,
        TaskTypeEnum,
    )
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
