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
from module_admin.api_testing.schema_nodes.service.schema_nodes_service import Schema_nodesService
from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import DeleteSchema_nodesModel, Schema_nodesModel, Schema_nodesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


schema_nodesController = APIRouter(prefix='/schemanode/schema_nodes', dependencies=[Depends(LoginService.get_current_user)])


@schema_nodesController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schemanode:schema_nodes:list'))],
    summary='获取JSON Schema 可视化节点列表',
    description='根据查询条件获取JSON Schema 可视化节点分页列表数据',
)
async def get_schemanode_schema_nodes_list(
    request: Request,
schema_nodes_page_query: Schema_nodesPageQueryModel = Depends(Schema_nodesPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(schema_nodes_page_query.model_dump())
    # 获取分页数据
    schema_nodes_page_query_result = await Schema_nodesService.get_schema_nodes_list_services(query_db, schema_nodes_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=schema_nodes_page_query_result)


@schema_nodesController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schemanode:schema_nodes:add'))],
    summary='新增JSON Schema 可视化节点',
    description='创建一条新的JSON Schema 可视化节点记录',
)
@ValidateFields(validate_model='add_schema_nodes')
# @Log(title='JSON Schema 可视化节点', business_type=BusinessType.INSERT)
async def add_schemanode_schema_nodes(
    request: Request,
    add_schema_nodes: Schema_nodesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_schema_nodes.create_by = current_user.user.user_name
    add_schema_nodes.create_time = datetime.now()
    add_schema_nodes.update_by = current_user.user.user_name
    add_schema_nodes.update_time = datetime.now()
    logger.info(add_schema_nodes.model_dump())
    add_schema_nodes_result = await Schema_nodesService.add_schema_nodes_services(query_db, add_schema_nodes)
    logger.info(add_schema_nodes_result.message)

    return ResponseUtil.success(msg=add_schema_nodes_result.message)


@schema_nodesController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('schemanode:schema_nodes:edit'))],
    summary='修改JSON Schema 可视化节点',
    description='根据主键更新JSON Schema 可视化节点信息',
)
@ValidateFields(validate_model='edit_schema_nodes')
# @Log(title='JSON Schema 可视化节点', business_type=BusinessType.UPDATE)
async def edit_schemanode_schema_nodes(
    request: Request,
    edit_schema_nodes: Schema_nodesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_schema_nodes.model_dump())
    edit_schema_nodes.update_by = current_user.user.user_name
    edit_schema_nodes.update_time = datetime.now()
    edit_schema_nodes_result = await Schema_nodesService.edit_schema_nodes_services(query_db, edit_schema_nodes)
    logger.info(edit_schema_nodes_result.message)

    return ResponseUtil.success(msg=edit_schema_nodes_result.message)


@schema_nodesController.delete(
    '/{node_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('schemanode:schema_nodes:remove'))],
    summary='删除JSON Schema 可视化节点',
    description='根据主键批量删除JSON Schema 可视化节点记录，多个主键以逗号分隔',
)
# @Log(title='JSON Schema 可视化节点', business_type=BusinessType.DELETE)
async def delete_schemanode_schema_nodes(request: Request, node_ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_schema_nodes = DeleteSchema_nodesModel(nodeIds=node_ids)
    logger.info(delete_schema_nodes.model_dump())
    delete_schema_nodes_result = await Schema_nodesService.delete_schema_nodes_services(query_db, delete_schema_nodes)
    logger.info(delete_schema_nodes_result.message)

    return ResponseUtil.success(msg=delete_schema_nodes_result.message)


@schema_nodesController.get(
    '/{node_id}',
    response_model=Schema_nodesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('schemanode:schema_nodes:query'))],
    summary='获取JSON Schema 可视化节点详情',
    description='根据主键获取JSON Schema 可视化节点详细信息',
)
async def query_detail_schemanode_schema_nodes(request: Request, node_id: str, query_db: AsyncSession = Depends(get_db)):
    logger.info(f'node_id:{node_id}')
    schema_nodes_detail_result = await Schema_nodesService.schema_nodes_detail_services(query_db, node_id)
    logger.info(f'获取node_id为{node_id}的信息成功')

    return ResponseUtil.success(data=schema_nodes_detail_result)


@schema_nodesController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('schemanode:schema_nodes:export'))],
    summary='导出JSON Schema 可视化节点',
    description='根据查询条件导出JSON Schema 可视化节点列表数据到Excel文件',
)
# @Log(title='JSON Schema 可视化节点', business_type=BusinessType.EXPORT)
async def export_schemanode_schema_nodes_list(
    request: Request,
    schema_nodes_page_query: Schema_nodesPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    schema_nodes_query_result = await Schema_nodesService.get_schema_nodes_list_services(query_db, schema_nodes_page_query, is_page=False)
    schema_nodes_export_result = await Schema_nodesService.export_schema_nodes_list_services(schema_nodes_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(schema_nodes_export_result))
