from datetime import datetime

from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_admin.api_testing.schema_model_groups.entity.vo.schema_model_groups_vo import (
    DeleteSchema_model_groupsModel,
    Schema_model_groupsModel,
    Schema_model_groupsPageQueryModel,
)
from module_admin.api_testing.schema_model_groups.service.schema_model_groups_service import Schema_model_groupsService
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

schema_model_groupsController = APIRouter(
    prefix='/schema_model/schema_model_groups',
    dependencies=[Depends(LoginService.get_current_user)],
)


@schema_model_groupsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_model_groups:list'))],
    summary='获取JSON Schema 数据模型目录列表',
)
async def get_schema_model_schema_model_groups_list(
    request: Request,
    schema_model_groups_page_query: Schema_model_groupsPageQueryModel = Depends(
        Schema_model_groupsPageQueryModel.as_query
    ),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(schema_model_groups_page_query.model_dump())
    result = await Schema_model_groupsService.get_schema_model_groups_list_services(
        query_db,
        schema_model_groups_page_query,
        is_page=True,
    )
    logger.info('获取成功')
    return ResponseUtil.success(model_content=result)


@schema_model_groupsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_model_groups:add'))],
    summary='新增JSON Schema 数据模型目录',
)
@ValidateFields(validate_model='add_schema_model_groups')
async def add_schema_model_schema_model_groups(
    request: Request,
    add_schema_model_groups: Schema_model_groupsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    now = datetime.now()
    add_schema_model_groups.create_by = current_user.user.user_name
    add_schema_model_groups.create_time = now
    add_schema_model_groups.update_by = current_user.user.user_name
    add_schema_model_groups.update_time = now
    logger.info(add_schema_model_groups.model_dump())
    result = await Schema_model_groupsService.add_schema_model_groups_services(query_db, add_schema_model_groups)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message, data=result.result)


@schema_model_groupsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_model_groups:edit'))],
    summary='修改JSON Schema 数据模型目录',
)
@ValidateFields(validate_model='edit_schema_model_groups')
async def edit_schema_model_schema_model_groups(
    request: Request,
    edit_schema_model_groups: Schema_model_groupsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_schema_model_groups.update_by = current_user.user.user_name
    edit_schema_model_groups.update_time = datetime.now()
    logger.info(edit_schema_model_groups.model_dump())
    result = await Schema_model_groupsService.edit_schema_model_groups_services(query_db, edit_schema_model_groups)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message, data=result.result)


@schema_model_groupsController.delete(
    '/{group_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_model_groups:remove'))],
    summary='删除JSON Schema 数据模型目录',
)
async def delete_schema_model_schema_model_groups(
    request: Request,
    group_ids: str,
    query_db: AsyncSession = Depends(get_db),
):
    delete_schema_model_groups = DeleteSchema_model_groupsModel(groupIds=group_ids)
    logger.info(delete_schema_model_groups.model_dump())
    result = await Schema_model_groupsService.delete_schema_model_groups_services(query_db, delete_schema_model_groups)
    logger.info(result.message)
    return ResponseUtil.success(msg=result.message)


@schema_model_groupsController.get(
    '/{group_id}',
    response_model=Schema_model_groupsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_model_groups:query'))],
    summary='获取JSON Schema 数据模型目录详情',
)
async def query_detail_schema_model_schema_model_groups(
    request: Request,
    group_id: str,
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(f'group_id:{group_id}')
    result = await Schema_model_groupsService.schema_model_groups_detail_services(query_db, group_id)
    logger.info(f'获取group_id为{group_id}的信息成功')
    return ResponseUtil.success(data=result)
