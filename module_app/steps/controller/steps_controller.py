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
from module_app.steps.service.steps_service import StepsService
from module_app.steps.entity.vo.steps_vo import DeleteStepsModel, StepsModel, StepsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


stepsController = APIRouter(prefix='/app/steps', dependencies=[Depends(LoginService.get_current_user)])


@stepsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps:list'))],
    summary='获取测试步骤列表',
    description='根据查询条件获取测试步骤分页列表数据',
)
async def get_app_steps_list(
    request: Request,
steps_page_query: StepsPageQueryModel = Depends(StepsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(steps_page_query.model_dump())
    # 获取分页数据
    steps_page_query_result = await StepsService.get_steps_list_services(query_db, steps_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=steps_page_query_result)


@stepsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps:add'))],
    summary='新增测试步骤',
    description='创建一条新的测试步骤记录',
)
@ValidateFields(validate_model='add_steps')
# @Log(title='测试步骤', business_type=BusinessType.INSERT)
async def add_app_steps(
    request: Request,
    add_steps: StepsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_steps.create_by = current_user.user.user_name
    add_steps.create_time = datetime.now()
    add_steps.update_by = current_user.user.user_name
    add_steps.update_time = datetime.now()
    logger.info(add_steps.model_dump())
    add_steps_result = await StepsService.add_steps_services(query_db, add_steps)
    logger.info(add_steps_result.message)

    return ResponseUtil.success(msg=add_steps_result.message)


@stepsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps:edit'))],
    summary='修改测试步骤',
    description='根据主键更新测试步骤信息',
)
@ValidateFields(validate_model='edit_steps')
# @Log(title='测试步骤', business_type=BusinessType.UPDATE)
async def edit_app_steps(
    request: Request,
    edit_steps: StepsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_steps.model_dump())
    edit_steps.update_by = current_user.user.user_name
    edit_steps.update_time = datetime.now()
    edit_steps_result = await StepsService.edit_steps_services(query_db, edit_steps)
    logger.info(edit_steps_result.message)

    return ResponseUtil.success(msg=edit_steps_result.message)


@stepsController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps:remove'))],
    summary='删除测试步骤',
    description='根据主键批量删除测试步骤记录，多个主键以逗号分隔',
)
# @Log(title='测试步骤', business_type=BusinessType.DELETE)
async def delete_app_steps(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_steps = DeleteStepsModel(ids=ids)
    logger.info(delete_steps.model_dump())
    delete_steps_result = await StepsService.delete_steps_services(query_db, delete_steps)
    logger.info(delete_steps_result.message)

    return ResponseUtil.success(msg=delete_steps_result.message)


@stepsController.get(
    '/{id}',
    response_model=StepsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps:query'))],
    summary='获取测试步骤详情',
    description='根据主键获取测试步骤详细信息',
)
async def query_detail_app_steps(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    steps_detail_result = await StepsService.steps_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=steps_detail_result)


@stepsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:steps:export'))],
    summary='导出测试步骤',
    description='根据查询条件导出测试步骤列表数据到Excel文件',
)
# @Log(title='测试步骤', business_type=BusinessType.EXPORT)
async def export_app_steps_list(
    request: Request,
    steps_page_query: StepsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    steps_query_result = await StepsService.get_steps_list_services(query_db, steps_page_query, is_page=False)
    steps_export_result = await StepsService.export_steps_list_services(steps_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(steps_export_result))
