from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemModel, \
    DeleteApi_param_itemModel
from module_admin.api_workflow.api_param_item.service.api_param_item_service import Api_param_itemService
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_workflow.api_param_table.service.api_param_table_service import Api_param_tableService
from module_admin.api_workflow.api_param_table.entity.vo.api_param_table_vo import DeleteApi_param_tableModel, \
    Api_param_tableModel, Api_param_tablePageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

api_param_tableController = APIRouter(prefix='/api_param_table/table',
                                      dependencies=[Depends(LoginService.get_current_user)])


@api_param_tableController.put(
    '/row', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:list'))]
)
async def edit_item_api_paramitem(
        request: Request,
        edit_api_param_item: Api_param_itemModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_api_param_item.model_dump())
    edit_api_param_item.update_by = current_user.user.user_name
    edit_api_param_item.update_time = datetime.now()
    edit_api_param_item_result = await Api_param_itemService.edit_api_param_item_services(query_db, edit_api_param_item)
    logger.info(edit_api_param_item_result.message)

    return ResponseUtil.success(msg=edit_api_param_item_result.message)


@api_param_tableController.post(
    '/row', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:list'))]
)
async def edit_item_api_paramitem(
        request: Request,
        add_api_param_item: Api_param_itemModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_api_param_item.create_by = current_user.user.user_name
    add_api_param_item.create_time = datetime.now()
    add_api_param_item.update_by = current_user.user.user_name
    add_api_param_item.update_time = datetime.now()
    logger.info(add_api_param_item.model_dump())
    add_api_param_item_result = await Api_param_itemService.add_api_param_item_services(query_db, add_api_param_item)
    logger.info(add_api_param_item_result.message)

    return ResponseUtil.success(msg=add_api_param_item_result.message)


@api_param_tableController.delete(
    '/row/{key_ids}', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:list'))]
)
async def delete_item_api_param_item(request: Request, key_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_api_param_item = DeleteApi_param_itemModel(keyIds=key_ids)
    logger.info(delete_api_param_item.model_dump())
    delete_api_param_item_result = await Api_param_itemService.delete_api_param_item_services(query_db,
                                                                                              delete_api_param_item)
    logger.info(delete_api_param_item_result.message)

    return ResponseUtil.success(msg=delete_api_param_item_result.message)


@api_param_tableController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:list'))]
)
async def get_table_api_param_table_list(
        request: Request,
        api_param_table_page_query: Api_param_tablePageQueryModel = Depends(Api_param_tablePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(api_param_table_page_query.model_dump())
    # 获取分页数据
    api_param_table_page_query_result = await Api_param_tableService.get_api_param_table_list_services(query_db,
                                                                                                       api_param_table_page_query,
                                                                                                       is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=api_param_table_page_query_result)


@api_param_tableController.post('', dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:add'))])
@ValidateFields(validate_model='add_api_param_table')
# @Log(title='参数化数据主', business_type=BusinessType.INSERT)
async def add_table_api_param_table(
        request: Request,
        add_api_param_table: Api_param_tableModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_api_param_table.create_by = current_user.user.user_name
    add_api_param_table.create_time = datetime.now()
    add_api_param_table.update_by = current_user.user.user_name
    add_api_param_table.update_time = datetime.now()
    logger.info(add_api_param_table.model_dump())
    add_api_param_table_result = await Api_param_tableService.add_api_param_table_services(query_db,
                                                                                           add_api_param_table)
    logger.info(add_api_param_table_result.message)

    return ResponseUtil.success(msg=add_api_param_table_result.message)


@api_param_tableController.put('', dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:edit'))])
@ValidateFields(validate_model='edit_api_param_table')
# @Log(title='参数化数据主', business_type=BusinessType.UPDATE)
async def edit_table_api_param_table(
        request: Request,
        edit_api_param_table: Api_param_tableModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_api_param_table.model_dump())
    edit_api_param_table.update_by = current_user.user.user_name
    edit_api_param_table.update_time = datetime.now()
    edit_api_param_table_result = await Api_param_tableService.edit_api_param_table_services(query_db,
                                                                                             edit_api_param_table)
    logger.info(edit_api_param_table_result.message)

    return ResponseUtil.success(msg=edit_api_param_table_result.message)


@api_param_tableController.delete('/{parameterization_ids}',
                                  dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:remove'))])
# @Log(title='参数化数据主', business_type=BusinessType.DELETE)
async def delete_table_api_param_table(request: Request, parameterization_ids: str,
                                       query_db: AsyncSession = Depends(get_db)):
    delete_api_param_table = DeleteApi_param_tableModel(parameterizationIds=parameterization_ids)
    logger.info(delete_api_param_table.model_dump())
    delete_api_param_table_result = await Api_param_tableService.delete_api_param_table_services(query_db,
                                                                                                 delete_api_param_table)
    logger.info(delete_api_param_table_result.message)

    return ResponseUtil.success(msg=delete_api_param_table_result.message)


@api_param_tableController.get(
    '/{parameterization_id}', response_model=Api_param_tableModel,
    dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:query'))]
)
async def query_detail_table_api_param_table(request: Request, parameterization_id: int,
                                             api_param_table_page_query: Api_param_tablePageQueryModel = Depends(
                                                 Api_param_tablePageQueryModel.as_query),
                                             query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    api_param_table_detail_result = await Api_param_tableService.api_param_table_detail_all_services(query_db,
                                                                                                     parameterization_id,
                                                                                                     api_param_table_page_query)
    logger.info(f'获取parameterization_id为{parameterization_id}的信息成功')

    return ResponseUtil.success(data=api_param_table_detail_result)


@api_param_tableController.post('/export',
                                dependencies=[Depends(CheckUserInterfaceAuth('table:api_param_table:export'))])
# @Log(title='参数化数据主', business_type=BusinessType.EXPORT)
async def export_table_api_param_table_list(
        request: Request,
        api_param_table_page_query: Api_param_tablePageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    api_param_table_query_result = await Api_param_tableService.get_api_param_table_list_services(query_db,
                                                                                                  api_param_table_page_query,
                                                                                                  is_page=False)
    api_param_table_export_result = await Api_param_tableService.export_api_param_table_list_services(
        api_param_table_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(api_param_table_export_result))
