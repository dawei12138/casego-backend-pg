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
from module_app.agents.service.agents_service import AgentsService
from module_app.agents.entity.vo.agents_vo import DeleteAgentsModel, AgentsModel, AgentsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


agentsController = APIRouter(prefix='/app/agents', dependencies=[Depends(LoginService.get_current_user)])


@agentsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:agents:list'))],
    summary='获取Agent代理列表',
    description='根据查询条件获取Agent代理分页列表数据',
)
async def get_app_agents_list(
    request: Request,
agents_page_query: AgentsPageQueryModel = Depends(AgentsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(agents_page_query.model_dump())
    # 获取分页数据
    agents_page_query_result = await AgentsService.get_agents_list_services(query_db, agents_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=agents_page_query_result)


@agentsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:agents:add'))],
    summary='新增Agent代理',
    description='创建一条新的Agent代理记录',
)
@ValidateFields(validate_model='add_agents')
# @Log(title='Agent代理', business_type=BusinessType.INSERT)
async def add_app_agents(
    request: Request,
    add_agents: AgentsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_agents.create_by = current_user.user.user_name
    add_agents.create_time = datetime.now()
    add_agents.update_by = current_user.user.user_name
    add_agents.update_time = datetime.now()
    logger.info(add_agents.model_dump())
    add_agents_result = await AgentsService.add_agents_services(query_db, add_agents)
    logger.info(add_agents_result.message)

    return ResponseUtil.success(msg=add_agents_result.message)


@agentsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:agents:edit'))],
    summary='修改Agent代理',
    description='根据主键更新Agent代理信息',
)
@ValidateFields(validate_model='edit_agents')
# @Log(title='Agent代理', business_type=BusinessType.UPDATE)
async def edit_app_agents(
    request: Request,
    edit_agents: AgentsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_agents.model_dump())
    edit_agents.update_by = current_user.user.user_name
    edit_agents.update_time = datetime.now()
    edit_agents_result = await AgentsService.edit_agents_services(query_db, edit_agents)
    logger.info(edit_agents_result.message)

    return ResponseUtil.success(msg=edit_agents_result.message)


@agentsController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:agents:remove'))],
    summary='删除Agent代理',
    description='根据主键批量删除Agent代理记录，多个主键以逗号分隔',
)
# @Log(title='Agent代理', business_type=BusinessType.DELETE)
async def delete_app_agents(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_agents = DeleteAgentsModel(ids=ids)
    logger.info(delete_agents.model_dump())
    delete_agents_result = await AgentsService.delete_agents_services(query_db, delete_agents)
    logger.info(delete_agents_result.message)

    return ResponseUtil.success(msg=delete_agents_result.message)


@agentsController.get(
    '/{id}',
    response_model=AgentsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:agents:query'))],
    summary='获取Agent代理详情',
    description='根据主键获取Agent代理详细信息',
)
async def query_detail_app_agents(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    agents_detail_result = await AgentsService.agents_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=agents_detail_result)


@agentsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:agents:export'))],
    summary='导出Agent代理',
    description='根据查询条件导出Agent代理列表数据到Excel文件',
)
# @Log(title='Agent代理', business_type=BusinessType.EXPORT)
async def export_app_agents_list(
    request: Request,
    agents_page_query: AgentsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    agents_query_result = await AgentsService.get_agents_list_services(query_db, agents_page_query, is_page=False)
    agents_export_result = await AgentsService.export_agents_list_services(agents_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(agents_export_result))
