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
from module_app.globalparams.service.globalparams_service import GlobalparamsService
from module_app.globalparams.entity.vo.globalparams_vo import DeleteGlobalparamsModel, GlobalparamsModel, GlobalparamsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


globalparamsController = APIRouter(prefix='/app/globalparams', dependencies=[Depends(LoginService.get_current_user)])


@globalparamsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:globalparams:list'))],
    summary='获取全局参数列表',
    description='根据查询条件获取全局参数分页列表数据',
)
async def get_app_globalparams_list(
    request: Request,
globalparams_page_query: GlobalparamsPageQueryModel = Depends(GlobalparamsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(globalparams_page_query.model_dump())
    # 获取分页数据
    globalparams_page_query_result = await GlobalparamsService.get_globalparams_list_services(query_db, globalparams_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=globalparams_page_query_result)


@globalparamsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:globalparams:add'))],
    summary='新增全局参数',
    description='创建一条新的全局参数记录',
)
@ValidateFields(validate_model='add_globalparams')
# @Log(title='全局参数', business_type=BusinessType.INSERT)
async def add_app_globalparams(
    request: Request,
    add_globalparams: GlobalparamsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_globalparams.create_by = current_user.user.user_name
    add_globalparams.create_time = datetime.now()
    add_globalparams.update_by = current_user.user.user_name
    add_globalparams.update_time = datetime.now()
    logger.info(add_globalparams.model_dump())
    add_globalparams_result = await GlobalparamsService.add_globalparams_services(query_db, add_globalparams)
    logger.info(add_globalparams_result.message)

    return ResponseUtil.success(msg=add_globalparams_result.message)


@globalparamsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:globalparams:edit'))],
    summary='修改全局参数',
    description='根据主键更新全局参数信息',
)
@ValidateFields(validate_model='edit_globalparams')
# @Log(title='全局参数', business_type=BusinessType.UPDATE)
async def edit_app_globalparams(
    request: Request,
    edit_globalparams: GlobalparamsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_globalparams.model_dump())
    edit_globalparams.update_by = current_user.user.user_name
    edit_globalparams.update_time = datetime.now()
    edit_globalparams_result = await GlobalparamsService.edit_globalparams_services(query_db, edit_globalparams)
    logger.info(edit_globalparams_result.message)

    return ResponseUtil.success(msg=edit_globalparams_result.message)


@globalparamsController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:globalparams:remove'))],
    summary='删除全局参数',
    description='根据主键批量删除全局参数记录，多个主键以逗号分隔',
)
# @Log(title='全局参数', business_type=BusinessType.DELETE)
async def delete_app_globalparams(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_globalparams = DeleteGlobalparamsModel(ids=ids)
    logger.info(delete_globalparams.model_dump())
    delete_globalparams_result = await GlobalparamsService.delete_globalparams_services(query_db, delete_globalparams)
    logger.info(delete_globalparams_result.message)

    return ResponseUtil.success(msg=delete_globalparams_result.message)


@globalparamsController.get(
    '/{id}',
    response_model=GlobalparamsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:globalparams:query'))],
    summary='获取全局参数详情',
    description='根据主键获取全局参数详细信息',
)
async def query_detail_app_globalparams(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    globalparams_detail_result = await GlobalparamsService.globalparams_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=globalparams_detail_result)


@globalparamsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:globalparams:export'))],
    summary='导出全局参数',
    description='根据查询条件导出全局参数列表数据到Excel文件',
)
# @Log(title='全局参数', business_type=BusinessType.EXPORT)
async def export_app_globalparams_list(
    request: Request,
    globalparams_page_query: GlobalparamsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    globalparams_query_result = await GlobalparamsService.get_globalparams_list_services(query_db, globalparams_page_query, is_page=False)
    globalparams_export_result = await GlobalparamsService.export_globalparams_list_services(globalparams_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(globalparams_export_result))
