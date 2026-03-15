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
from module_admin.api_testing.api_teardown.service.teardown_service import TeardownService
from module_admin.api_testing.api_teardown.entity.vo.teardown_vo import DeleteTeardownModel, TeardownModel, TeardownPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


teardownController = APIRouter(prefix='/api_teardown/teardown', dependencies=[Depends(LoginService.get_current_user)])


@teardownController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_teardown:teardown:list'))]
)
async def get_api_teardown_teardown_list(
    request: Request,
    teardown_page_query: TeardownPageQueryModel = Depends(TeardownPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(teardown_page_query.model_dump())
    # 获取分页数据
    teardown_page_query_result = await TeardownService.get_teardown_list_services(query_db, teardown_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=teardown_page_query_result)


@teardownController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_teardown:teardown:add'))])
@ValidateFields(validate_model='add_teardown')
# @Log(title='接口后置操作', business_type=BusinessType.INSERT)
async def add_api_teardown_teardown(
    request: Request,
    add_teardown: TeardownModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_teardown.create_by = current_user.user.user_name
    add_teardown.create_time = datetime.now()
    add_teardown.update_by = current_user.user.user_name
    add_teardown.update_time = datetime.now()
    logger.info(add_teardown.model_dump())
    add_teardown_result = await TeardownService.add_teardown_services(query_db, add_teardown)
    logger.info(add_teardown_result.message)

    return ResponseUtil.success(msg=add_teardown_result.message)


@teardownController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_teardown:teardown:edit'))])
@ValidateFields(validate_model='edit_teardown')
@Log(title='接口后置操作', business_type=BusinessType.UPDATE)
async def edit_api_teardown_teardown(
    request: Request,
    edit_teardown: TeardownModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_teardown.model_dump())
    edit_teardown.update_by = current_user.user.user_name
    edit_teardown.update_time = datetime.now()
    edit_teardown_result = await TeardownService.edit_teardown_services(query_db, edit_teardown)
    logger.info(edit_teardown_result.message)

    return ResponseUtil.success(msg=edit_teardown_result.message)


@teardownController.delete('/{teardown_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_teardown:teardown:remove'))])
@Log(title='接口后置操作', business_type=BusinessType.DELETE)
async def delete_api_teardown_teardown(request: Request, teardown_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_teardown = DeleteTeardownModel(teardownIds=teardown_ids)
    logger.info(delete_teardown.model_dump())
    delete_teardown_result = await TeardownService.delete_teardown_services(query_db, delete_teardown)
    logger.info(delete_teardown_result.message)

    return ResponseUtil.success(msg=delete_teardown_result.message)


@teardownController.get(
    '/{teardown_id}', response_model=TeardownModel, dependencies=[Depends(CheckUserInterfaceAuth('api_teardown:teardown:query'))]
)
async def query_detail_api_teardown_teardown(request: Request, teardown_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    teardown_detail_result = await TeardownService.teardown_detail_services(query_db, teardown_id)
    logger.info(f'获取teardown_id为{teardown_id}的信息成功')

    return ResponseUtil.success(data=teardown_detail_result)


@teardownController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_teardown:teardown:export'))])
@Log(title='接口后置操作', business_type=BusinessType.EXPORT)
async def export_api_teardown_teardown_list(
    request: Request,
    teardown_page_query: TeardownPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    teardown_query_result = await TeardownService.get_teardown_list_services(query_db, teardown_page_query, is_page=False)
    teardown_export_result = await TeardownService.export_teardown_list_services(teardown_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(teardown_export_result))
