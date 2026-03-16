from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_llm.chat_mcp_config.service.mcpconfig_service import McpconfigService
from module_llm.chat_mcp_config.entity.vo.mcpconfig_vo import DeleteMcpconfigModel, McpconfigModel, \
    McpconfigPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

mcpconfigController = APIRouter(prefix='/mcpconfig/mcpconfig', dependencies=[Depends(LoginService.get_current_user)])


@mcpconfigController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('mcpconfig:mcpconfig:list'))],
    summary='获取MCP服务器配置列表',
    description='根据查询条件获取MCP服务器配置分页列表数据',
)
async def get_mcpconfig_mcpconfig_list(
        request: Request,
        mcpconfig_page_query: McpconfigPageQueryModel = Depends(McpconfigPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(mcpconfig_page_query.model_dump())
    # 获取分页数据
    mcpconfig_page_query_result = await McpconfigService.get_mcpconfig_list_services(query_db, mcpconfig_page_query,
                                                                                     is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=mcpconfig_page_query_result)


@mcpconfigController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('mcpconfig:mcpconfig:add'))],
    summary='新增MCP服务器配置',
    description='创建一条新的MCP服务器配置记录',
)
@ValidateFields(validate_model='add_mcpconfig')
# @Log(title='MCP服务器配置', business_type=BusinessType.INSERT)
async def add_mcpconfig_mcpconfig(
        request: Request,
        add_mcpconfig: McpconfigModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_mcpconfig.create_by = current_user.user.user_name
    add_mcpconfig.create_time = datetime.now()
    add_mcpconfig.update_by = current_user.user.user_name
    add_mcpconfig.update_time = datetime.now()
    logger.info(add_mcpconfig.model_dump())
    add_mcpconfig_result = await McpconfigService.add_mcpconfig_services(query_db, add_mcpconfig)
    logger.info(add_mcpconfig_result.message)

    return ResponseUtil.success(msg=add_mcpconfig_result.message)


@mcpconfigController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('mcpconfig:mcpconfig:edit'))],
    summary='修改MCP服务器配置',
    description='根据主键更新MCP服务器配置信息',
)
@ValidateFields(validate_model='edit_mcpconfig')
# @Log(title='MCP服务器配置', business_type=BusinessType.UPDATE)
async def edit_mcpconfig_mcpconfig(
        request: Request,
        edit_mcpconfig: McpconfigModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_mcpconfig.model_dump())
    edit_mcpconfig.update_by = current_user.user.user_name
    edit_mcpconfig.update_time = datetime.now()
    edit_mcpconfig_result = await McpconfigService.edit_mcpconfig_services(query_db, edit_mcpconfig)
    logger.info(edit_mcpconfig_result.message)

    return ResponseUtil.success(msg=edit_mcpconfig_result.message)


@mcpconfigController.delete(
    '/{config_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('mcpconfig:mcpconfig:remove'))],
    summary='删除MCP服务器配置',
    description='根据主键批量删除MCP服务器配置记录，多个主键以逗号分隔',
)
# @Log(title='MCP服务器配置', business_type=BusinessType.DELETE)
async def delete_mcpconfig_mcpconfig(request: Request, config_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_mcpconfig = DeleteMcpconfigModel(configIds=config_ids)
    logger.info(delete_mcpconfig.model_dump())
    delete_mcpconfig_result = await McpconfigService.delete_mcpconfig_services(query_db, delete_mcpconfig)
    logger.info(delete_mcpconfig_result.message)

    return ResponseUtil.success(msg=delete_mcpconfig_result.message)


@mcpconfigController.get(
    '/{config_id}',
    response_model=McpconfigModel,
    dependencies=[Depends(CheckUserInterfaceAuth('mcpconfig:mcpconfig:query'))],
    summary='获取MCP服务器配置详情',
    description='根据主键获取MCP服务器配置详细信息',
)
async def query_detail_mcpconfig_mcpconfig(request: Request, config_id: str,
                                           query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    mcpconfig_detail_result = await McpconfigService.mcpconfig_detail_services(query_db, config_id)
    logger.info(f'获取config_id为{config_id}的信息成功')

    return ResponseUtil.success(data=mcpconfig_detail_result)


@mcpconfigController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('mcpconfig:mcpconfig:export'))],
    summary='导出MCP服务器配置',
    description='根据查询条件导出MCP服务器配置列表数据到Excel文件',
)
# @Log(title='MCP服务器配置', business_type=BusinessType.EXPORT)
async def export_mcpconfig_mcpconfig_list(
        request: Request,
        mcpconfig_page_query: McpconfigPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    mcpconfig_query_result = await McpconfigService.get_mcpconfig_list_services(query_db, mcpconfig_page_query,
                                                                                is_page=False)
    mcpconfig_export_result = await McpconfigService.export_mcpconfig_list_services(mcpconfig_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(mcpconfig_export_result))
