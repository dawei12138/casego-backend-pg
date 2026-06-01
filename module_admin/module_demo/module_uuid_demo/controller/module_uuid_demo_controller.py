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
from module_admin.module_demo.module_uuid_demo.service.module_uuid_demo_service import Module_uuid_demoService
from module_admin.module_demo.module_uuid_demo.entity.vo.module_uuid_demo_vo import DeleteModule_uuid_demoModel, Module_uuid_demoModel, Module_uuid_demoPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


module_uuid_demoController = APIRouter(prefix='/uuid_demo/module_uuid_demo', dependencies=[Depends(LoginService.get_current_user)])


@module_uuid_demoController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('uuid_demo:module_uuid_demo:list'))],
    summary='获取UUID主键业务示例列表',
    description='根据查询条件获取UUID主键业务示例分页列表数据',
)
async def get_uuid_demo_module_uuid_demo_list(
    request: Request,
module_uuid_demo_page_query: Module_uuid_demoPageQueryModel = Depends(Module_uuid_demoPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(module_uuid_demo_page_query.model_dump())
    # 获取分页数据
    module_uuid_demo_page_query_result = await Module_uuid_demoService.get_module_uuid_demo_list_services(query_db, module_uuid_demo_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=module_uuid_demo_page_query_result)


@module_uuid_demoController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('uuid_demo:module_uuid_demo:add'))],
    summary='新增UUID主键业务示例',
    description='创建一条新的UUID主键业务示例记录',
)
@ValidateFields(validate_model='add_module_uuid_demo')
# @Log(title='UUID主键业务示例', business_type=BusinessType.INSERT)
async def add_uuid_demo_module_uuid_demo(
    request: Request,
    add_module_uuid_demo: Module_uuid_demoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_module_uuid_demo.create_by = current_user.user.user_name
    add_module_uuid_demo.create_time = datetime.now()
    add_module_uuid_demo.update_by = current_user.user.user_name
    add_module_uuid_demo.update_time = datetime.now()
    logger.info(add_module_uuid_demo.model_dump())
    add_module_uuid_demo_result = await Module_uuid_demoService.add_module_uuid_demo_services(query_db, add_module_uuid_demo)
    logger.info(add_module_uuid_demo_result.message)

    return ResponseUtil.success(msg=add_module_uuid_demo_result.message)


@module_uuid_demoController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('uuid_demo:module_uuid_demo:edit'))],
    summary='修改UUID主键业务示例',
    description='根据主键更新UUID主键业务示例信息',
)
@ValidateFields(validate_model='edit_module_uuid_demo')
# @Log(title='UUID主键业务示例', business_type=BusinessType.UPDATE)
async def edit_uuid_demo_module_uuid_demo(
    request: Request,
    edit_module_uuid_demo: Module_uuid_demoModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_module_uuid_demo.model_dump())
    edit_module_uuid_demo.update_by = current_user.user.user_name
    edit_module_uuid_demo.update_time = datetime.now()
    edit_module_uuid_demo_result = await Module_uuid_demoService.edit_module_uuid_demo_services(query_db, edit_module_uuid_demo)
    logger.info(edit_module_uuid_demo_result.message)

    return ResponseUtil.success(msg=edit_module_uuid_demo_result.message)


@module_uuid_demoController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('uuid_demo:module_uuid_demo:remove'))],
    summary='删除UUID主键业务示例',
    description='根据主键批量删除UUID主键业务示例记录，多个主键以逗号分隔',
)
# @Log(title='UUID主键业务示例', business_type=BusinessType.DELETE)
async def delete_uuid_demo_module_uuid_demo(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_module_uuid_demo = DeleteModule_uuid_demoModel(ids=ids)
    logger.info(delete_module_uuid_demo.model_dump())
    delete_module_uuid_demo_result = await Module_uuid_demoService.delete_module_uuid_demo_services(query_db, delete_module_uuid_demo)
    logger.info(delete_module_uuid_demo_result.message)

    return ResponseUtil.success(msg=delete_module_uuid_demo_result.message)


@module_uuid_demoController.get(
    '/{id}',
    response_model=Module_uuid_demoModel,
    dependencies=[Depends(CheckUserInterfaceAuth('uuid_demo:module_uuid_demo:query'))],
    summary='获取UUID主键业务示例详情',
    description='根据主键获取UUID主键业务示例详细信息',
)
async def query_detail_uuid_demo_module_uuid_demo(request: Request, id: str, query_db: AsyncSession = Depends(get_db)):
    logger.info(f'id:{id}')
    module_uuid_demo_detail_result = await Module_uuid_demoService.module_uuid_demo_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=module_uuid_demo_detail_result)


@module_uuid_demoController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('uuid_demo:module_uuid_demo:export'))],
    summary='导出UUID主键业务示例',
    description='根据查询条件导出UUID主键业务示例列表数据到Excel文件',
)
# @Log(title='UUID主键业务示例', business_type=BusinessType.EXPORT)
async def export_uuid_demo_module_uuid_demo_list(
    request: Request,
    module_uuid_demo_page_query: Module_uuid_demoPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    module_uuid_demo_query_result = await Module_uuid_demoService.get_module_uuid_demo_list_services(query_db, module_uuid_demo_page_query, is_page=False)
    module_uuid_demo_export_result = await Module_uuid_demoService.export_module_uuid_demo_list_services(module_uuid_demo_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(module_uuid_demo_export_result))
