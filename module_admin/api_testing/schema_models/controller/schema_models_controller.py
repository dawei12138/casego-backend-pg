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
from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService
from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import (
    CreateSchemaModelWithRootModel,
    DeleteSchema_modelsModel,
    SchemaModelPreviewRequestModel,
    Schema_modelsModel,
    Schema_modelsPageQueryModel,
)
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


schema_modelsController = APIRouter(prefix='/schema_model/schema_models', dependencies=[Depends(LoginService.get_current_user)])


@schema_modelsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:list'))],
    summary='获取JSON Schema 数据模型主列表',
    description='根据查询条件获取JSON Schema 数据模型主分页列表数据',
)
async def get_schema_model_schema_models_list(
    request: Request,
schema_models_page_query: Schema_modelsPageQueryModel = Depends(Schema_modelsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(schema_models_page_query.model_dump())
    # 获取分页数据
    schema_models_page_query_result = await Schema_modelsService.get_schema_models_list_services(query_db, schema_models_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=schema_models_page_query_result)


@schema_modelsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:add'))],
    summary='新增JSON Schema 数据模型主',
    description='创建一条新的JSON Schema 数据模型主记录',
)
@ValidateFields(validate_model='add_schema_models')
# @Log(title='JSON Schema 数据模型主', business_type=BusinessType.INSERT)
async def add_schema_model_schema_models(
    request: Request,
    add_schema_models: Schema_modelsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_schema_models.create_by = current_user.user.user_name
    add_schema_models.create_time = datetime.now()
    add_schema_models.update_by = current_user.user.user_name
    add_schema_models.update_time = datetime.now()
    logger.info(add_schema_models.model_dump())
    add_schema_models_result = await Schema_modelsService.add_schema_models_services(query_db, add_schema_models)
    logger.info(add_schema_models_result.message)

    return ResponseUtil.success(msg=add_schema_models_result.message, data=add_schema_models_result.result)


@schema_modelsController.post(
    '/create-with-root',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:add'))],
    summary='新增JSON Schema 数据模型主及根节点',
    description='在同一事务中创建JSON Schema 数据模型主记录及根节点记录',
)
# @Log(title='JSON Schema 数据模型主及根节点', business_type=BusinessType.INSERT)
async def add_schema_model_schema_model_with_root(
    request: Request,
    create_schema_model: CreateSchemaModelWithRootModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    now = datetime.now()
    create_schema_model.model.create_by = current_user.user.user_name
    create_schema_model.model.create_time = now
    create_schema_model.model.update_by = current_user.user.user_name
    create_schema_model.model.update_time = now
    create_schema_model.root_node.create_by = current_user.user.user_name
    create_schema_model.root_node.create_time = now
    create_schema_model.root_node.update_by = current_user.user.user_name
    create_schema_model.root_node.update_time = now
    logger.info(create_schema_model.model_dump())
    create_schema_model_result = await Schema_modelsService.add_schema_model_with_root_services(query_db, create_schema_model)
    logger.info(create_schema_model_result.message)

    return ResponseUtil.success(msg=create_schema_model_result.message, data=create_schema_model_result.result)


@schema_modelsController.post(
    '/preview',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:query'))],
    summary='预览JSON Schema 数据模型示例',
    description='根据当前模型节点生成JSON Schema和Mock示例数据，支持未保存节点和引用模型',
)
async def preview_schema_model_schema_models(
    request: Request,
    preview_schema_model: SchemaModelPreviewRequestModel,
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(preview_schema_model.model_dump())
    preview_result = await Schema_modelsService.preview_schema_model_services(query_db, preview_schema_model)
    logger.info('预览生成成功')

    return ResponseUtil.success(data=preview_result.model_dump(by_alias=True))


@schema_modelsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:edit'))],
    summary='修改JSON Schema 数据模型主',
    description='根据主键更新JSON Schema 数据模型主信息',
)
@ValidateFields(validate_model='edit_schema_models')
# @Log(title='JSON Schema 数据模型主', business_type=BusinessType.UPDATE)
async def edit_schema_model_schema_models(
    request: Request,
    edit_schema_models: Schema_modelsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_schema_models.model_dump())
    edit_schema_models.update_by = current_user.user.user_name
    edit_schema_models.update_time = datetime.now()
    edit_schema_models_result = await Schema_modelsService.edit_schema_models_services(query_db, edit_schema_models)
    logger.info(edit_schema_models_result.message)

    return ResponseUtil.success(msg=edit_schema_models_result.message, data=edit_schema_models_result.result)


@schema_modelsController.delete(
    '/{model_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:remove'))],
    summary='删除JSON Schema 数据模型主',
    description='根据主键批量删除JSON Schema 数据模型主记录，多个主键以逗号分隔',
)
# @Log(title='JSON Schema 数据模型主', business_type=BusinessType.DELETE)
async def delete_schema_model_schema_models(request: Request, model_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_schema_models = DeleteSchema_modelsModel(modelIds=model_ids)
    logger.info(delete_schema_models.model_dump())
    delete_schema_models_result = await Schema_modelsService.delete_schema_models_services(query_db, delete_schema_models)
    logger.info(delete_schema_models_result.message)

    return ResponseUtil.success(msg=delete_schema_models_result.message)


@schema_modelsController.get(
    '/{model_id}',
    response_model=Schema_modelsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:query'))],
    summary='获取JSON Schema 数据模型主详情',
    description='根据主键获取JSON Schema 数据模型主详细信息',
)
async def query_detail_schema_model_schema_models(request: Request, model_id: str, query_db: AsyncSession = Depends(get_db)):
    logger.info(f'model_id:{model_id}')
    schema_models_detail_result = await Schema_modelsService.schema_models_detail_services(query_db, model_id)
    logger.info(f'获取model_id为{model_id}的信息成功')

    return ResponseUtil.success(data=schema_models_detail_result)


@schema_modelsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:schema_models:export'))],
    summary='导出JSON Schema 数据模型主',
    description='根据查询条件导出JSON Schema 数据模型主列表数据到Excel文件',
)
# @Log(title='JSON Schema 数据模型主', business_type=BusinessType.EXPORT)
async def export_schema_model_schema_models_list(
    request: Request,
    schema_models_page_query: Schema_modelsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    schema_models_query_result = await Schema_modelsService.get_schema_models_list_services(query_db, schema_models_page_query, is_page=False)
    schema_models_export_result = await Schema_modelsService.export_schema_models_list_services(schema_models_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(schema_models_export_result))
