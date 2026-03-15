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
from module_admin.api_testing.api_headers.service.headers_service import HeadersService
from module_admin.api_testing.api_headers.entity.vo.headers_vo import DeleteHeadersModel, HeadersModel, HeadersPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


headersController = APIRouter(prefix='/api_headers/headers', dependencies=[Depends(LoginService.get_current_user)])


@headersController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_headers:headers:list'))]
)
async def get_api_headers_headers_list(
    request: Request,
headers_page_query: HeadersPageQueryModel = Depends(HeadersPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(headers_page_query.model_dump())
    # 获取分页数据
    headers_page_query_result = await HeadersService.get_headers_list_services(query_db, headers_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=headers_page_query_result)


@headersController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_headers:headers:add'))])
@ValidateFields(validate_model='add_headers')
# @Log(title='接口请求头', business_type=BusinessType.INSERT)
async def add_api_headers_headers(
    request: Request,
    add_headers: HeadersModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_headers.create_by = current_user.user.user_name
    add_headers.create_time = datetime.now()
    add_headers.update_by = current_user.user.user_name
    add_headers.update_time = datetime.now()
    logger.info(add_headers.model_dump())
    add_headers_result = await HeadersService.add_headers_services(query_db, add_headers)
    logger.info(add_headers_result.message)

    return ResponseUtil.success(msg=add_headers_result.message)


@headersController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_headers:headers:edit'))])
@ValidateFields(validate_model='edit_headers')
@Log(title='接口请求头', business_type=BusinessType.UPDATE)
async def edit_api_headers_headers(
    request: Request,
    edit_headers: HeadersModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_headers.model_dump())
    edit_headers.update_by = current_user.user.user_name
    edit_headers.update_time = datetime.now()
    edit_headers_result = await HeadersService.edit_headers_services(query_db, edit_headers)
    logger.info(edit_headers_result.message)

    return ResponseUtil.success(msg=edit_headers_result.message)


@headersController.delete('/{header_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_headers:headers:remove'))])
@Log(title='接口请求头', business_type=BusinessType.DELETE)
async def delete_api_headers_headers(request: Request, header_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_headers = DeleteHeadersModel(headerIds=header_ids)
    logger.info(delete_headers.model_dump())
    delete_headers_result = await HeadersService.delete_headers_services(query_db, delete_headers)
    logger.info(delete_headers_result.message)

    return ResponseUtil.success(msg=delete_headers_result.message)


@headersController.get(
    '/{header_id}', response_model=HeadersModel, dependencies=[Depends(CheckUserInterfaceAuth('api_headers:headers:query'))]
)
async def query_detail_api_headers_headers(request: Request, header_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    headers_detail_result = await HeadersService.headers_detail_services(query_db, header_id)
    logger.info(f'获取header_id为{header_id}的信息成功')

    return ResponseUtil.success(data=headers_detail_result)


@headersController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_headers:headers:export'))])
@Log(title='接口请求头', business_type=BusinessType.EXPORT)
async def export_api_headers_headers_list(
    request: Request,
    headers_page_query: HeadersPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    headers_query_result = await HeadersService.get_headers_list_services(query_db, headers_page_query, is_page=False)
    headers_export_result = await HeadersService.export_headers_list_services(headers_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(headers_export_result))
