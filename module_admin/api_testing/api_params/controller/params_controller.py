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
from module_admin.api_testing.api_params.service.params_service import ParamsService
from module_admin.api_testing.api_params.entity.vo.params_vo import DeleteParamsModel, ParamsModel, ParamsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

paramsController = APIRouter(prefix='/api_params/params', dependencies=[Depends(LoginService.get_current_user)])


@paramsController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('api_params:params:list'))]
)
async def get_api_params_params_list(
        request: Request,
        params_page_query: ParamsPageQueryModel = Depends(ParamsPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(params_page_query.model_dump())
    # 获取分页数据
    params_page_query_result = await ParamsService.get_params_list_services(query_db, params_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=params_page_query_result)


@paramsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_params:params:add'))])
@ValidateFields(validate_model='add_params')
# @Log(title='接口请求参数', business_type=BusinessType.INSERT)
async def add_api_params_params(
        request: Request,
        add_params: ParamsModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_params.create_by = current_user.user.user_name
    add_params.create_time = datetime.now()
    add_params.update_by = current_user.user.user_name
    add_params.update_time = datetime.now()
    logger.info(add_params.model_dump())
    add_params_result = await ParamsService.add_params_services(query_db, add_params)
    logger.info(add_params_result.message)

    return ResponseUtil.success(msg=add_params_result.message)


@paramsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_params:params:edit'))])
@ValidateFields(validate_model='edit_params')
@Log(title='接口请求参数', business_type=BusinessType.UPDATE)
async def edit_api_params_params(
        request: Request,
        edit_params: ParamsModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_params.model_dump())
    edit_params.update_by = current_user.user.user_name
    edit_params.update_time = datetime.now()
    edit_params_result = await ParamsService.edit_params_services(query_db, edit_params)
    logger.info(edit_params_result.message)

    return ResponseUtil.success(msg=edit_params_result.message)


@paramsController.delete('/{param_ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_params:params:remove'))])
@Log(title='接口请求参数', business_type=BusinessType.DELETE)
async def delete_api_params_params(request: Request, param_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_params = DeleteParamsModel(paramIds=param_ids)
    logger.info(delete_params.model_dump())
    delete_params_result = await ParamsService.delete_params_services(query_db, delete_params)
    logger.info(delete_params_result.message)

    return ResponseUtil.success(msg=delete_params_result.message)


@paramsController.get(
    '/{param_id}', response_model=ParamsModel, dependencies=[Depends(CheckUserInterfaceAuth('api_params:params:query'))]
)
async def query_detail_api_params_params(request: Request, param_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    params_detail_result = await ParamsService.params_detail_services(query_db, param_id)
    logger.info(f'获取param_id为{param_id}的信息成功')

    return ResponseUtil.success(data=params_detail_result)


@paramsController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_params:params:export'))])
@Log(title='接口请求参数', business_type=BusinessType.EXPORT)
async def export_api_params_params_list(
        request: Request,
        params_page_query: ParamsPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    params_query_result = await ParamsService.get_params_list_services(query_db, params_page_query, is_page=False)
    params_export_result = await ParamsService.export_params_list_services(params_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(params_export_result))
