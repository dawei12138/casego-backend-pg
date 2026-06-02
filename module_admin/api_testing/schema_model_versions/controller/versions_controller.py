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
from module_admin.api_testing.schema_model_versions.service.versions_service import VersionsService
from module_admin.api_testing.schema_model_versions.entity.vo.versions_vo import DeleteVersionsModel, VersionsModel, VersionsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


versionsController = APIRouter(prefix='/schema_model/versions', dependencies=[Depends(LoginService.get_current_user)])


@versionsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:versions:list'))],
    summary='获取JSON Schema 模型版本列表',
    description='根据查询条件获取JSON Schema 模型版本分页列表数据',
)
async def get_schema_model_versions_list(
    request: Request,
versions_page_query: VersionsPageQueryModel = Depends(VersionsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(versions_page_query.model_dump())
    # 获取分页数据
    versions_page_query_result = await VersionsService.get_versions_list_services(query_db, versions_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=versions_page_query_result)


@versionsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:versions:add'))],
    summary='新增JSON Schema 模型版本',
    description='创建一条新的JSON Schema 模型版本记录',
)
@ValidateFields(validate_model='add_versions')
# @Log(title='JSON Schema 模型版本', business_type=BusinessType.INSERT)
async def add_schema_model_versions(
    request: Request,
    add_versions: VersionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_versions.create_by = current_user.user.user_name
    add_versions.create_time = datetime.now()
    add_versions.update_by = current_user.user.user_name
    add_versions.update_time = datetime.now()
    logger.info(add_versions.model_dump())
    add_versions_result = await VersionsService.add_versions_services(query_db, add_versions)
    logger.info(add_versions_result.message)

    return ResponseUtil.success(msg=add_versions_result.message)


@versionsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:versions:edit'))],
    summary='修改JSON Schema 模型版本',
    description='根据主键更新JSON Schema 模型版本信息',
)
@ValidateFields(validate_model='edit_versions')
# @Log(title='JSON Schema 模型版本', business_type=BusinessType.UPDATE)
async def edit_schema_model_versions(
    request: Request,
    edit_versions: VersionsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_versions.model_dump())
    edit_versions.update_by = current_user.user.user_name
    edit_versions.update_time = datetime.now()
    edit_versions_result = await VersionsService.edit_versions_services(query_db, edit_versions)
    logger.info(edit_versions_result.message)

    return ResponseUtil.success(msg=edit_versions_result.message)


@versionsController.delete(
    '/{version_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:versions:remove'))],
    summary='删除JSON Schema 模型版本',
    description='根据主键批量删除JSON Schema 模型版本记录，多个主键以逗号分隔',
)
# @Log(title='JSON Schema 模型版本', business_type=BusinessType.DELETE)
async def delete_schema_model_versions(request: Request, version_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_versions = DeleteVersionsModel(versionIds=version_ids)
    logger.info(delete_versions.model_dump())
    delete_versions_result = await VersionsService.delete_versions_services(query_db, delete_versions)
    logger.info(delete_versions_result.message)

    return ResponseUtil.success(msg=delete_versions_result.message)


@versionsController.get(
    '/{version_id}',
    response_model=VersionsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:versions:query'))],
    summary='获取JSON Schema 模型版本详情',
    description='根据主键获取JSON Schema 模型版本详细信息',
)
async def query_detail_schema_model_versions(request: Request, version_id: str, query_db: AsyncSession = Depends(get_db)):
    logger.info(f'version_id:{version_id}')
    versions_detail_result = await VersionsService.versions_detail_services(query_db, version_id)
    logger.info(f'获取version_id为{version_id}的信息成功')

    return ResponseUtil.success(data=versions_detail_result)


@versionsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('schema_model:versions:export'))],
    summary='导出JSON Schema 模型版本',
    description='根据查询条件导出JSON Schema 模型版本列表数据到Excel文件',
)
# @Log(title='JSON Schema 模型版本', business_type=BusinessType.EXPORT)
async def export_schema_model_versions_list(
    request: Request,
    versions_page_query: VersionsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    versions_query_result = await VersionsService.get_versions_list_services(query_db, versions_page_query, is_page=False)
    versions_export_result = await VersionsService.export_versions_list_services(versions_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(versions_export_result))
