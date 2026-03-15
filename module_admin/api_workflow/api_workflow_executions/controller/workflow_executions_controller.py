from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_workflow.api_workflow_executions.service.workflow_executions_service import Workflow_executionsService
from module_admin.api_workflow.api_workflow_executions.entity.vo.workflow_executions_vo import DeleteWorkflow_executionsModel, Workflow_executionsModel, Workflow_executionsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


workflow_executionsController = APIRouter(prefix='/api_workflow_executions/workflow_executions', dependencies=[Depends(LoginService.get_current_user)])


@workflow_executionsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_workflow_executions:workflow_executions:list'))]
)
async def get_api_workflow_executions_workflow_executions_list(
    request: Request,
workflow_executions_page_query: Workflow_executionsPageQueryModel = Depends(Workflow_executionsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(workflow_executions_page_query.model_dump())
    # 获取分页数据
    workflow_executions_page_query_result = await Workflow_executionsService.get_workflow_executions_list_services(query_db, workflow_executions_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=workflow_executions_page_query_result)


@workflow_executionsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_workflow_executions:workflow_executions:add'))])
@ValidateFields(validate_model='add_workflow_executions')
# @Log(title='执行器执行记录', business_type=BusinessType.INSERT)
async def add_api_workflow_executions_workflow_executions(
    request: Request,
    add_workflow_executions: Workflow_executionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_workflow_executions.create_by = current_user.user.user_name
    add_workflow_executions.create_time = datetime.now()
    add_workflow_executions.update_by = current_user.user.user_name
    add_workflow_executions.update_time = datetime.now()
    logger.info(add_workflow_executions.model_dump())
    add_workflow_executions_result = await Workflow_executionsService.add_workflow_executions_services(query_db, add_workflow_executions)
    logger.info(add_workflow_executions_result.message)

    return ResponseUtil.success(msg=add_workflow_executions_result.message)


@workflow_executionsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_workflow_executions:workflow_executions:edit'))])
@ValidateFields(validate_model='edit_workflow_executions')
# @Log(title='执行器执行记录', business_type=BusinessType.UPDATE)
async def edit_api_workflow_executions_workflow_executions(
    request: Request,
    edit_workflow_executions: Workflow_executionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_workflow_executions.model_dump())
    edit_workflow_executions.update_by = current_user.user.user_name
    edit_workflow_executions.update_time = datetime.now()
    edit_workflow_executions_result = await Workflow_executionsService.edit_workflow_executions_services(query_db, edit_workflow_executions)
    logger.info(edit_workflow_executions_result.message)

    return ResponseUtil.success(msg=edit_workflow_executions_result.message)


@workflow_executionsController.delete('/{workflow_execution_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_workflow_executions:workflow_executions:remove'))])
# @Log(title='执行器执行记录', business_type=BusinessType.DELETE)
async def delete_api_workflow_executions_workflow_executions(request: Request, workflow_execution_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_workflow_executions = DeleteWorkflow_executionsModel(workflowExecutionIds=workflow_execution_ids)
    logger.info(delete_workflow_executions.model_dump())
    delete_workflow_executions_result = await Workflow_executionsService.delete_workflow_executions_services(query_db, delete_workflow_executions)
    logger.info(delete_workflow_executions_result.message)

    return ResponseUtil.success(msg=delete_workflow_executions_result.message)


@workflow_executionsController.get(
    '/{workflow_execution_id}', response_model=Workflow_executionsModel, dependencies=[Depends(CheckUserInterfaceAuth('api_workflow_executions:workflow_executions:query'))]
)
async def query_detail_api_workflow_executions_workflow_executions(request: Request, workflow_execution_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    workflow_executions_detail_result = await Workflow_executionsService.workflow_executions_detail_services(query_db, workflow_execution_id)
    logger.info(f'获取workflow_execution_id为{workflow_execution_id}的信息成功')

    return ResponseUtil.success(data=workflow_executions_detail_result)


@workflow_executionsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_workflow_executions:workflow_executions:export'))])
# @Log(title='执行器执行记录', business_type=BusinessType.EXPORT)
async def export_api_workflow_executions_workflow_executions_list(
    request: Request,
    workflow_executions_page_query: Workflow_executionsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    workflow_executions_query_result = await Workflow_executionsService.get_workflow_executions_list_services(query_db, workflow_executions_page_query, is_page=False)
    workflow_executions_export_result = await Workflow_executionsService.export_workflow_executions_list_services(workflow_executions_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(workflow_executions_export_result))
