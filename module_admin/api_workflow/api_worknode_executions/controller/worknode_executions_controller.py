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
from module_admin.api_workflow.api_worknode_executions.service.worknode_executions_service import Worknode_executionsService
from module_admin.api_workflow.api_worknode_executions.entity.vo.worknode_executions_vo import DeleteWorknode_executionsModel, Worknode_executionsModel, Worknode_executionsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


worknode_executionsController = APIRouter(prefix='/api_worknode_executions/worknode_executions', dependencies=[Depends(LoginService.get_current_user)])


@worknode_executionsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_worknode_executions:worknode_executions:list'))]
)
async def get_api_worknode_executions_worknode_executions_list(
    request: Request,
worknode_executions_page_query: Worknode_executionsPageQueryModel = Depends(Worknode_executionsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(worknode_executions_page_query.model_dump())
    # 获取分页数据
    worknode_executions_page_query_result = await Worknode_executionsService.get_worknode_executions_list_services(query_db, worknode_executions_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=worknode_executions_page_query_result)


@worknode_executionsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_worknode_executions:worknode_executions:add'))])
@ValidateFields(validate_model='add_worknode_executions')
# @Log(title='节点执行记录', business_type=BusinessType.INSERT)
async def add_api_worknode_executions_worknode_executions(
    request: Request,
    add_worknode_executions: Worknode_executionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_worknode_executions.create_by = current_user.user.user_name
    add_worknode_executions.create_time = datetime.now()
    add_worknode_executions.update_by = current_user.user.user_name
    add_worknode_executions.update_time = datetime.now()
    logger.info(add_worknode_executions.model_dump())
    add_worknode_executions_result = await Worknode_executionsService.add_worknode_executions_services(query_db, add_worknode_executions)
    logger.info(add_worknode_executions_result.message)

    return ResponseUtil.success(msg=add_worknode_executions_result.message)


@worknode_executionsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_worknode_executions:worknode_executions:edit'))])
@ValidateFields(validate_model='edit_worknode_executions')
# @Log(title='节点执行记录', business_type=BusinessType.UPDATE)
async def edit_api_worknode_executions_worknode_executions(
    request: Request,
    edit_worknode_executions: Worknode_executionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_worknode_executions.model_dump())
    edit_worknode_executions.update_by = current_user.user.user_name
    edit_worknode_executions.update_time = datetime.now()
    edit_worknode_executions_result = await Worknode_executionsService.edit_worknode_executions_services(query_db, edit_worknode_executions)
    logger.info(edit_worknode_executions_result.message)

    return ResponseUtil.success(msg=edit_worknode_executions_result.message)


@worknode_executionsController.delete('/{node_execution_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_worknode_executions:worknode_executions:remove'))])
# @Log(title='节点执行记录', business_type=BusinessType.DELETE)
async def delete_api_worknode_executions_worknode_executions(request: Request, node_execution_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_worknode_executions = DeleteWorknode_executionsModel(nodeExecutionIds=node_execution_ids)
    logger.info(delete_worknode_executions.model_dump())
    delete_worknode_executions_result = await Worknode_executionsService.delete_worknode_executions_services(query_db, delete_worknode_executions)
    logger.info(delete_worknode_executions_result.message)

    return ResponseUtil.success(msg=delete_worknode_executions_result.message)


@worknode_executionsController.get(
    '/{node_execution_id}', response_model=Worknode_executionsModel, dependencies=[Depends(CheckUserInterfaceAuth('api_worknode_executions:worknode_executions:query'))]
)
async def query_detail_api_worknode_executions_worknode_executions(request: Request, node_execution_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    worknode_executions_detail_result = await Worknode_executionsService.worknode_executions_detail_services(query_db, node_execution_id)
    logger.info(f'获取node_execution_id为{node_execution_id}的信息成功')

    return ResponseUtil.success(data=worknode_executions_detail_result)


@worknode_executionsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_worknode_executions:worknode_executions:export'))])
# @Log(title='节点执行记录', business_type=BusinessType.EXPORT)
async def export_api_worknode_executions_worknode_executions_list(
    request: Request,
    worknode_executions_page_query: Worknode_executionsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    worknode_executions_query_result = await Worknode_executionsService.get_worknode_executions_list_services(query_db, worknode_executions_page_query, is_page=False)
    worknode_executions_export_result = await Worknode_executionsService.export_worknode_executions_list_services(worknode_executions_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(worknode_executions_export_result))
