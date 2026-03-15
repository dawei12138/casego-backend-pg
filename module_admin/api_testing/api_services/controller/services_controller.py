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
from module_admin.api_testing.api_services.service.services_service import ServicesService
from module_admin.api_testing.api_services.entity.vo.services_vo import DeleteServicesModel, ServicesModel, ServicesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

servicesController = APIRouter(prefix='/api_services/services', dependencies=[Depends(LoginService.get_current_user)])


@servicesController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_services:services:list'))]
)
async def get_api_services_services_list(
        request: Request,
        services_page_query: ServicesPageQueryModel = Depends(ServicesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(services_page_query.model_dump())
    # 获取分页数据
    services_page_query_result = await ServicesService.get_services_list_services(query_db, services_page_query,
                                                                                  is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=services_page_query_result)


@servicesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_services:services:add'))])
@ValidateFields(validate_model='add_services')
# @Log(title='环境服务地址', business_type=BusinessType.INSERT)
async def add_api_services_services(
        request: Request,
        add_services: ServicesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_services.create_by = current_user.user.user_name
    add_services.create_time = datetime.now()
    add_services.update_by = current_user.user.user_name
    add_services.update_time = datetime.now()
    logger.info(add_services.model_dump())
    add_services_result = await ServicesService.add_services_services(query_db, add_services)
    logger.info(add_services_result.message)

    return ResponseUtil.success(msg=add_services_result.message)


@servicesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_services:services:edit'))])
@ValidateFields(validate_model='edit_services')
@Log(title='环境服务地址', business_type=BusinessType.UPDATE)
async def edit_api_services_services(
        request: Request,
        edit_services: ServicesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_services.model_dump())
    edit_services.update_by = current_user.user.user_name
    edit_services.update_time = datetime.now()

    edit_services_result = await ServicesService.edit_services_services(query_db, edit_services)
    logger.info(edit_services_result.message)

    return ResponseUtil.success(msg=edit_services_result.message)


@servicesController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_services:services:remove'))])
@Log(title='环境服务地址', business_type=BusinessType.DELETE)
async def delete_api_services_services(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_services = DeleteServicesModel(ids=ids)
    logger.info(delete_services.model_dump())
    delete_services_result = await ServicesService.delete_services_services(query_db, delete_services)
    logger.info(delete_services_result.message)

    return ResponseUtil.success(msg=delete_services_result.message)


@servicesController.get(
    '/{id}', response_model=ServicesModel, dependencies=[Depends(CheckUserInterfaceAuth('api_services:services:query'))]
)
async def query_detail_api_services_services(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    services_detail_result = await ServicesService.services_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=services_detail_result)


@servicesController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_services:services:export'))])
@Log(title='环境服务地址', business_type=BusinessType.EXPORT)
async def export_api_services_services_list(
        request: Request,
        services_page_query: ServicesPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    services_query_result = await ServicesService.get_services_list_services(query_db, services_page_query,
                                                                             is_page=False)
    services_export_result = await ServicesService.export_services_list_services(request, services_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(services_export_result))
