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
from module_app.steps_elements.service.steps_elements_service import Steps_elementsService
from module_app.steps_elements.entity.vo.steps_elements_vo import DeleteSteps_elementsModel, Steps_elementsModel, Steps_elementsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


steps_elementsController = APIRouter(prefix='/app/steps_elements', dependencies=[Depends(LoginService.get_current_user)])


@steps_elementsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps_elements:list'))],
    summary='获取步骤-元素关联列表',
    description='根据查询条件获取步骤-元素关联分页列表数据',
)
async def get_app_steps_elements_list(
    request: Request,
steps_elements_page_query: Steps_elementsPageQueryModel = Depends(Steps_elementsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(steps_elements_page_query.model_dump())
    # 获取分页数据
    steps_elements_page_query_result = await Steps_elementsService.get_steps_elements_list_services(query_db, steps_elements_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=steps_elements_page_query_result)


@steps_elementsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps_elements:add'))],
    summary='新增步骤-元素关联',
    description='创建一条新的步骤-元素关联记录',
)
@ValidateFields(validate_model='add_steps_elements')
# @Log(title='步骤-元素关联', business_type=BusinessType.INSERT)
async def add_app_steps_elements(
    request: Request,
    add_steps_elements: Steps_elementsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_steps_elements.create_by = current_user.user.user_name
    add_steps_elements.create_time = datetime.now()
    add_steps_elements.update_by = current_user.user.user_name
    add_steps_elements.update_time = datetime.now()
    logger.info(add_steps_elements.model_dump())
    add_steps_elements_result = await Steps_elementsService.add_steps_elements_services(query_db, add_steps_elements)
    logger.info(add_steps_elements_result.message)

    return ResponseUtil.success(msg=add_steps_elements_result.message)


@steps_elementsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps_elements:edit'))],
    summary='修改步骤-元素关联',
    description='根据主键更新步骤-元素关联信息',
)
@ValidateFields(validate_model='edit_steps_elements')
# @Log(title='步骤-元素关联', business_type=BusinessType.UPDATE)
async def edit_app_steps_elements(
    request: Request,
    edit_steps_elements: Steps_elementsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_steps_elements.model_dump())
    edit_steps_elements.update_by = current_user.user.user_name
    edit_steps_elements.update_time = datetime.now()
    edit_steps_elements_result = await Steps_elementsService.edit_steps_elements_services(query_db, edit_steps_elements)
    logger.info(edit_steps_elements_result.message)

    return ResponseUtil.success(msg=edit_steps_elements_result.message)


@steps_elementsController.delete(
    '/{steps_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps_elements:remove'))],
    summary='删除步骤-元素关联',
    description='根据主键批量删除步骤-元素关联记录，多个主键以逗号分隔',
)
# @Log(title='步骤-元素关联', business_type=BusinessType.DELETE)
async def delete_app_steps_elements(request: Request, steps_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_steps_elements = DeleteSteps_elementsModel(stepsIds=steps_ids)
    logger.info(delete_steps_elements.model_dump())
    delete_steps_elements_result = await Steps_elementsService.delete_steps_elements_services(query_db, delete_steps_elements)
    logger.info(delete_steps_elements_result.message)

    return ResponseUtil.success(msg=delete_steps_elements_result.message)


@steps_elementsController.get(
    '/{steps_id}',
    response_model=Steps_elementsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps_elements:query'))],
    summary='获取步骤-元素关联详情',
    description='根据主键获取步骤-元素关联详细信息',
)
async def query_detail_app_steps_elements(request: Request, steps_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    steps_elements_detail_result = await Steps_elementsService.steps_elements_detail_services(query_db, steps_id)
    logger.info(f'获取steps_id为{steps_id}的信息成功')

    return ResponseUtil.success(data=steps_elements_detail_result)


@steps_elementsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps_elements:export'))],
    summary='导出步骤-元素关联',
    description='根据查询条件导出步骤-元素关联列表数据到Excel文件',
)
# @Log(title='步骤-元素关联', business_type=BusinessType.EXPORT)
async def export_app_steps_elements_list(
    request: Request,
    steps_elements_page_query: Steps_elementsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    steps_elements_query_result = await Steps_elementsService.get_steps_elements_list_services(query_db, steps_elements_page_query, is_page=False)
    steps_elements_export_result = await Steps_elementsService.export_steps_elements_list_services(steps_elements_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(steps_elements_export_result))
