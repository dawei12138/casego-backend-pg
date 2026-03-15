#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import asyncio
from datetime import datetime

from config.get_db import get_db
from config.get_httpclient import get_http_client
from config.get_redis import RedisUtil
from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsConfig
from module_admin.api_testing.api_environments.service.environments_service import EnvironmentsService
from module_admin.api_workflow.api_param_item.dao.api_param_item_dao import Api_param_itemDao
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemPageQueryModel
from module_admin.api_workflow.api_param_item.service.api_param_item_service import Api_param_itemService
from module_admin.api_workflow.api_worknodes.dao.worknodes_dao import WorknodesDao
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import WorknodesPageQueryModel
from module_admin.api_workflow.api_worknodes.service.worknodes_service import WorknodesService
from module_admin.api_workflow.workflow.entity.vo.workflow_vo import WorkflowTreeModel
from module_admin.api_workflow.workflow.service.workflow_service import WorkflowService
from utils.api_tools.executors.models import ExecutorContext
from utils.api_workflow_tools.api_workflows_exectors import StreamingWorkflowExecutor
from utils.log_util import logger


async def execute_workflow_by_id(workflow_id: int):
    """根据工作流ID执行工作流"""

    async for query_db in get_db():
        async for session in get_http_client():
            try:

                workflow = await WorkflowService.get_workflow_nodetree_services(query_db, workflow_id)
                redis = await RedisUtil.create_redis_pool()
                env_id = workflow.execution_config.env_id
                if not env_id:
                    return '环境为空，无法执行'

                env_config = await EnvironmentsService.get_request_config_services(query_db,
                                                                                   EnvironmentsConfig(id=env_id))

                # session = await get_http_client()
                # 接口任务执行器上下文
                api_executor_context = ExecutorContext(
                    user_id=1,
                    env_id=env_id,
                    # parameterization_id=6,
                    parameterization={},
                    variables={},
                    redis_obj=redis,
                    mysql_obj=query_db,
                    env_config=env_config,
                    session=session
                )
                if api_executor_context.parameterization_id:
                    api_param_item_page_query_result = await Api_param_itemDao.get_api_param_item_orm_list(query_db,
                                                                                                           Api_param_itemPageQueryModel(
                                                                                                               parameterization_id=api_executor_context.parameterization_id))
                    api_param_item_page_query_result = [Api_param_itemPageQueryModel(**dict())] if not api_param_item_page_query_result else api_param_item_page_query_result
                else:
                    api_param_item_page_query_result = [Api_param_itemPageQueryModel(**dict())]
                # 创建执行器
                executor = StreamingWorkflowExecutor()

                for api_param_item in api_param_item_page_query_result:
                    logger.info(f"执行数据集合——>{api_param_item.group_name}: 数据信息{api_param_item.item}")
                    logger.info(f"开始执行工作流 ID: {workflow_id}")
                    logger.info("=" * 60)
                    # 开始流式执行并打印输出
                    api_executor_context.parameterization = api_param_item.item

                    async for event in executor.execute_workflow_stream(
                            workflow=workflow,
                            executor_context=api_executor_context
                    ):

                        timestamp = event.timestamp.strftime("%H:%M:%S")

                        if event.node_id:
                            logger.info(
                                f"[{timestamp}] [{event.event_type.value.upper()}] [节点{event.node_id}] {event.message}")
                        else:
                            logger.info(f"[{timestamp}] [{event.event_type.value.upper()}] {event.message}")

                        # 显示进度
                        if event.progress is not None:
                            logger.info(f"    >> 进度: {event.progress:.1f}%")

                        # 显示关键数据
                        if event.data and "task_result" in event.data:
                            result = event.data["task_result"]
                            logger.info(f"    >> 任务结果: {result}")

                    logger.info("=" * 60)
                    logger.info(f"工作流 {workflow_id} 执行完成")
                    logger.info(f"执行完成数据集合——>{api_param_item.group_name}: 数据信息{api_param_item.item}")
            except Exception as e:
                logger.info(f"执行失败: {e}")
                import traceback
                traceback.logger.info_exc()
            finally:
                await query_db.close()


async def demo(workflow_id):
    """主函数"""
    try:
        await execute_workflow_by_id(workflow_id)
    except ValueError:
        logger.info("请输入有效的数字ID")
    except Exception as e:
        logger.info(f"执行出错: {e}")


if __name__ == "__main__":
    asyncio.run(demo(1))
