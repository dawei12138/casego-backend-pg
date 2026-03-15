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
from module_admin.api_testing.api_assertions.service.assertions_service import AssertionsService
from module_admin.api_testing.api_assertions.entity.vo.assertions_vo import DeleteAssertionsModel, AssertionsModel, AssertionsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


assertionsController = APIRouter(prefix='/api_assertions/assertions', dependencies=[Depends(LoginService.get_current_user)])


@assertionsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_assertions:assertions:list'))]
)
async def get_api_assertions_assertions_list(
    request: Request,
assertions_page_query: AssertionsPageQueryModel = Depends(AssertionsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(assertions_page_query.model_dump())
    # 获取分页数据
    assertions_page_query_result = await AssertionsService.get_assertions_list_services(query_db, assertions_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=assertions_page_query_result)


@assertionsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_assertions:assertions:add'))])
@ValidateFields(validate_model='add_assertions')
# @Log(title='接口断言', business_type=BusinessType.INSERT)
async def add_api_assertions_assertions(
    request: Request,
    add_assertions: AssertionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_assertions.create_by = current_user.user.user_name
    add_assertions.create_time = datetime.now()
    add_assertions.update_by = current_user.user.user_name
    add_assertions.update_time = datetime.now()
    logger.info(add_assertions.model_dump())
    add_assertions_result = await AssertionsService.add_assertions_services(query_db, add_assertions)
    logger.info(add_assertions_result.message)

    return ResponseUtil.success(msg=add_assertions_result.message)


@assertionsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_assertions:assertions:edit'))])
@ValidateFields(validate_model='edit_assertions')
@Log(title='接口断言', business_type=BusinessType.UPDATE)
async def edit_api_assertions_assertions(
    request: Request,
    edit_assertions: AssertionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_assertions.model_dump())
    edit_assertions.update_by = current_user.user.user_name
    edit_assertions.update_time = datetime.now()
    edit_assertions_result = await AssertionsService.edit_assertions_services(query_db, edit_assertions)
    logger.info(edit_assertions_result.message)

    return ResponseUtil.success(msg=edit_assertions_result.message)


@assertionsController.delete('/{assertion_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_assertions:assertions:remove'))])
@Log(title='接口断言', business_type=BusinessType.DELETE)
async def delete_api_assertions_assertions(request: Request, assertion_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_assertions = DeleteAssertionsModel(assertionIds=assertion_ids)
    logger.info(delete_assertions.model_dump())
    delete_assertions_result = await AssertionsService.delete_assertions_services(query_db, delete_assertions)
    logger.info(delete_assertions_result.message)

    return ResponseUtil.success(msg=delete_assertions_result.message)


@assertionsController.get(
    '/{assertion_id}', response_model=AssertionsModel, dependencies=[Depends(CheckUserInterfaceAuth('api_assertions:assertions:query'))]
)
async def query_detail_api_assertions_assertions(request: Request, assertion_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    assertions_detail_result = await AssertionsService.assertions_detail_services(query_db, assertion_id)
    logger.info(f'获取assertion_id为{assertion_id}的信息成功')

    return ResponseUtil.success(data=assertions_detail_result)


@assertionsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_assertions:assertions:export'))])
@Log(title='接口断言', business_type=BusinessType.EXPORT)
async def export_api_assertions_assertions_list(
    request: Request,
    assertions_page_query: AssertionsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    assertions_query_result = await AssertionsService.get_assertions_list_services(query_db, assertions_page_query, is_page=False)
    assertions_export_result = await AssertionsService.export_assertions_list_services(assertions_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(assertions_export_result))
