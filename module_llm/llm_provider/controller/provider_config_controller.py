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
from module_llm.llm_provider.service.provider_config_service import Provider_configService
from module_llm.llm_provider.entity.vo.provider_config_vo import DeleteProvider_configModel, Provider_configModel, Provider_configPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


provider_configController = APIRouter(prefix='/provider/provider_config', dependencies=[Depends(LoginService.get_current_user)])


@provider_configController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('provider:provider_config:list'))],
    summary='获取LLM提供商配置列表',
    description='根据查询条件获取LLM提供商配置分页列表数据',
)
async def get_provider_provider_config_list(
    request: Request,
provider_config_page_query: Provider_configPageQueryModel = Depends(Provider_configPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(provider_config_page_query.model_dump())
    # 获取分页数据
    provider_config_page_query_result = await Provider_configService.get_provider_config_list_services(query_db, provider_config_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=provider_config_page_query_result)


@provider_configController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('provider:provider_config:add'))],
    summary='新增LLM提供商配置',
    description='创建一条新的LLM提供商配置记录',
)
@ValidateFields(validate_model='add_provider_config')
# @Log(title='LLM提供商配置', business_type=BusinessType.INSERT)
async def add_provider_provider_config(
    request: Request,
    add_provider_config: Provider_configModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_provider_config.create_by = current_user.user.user_name
    add_provider_config.create_time = datetime.now()
    add_provider_config.update_by = current_user.user.user_name
    add_provider_config.update_time = datetime.now()
    logger.info(add_provider_config.model_dump())
    add_provider_config_result = await Provider_configService.add_provider_config_services(query_db, add_provider_config)
    logger.info(add_provider_config_result.message)

    return ResponseUtil.success(msg=add_provider_config_result.message)


@provider_configController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('provider:provider_config:edit'))],
    summary='修改LLM提供商配置',
    description='根据主键更新LLM提供商配置信息',
)
@ValidateFields(validate_model='edit_provider_config')
# @Log(title='LLM提供商配置', business_type=BusinessType.UPDATE)
async def edit_provider_provider_config(
    request: Request,
    edit_provider_config: Provider_configModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_provider_config.model_dump())
    edit_provider_config.update_by = current_user.user.user_name
    edit_provider_config.update_time = datetime.now()
    edit_provider_config_result = await Provider_configService.edit_provider_config_services(query_db, edit_provider_config)
    logger.info(edit_provider_config_result.message)

    return ResponseUtil.success(msg=edit_provider_config_result.message)


@provider_configController.delete(
    '/{provider_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('provider:provider_config:remove'))],
    summary='删除LLM提供商配置',
    description='根据主键批量删除LLM提供商配置记录，多个主键以逗号分隔',
)
# @Log(title='LLM提供商配置', business_type=BusinessType.DELETE)
async def delete_provider_provider_config(request: Request, provider_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_provider_config = DeleteProvider_configModel(providerIds=provider_ids)
    logger.info(delete_provider_config.model_dump())
    delete_provider_config_result = await Provider_configService.delete_provider_config_services(query_db, delete_provider_config)
    logger.info(delete_provider_config_result.message)

    return ResponseUtil.success(msg=delete_provider_config_result.message)


@provider_configController.get(
    '/{provider_id}',
    response_model=Provider_configModel,
    dependencies=[Depends(CheckUserInterfaceAuth('provider:provider_config:query'))],
    summary='获取LLM提供商配置详情',
    description='根据主键获取LLM提供商配置详细信息',
)
async def query_detail_provider_provider_config(request: Request, provider_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    provider_config_detail_result = await Provider_configService.provider_config_detail_services(query_db, provider_id)
    logger.info(f'获取provider_id为{provider_id}的信息成功')

    return ResponseUtil.success(data=provider_config_detail_result)


@provider_configController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('provider:provider_config:export'))],
    summary='导出LLM提供商配置',
    description='根据查询条件导出LLM提供商配置列表数据到Excel文件',
)
# @Log(title='LLM提供商配置', business_type=BusinessType.EXPORT)
async def export_provider_provider_config_list(
    request: Request,
    provider_config_page_query: Provider_configPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    provider_config_query_result = await Provider_configService.get_provider_config_list_services(query_db, provider_config_page_query, is_page=False)
    provider_config_export_result = await Provider_configService.export_provider_config_list_services(provider_config_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(provider_config_export_result))
