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
from module_admin.api_testing.api_setup.service.setup_service import SetupService
from module_admin.api_testing.api_setup.entity.vo.setup_vo import DeleteSetupModel, SetupModel, SetupPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

setupController = APIRouter(prefix='/api_setup/setup', dependencies=[Depends(LoginService.get_current_user)])


@setupController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_setup:setup:list'))]
)
async def get_api_setup_setup_list(
        request: Request,
        setup_page_query: SetupPageQueryModel = Depends(SetupPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(setup_page_query.model_dump())
    # 获取分页数据
    setup_page_query_result = await SetupService.get_setup_list_services(query_db, setup_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=setup_page_query_result)


@setupController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_setup:setup:add'))])
@ValidateFields(validate_model='add_setup')
# @Log(title='接口前置操作', business_type=BusinessType.INSERT)
async def add_api_setup_setup(
        request: Request,
        add_setup: SetupModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_setup.create_by = current_user.user.user_name
    add_setup.create_time = datetime.now()
    add_setup.update_by = current_user.user.user_name
    add_setup.update_time = datetime.now()
    logger.info(add_setup.model_dump())
    add_setup_result = await SetupService.add_setup_services(query_db, add_setup)
    logger.info(add_setup_result.message)

    return ResponseUtil.success(msg=add_setup_result.message)


@setupController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_setup:setup:edit'))])
@ValidateFields(validate_model='edit_setup')
@Log(title='接口前置操作', business_type=BusinessType.UPDATE)
async def edit_api_setup_setup(
        request: Request,
        edit_setup: SetupModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_setup.model_dump())
    edit_setup.update_by = current_user.user.user_name
    edit_setup.update_time = datetime.now()
    edit_setup_result = await SetupService.edit_setup_services(query_db, edit_setup)
    logger.info(edit_setup_result.message)

    return ResponseUtil.success(msg=edit_setup_result.message)


@setupController.delete('/{setup_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_setup:setup:remove'))])
@Log(title='接口前置操作', business_type=BusinessType.DELETE)
async def delete_api_setup_setup(request: Request, setup_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_setup = DeleteSetupModel(setupIds=setup_ids)
    logger.info(delete_setup.model_dump())
    delete_setup_result = await SetupService.delete_setup_services(query_db, delete_setup)
    logger.info(delete_setup_result.message)

    return ResponseUtil.success(msg=delete_setup_result.message)


@setupController.get(
    '/{setup_id}', response_model=SetupModel, dependencies=[Depends(CheckUserInterfaceAuth('api_setup:setup:query'))]
)
async def query_detail_api_setup_setup(request: Request, setup_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    setup_detail_result = await SetupService.setup_detail_services(query_db, setup_id)
    logger.info(f'获取setup_id为{setup_id}的信息成功')

    return ResponseUtil.success(data=setup_detail_result)


@setupController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_setup:setup:export'))])
@Log(title='接口前置操作', business_type=BusinessType.EXPORT)
async def export_api_setup_setup_list(
        request: Request,
        setup_page_query: SetupPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    setup_query_result = await SetupService.get_setup_list_services(query_db, setup_page_query, is_page=False)
    setup_export_result = await SetupService.export_setup_list_services(setup_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(setup_export_result))
