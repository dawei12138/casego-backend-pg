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
from module_app.elements.service.elements_service import ElementsService
from module_app.elements.entity.vo.elements_vo import DeleteElementsModel, ElementsModel, ElementsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


elementsController = APIRouter(prefix='/app/elements', dependencies=[Depends(LoginService.get_current_user)])


@elementsController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:elements:list'))],
    summary='获取控件元素列表',
    description='根据查询条件获取控件元素分页列表数据',
)
async def get_app_elements_list(
    request: Request,
elements_page_query: ElementsPageQueryModel = Depends(ElementsPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(elements_page_query.model_dump())
    # 获取分页数据
    elements_page_query_result = await ElementsService.get_elements_list_services(query_db, elements_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=elements_page_query_result)


@elementsController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:elements:add'))],
    summary='新增控件元素',
    description='创建一条新的控件元素记录',
)
@ValidateFields(validate_model='add_elements')
# @Log(title='控件元素', business_type=BusinessType.INSERT)
async def add_app_elements(
    request: Request,
    add_elements: ElementsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_elements.create_by = current_user.user.user_name
    add_elements.create_time = datetime.now()
    add_elements.update_by = current_user.user.user_name
    add_elements.update_time = datetime.now()
    logger.info(add_elements.model_dump())
    add_elements_result = await ElementsService.add_elements_services(query_db, add_elements)
    logger.info(add_elements_result.message)

    return ResponseUtil.success(msg=add_elements_result.message)


@elementsController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:elements:edit'))],
    summary='修改控件元素',
    description='根据主键更新控件元素信息',
)
@ValidateFields(validate_model='edit_elements')
# @Log(title='控件元素', business_type=BusinessType.UPDATE)
async def edit_app_elements(
    request: Request,
    edit_elements: ElementsModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_elements.model_dump())
    edit_elements.update_by = current_user.user.user_name
    edit_elements.update_time = datetime.now()
    edit_elements_result = await ElementsService.edit_elements_services(query_db, edit_elements)
    logger.info(edit_elements_result.message)

    return ResponseUtil.success(msg=edit_elements_result.message)


@elementsController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:elements:remove'))],
    summary='删除控件元素',
    description='根据主键批量删除控件元素记录，多个主键以逗号分隔',
)
# @Log(title='控件元素', business_type=BusinessType.DELETE)
async def delete_app_elements(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_elements = DeleteElementsModel(ids=ids)
    logger.info(delete_elements.model_dump())
    delete_elements_result = await ElementsService.delete_elements_services(query_db, delete_elements)
    logger.info(delete_elements_result.message)

    return ResponseUtil.success(msg=delete_elements_result.message)


@elementsController.get(
    '/{id}',
    response_model=ElementsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:elements:query'))],
    summary='获取控件元素详情',
    description='根据主键获取控件元素详细信息',
)
async def query_detail_app_elements(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    elements_detail_result = await ElementsService.elements_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=elements_detail_result)


@elementsController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:elements:export'))],
    summary='导出控件元素',
    description='根据查询条件导出控件元素列表数据到Excel文件',
)
# @Log(title='控件元素', business_type=BusinessType.EXPORT)
async def export_app_elements_list(
    request: Request,
    elements_page_query: ElementsPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    elements_query_result = await ElementsService.get_elements_list_services(query_db, elements_page_query, is_page=False)
    elements_export_result = await ElementsService.export_elements_list_services(elements_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(elements_export_result))
