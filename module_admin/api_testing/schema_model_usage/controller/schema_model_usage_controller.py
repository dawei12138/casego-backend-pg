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
from module_admin.api_testing.schema_model_usage.service.schema_model_usage_service import Schema_model_usageService
from module_admin.api_testing.schema_model_usage.entity.vo.schema_model_usage_vo import DeleteSchema_model_usageModel, Schema_model_usageModel, Schema_model_usagePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


schema_model_usageController = APIRouter(prefix='/schema_model_usage/schema_model_usage', dependencies=[Depends(LoginService.get_current_user)])


@schema_model_usageController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model_usage:schema_model_usage:list'))],
    summary='获取JSON Schema 模型使用关系列表',
    description='根据查询条件获取JSON Schema 模型使用关系分页列表数据',
)
async def get_schema_model_usage_schema_model_usage_list(
    request: Request,
schema_model_usage_page_query: Schema_model_usagePageQueryModel = Depends(Schema_model_usagePageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(schema_model_usage_page_query.model_dump())
    # 获取分页数据
    schema_model_usage_page_query_result = await Schema_model_usageService.get_schema_model_usage_list_services(query_db, schema_model_usage_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=schema_model_usage_page_query_result)


@schema_model_usageController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model_usage:schema_model_usage:add'))],
    summary='新增JSON Schema 模型使用关系',
    description='创建一条新的JSON Schema 模型使用关系记录',
)
@ValidateFields(validate_model='add_schema_model_usage')
# @Log(title='JSON Schema 模型使用关系', business_type=BusinessType.INSERT)
async def add_schema_model_usage_schema_model_usage(
    request: Request,
    add_schema_model_usage: Schema_model_usageModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_schema_model_usage.create_by = current_user.user.user_name
    add_schema_model_usage.create_time = datetime.now()
    add_schema_model_usage.update_by = current_user.user.user_name
    add_schema_model_usage.update_time = datetime.now()
    logger.info(add_schema_model_usage.model_dump())
    add_schema_model_usage_result = await Schema_model_usageService.add_schema_model_usage_services(query_db, add_schema_model_usage)
    logger.info(add_schema_model_usage_result.message)

    return ResponseUtil.success(msg=add_schema_model_usage_result.message)


@schema_model_usageController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model_usage:schema_model_usage:edit'))],
    summary='修改JSON Schema 模型使用关系',
    description='根据主键更新JSON Schema 模型使用关系信息',
)
@ValidateFields(validate_model='edit_schema_model_usage')
# @Log(title='JSON Schema 模型使用关系', business_type=BusinessType.UPDATE)
async def edit_schema_model_usage_schema_model_usage(
    request: Request,
    edit_schema_model_usage: Schema_model_usageModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_schema_model_usage.model_dump())
    edit_schema_model_usage.update_by = current_user.user.user_name
    edit_schema_model_usage.update_time = datetime.now()
    edit_schema_model_usage_result = await Schema_model_usageService.edit_schema_model_usage_services(query_db, edit_schema_model_usage)
    logger.info(edit_schema_model_usage_result.message)

    return ResponseUtil.success(msg=edit_schema_model_usage_result.message)


@schema_model_usageController.delete(
    '/{usage_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model_usage:schema_model_usage:remove'))],
    summary='删除JSON Schema 模型使用关系',
    description='根据主键批量删除JSON Schema 模型使用关系记录，多个主键以逗号分隔',
)
# @Log(title='JSON Schema 模型使用关系', business_type=BusinessType.DELETE)
async def delete_schema_model_usage_schema_model_usage(request: Request, usage_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_schema_model_usage = DeleteSchema_model_usageModel(usageIds=usage_ids)
    logger.info(delete_schema_model_usage.model_dump())
    delete_schema_model_usage_result = await Schema_model_usageService.delete_schema_model_usage_services(query_db, delete_schema_model_usage)
    logger.info(delete_schema_model_usage_result.message)

    return ResponseUtil.success(msg=delete_schema_model_usage_result.message)


@schema_model_usageController.get(
    '/{usage_id}',
    response_model=Schema_model_usageModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model_usage:schema_model_usage:query'))],
    summary='获取JSON Schema 模型使用关系详情',
    description='根据主键获取JSON Schema 模型使用关系详细信息',
)
async def query_detail_schema_model_usage_schema_model_usage(request: Request, usage_id: str, query_db: AsyncSession = Depends(get_db)):
    logger.info(f'usage_id:{usage_id}')
    schema_model_usage_detail_result = await Schema_model_usageService.schema_model_usage_detail_services(query_db, usage_id)
    logger.info(f'获取usage_id为{usage_id}的信息成功')

    return ResponseUtil.success(data=schema_model_usage_detail_result)


@schema_model_usageController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model_usage:schema_model_usage:export'))],
    summary='导出JSON Schema 模型使用关系',
    description='根据查询条件导出JSON Schema 模型使用关系列表数据到Excel文件',
)
# @Log(title='JSON Schema 模型使用关系', business_type=BusinessType.EXPORT)
async def export_schema_model_usage_schema_model_usage_list(
    request: Request,
    schema_model_usage_page_query: Schema_model_usagePageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    schema_model_usage_query_result = await Schema_model_usageService.get_schema_model_usage_list_services(query_db, schema_model_usage_page_query, is_page=False)
    schema_model_usage_export_result = await Schema_model_usageService.export_schema_model_usage_list_services(schema_model_usage_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(schema_model_usage_export_result))
