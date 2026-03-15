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
from module_admin.api_testing.api_test_execution_log.service.execution_log_service import Execution_logService
from module_admin.api_testing.api_test_execution_log.entity.vo.execution_log_vo import DeleteExecution_logModel, \
    Execution_logModel, Execution_logPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

execution_logController = APIRouter(prefix='/api_test_execution_log/execution_log',
                                    dependencies=[Depends(LoginService.get_current_user)])


@execution_logController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_execution_log:execution_log:list'))]
)
async def get_api_test_execution_log_execution_log_list(
        request: Request,
        execution_log_page_query: Execution_logPageQueryModel = Depends(Execution_logPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(execution_log_page_query.model_dump())
    # 获取分页数据
    execution_log_page_query_result = await Execution_logService.get_execution_log_list_services(query_db,
                                                                                                 execution_log_page_query,
                                                                                                 is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=execution_log_page_query_result)


@execution_logController.post('', dependencies=[
    Depends(CheckUserInterfaceAuth('api_test_execution_log:execution_log:add'))])
@ValidateFields(validate_model='add_execution_log')
# @Log(title='接口测试执行日志', business_type=BusinessType.INSERT)
async def add_api_test_execution_log_execution_log(
        request: Request,
        add_execution_log: Execution_logModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_execution_log.create_by = current_user.user.user_name
    add_execution_log.create_time = datetime.now()
    add_execution_log.update_by = current_user.user.user_name
    add_execution_log.update_time = datetime.now()
    logger.info(add_execution_log.model_dump())
    add_execution_log_result = await Execution_logService.add_execution_log_services(query_db, add_execution_log)
    logger.info(add_execution_log_result.message)

    return ResponseUtil.success(msg=add_execution_log_result.message)


@execution_logController.put('', dependencies=[
    Depends(CheckUserInterfaceAuth('api_test_execution_log:execution_log:edit'))])
@ValidateFields(validate_model='edit_execution_log')
# @Log(title='接口测试执行日志', business_type=BusinessType.UPDATE)
async def edit_api_test_execution_log_execution_log(
        request: Request,
        edit_execution_log: Execution_logModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_execution_log.model_dump())
    edit_execution_log.update_by = current_user.user.user_name
    edit_execution_log.update_time = datetime.now()
    edit_execution_log_result = await Execution_logService.edit_execution_log_services(query_db, edit_execution_log)
    logger.info(edit_execution_log_result.message)

    return ResponseUtil.success(msg=edit_execution_log_result.message)


@execution_logController.delete('/{log_ids}', dependencies=[
    Depends(CheckUserInterfaceAuth('api_test_execution_log:execution_log:remove'))])
# @Log(title='接口测试执行日志', business_type=BusinessType.DELETE)
async def delete_api_test_execution_log_execution_log(request: Request, log_ids: str,
                                                      query_db: AsyncSession = Depends(get_db)):
    delete_execution_log = DeleteExecution_logModel(logIds=log_ids)
    logger.info(delete_execution_log.model_dump())
    delete_execution_log_result = await Execution_logService.delete_execution_log_services(query_db,
                                                                                           delete_execution_log)
    logger.info(delete_execution_log_result.message)

    return ResponseUtil.success(msg=delete_execution_log_result.message)


@execution_logController.get(
    '/{log_id}', response_model=Execution_logModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_execution_log:execution_log:query'))]
)
async def query_detail_api_test_execution_log_execution_log(request: Request, log_id: int,
                                                            query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    execution_log_detail_result = await Execution_logService.execution_log_detail_services(query_db, log_id)
    logger.info(f'获取log_id为{log_id}的信息成功')

    return ResponseUtil.success(data=execution_log_detail_result)


@execution_logController.post('/export', dependencies=[
    Depends(CheckUserInterfaceAuth('api_test_execution_log:execution_log:export'))])
# @Log(title='接口测试执行日志', business_type=BusinessType.EXPORT)
async def export_api_test_execution_log_execution_log_list(
        request: Request,
        execution_log_page_query: Execution_logPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    execution_log_query_result = await Execution_logService.get_execution_log_list_services(query_db,
                                                                                            execution_log_page_query,
                                                                                            is_page=False)
    execution_log_export_result = await Execution_logService.export_execution_log_list_services(
        execution_log_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(execution_log_export_result))
