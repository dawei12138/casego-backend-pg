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
from module_admin.api_testing.api_formdata.service.formdata_service import FormdataService
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import DeleteFormdataModel, FormdataModel, \
    FormdataPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

formdataController = APIRouter(prefix='/api_formdata/formdata', dependencies=[Depends(LoginService.get_current_user)])


@formdataController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_formdata:formdata:list'))]
)
async def get_api_formdata_formdata_list(
        request: Request,
        formdata_page_query: FormdataPageQueryModel = Depends(FormdataPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(formdata_page_query.model_dump())
    # 获取分页数据
    formdata_page_query_result = await FormdataService.get_formdata_list_services(query_db, formdata_page_query,
                                                                                  is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=formdata_page_query_result)


@formdataController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_formdata:formdata:add'))])
@ValidateFields(validate_model='add_formdata')
# @Log(title='接口单body', business_type=BusinessType.INSERT)
async def add_api_formdata_formdata(
        request: Request,
        add_formdata: FormdataModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_formdata.create_by = current_user.user.user_name
    add_formdata.create_time = datetime.now()
    add_formdata.update_by = current_user.user.user_name
    add_formdata.update_time = datetime.now()
    logger.info(add_formdata.model_dump())
    add_formdata_result = await FormdataService.add_formdata_services(query_db, add_formdata)
    logger.info(add_formdata_result.message)

    return ResponseUtil.success(msg=add_formdata_result.message)


@formdataController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_formdata:formdata:edit'))])
@ValidateFields(validate_model='edit_formdata')
@Log(title='接口单body', business_type=BusinessType.UPDATE)
async def edit_api_formdata_formdata(
        request: Request,
        edit_formdata: FormdataModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_formdata.model_dump())
    edit_formdata.update_by = current_user.user.user_name
    edit_formdata.update_time = datetime.now()
    edit_formdata_result = await FormdataService.edit_formdata_services(query_db, edit_formdata)
    logger.info(edit_formdata_result.message)

    return ResponseUtil.success(msg=edit_formdata_result.message)


@formdataController.delete('/{formdata_ids}',
                           dependencies=[Depends(CheckUserInterfaceAuth('api_formdata:formdata:remove'))])
@Log(title='接口单body', business_type=BusinessType.DELETE)
async def delete_api_formdata_formdata(request: Request, formdata_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_formdata = DeleteFormdataModel(formdataIds=formdata_ids)
    logger.info(delete_formdata.model_dump())
    delete_formdata_result = await FormdataService.delete_formdata_services(query_db, delete_formdata)
    logger.info(delete_formdata_result.message)

    return ResponseUtil.success(msg=delete_formdata_result.message)


@formdataController.get(
    '/{formdata_id}', response_model=FormdataModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_formdata:formdata:query'))]
)
async def query_detail_api_formdata_formdata(request: Request, formdata_id: int,
                                             query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    formdata_detail_result = await FormdataService.formdata_detail_services(query_db, formdata_id)
    logger.info(f'获取formdata_id为{formdata_id}的信息成功')

    return ResponseUtil.success(data=formdata_detail_result)


@formdataController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_formdata:formdata:export'))])
@Log(title='接口单body', business_type=BusinessType.EXPORT)
async def export_api_formdata_formdata_list(
        request: Request,
        formdata_page_query: FormdataPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    formdata_query_result = await FormdataService.get_formdata_list_services(query_db, formdata_page_query,
                                                                             is_page=False)
    formdata_export_result = await FormdataService.export_formdata_list_services(formdata_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(formdata_export_result))
