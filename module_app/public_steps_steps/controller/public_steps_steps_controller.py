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
from module_app.public_steps_steps.service.public_steps_steps_service import Public_steps_stepsService
from module_app.public_steps_steps.entity.vo.public_steps_steps_vo import DeletePublic_steps_stepsModel, Public_steps_stepsModel, Public_steps_stepsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


public_steps_stepsController = APIRouter(prefix='/app/public_steps_steps', dependencies=[Depends(LoginService.get_current_user)])


@public_steps_stepsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:public_steps_steps:list'))],
    summary='获取公共步骤-步骤关联列表',
    description='根据查询条件获取公共步骤-步骤关联分页列表数据',
)
async def get_app_public_steps_steps_list(
    request: Request,
public_steps_steps_page_query: Public_steps_stepsPageQueryModel = Depends(Public_steps_stepsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(public_steps_steps_page_query.model_dump())
    # 获取分页数据
    public_steps_steps_page_query_result = await Public_steps_stepsService.get_public_steps_steps_list_services(query_db, public_steps_steps_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=public_steps_steps_page_query_result)


@public_steps_stepsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:public_steps_steps:add'))],
    summary='新增公共步骤-步骤关联',
    description='创建一条新的公共步骤-步骤关联记录',
)
@ValidateFields(validate_model='add_public_steps_steps')
# @Log(title='公共步骤-步骤关联', business_type=BusinessType.INSERT)
async def add_app_public_steps_steps(
    request: Request,
    add_public_steps_steps: Public_steps_stepsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_public_steps_steps.create_by = current_user.user.user_name
    add_public_steps_steps.create_time = datetime.now()
    add_public_steps_steps.update_by = current_user.user.user_name
    add_public_steps_steps.update_time = datetime.now()
    logger.info(add_public_steps_steps.model_dump())
    add_public_steps_steps_result = await Public_steps_stepsService.add_public_steps_steps_services(query_db, add_public_steps_steps)
    logger.info(add_public_steps_steps_result.message)

    return ResponseUtil.success(msg=add_public_steps_steps_result.message)


@public_steps_stepsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:public_steps_steps:edit'))],
    summary='修改公共步骤-步骤关联',
    description='根据主键更新公共步骤-步骤关联信息',
)
@ValidateFields(validate_model='edit_public_steps_steps')
# @Log(title='公共步骤-步骤关联', business_type=BusinessType.UPDATE)
async def edit_app_public_steps_steps(
    request: Request,
    edit_public_steps_steps: Public_steps_stepsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_public_steps_steps.model_dump())
    edit_public_steps_steps.update_by = current_user.user.user_name
    edit_public_steps_steps.update_time = datetime.now()
    edit_public_steps_steps_result = await Public_steps_stepsService.edit_public_steps_steps_services(query_db, edit_public_steps_steps)
    logger.info(edit_public_steps_steps_result.message)

    return ResponseUtil.success(msg=edit_public_steps_steps_result.message)


@public_steps_stepsController.delete(
    '/{public_steps_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:public_steps_steps:remove'))],
    summary='删除公共步骤-步骤关联',
    description='根据主键批量删除公共步骤-步骤关联记录，多个主键以逗号分隔',
)
# @Log(title='公共步骤-步骤关联', business_type=BusinessType.DELETE)
async def delete_app_public_steps_steps(request: Request, public_steps_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_public_steps_steps = DeletePublic_steps_stepsModel(publicStepsIds=public_steps_ids)
    logger.info(delete_public_steps_steps.model_dump())
    delete_public_steps_steps_result = await Public_steps_stepsService.delete_public_steps_steps_services(query_db, delete_public_steps_steps)
    logger.info(delete_public_steps_steps_result.message)

    return ResponseUtil.success(msg=delete_public_steps_steps_result.message)


@public_steps_stepsController.get(
    '/{public_steps_id}',
    response_model=Public_steps_stepsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:public_steps_steps:query'))],
    summary='获取公共步骤-步骤关联详情',
    description='根据主键获取公共步骤-步骤关联详细信息',
)
async def query_detail_app_public_steps_steps(request: Request, public_steps_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    public_steps_steps_detail_result = await Public_steps_stepsService.public_steps_steps_detail_services(query_db, public_steps_id)
    logger.info(f'获取public_steps_id为{public_steps_id}的信息成功')

    return ResponseUtil.success(data=public_steps_steps_detail_result)


@public_steps_stepsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:public_steps_steps:export'))],
    summary='导出公共步骤-步骤关联',
    description='根据查询条件导出公共步骤-步骤关联列表数据到Excel文件',
)
# @Log(title='公共步骤-步骤关联', business_type=BusinessType.EXPORT)
async def export_app_public_steps_steps_list(
    request: Request,
    public_steps_steps_page_query: Public_steps_stepsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    public_steps_steps_query_result = await Public_steps_stepsService.get_public_steps_steps_list_services(query_db, public_steps_steps_page_query, is_page=False)
    public_steps_steps_export_result = await Public_steps_stepsService.export_public_steps_steps_list_services(public_steps_steps_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(public_steps_steps_export_result))
