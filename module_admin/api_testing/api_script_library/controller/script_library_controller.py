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
from module_admin.api_testing.api_script_library.service.script_library_service import Script_libraryService
from module_admin.api_testing.api_script_library.entity.vo.script_library_vo import (
    DeleteScript_libraryModel,
    Script_libraryModel,
    Script_libraryPageQueryModel,
    ExecuteScriptRequestModel,
    ExecuteScriptResponseModel,
    ScriptTypeEnum
)
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.api_tools.executors.js_script_control import execute_js_script_simple
from utils.api_tools.executors.py_script_control import execute_py_script_simple

script_libraryController = APIRouter(prefix='/api_script_library/script_library',
                                     dependencies=[Depends(LoginService.get_current_user)])


@script_libraryController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_script_library:script_library:list'))]
)
async def get_api_script_library_script_library_list(
        request: Request,
        script_library_page_query: Script_libraryPageQueryModel = Depends(Script_libraryPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(script_library_page_query.model_dump())
    # 获取分页数据
    script_library_page_query_result = await Script_libraryService.get_script_library_list_services(query_db,
                                                                                                    script_library_page_query,
                                                                                                    is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=script_library_page_query_result)


@script_libraryController.post('',
                               dependencies=[Depends(CheckUserInterfaceAuth('api_script_library:script_library:add'))])
@ValidateFields(validate_model='add_script_library')
# @Log(title='公共脚本库', business_type=BusinessType.INSERT)
async def add_api_script_library_script_library(
        request: Request,
        add_script_library: Script_libraryModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_script_library.create_by = current_user.user.user_name
    add_script_library.create_time = datetime.now()
    add_script_library.update_by = current_user.user.user_name
    add_script_library.update_time = datetime.now()
    logger.info(add_script_library.model_dump())
    add_script_library_result = await Script_libraryService.add_script_library_services(query_db, add_script_library)
    logger.info(add_script_library_result.message)

    return ResponseUtil.success(msg=add_script_library_result.message)


@script_libraryController.put('',
                              dependencies=[Depends(CheckUserInterfaceAuth('api_script_library:script_library:edit'))])
@ValidateFields(validate_model='edit_script_library')
# @Log(title='公共脚本库', business_type=BusinessType.UPDATE)
async def edit_api_script_library_script_library(
        request: Request,
        edit_script_library: Script_libraryModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_script_library.model_dump())
    edit_script_library.update_by = current_user.user.user_name
    edit_script_library.update_time = datetime.now()
    edit_script_library_result = await Script_libraryService.edit_script_library_services(query_db, edit_script_library)
    logger.info(edit_script_library_result.message)

    return ResponseUtil.success(msg=edit_script_library_result.message)


@script_libraryController.delete('/{script_ids}', dependencies=[
    Depends(CheckUserInterfaceAuth('api_script_library:script_library:remove'))])
# @Log(title='公共脚本库', business_type=BusinessType.DELETE)
async def delete_api_script_library_script_library(request: Request, script_ids: str,
                                                   query_db: AsyncSession = Depends(get_db)):
    delete_script_library = DeleteScript_libraryModel(scriptIds=script_ids)
    logger.info(delete_script_library.model_dump())
    delete_script_library_result = await Script_libraryService.delete_script_library_services(query_db,
                                                                                              delete_script_library)
    logger.info(delete_script_library_result.message)

    return ResponseUtil.success(msg=delete_script_library_result.message)


@script_libraryController.get(
    '/{script_id}', response_model=Script_libraryModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_script_library:script_library:query'))]
)
async def query_detail_api_script_library_script_library(request: Request, script_id: int,
                                                         query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    script_library_detail_result = await Script_libraryService.script_library_detail_services(query_db, script_id)
    logger.info(f'获取script_id为{script_id}的信息成功')

    return ResponseUtil.success(data=script_library_detail_result)


@script_libraryController.post('/export', dependencies=[
    Depends(CheckUserInterfaceAuth('api_script_library:script_library:export'))])
# @Log(title='公共脚本库', business_type=BusinessType.EXPORT)
async def export_api_script_library_script_library_list(
        request: Request,
        script_library_page_query: Script_libraryPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    script_library_query_result = await Script_libraryService.get_script_library_list_services(query_db,
                                                                                               script_library_page_query,
                                                                                               is_page=False)
    script_library_export_result = await Script_libraryService.export_script_library_list_services(
        script_library_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(script_library_export_result))


@script_libraryController.post(
    '/debug',
    response_model=ExecuteScriptResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_script_library:script_library:list'))]
)
async def execute_script(
        request: Request,
        execute_request: ExecuteScriptRequestModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    执行脚本库中的脚本或直接执行传入的脚本内容

    支持两种方式：
    1. 通过 script_id 执行已保存的脚本
    2. 直接传入 script_content 和 script_type 执行
    """
    script_content = execute_request.script_content
    script_type = execute_request.script_type

    # 如果传入了 script_id，从数据库获取脚本
    if execute_request.script_id:
        script_detail = await Script_libraryService.script_library_detail_services(
            query_db, execute_request.script_id
        )
        if not script_detail:
            return ResponseUtil.failure(msg="脚本不存在")
        script_content = script_detail.script_content
        script_type = script_detail.script_type

    # 验证脚本内容和类型
    if not script_content:
        return ResponseUtil.failure(msg="脚本内容不能为空")
    if not script_type:
        return ResponseUtil.failure(msg="脚本类型不能为空")

    logger.info(f"执行脚本，类型: {script_type}, 用户: {current_user.user.user_name}")

    # 根据脚本类型执行
    if script_type == ScriptTypeEnum.JAVASCRIPT:
        result = execute_js_script_simple(script_content)
    elif script_type == ScriptTypeEnum.PYTHON:
        result = execute_py_script_simple(
            script_content,
            env_id=execute_request.env_id or 0,
            user_id=current_user.user.user_id
        )
    else:
        return ResponseUtil.failure(msg=f"不支持的脚本类型: {script_type}")

    logger.info(f"脚本执行完成，成功: {result.get('success')}")

    return ResponseUtil.success(data=ExecuteScriptResponseModel(
        success=result.get("success", False),
        result=str(result.get("result")) if result.get("result") is not None else None,
        logs=result.get("logs"),
        error=result.get("error")
    ))
