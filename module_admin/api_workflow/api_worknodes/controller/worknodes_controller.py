from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import NodeTypeEnum
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_workflow.api_worknodes.service.worknodes_service import WorknodesService
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import DeleteWorknodesModel, WorknodesModel, \
    WorknodesPageQueryModel, WorknodesSortModel, AddWorknodesModel, CopyWorknodesModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

worknodesController = APIRouter(prefix='/api_worknodes/worknodes',
                                dependencies=[Depends(LoginService.get_current_user)])


@worknodesController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:list'))]
)
async def get_api_worknodes_worknodes_list(
        request: Request,
        worknodes_page_query: WorknodesPageQueryModel = Depends(WorknodesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(worknodes_page_query.model_dump())
    # 获取分页数据
    worknodes_page_query_result = await WorknodesService.get_worknodes_list_services(query_db, worknodes_page_query,
                                                                                     is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=worknodes_page_query_result)


@worknodesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:add'))])
@ValidateFields(validate_model='add_worknodes')
# @Log(title='执行器节点', business_type=BusinessType.INSERT)
async def add_api_worknodes_worknodes(
        request: Request,
        add_worknodes: AddWorknodesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_worknodes.create_by = current_user.user.user_name
    add_worknodes.create_time = datetime.now()
    add_worknodes.update_by = current_user.user.user_name
    add_worknodes.update_time = datetime.now()
    logger.info(add_worknodes.model_dump())
    add_worknodes_result = await WorknodesService.add_worknodes_services(query_db, add_worknodes)
    logger.info(add_worknodes_result.get('message'))

    return ResponseUtil.success(
        msg=add_worknodes_result.get('message'),
        data={
            'nodeId': add_worknodes_result.get('node_id'),
            'sortNo': add_worknodes_result.get('sort_no'),
        }
    )


@worknodesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:edit'))])
@ValidateFields(validate_model='edit_worknodes')
# @Log(title='执行器节点', business_type=BusinessType.UPDATE)
async def edit_api_worknodes_worknodes(
        request: Request,
        edit_worknodes: WorknodesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_worknodes.model_dump())
    edit_worknodes.update_by = current_user.user.user_name
    edit_worknodes.update_time = datetime.now()
    edit_worknodes_result = await WorknodesService.edit_worknodes_services(query_db, edit_worknodes)
    logger.info(edit_worknodes_result.message)

    return ResponseUtil.success(msg=edit_worknodes_result.message)


@worknodesController.put('/sort', dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:edit'))])
@ValidateFields(validate_model='edit_worknodes')
# @Log(title='执行器节点', business_type=BusinessType.UPDATE)
async def edit_api_worknodes_sort(
        request: Request,
        edit_worknodes: List[WorknodesModel],
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    for i in edit_worknodes:
        if i.type == NodeTypeEnum.ELSE:
            continue
        edit_worknodes_result = await WorknodesService.edit_worknodes_services(query_db, i)

        logger.info(edit_worknodes_result.message)

    return ResponseUtil.success(msg=CrudResponseModel(is_success=True, message='更新成功').message)


@worknodesController.post('/copy/{worknodeid}', dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:edit'))])
# @Log(title='执行器节点', business_type=BusinessType.UPDATE)
async def copy_api_worknodes(
        request: Request,
        worknodeid: int,
        copy_worknodes: CopyWorknodesModel = None,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    复制节点及其所有子节点

    :param worknodeid:
    :param current_user:
    :param query_db:
    :param request:
    :param copy_worknodes: 可选的复制参数，包含target_parent_id
    """
    logger.info(f"复制节点，源节点ID: {worknodeid}")

    # 如果没有传入body，创建默认的copy_model
    if copy_worknodes is None:
        copy_worknodes = CopyWorknodesModel(node_id=worknodeid)
    else:
        copy_worknodes.node_id = worknodeid

    copy_worknodes_result = await WorknodesService.copy_worknodes_services(
        query_db, copy_worknodes,
        create_by=current_user.user.user_name,
        create_time=datetime.now(),
        update_by=current_user.user.user_name,
        update_time=datetime.now()
    )
    logger.info(copy_worknodes_result.message)

    return ResponseUtil.success(msg=copy_worknodes_result.message)


@worknodesController.delete('/{node_ids}',
                            dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:remove'))])
# @Log(title='执行器节点', business_type=BusinessType.DELETE)
async def delete_api_worknodes_worknodes(request: Request, node_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_worknodes = DeleteWorknodesModel(nodeIds=node_ids)
    logger.info(delete_worknodes.model_dump())
    delete_worknodes_result = await WorknodesService.delete_worknodes_services(query_db, delete_worknodes)
    logger.info(delete_worknodes_result.message)

    return ResponseUtil.success(msg=delete_worknodes_result.message)


@worknodesController.get(
    '/{node_id}', response_model=WorknodesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:query'))]
)
async def query_detail_api_worknodes_worknodes(request: Request, node_id: int,
                                               query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    worknodes_detail_result = await WorknodesService.worknodes_detail_services(query_db, node_id)
    logger.info(f'获取node_id为{node_id}的信息成功')

    return ResponseUtil.success(data=worknodes_detail_result)


@worknodesController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_worknodes:worknodes:export'))])
# @Log(title='执行器节点', business_type=BusinessType.EXPORT)
async def export_api_worknodes_worknodes_list(
        request: Request,
        worknodes_page_query: WorknodesPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    worknodes_query_result = await WorknodesService.get_worknodes_list_services(query_db, worknodes_page_query,
                                                                                is_page=False)
    worknodes_export_result = await WorknodesService.export_worknodes_list_services(worknodes_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(worknodes_export_result))
