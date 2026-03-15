from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_workflow.api_param_item.service.api_param_item_service import Api_param_itemService
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import DeleteApi_param_itemModel, \
    Api_param_itemModel, Api_param_itemPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

api_param_itemController = APIRouter(prefix='/api_param_item/item',
                                     dependencies=[Depends(LoginService.get_current_user)])


@api_param_itemController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('item:api_param_item:list'))]
)
async def get_item_api_param_item_list(
        request: Request,
        api_param_item_page_query: Api_param_itemPageQueryModel = Depends(Api_param_itemPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(api_param_item_page_query.model_dump())
    # 获取分页数据
    api_param_item_page_query_result = await Api_param_itemService.get_api_param_item_list_services(query_db,
                                                                                                    api_param_item_page_query,
                                                                                                    is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=api_param_item_page_query_result)


@api_param_itemController.post('', dependencies=[Depends(CheckUserInterfaceAuth('item:api_param_item:add'))])
@ValidateFields(validate_model='add_api_param_item')
# @Log(title='参数化数据行', business_type=BusinessType.INSERT)
async def add_item_api_param_item(
        request: Request,
        add_api_param_item: List[Api_param_itemModel],
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    for item in add_api_param_item:
        item.create_by = current_user.user.user_name
        item.create_time = datetime.now()
        item.update_by = current_user.user.user_name
        item.update_time = datetime.now()
        # logger.info(add_api_param_item.model_dump())
        add_api_param_item_result = await Api_param_itemService.add_api_param_item_services(query_db, item)
        # logger.info(add_api_param_item_result.message)

    return ResponseUtil.success(msg=CrudResponseModel(is_success=True, message='更新成功').message)


@api_param_itemController.put('', dependencies=[Depends(CheckUserInterfaceAuth('item:api_param_item:edit'))])
@ValidateFields(validate_model='edit_api_param_item')
# @Log(title='参数化数据行', business_type=BusinessType.UPDATE)
async def edit_item_api_param_item1(
        request: Request,
        edit_api_param_item: List[Api_param_itemModel],
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    # logger.info(edit_api_param_item.model_dump())
    for i in edit_api_param_item:
        i.update_by = current_user.user.user_name
        i.update_time = datetime.now()
        edit_api_param_item_result = await Api_param_itemService.edit_api_param_item_services(query_db, i)
        # logger.info(edit_api_param_item_result.message)

    return ResponseUtil.success(msg=CrudResponseModel(is_success=True, message='更新成功').message)


@api_param_itemController.delete('/{key_ids}',
                                 dependencies=[Depends(CheckUserInterfaceAuth('item:api_param_item:remove'))])
# @Log(title='参数化数据行', business_type=BusinessType.DELETE)
async def delete_item_api_param_item(request: Request, key_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_api_param_item = DeleteApi_param_itemModel(keyIds=key_ids)
    logger.info(delete_api_param_item.model_dump())
    delete_api_param_item_result = await Api_param_itemService.delete_api_param_item_services(query_db,
                                                                                              delete_api_param_item)
    logger.info(delete_api_param_item_result.message)

    return ResponseUtil.success(msg=delete_api_param_item_result.message)


@api_param_itemController.get(
    '/{key_id}', response_model=Api_param_itemModel,
    dependencies=[Depends(CheckUserInterfaceAuth('item:api_param_item:query'))]
)
async def query_detail_item_api_param_item(request: Request, key_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    api_param_item_detail_result = await Api_param_itemService.api_param_item_detail_services(query_db, key_id)
    logger.info(f'获取key_id为{key_id}的信息成功')

    return ResponseUtil.success(data=api_param_item_detail_result)


@api_param_itemController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('item:api_param_item:export'))])
# @Log(title='参数化数据行', business_type=BusinessType.EXPORT)
async def export_item_api_param_item_list(
        request: Request,
        api_param_item_page_query: Api_param_itemPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    api_param_item_query_result = await Api_param_itemService.get_api_param_item_list_services(query_db,
                                                                                               api_param_item_page_query,
                                                                                               is_page=False)
    api_param_item_export_result = await Api_param_itemService.export_api_param_item_list_services(
        api_param_item_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(api_param_item_export_result))
