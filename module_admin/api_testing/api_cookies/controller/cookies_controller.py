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
from module_admin.api_testing.api_cookies.service.cookies_service import CookiesService
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import DeleteCookiesModel, CookiesModel, CookiesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


cookiesController = APIRouter(prefix='/api_cookies/cookies', dependencies=[Depends(LoginService.get_current_user)])


@cookiesController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_cookies:cookies:list'))]
)
async def get_api_cookies_cookies_list(
    request: Request,
cookies_page_query: CookiesPageQueryModel = Depends(CookiesPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(cookies_page_query.model_dump())
    # 获取分页数据
    cookies_page_query_result = await CookiesService.get_cookies_list_services(query_db, cookies_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=cookies_page_query_result)


@cookiesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_cookies:cookies:add'))])
@ValidateFields(validate_model='add_cookies')
# @Log(title='接口请求Cookie', business_type=BusinessType.INSERT)
async def add_api_cookies_cookies(
    request: Request,
    add_cookies: CookiesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_cookies.create_by = current_user.user.user_name
    add_cookies.create_time = datetime.now()
    add_cookies.update_by = current_user.user.user_name
    add_cookies.update_time = datetime.now()
    logger.info(add_cookies.model_dump())
    add_cookies_result = await CookiesService.add_cookies_services(query_db, add_cookies)
    logger.info(add_cookies_result.message)

    return ResponseUtil.success(msg=add_cookies_result.message)


@cookiesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_cookies:cookies:edit'))])
@ValidateFields(validate_model='edit_cookies')
@Log(title='接口请求Cookie', business_type=BusinessType.UPDATE)
async def edit_api_cookies_cookies(
    request: Request,
    edit_cookies: CookiesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_cookies.model_dump())
    edit_cookies.update_by = current_user.user.user_name
    edit_cookies.update_time = datetime.now()
    edit_cookies_result = await CookiesService.edit_cookies_services(query_db, edit_cookies)
    logger.info(edit_cookies_result.message)

    return ResponseUtil.success(msg=edit_cookies_result.message)


@cookiesController.delete('/{cookie_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_cookies:cookies:remove'))])
@Log(title='接口请求Cookie', business_type=BusinessType.DELETE)
async def delete_api_cookies_cookies(request: Request, cookie_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_cookies = DeleteCookiesModel(cookieIds=cookie_ids)
    logger.info(delete_cookies.model_dump())
    delete_cookies_result = await CookiesService.delete_cookies_services(query_db, delete_cookies)
    logger.info(delete_cookies_result.message)

    return ResponseUtil.success(msg=delete_cookies_result.message)


@cookiesController.get(
    '/{cookie_id}', response_model=CookiesModel, dependencies=[Depends(CheckUserInterfaceAuth('api_cookies:cookies:query'))]
)
async def query_detail_api_cookies_cookies(request: Request, cookie_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    cookies_detail_result = await CookiesService.cookies_detail_services(query_db, cookie_id)
    logger.info(f'获取cookie_id为{cookie_id}的信息成功')

    return ResponseUtil.success(data=cookies_detail_result)


@cookiesController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_cookies:cookies:export'))])
@Log(title='接口请求Cookie', business_type=BusinessType.EXPORT)
async def export_api_cookies_cookies_list(
    request: Request,
    cookies_page_query: CookiesPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    cookies_query_result = await CookiesService.get_cookies_list_services(query_db, cookies_page_query, is_page=False)
    cookies_export_result = await CookiesService.export_cookies_list_services(cookies_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(cookies_export_result))
