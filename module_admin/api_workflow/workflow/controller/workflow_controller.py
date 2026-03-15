import asyncio
import json
from datetime import datetime
from typing import Optional

import aiohttp
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
# from starlette.responses import StreamingResponse
from fastapi.responses import StreamingResponse

from typing_extensions import AsyncGenerator

from config.enums import BusinessType, NotificationType
from config.get_db import get_db
from config.get_httpclient import get_http_client
from module_admin.annotation.log_annotation import Log
from module_admin.api_project_submodules.dao.project_submodules_dao import Project_submodulesDao
from module_admin.api_project_submodules.entity.vo.project_submodules_vo import Project_submodulesPageQueryModel
from module_admin.api_testing.api_test_execution_log.service.execution_log_service import Execution_logService
from module_admin.api_workflow.api_param_table.service.api_param_table_service import Api_param_tableService
from module_admin.api_workflow.api_workflow_report.dao.api_workflow_report_dao import Api_workflow_reportDao
from module_admin.api_workflow.api_workflow_report.entity.vo.api_workflow_report_vo import Api_workflow_reportModel
from module_admin.api_workflow.api_workflow_report.service.api_workflow_report_service import Api_workflow_reportService
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.notification.entity.vo.notification_vo import NotificationModel
from module_admin.system.notification.service.notification_service import NotificationService
from module_admin.system.service.login_service import LoginService
from module_admin.api_workflow.workflow.service.workflow_service import WorkflowService
from module_admin.api_workflow.workflow.entity.vo.workflow_vo import DeleteWorkflowModel, WorkflowModel, \
    WorkflowPageQueryModel, ExecWorkflowModel
from module_admin.websocket.service.websocket_service import WebSocketService
from utils.api_workflow_tools.api_workflows_exectors import StreamingWorkflowExecutor
from utils.api_workflow_tools.models import StreamEvent, StreamEventType
from utils.api_workflow_tools.workflow_visual_executor import execute_workflow_visual
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

workflowController = APIRouter(prefix='/workflow/workflow', dependencies=[Depends(LoginService.get_current_user)])


@workflowController.get(
    '/tree', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:list'))]
)
async def get_workflow_workflow_list(
        request: Request,
        project_submodules_page_query: Project_submodulesPageQueryModel = Depends(
            Project_submodulesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(project_submodules_page_query.model_dump())
    # workflow_page_query_result = await WorkflowService.get_workflow_moduletree_services(query_db,
    #                                                                                     project_submodules_page_query,
    #                                                                                     )
    project_submodules_page_query_result = await Project_submodulesDao.get_project_workflow_tree_by_project_id(query_db,
                                                                                                               project_submodules_page_query.project_id)
    logger.info('获取成功')

    return ResponseUtil.success(dict_content=project_submodules_page_query_result)


@workflowController.get(
    '/workflowtable', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:list'))]
)
async def get_workflow_workflowtable_list(
        request: Request,
        workflow_page_query: WorkflowPageQueryModel = Depends(WorkflowPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(workflow_page_query.model_dump())
    # 获取分页数据
    api_param_table_page_query_result = await Api_param_tableService.get_api_param_table_list_services(query_db,
                                                                                                       workflow_page_query,
                                                                                                       is_page=False)
    logger.info('获取成功')

    return ResponseUtil.success(rows=api_param_table_page_query_result)


@workflowController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:list'))]
)
async def get_workflow_workflow_list(
        request: Request,
        workflow_page_query: WorkflowPageQueryModel = Depends(WorkflowPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(workflow_page_query.model_dump())
    # 获取分页数据
    workflow_page_query_result = await WorkflowService.get_workflow_list_services(query_db, workflow_page_query,
                                                                                  is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=workflow_page_query_result)


@workflowController.post('', dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:add'))])
@ValidateFields(validate_model='add_workflow')
# @Log(title='测试执行器主', business_type=BusinessType.INSERT)
async def add_workflow_workflow(
        request: Request,
        add_workflow: WorkflowModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_workflow.create_by = current_user.user.user_name
    add_workflow.create_time = datetime.now()
    add_workflow.update_by = current_user.user.user_name
    add_workflow.update_time = datetime.now()
    logger.info(add_workflow.model_dump())
    add_workflow_result = await WorkflowService.add_workflow_services(query_db, add_workflow)
    # logger.info(add_workflow_result.message)

    return ResponseUtil.success(dict_content=add_workflow_result)


@workflowController.put('', dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:edit'))])
@ValidateFields(validate_model='edit_workflow')
# @Log(title='测试执行器主', business_type=BusinessType.UPDATE)
async def edit_workflow_workflow(
        request: Request,
        edit_workflow: WorkflowModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_workflow.model_dump())
    edit_workflow.update_by = current_user.user.user_name
    edit_workflow.update_time = datetime.now()
    edit_workflow_result = await WorkflowService.edit_workflow_services(query_db, edit_workflow)
    logger.info(edit_workflow_result.message)

    return ResponseUtil.success(msg=edit_workflow_result.message)


@workflowController.delete('/{workflow_ids}',
                           dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:remove'))])
# @Log(title='测试执行器主', business_type=BusinessType.DELETE)
async def delete_workflow_workflow(request: Request, workflow_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_workflow = DeleteWorkflowModel(workflowIds=workflow_ids)
    logger.info(delete_workflow.model_dump())
    delete_workflow_result = await WorkflowService.delete_workflow_services(query_db, delete_workflow)
    logger.info(delete_workflow_result.message)

    return ResponseUtil.success(msg=delete_workflow_result.message)


@workflowController.get(
    '/{workflow_id}', response_model=WorkflowModel,
    dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:query'))]
)
async def query_detail_workflow_workflow(request: Request, workflow_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    workflow_detail_result = await WorkflowService.get_workflow_nodetree_services(query_db, workflow_id)
    logger.info(f'获取workflow_id为{workflow_id}的信息成功')

    return ResponseUtil.success(model_content=workflow_detail_result)


@workflowController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:export'))])
# @Log(title='测试执行器主', business_type=BusinessType.EXPORT)
async def export_workflow_workflow_list(
        request: Request,
        workflow_page_query: WorkflowPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    workflow_query_result = await WorkflowService.get_workflow_list_services(query_db, workflow_page_query,
                                                                             is_page=False)
    workflow_export_result = await WorkflowService.export_workflow_list_services(workflow_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(workflow_export_result))


@workflowController.post('/exec', dependencies=[Depends(CheckUserInterfaceAuth('workflow:workflow:query'))])
async def exec_workflow_stream(
        request: Request,
        execWorkflowmodel: ExecWorkflowModel,
        query_db: AsyncSession = Depends(get_db),
        # session: AsyncGenerator[aiohttp.ClientSession, None] = Depends(get_http_client),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    执行工作流并流式返回结果

    参数:
        workflow_id: 工作流ID
        env_id: 环境ID（可选）

    返回:
        流式响应，前端可实时显示执行进度
    """
    user_id = current_user.user.user_id

    # 定义一个函数来处理无法直接序列化的对象
    def datetime_converter(o):
        if isinstance(o, datetime):
            return o.isoformat()  # 将datetime对象转换为ISO格式的字符串
        raise TypeError("Type not serializable")

    workflow_info = await WorkflowService.workflow_detail_services(query_db, execWorkflowmodel.workflow_id)

    async def event_stream():
        """事件流生成器"""
        sort = 0
        start_time = datetime.now()
        total_cases = 0
        success_cases = 0
        failed_cases = 0
        workflow_name = workflow_info.name
        has_error = False
        error_message = ""

        report_id = await Api_workflow_reportService.add_workflow_report_services(query_db,
                                                                                  Api_workflow_reportModel(
                                                                                      workflow_id=execWorkflowmodel.workflow_id,
                                                                                      name=f"{workflow_info.name}-{datetime.now().isoformat(timespec='seconds')}",
                                                                                      trigger_type="manual",
                                                                                      start_time=start_time.isoformat(timespec='seconds')
                                                                                  ))
        async for session in get_http_client():
            try:
                # 执行工作流并获取可视化事件
                async for event in execute_workflow_visual(query_db=query_db, session=session,
                                                           redis=request.app.state.redis,
                                                           workflow_id=execWorkflowmodel.workflow_id, user_id=user_id,
                                                           parameterization_id=execWorkflowmodel.parameterization_id,
                                                           env_id=execWorkflowmodel.env_id,
                                                           loop_count=execWorkflowmodel.loop_count):
                    sort += 1
                    log_id = await Execution_logService.add_event_log(event, query_db, sort, report_id)
                    event.log_id = log_id

                    # 统计用例结果
                    if event.event_type == StreamEventType.CASE_RESULT:
                        total_cases += 1
                        if event.is_success and event.assertion_success:
                            success_cases += 1
                        else:
                            failed_cases += 1
                    data = event.model_dump_json(by_alias=True)
                    yield f"data: {data}\n\n"

                    await asyncio.sleep(0.01)

            except Exception as e:
                has_error = True
                error_message = str(e)
                # 发送错误事件
                error_event = StreamEvent(
                    event_type=StreamEventType.ERROR,
                    message=f"{workflow_name}执行异常: {str(e)}",
                )
                yield f"data: {error_event.model_dump_json()}\n\n"
            finally:
                # 更新报告统计数据
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                is_success = 1 if failed_cases == 0 and total_cases > 0 and not has_error else 0

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
                            workflow_id=execWorkflowmodel.workflow_id,
                            workflow_name=workflow_name,
                            error=error_message
                        )

                        add_notification_result = await NotificationService.add_notification_services(query_db,
                                                                                                      NotificationModel(
                                                                                                          notification_type=NotificationType.ERROR,
                                                                                                          user_id=user_id,
                                                                                                          message=f"{workflow_name}执行异常:{error_message}",
                                                                                                          is_read=False))
                    else:
                        await WebSocketService.notify_workflow_complete(
                            user_id=user_id,
                            workflow_id=execWorkflowmodel.workflow_id,
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

                error_event = StreamEvent(
                    event_type=StreamEventType.LOG,
                    message=f"执行结束",
                )
                yield f"data: {error_event.model_dump_json(by_alias=True)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Content-Encoding": "identity",  # ⭐ 禁止 gzip 压缩
        },
        background=None
    )
