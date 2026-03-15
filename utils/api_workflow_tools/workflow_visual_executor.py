#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
工作流可视化执行工具 - 简洁版
提供前端友好的结构化输出
"""
import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator, Optional

from config.enums import NotificationType
from config.get_db import get_db
from config.get_httpclient import get_http_client
from config.get_redis import RedisUtil
from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsConfig
from module_admin.api_testing.api_environments.service.environments_service import EnvironmentsService
from module_admin.api_testing.api_test_execution_log.service.execution_log_service import Execution_logService
from module_admin.api_workflow.api_param_item.dao.api_param_item_dao import Api_param_itemDao
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemPageQueryModel
from module_admin.api_workflow.workflow.service.workflow_service import WorkflowService
from module_admin.system.notification.entity.vo.notification_vo import NotificationModel
from module_admin.system.notification.service.notification_service import NotificationService
from utils.api_tools.executors.models import ExecutorContext
from utils.api_workflow_tools.api_workflows_exectors import StreamingWorkflowExecutor
from utils.api_workflow_tools.models import StreamEvent, StreamEventType
from utils.log_util import logger


async def execute_workflow_visual(query_db, session, redis, workflow_id: int, user_id: int,
                                  parameterization_id: Optional[int] = None,
                                  env_id: Optional[int] = None, loop_count=1):
    """
    执行工作流并返回可视化事件流

    参数:
        workflow_id: 工作流ID
        user_id: 用户ID
        env_id: 环境ID（可选，从工作流配置获取）

    返回:
        生成器，产出格式化的执行事件
    """

    try:
        # 1. 获取工作流定义
        from module_admin.api_workflow.workflow.service.workflow_service import WorkflowService
        workflow = await WorkflowService.get_workflow_nodetree_services(query_db, workflow_id)

        # 2. 获取环境配置
        if not env_id and workflow.execution_config:
            env_id = workflow.execution_config.env_id

        if not env_id:
            # yield create_event("error", "❌ 错误", "环境ID为空，无法执行", {"workflow_id": workflow_id})
            yield StreamEvent(event_type=StreamEventType.ERROR, workflow_id=workflow_id, message="环境ID为空，无法执行")
            return

        workflow.execution_config.loop_count = loop_count

        # 3. 准备执行环境

        env_config = await EnvironmentsService.get_request_config_services(
            query_db, EnvironmentsConfig(id=env_id)
        )

        # 4. 构建执行上下文
        executor_context = ExecutorContext(
            user_id=user_id,
            env_id=env_id,
            parameterization={},
            variables={},
            redis_obj=redis,
            mysql_obj=query_db,
            env_config=env_config,
            session=session,
            # sort=0
        )

        # 5. 获取参数化数据（如果有）
        # parameterization_id = workflow.execution_config.parameterization_id if workflow.execution_config else None
        if parameterization_id:
            param_items = await Api_param_itemDao.get_api_param_item_orm_list(
                query_db, Api_param_itemPageQueryModel(parameterization_id=parameterization_id)
            )
            param_list = param_items if param_items else [Api_param_itemPageQueryModel(**dict())]
        else:
            param_list = [Api_param_itemPageQueryModel(**dict())]

        # 6. 创建执行器
        executor = StreamingWorkflowExecutor()

        # 7. 执行工作流（支持多组参数）
        for param_item in param_list:
            # 显示数据集信息
            if param_item.group_name:
                yield StreamEvent(
                    event_type=StreamEventType.LOG,
                    message=f"使用数据集: {param_item.group_name}"
                )

            # 设置参数化数据
            executor_context.parameterization = param_item.item or {}

            # 流式执行并转换事件
            async for event in executor.execute_workflow_stream(workflow, executor_context):
                yield event
    except Exception as e:
        logger.error(f"工作流执行失败: {e}")
        yield StreamEvent(event_type=StreamEventType.ERROR, workflow_id=workflow_id,
                          message=f"执行工作流失败: {str(e)}")
    # finally:
    #     await query_db.close()


async def execute_workflow_sync(
        workflow_id: int,
        user_id: int,
        env_id: Optional[int] = None,
        parameterization_id: Optional[int] = None,
        loop_count: int = 1,
        trigger_type: str = "cron"
) -> dict:
    """
    非流式执行工作流（用于定时任务等场景）

    参数:
        workflow_id: 工作流ID
        user_id: 用户ID
        env_id: 环境ID（可选）
        parameterization_id: 参数化ID（可选）
        loop_count: 循环次数
        trigger_type: 触发类型 (manual/cron/api/system)

    返回:
        执行结果字典
    """
    from module_admin.api_workflow.api_workflow_report.entity.vo.api_workflow_report_vo import Api_workflow_reportModel
    from module_admin.api_workflow.api_workflow_report.service.api_workflow_report_service import \
        Api_workflow_reportService
    from module_admin.api_testing.api_test_execution_log.service.execution_log_service import Execution_logService
    from module_admin.websocket.service.websocket_service import WebSocketService

    logger.info(f"[execute_workflow_sync] 开始执行，workflow_id={workflow_id}")

    start_time = datetime.now()
    total_cases = 0
    success_cases = 0
    failed_cases = 0

    has_error = False
    error_message = ""
    sort = 0

    # logger.debug(f"[execute_workflow_sync] 准备获取数据库连接...")
    async for query_db in get_db():
        # logger.debug(f"[execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...")
        async for session in get_http_client():
            # logger.debug(f"[execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...")
            redis = await RedisUtil.create_redis_pool()
            logger.debug(f"[execute_workflow_sync] Redis 连接成功，准备查询工作流信息...")
            workflow_info = await WorkflowService.workflow_detail_services(query_db, workflow_id)
            workflow_name = workflow_info.name
            logger.debug(f"[execute_workflow_sync] 工作流信息获取成功: {workflow_name}")
            # 创建执行报告
            report_id = await Api_workflow_reportService.add_workflow_report_services(
                query_db,
                Api_workflow_reportModel(
                    workflow_id=workflow_id,
                    name=f"{workflow_name}-{datetime.now().isoformat(timespec='seconds')}",
                    trigger_type=trigger_type,
                    start_time=start_time.isoformat(timespec='seconds')
                )
            )

            try:
                # 执行工作流并收集所有事件
                async for event in execute_workflow_visual(
                        query_db=query_db,
                        session=session,
                        redis=redis,
                        workflow_id=workflow_id,
                        user_id=user_id,
                        parameterization_id=parameterization_id,
                        env_id=env_id,
                        loop_count=loop_count
                ):
                    sort += 1
                    # 记录日志到数据库
                    await Execution_logService.add_event_log(event, query_db, sort, report_id)


                    # 统计用例结果
                    if event.event_type == StreamEventType.CASE_RESULT:
                        total_cases += 1
                        if event.is_success and event.assertion_success:
                            success_cases += 1
                        else:
                            failed_cases += 1

                    # 打印日志
                    logger.info(f"[{event.event_type.value}] {event.message}")

            except Exception as e:
                has_error = True
                error_message = str(e)
                logger.error(f"工作流执行异常: {error_message}")

            finally:
                # 关闭 Redis 连接（防止连接泄漏）
                try:
                    await redis.close()
                except Exception as redis_close_error:
                    logger.error(f"关闭 Redis 连接失败: {str(redis_close_error)}")

                # 更新报告统计数据
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                is_success = 1 if failed_cases == 0 and total_cases >= 0 and not has_error else 0

                try:
                    await Api_workflow_reportService.edit_api_workflow_report_services(
                        query_db,
                        Api_workflow_reportModel(
                            report_id=report_id,
                            end_time=end_time,
                            total_cases=total_cases,
                            success_cases=success_cases,
                            failed_cases=failed_cases,
                            duration=duration,
                            is_success=is_success
                        )
                    )
                except Exception as update_error:
                    logger.error(f"更新工作流报告失败: {str(update_error)}")

                # 发送 WebSocket 通知
                try:
                    if has_error:
                        await WebSocketService.notify_workflow_failed(
                            user_id=user_id,
                            workflow_id=workflow_id,
                            workflow_name=workflow_name ,
                            error=error_message
                        )
                        add_notification_result = await NotificationService.add_notification_services(query_db,
                                                                                                      NotificationModel(
                                                                                                          notification_type=NotificationType.ERROR,
                                                                                                          user_id=user_id,
                                                                                                          message=f"{workflow_name}执行异常:{error_message}",
                                                                                                          is_read=False))
                    else:
                        await WebSocketService.notify_task_complete(
                            user_id=user_id,
                            workflow_id=workflow_id,
                            workflow_name=workflow_name,
                            total=total_cases,
                            success=success_cases,
                            failed=failed_cases,
                            duration=duration
                        )
                        add_notification_result = await NotificationService.add_notification_services(query_db,
                                                                                                      NotificationModel(
                                                                                                          notification_type=NotificationType.SUCCESS if failed_cases == 0 else NotificationType.ERROR,
                                                                                                          user_id=user_id,
                                                                                                          message=f'{workflow_name} 执行完成，共{total_cases}条，成功{success_cases}条，失败{failed_cases}条，耗时{round(duration, 2)}秒',
                                                                                                          is_read=False))
                except Exception as ws_error:
                    logger.error(f"发送 WebSocket 通知失败: {str(ws_error)}")

                return {
                    "reportId": report_id,
                    "workflowId": workflow_id,
                    "workflowName": workflow_name,
                    "totalCases": total_cases,
                    "successCases": success_cases,
                    "failedCases": failed_cases,
                    "duration": duration,
                    "isSuccess": is_success == 1,
                    "error": error_message if has_error else None
                }


# 直接运行
if __name__ == "__main__":
    pass
