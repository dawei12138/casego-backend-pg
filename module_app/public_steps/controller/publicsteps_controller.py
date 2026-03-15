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
from module_app.public_steps.service.publicsteps_service import PublicstepsService
from module_app.public_steps.entity.vo.publicsteps_vo import DeletePublicstepsModel, PublicstepsModel, PublicstepsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


publicstepsController = APIRouter(prefix='/app/publicsteps', dependencies=[Depends(LoginService.get_current_user)])


@publicstepsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:publicsteps:list'))],
    summary='获取公共步骤列表',
    description='根据查询条件获取公共步骤分页列表数据',
)
async def get_app_publicsteps_list(
    request: Request,
publicsteps_page_query: PublicstepsPageQueryModel = Depends(PublicstepsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(publicsteps_page_query.model_dump())
    # 获取分页数据
    publicsteps_page_query_result = await PublicstepsService.get_publicsteps_list_services(query_db, publicsteps_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=publicsteps_page_query_result)


@publicstepsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:publicsteps:add'))],
    summary='新增公共步骤',
    description='创建一条新的公共步骤记录',
)
@ValidateFields(validate_model='add_publicsteps')
# @Log(title='公共步骤', business_type=BusinessType.INSERT)
async def add_app_publicsteps(
    request: Request,
    add_publicsteps: PublicstepsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_publicsteps.create_by = current_user.user.user_name
    add_publicsteps.create_time = datetime.now()
    add_publicsteps.update_by = current_user.user.user_name
    add_publicsteps.update_time = datetime.now()
    logger.info(add_publicsteps.model_dump())
    add_publicsteps_result = await PublicstepsService.add_publicsteps_services(query_db, add_publicsteps)
    logger.info(add_publicsteps_result.message)

    return ResponseUtil.success(msg=add_publicsteps_result.message)


@publicstepsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:publicsteps:edit'))],
    summary='修改公共步骤',
    description='根据主键更新公共步骤信息',
)
@ValidateFields(validate_model='edit_publicsteps')
# @Log(title='公共步骤', business_type=BusinessType.UPDATE)
async def edit_app_publicsteps(
    request: Request,
    edit_publicsteps: PublicstepsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_publicsteps.model_dump())
    edit_publicsteps.update_by = current_user.user.user_name
    edit_publicsteps.update_time = datetime.now()
    edit_publicsteps_result = await PublicstepsService.edit_publicsteps_services(query_db, edit_publicsteps)
    logger.info(edit_publicsteps_result.message)

    return ResponseUtil.success(msg=edit_publicsteps_result.message)


@publicstepsController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:publicsteps:remove'))],
    summary='删除公共步骤',
    description='根据主键批量删除公共步骤记录，多个主键以逗号分隔',
)
# @Log(title='公共步骤', business_type=BusinessType.DELETE)
async def delete_app_publicsteps(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_publicsteps = DeletePublicstepsModel(ids=ids)
    logger.info(delete_publicsteps.model_dump())
    delete_publicsteps_result = await PublicstepsService.delete_publicsteps_services(query_db, delete_publicsteps)
    logger.info(delete_publicsteps_result.message)

    return ResponseUtil.success(msg=delete_publicsteps_result.message)


@publicstepsController.get(
    '/{id}',
    response_model=PublicstepsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:publicsteps:query'))],
    summary='获取公共步骤详情',
    description='根据主键获取公共步骤详细信息',
)
async def query_detail_app_publicsteps(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    publicsteps_detail_result = await PublicstepsService.publicsteps_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=publicsteps_detail_result)


@publicstepsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:publicsteps:export'))],
    summary='导出公共步骤',
    description='根据查询条件导出公共步骤列表数据到Excel文件',
)
# @Log(title='公共步骤', business_type=BusinessType.EXPORT)
async def export_app_publicsteps_list(
    request: Request,
    publicsteps_page_query: PublicstepsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    publicsteps_query_result = await PublicstepsService.get_publicsteps_list_services(query_db, publicsteps_page_query, is_page=False)
    publicsteps_export_result = await PublicstepsService.export_publicsteps_list_services(publicsteps_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(publicsteps_export_result))
