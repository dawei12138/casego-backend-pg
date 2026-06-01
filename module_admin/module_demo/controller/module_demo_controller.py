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
from module_admin.module_demo.service.module_demo_service import Module_demoService
from module_admin.module_demo.entity.vo.module_demo_vo import DeleteModule_demoModel, Module_demoModel, Module_demoPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


module_demoController = APIRouter(prefix='/demo/module_demo', dependencies=[Depends(LoginService.get_current_user)])


@module_demoController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('demo:module_demo:list'))],
    summary='获取Demo全类型测试列表',
    description='根据查询条件获取Demo全类型测试分页列表数据',
)
async def get_demo_module_demo_list(
    request: Request,
module_demo_page_query: Module_demoPageQueryModel = Depends(Module_demoPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(module_demo_page_query.model_dump())
    # 获取分页数据
    module_demo_page_query_result = await Module_demoService.get_module_demo_list_services(query_db, module_demo_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=module_demo_page_query_result)


@module_demoController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('demo:module_demo:add'))],
    summary='新增Demo全类型测试',
    description='创建一条新的Demo全类型测试记录',
)
@ValidateFields(validate_model='add_module_demo')
# @Log(title='Demo全类型测试', business_type=BusinessType.INSERT)
async def add_demo_module_demo(
    request: Request,
    add_module_demo: Module_demoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_module_demo.create_by = current_user.user.user_name
    add_module_demo.create_time = datetime.now()
    add_module_demo.update_by = current_user.user.user_name
    add_module_demo.update_time = datetime.now()
    logger.info(add_module_demo.model_dump())
    add_module_demo_result = await Module_demoService.add_module_demo_services(query_db, add_module_demo)
    logger.info(add_module_demo_result.message)

    return ResponseUtil.success(msg=add_module_demo_result.message)


@module_demoController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('demo:module_demo:edit'))],
    summary='修改Demo全类型测试',
    description='根据主键更新Demo全类型测试信息',
)
@ValidateFields(validate_model='edit_module_demo')
# @Log(title='Demo全类型测试', business_type=BusinessType.UPDATE)
async def edit_demo_module_demo(
    request: Request,
    edit_module_demo: Module_demoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_module_demo.model_dump())
    edit_module_demo.update_by = current_user.user.user_name
    edit_module_demo.update_time = datetime.now()
    edit_module_demo_result = await Module_demoService.edit_module_demo_services(query_db, edit_module_demo)
    logger.info(edit_module_demo_result.message)

    return ResponseUtil.success(msg=edit_module_demo_result.message)


@module_demoController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('demo:module_demo:remove'))],
    summary='删除Demo全类型测试',
    description='根据主键批量删除Demo全类型测试记录，多个主键以逗号分隔',
)
# @Log(title='Demo全类型测试', business_type=BusinessType.DELETE)
async def delete_demo_module_demo(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_module_demo = DeleteModule_demoModel(ids=ids)
    logger.info(delete_module_demo.model_dump())
    delete_module_demo_result = await Module_demoService.delete_module_demo_services(query_db, delete_module_demo)
    logger.info(delete_module_demo_result.message)

    return ResponseUtil.success(msg=delete_module_demo_result.message)


@module_demoController.get(
    '/{id}',
    response_model=Module_demoModel,
    dependencies=[Depends(CheckUserInterfaceAuth('demo:module_demo:query'))],
    summary='获取Demo全类型测试详情',
    description='根据主键获取Demo全类型测试详细信息',
)
async def query_detail_demo_module_demo(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    module_demo_detail_result = await Module_demoService.module_demo_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=module_demo_detail_result)


@module_demoController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('demo:module_demo:export'))],
    summary='导出Demo全类型测试',
    description='根据查询条件导出Demo全类型测试列表数据到Excel文件',
)
# @Log(title='Demo全类型测试', business_type=BusinessType.EXPORT)
async def export_demo_module_demo_list(
    request: Request,
    module_demo_page_query: Module_demoPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    module_demo_query_result = await Module_demoService.get_module_demo_list_services(query_db, module_demo_page_query, is_page=False)
    module_demo_export_result = await Module_demoService.export_module_demo_list_services(module_demo_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(module_demo_export_result))
