import json
import mimetypes
import os
import time
from datetime import datetime
from typing import AsyncGenerator, List, Optional
import asyncio

import aiofiles
import httpx
from fastapi import BackgroundTasks, UploadFile, File, HTTPException
import aiohttp

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from config.get_httpclient import get_http_client
from module_admin.api_testing.api_test_cases.dao.test_cases_dao import Test_casesDao
from module_admin.api_testing.api_test_execution_log.entity.vo.execution_log_vo import Execution_logModel
from module_admin.api_testing.api_test_execution_log.service.execution_log_service import Execution_logService
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.entity.vo.file_vo import FileModel
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.file_service import FileService
from module_admin.system.service.login_service import LoginService
from module_admin.api_testing.api_test_cases.service.test_cases_service import Test_casesService
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import DeleteTest_casesModel, Test_casesModel, \
    Test_casesPageQueryModel, Test_casesAllParamsQueryModel, Test_casesExecModel, Test_cases_generator, \
    Test_casesImportModel
from utils.api_import.import_har import parse_har_to_requests
from utils.api_import.import_processor import (
    parse_to_preview,
    analyze_diff,
    execute_import,
    ImportConfig,
    ImportExecuteConfig,
    ModuleStrategy,
    ConflictStrategy,
    PreviewResult
)
from utils.api_import.import_har_processor import (
    har_parse_to_preview,
    har_execute_import,
    HarImportConfig,
    HarImportExecuteConfig
)
from utils.api_import.import_curl import parse_curl_command, CurlImportRequest
from utils.api_tools.executors.models import ExecutorContext

from utils.api_tools.executors.api_single_all_executor import api_single_all_executor
from utils.common_util import bytes2file_response, ensure_path_sep
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.sys_upload_util import UploadConfig, UploadResponse, UploadUtil, FileInfo

test_casesController = APIRouter(prefix='/api_test_cases/test_cases',
                                 dependencies=[Depends(LoginService.get_current_user)])


@test_casesController.post(
    '/importbyfile/{type}', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:list'))]
)
async def upload_files(
        request: Request,
        # import_test_cases: Test_casesImportModel,
        query_db: AsyncSession = Depends(get_db),
        file: Optional[List[UploadFile]] = File(None),  # 原有 form-data 上传
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
        targetModuleId: Optional[str] = Form(None),
        projectId: Optional[str] = Form(None),
        fileName: Optional[str] = Form(None),
        fileSize: Optional[int] = Form(None),
        fileType: Optional[str] = Form(None),
        uploadTime: Optional[str] = Form(None),
):

    content_type = request.headers.get("Content-Type", "")

    uploaded_files = []
    failed_files = []

    # 创建日期目录
    now = datetime.now()
    relative_path = f"files/{now.strftime('%Y')}/{now.strftime('%m')}/{now.strftime('%d')}"
    dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
    os.makedirs(dir_path, exist_ok=True)

    # ========= 1. multipart/form-data =========
    if "multipart/form-data" in content_type:
        if not file:
            raise HTTPException(status_code=400, detail="没有上传文件")

        if len(file) > 20:
            raise HTTPException(status_code=400, detail="批量上传文件数量不能超过20个")

        for file_item in file:
            try:
                content = await file_item.read()

                # 检查大小
                if len(content) > UploadConfig.MAX_FILE_SIZE:
                    failed_files.append({"filename": file_item.filename, "error": "文件大小超过限制"})
                    continue

                # 保存文件
                file_ext = UploadUtil.get_file_extension(file_item.filename)
                file_hash = UploadUtil.get_file_hash(content)[:8]
                unique_name = f"file_{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{UploadUtil.generate_random_number()}{file_ext}"
                file_path = os.path.join(dir_path, unique_name)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(content)

                file_url = f"{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{unique_name}"
                mime_type, _ = mimetypes.guess_type(file_item.filename)

                file_info = FileInfo(
                    filename=unique_name,
                    original_name=file_item.filename,
                    file_path=file_path.replace('\\', '/'),
                    file_url=file_url,
                    file_size=len(content),
                    file_type=mime_type or "application/octet-stream",
                    upload_time=now.isoformat()
                )

                add_file = FileModel(
                    original_name=file_item.filename,
                    stored_name=unique_name,
                    mime_type=mime_type,
                    file_size=len(content),
                    file_path=file_path.replace('\\', '/'),
                    file_url=file_url
                )
                add_file.create_by = current_user.user.user_name
                add_file.create_time = datetime.now()
                add_file.update_by = current_user.user.user_name
                add_file.update_time = datetime.now()
                await FileService.add_file_services(query_db, add_file)

                uploaded_files.append(file_info.dict())
                path = ensure_path_sep(
                    f"{file_url}")

                # 默认：过滤静态资源
                print("解析HAR文件...")
                har_requests = parse_har_to_requests(path)
                for testcase in har_requests:
                    add_test_cases = Test_casesModel()
                    add_test_cases.parent_submodule_id = targetModuleId
                    add_test_cases.create_by = current_user.user.user_name
                    add_test_cases.create_time = datetime.now()
                    add_test_cases.update_by = current_user.user.user_name
                    add_test_cases.update_time = datetime.now()
                    add_test_cases.project_id = projectId
                    add_test_cases.case_type = 1
                    add_test_cases_result = await Test_casesService.add_test_cases_services(query_db, add_test_cases)
                    testcase.case_id = add_test_cases_result.get('caseId')
                    edit_test_cases_result = await Test_casesService.edit_test_cases_services(query_db, testcase)
                print(f"共解析 {len(har_requests)} 个API请求\n")
            except Exception as e:
                logger.info(e)
                failed_files.append({"filename": file_item.filename, "error": str(e)})

    # ========= 2. binary/octet-stream =========
    # elif "application/octet-stream" in content_type or "binary/octet-stream" in content_type:

    # ========= 返回结果 =========
    return ResponseUtil.success(msg=CrudResponseModel(is_success=True, message='更新成功').message)


@test_casesController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:list'))]
)
async def get_api_test_cases_test_cases_list(
        request: Request,
        test_cases_page_query: Test_casesPageQueryModel = Depends(Test_casesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(test_cases_page_query.model_dump())
    # 获取分页数据
    test_cases_page_query_result = await Test_casesService.get_test_cases_list_services(query_db, test_cases_page_query,
                                                                                        is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=test_cases_page_query_result)


@test_casesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))])
@ValidateFields(validate_model='add_test_cases')
# @Log(title='接口用例', business_type=BusinessType.INSERT)
async def add_api_test_cases_test_cases(
        request: Request,
        add_test_cases: Test_casesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_test_cases.create_by = current_user.user.user_name
    add_test_cases.create_time = datetime.now()
    add_test_cases.update_by = current_user.user.user_name
    add_test_cases.update_time = datetime.now()
    logger.info(add_test_cases.model_dump())
    add_test_cases_result = await Test_casesService.add_test_cases_services(query_db, add_test_cases)
    logger.info(add_test_cases_result)

    return ResponseUtil.success(dict_content=add_test_cases_result)


@test_casesController.post('/sort', dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:edit'))])
@ValidateFields(validate_model='edit_test_cases')
async def edit_api_test_cases_test_cases(
        request: Request,
        edit_test_cases: List[Test_casesModel],
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    for i in edit_test_cases:
        i.update_by = current_user.user.user_name
        i.update_time = datetime.now()
        edit_test_cases = i.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', })
        await Test_casesDao.edit_test_cases_dao(query_db, edit_test_cases)
        # logger.info(edit_test_cases_result.message)
    await query_db.commit()
    return ResponseUtil.success(msg=CrudResponseModel(is_success=True, message='更新成功').message)


@test_casesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:edit'))])
@ValidateFields(validate_model='edit_test_cases')
async def edit_api_test_cases_test_cases(
        request: Request,
        edit_test_cases: Test_casesAllParamsQueryModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    start_time = time.time()  # 时间测试
    logger.info(edit_test_cases.model_dump(by_alias=False))
    edit_test_cases.update_by = current_user.user.user_name
    edit_test_cases.update_time = datetime.now()
    edit_test_cases_result = await Test_casesService.edit_test_cases_services(query_db, edit_test_cases)
    logger.info(edit_test_cases_result.message)
    acquire_time = time.time() - start_time
    logger.warning(f"执行保存耗时: {acquire_time:.3f}s")
    return ResponseUtil.success(msg=edit_test_cases_result.message)


async def _save_execution_log_background(case_id: int, res_json: str):
    """
    后台任务:保存执行日志

    :param case_id: 测试用例ID
    :param res_json: 执行结果JSON字符串
    """
    try:
        start_time = time.time()

        # 重新创建数据库会话(后台任务不能使用主请求的session)
        from config.database import async_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.asyncio import AsyncSession as NewAsyncSession

        async_session = sessionmaker(async_engine, class_=NewAsyncSession, expire_on_commit=False)

        async with async_session() as new_db:
            # 解析执行结果
            res_data = json.loads(res_json)

            # 构建日志模型
            log_model = Execution_logModel(
                case_id=case_id,
                execution_data=res_data,
                execution_time=res_data.get('response', {}).get('executionTime'),
                method=res_data.get('response', {}).get('requestMethod'),
                path=res_data.get('response', {}).get('requestUrl'),
                name=res_data.get('response', {}).get('caseName'),
                is_success=res_data.get('response', {}).get('isSuccess'),
                response_status_code=res_data.get('response', {}).get('responseStatusCode'),
                response_time=res_data.get('response', {}).get('responseTime'),
                assertion_success=res_data.get('asserionResult', {}).get('success'),
            )

            # 保存日志
            await Execution_logService.add_execution_log_services(new_db, log_model)

            acquire_time = time.time() - start_time
            logger.warning(f"后台保存日志耗时: {acquire_time:.3f}s")

    except Exception as e:
        logger.error(f"后台保存执行日志失败: {str(e)}")
        logger.exception(e)


@test_casesController.post('/exec', dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:edit'))])
@ValidateFields(validate_model='Test_casesExecModel')
# @Log(title='接口用例', business_type=BusinessType.UPDATE)
async def exec_api_test_cases(
        request: Request,
        exec_test_cases: Test_casesExecModel,
        background_tasks: BackgroundTasks,
        query_db: AsyncSession = Depends(get_db),
        session: AsyncGenerator[aiohttp.ClientSession, None] = Depends(get_http_client),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    start_time = time.time()  # 时间测试
    logger.info(exec_test_cases.model_dump())
    exec_test_cases.use_env_cookies = True
    context = ExecutorContext(
        user_id=current_user.user.user_id,
        env_id=exec_test_cases.env_id,
        case_id=exec_test_cases.case_id,
        mysql_obj=query_db,
        redis_obj=request.app.state.redis,
        variables={},
        parameterization={},
        session=session,
        use_env_cookies=exec_test_cases.use_env_cookies  # 传递环境Cookies开关参数
    )

    acquire_2time = time.time() - start_time
    logger.warning(f"执行接口一阶段耗时: {acquire_2time:.3f}s")

    start_2time = time.time()
    res = await api_single_all_executor(context)
    acquire_time = time.time() - start_2time
    logger.warning(f"执行接口二阶段耗时: {acquire_time:.3f}s")

    # 将日志记录添加到后台任务,异步执行
    res_json = res.model_dump_json(by_alias=True)
    background_tasks.add_task(_save_execution_log_background, exec_test_cases.case_id, res_json)

    logger.info("执行结果已返回,日志记录将在后台完成")

    return ResponseUtil.success(data=res)


@test_casesController.delete('/{case_ids}',
                             dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:remove'))])
# @Log(title='接口用例', business_type=BusinessType.DELETE)
async def delete_api_test_cases_test_cases(request: Request, case_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_test_cases = DeleteTest_casesModel(caseIds=case_ids)
    logger.info(delete_test_cases.model_dump())
    delete_test_cases_result = await Test_casesService.delete_test_cases_services(query_db, delete_test_cases)
    logger.info(delete_test_cases_result.message)

    return ResponseUtil.success(msg=delete_test_cases_result.message)


@test_casesController.get(
    '/{case_id}', response_model=Test_casesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:query'))]
)
async def query_detail_api_test_cases_test_cases(request: Request, case_id: int,
                                                 query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    test_cases_detail_result = await Test_casesService.test_cases_detail_services(query_db, case_id)
    logger.info(f'获取case_id为{case_id}的信息成功')

    return ResponseUtil.success(data=test_cases_detail_result)


@test_casesController.post('/copy', dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))])
@ValidateFields(validate_model='add_test_cases')
async def copy_api_test_cases_test_cases(
        request: Request,
        copy_test_cases: Test_casesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    copy_test_cases.create_by = current_user.user.user_name
    copy_test_cases.create_time = datetime.now()
    copy_test_cases.update_by = current_user.user.user_name
    copy_test_cases.update_time = datetime.now()
    logger.info(copy_test_cases.model_dump())
    add_test_cases_result = await Test_casesService.test_cases_copy_services(query_db, copy_test_cases)
    logger.info(add_test_cases_result)

    return ResponseUtil.success(dict_content=add_test_cases_result)


@test_casesController.post('/copy_to_case',
                           dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))])
@ValidateFields(validate_model='add_test_cases')
async def copy_to_case(
        request: Request,
        copy_test_cases: Test_casesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    copy_test_cases.create_by = current_user.user.user_name
    copy_test_cases.create_time = datetime.now()
    copy_test_cases.update_by = current_user.user.user_name
    copy_test_cases.update_time = datetime.now()
    logger.info(copy_test_cases.model_dump())
    add_test_cases_result = await Test_casesService.test_cases_copy_services(query_db, copy_test_cases,
                                                                             is_copy_to_case=True)
    logger.info(add_test_cases_result)

    return ResponseUtil.success(dict_content=add_test_cases_result)


async def run_workflow(payload: dict):
    url = "http://116.196.75.29:9080/v1/workflows/run"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer app-13qfsx5ntXnAbhSba0ILKcKk',
        'Accept': '*/*',
        'Host': '116.196.75.29:9080',
        'Connection': 'keep-alive'
    }
    async with httpx.AsyncClient(timeout=None) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            print("后台任务完成，返回结果：", response.text)
        except Exception as e:
            print("后台任务异常：", e)


@test_casesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:edit'))])
@ValidateFields(validate_model='edit_test_cases')
async def edit_api_test_cases_test_cases(
        request: Request,
        generator_test_cases: Test_cases_generator,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(generator_test_cases.model_dump(by_alias=False))
    generator_test_cases.user = current_user.user.user_name

    # 保存编辑记录
    # edit_test_cases_result = await Test_casesService.edit_test_cases_services(query_db, generator_test_cases)
    # logger.info(edit_test_cases_result.message)

    # 立刻返回，不等待外部耗时任务
    asyncio.create_task(run_workflow(generator_test_cases.model_dump()))

    return ResponseUtil.success(msg="用例生成外部任务已启动")


@test_casesController.post('/export',
                           dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:export'))])
# @Log(title='接口用例', business_type=BusinessType.EXPORT)
async def export_api_test_cases_test_cases_list(
        request: Request,
        test_cases_page_query: Test_casesPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    test_cases_query_result = await Test_casesService.get_test_cases_list_services(query_db, test_cases_page_query,
                                                                                   is_page=False)
    test_cases_export_result = await Test_casesService.export_test_cases_list_services(request, test_cases_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(test_cases_export_result))


# ==================== OpenAPI/Swagger 导入接口 ====================

@test_casesController.post(
    '/openapi/preview/url',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='从URL预览OpenAPI/Swagger接口'
)
async def preview_openapi_from_url(
        request: Request,
        url: str = Form(..., description='OpenAPI/Swagger规范的URL地址'),
        projectId: int = Form(..., description='目标项目ID'),
        targetModuleId: Optional[int] = Form(None, description='目标父模块ID'),
        moduleStrategy: str = Form('auto_match', description='模块策略: auto_match/create_all/target_only'),
        conflictStrategy: str = Form('smart_merge', description='冲突策略: skip/overwrite/smart_merge'),
        includeDeprecated: bool = Form(False, description='是否包含已废弃接口'),
        query_db: AsyncSession = Depends(get_db),
):
    """
    从URL预览OpenAPI/Swagger接口列表

    - 支持 OpenAPI 3.0、3.1 和 Swagger 2.0 格式
    - 返回树形结构的预览数据，与现有数据进行对比
    """
    try:
        config = ImportConfig(
            project_id=projectId,
            target_module_id=targetModuleId,
            module_strategy=ModuleStrategy(moduleStrategy),
            conflict_strategy=ConflictStrategy(conflictStrategy),
            include_deprecated=includeDeprecated
        )

        # Step 1: 解析为预览
        preview = parse_to_preview(url, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 2: 与数据库对比
        preview = await analyze_diff(preview, query_db, config)

        return ResponseUtil.success(data=preview.data, msg=preview.msg)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'预览失败: {str(e)}')


@test_casesController.post(
    '/openapi/preview/file',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='从文件预览OpenAPI/Swagger接口'
)
async def preview_openapi_from_file(
        request: Request,
        file: UploadFile = File(..., description='OpenAPI/Swagger规范文件（JSON或YAML）'),
        projectId: int = Form(..., description='目标项目ID'),
        targetModuleId: Optional[int] = Form(None, description='目标父模块ID'),
        moduleStrategy: str = Form('auto_match', description='模块策略: auto_match/create_all/target_only'),
        conflictStrategy: str = Form('smart_merge', description='冲突策略: skip/overwrite/smart_merge'),
        includeDeprecated: bool = Form(False, description='是否包含已废弃接口'),
        query_db: AsyncSession = Depends(get_db),
):
    """
    从文件预览OpenAPI/Swagger接口列表

    - 支持 JSON 和 YAML 格式文件
    - 支持 OpenAPI 3.0、3.1 和 Swagger 2.0 格式
    """
    try:
        # 保存上传的文件到临时位置
        now = datetime.now()
        relative_path = f"temp/{now.strftime('%Y%m%d')}"
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        os.makedirs(dir_path, exist_ok=True)

        # 获取文件扩展名
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.json', '.yaml', '.yml']:
            return ResponseUtil.failure(msg='只支持 JSON 和 YAML 格式文件')

        # 保存文件
        unique_name = f"openapi_{now.strftime('%Y%m%d%H%M%S')}_{UploadUtil.generate_random_number()}{file_ext}"
        file_path = os.path.join(dir_path, unique_name)

        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        config = ImportConfig(
            project_id=projectId,
            target_module_id=targetModuleId,
            module_strategy=ModuleStrategy(moduleStrategy),
            conflict_strategy=ConflictStrategy(conflictStrategy),
            include_deprecated=includeDeprecated
        )

        # Step 1: 解析为预览
        preview = parse_to_preview(file_path, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 2: 与数据库对比
        preview = await analyze_diff(preview, query_db, config)

        # 清理临时文件
        try:
            os.remove(file_path)
        except:
            pass

        return ResponseUtil.success(data=preview.data, msg=preview.msg)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'预览失败: {str(e)}')


@test_casesController.post(
    '/openapi/import/url',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='从URL导入OpenAPI/Swagger接口'
)
async def import_openapi_from_url(
        request: Request,
        url: str = Form(..., description='OpenAPI/Swagger规范的URL地址'),
        projectId: int = Form(..., description='目标项目ID'),
        targetModuleId: Optional[int] = Form(None, description='目标父模块ID'),
        moduleStrategy: str = Form('auto_match', description='模块策略: auto_match/create_all/target_only'),
        conflictStrategy: str = Form('smart_merge', description='冲突策略: skip/overwrite/smart_merge'),
        includeDeprecated: bool = Form(False, description='是否包含已废弃接口'),
        importHeaders: bool = Form(True, description='是否导入headers'),
        importParams: bool = Form(True, description='是否导入params'),
        importBody: bool = Form(True, description='是否导入请求体'),
        importCookies: bool = Form(True, description='是否导入cookies'),
        selectedModules: Optional[str] = Form(None, description='选中的模块名称，逗号分隔，为空表示全选'),
        selectedApis: Optional[str] = Form(None, description='选中的接口标识，逗号分隔，为空表示全选'),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    从URL导入OpenAPI/Swagger接口到数据库

    - 支持 OpenAPI 3.0、3.1 和 Swagger 2.0 格式
    - 支持选择性导入（通过 selectedModules 和 selectedApis）
    - 支持三种冲突处理策略：skip（跳过）、overwrite（覆盖）、smart_merge（智能合并）
    """
    try:
        # 解析选中的模块和接口
        selected_modules_list = None
        if selectedModules:
            selected_modules_list = [s.strip() for s in selectedModules.split(',') if s.strip()]

        selected_apis_list = None
        if selectedApis:
            selected_apis_list = [s.strip() for s in selectedApis.split(',') if s.strip()]

        config = ImportExecuteConfig(
            project_id=projectId,
            target_module_id=targetModuleId,
            module_strategy=ModuleStrategy(moduleStrategy),
            conflict_strategy=ConflictStrategy(conflictStrategy),
            include_deprecated=includeDeprecated,
            import_headers=importHeaders,
            import_params=importParams,
            import_body=importBody,
            import_cookies=importCookies,
            selected_modules=selected_modules_list,
            selected_apis=selected_apis_list
        )

        # Step 1: 解析为预览
        preview = parse_to_preview(url, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 2: 与数据库对比
        preview = await analyze_diff(preview, query_db, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 3: 执行导入
        result = await execute_import(preview, query_db, config)

        if result.success:
            return ResponseUtil.success(
                data=result.data.model_dump(by_alias=True),
                msg=f"导入成功：创建 {result.data.modules_created} 个模块，"
                    f"新增 {result.data.apis_created} 个接口，"
                    f"更新 {result.data.apis_updated} 个接口，"
                    f"跳过 {result.data.apis_skipped} 个接口"
            )
        else:
            return ResponseUtil.failure(msg=result.msg)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'导入失败: {str(e)}')


@test_casesController.post(
    '/openapi/import/file',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='从文件导入OpenAPI/Swagger接口'
)
async def import_openapi_from_file(
        request: Request,
        file: UploadFile = File(..., description='OpenAPI/Swagger规范文件（JSON或YAML）'),
        projectId: int = Form(..., description='目标项目ID'),
        targetModuleId: Optional[int] = Form(None, description='目标父模块ID'),
        moduleStrategy: str = Form('auto_match', description='模块策略: auto_match/create_all/target_only'),
        conflictStrategy: str = Form('smart_merge', description='冲突策略: skip/overwrite/smart_merge'),
        includeDeprecated: bool = Form(False, description='是否包含已废弃接口'),
        importHeaders: bool = Form(True, description='是否导入headers'),
        importParams: bool = Form(True, description='是否导入params'),
        importBody: bool = Form(True, description='是否导入请求体'),
        importCookies: bool = Form(True, description='是否导入cookies'),
        selectedModules: Optional[str] = Form(None, description='选中的模块名称，逗号分隔，为空表示全选'),
        selectedApis: Optional[str] = Form(None, description='选中的接口标识，逗号分隔，为空表示全选'),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    从文件导入OpenAPI/Swagger接口到数据库

    - 支持 JSON 和 YAML 格式文件
    - 支持 OpenAPI 3.0、3.1 和 Swagger 2.0 格式
    - 支持选择性导入（通过 selectedModules 和 selectedApis）
    """
    try:
        # 保存上传的文件到临时位置
        now = datetime.now()
        relative_path = f"temp/{now.strftime('%Y%m%d')}"
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        os.makedirs(dir_path, exist_ok=True)

        # 获取文件扩展名
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.json', '.yaml', '.yml']:
            return ResponseUtil.failure(msg='只支持 JSON 和 YAML 格式文件')

        # 保存文件
        unique_name = f"openapi_{now.strftime('%Y%m%d%H%M%S')}_{UploadUtil.generate_random_number()}{file_ext}"
        file_path = os.path.join(dir_path, unique_name)

        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        # 解析选中的模块和接口
        selected_modules_list = None
        if selectedModules:
            selected_modules_list = [s.strip() for s in selectedModules.split(',') if s.strip()]

        selected_apis_list = None
        if selectedApis:
            selected_apis_list = [s.strip() for s in selectedApis.split(',') if s.strip()]

        config = ImportExecuteConfig(
            project_id=projectId,
            target_module_id=targetModuleId,
            module_strategy=ModuleStrategy(moduleStrategy),
            conflict_strategy=ConflictStrategy(conflictStrategy),
            include_deprecated=includeDeprecated,
            import_headers=importHeaders,
            import_params=importParams,
            import_body=importBody,
            import_cookies=importCookies,
            selected_modules=selected_modules_list,
            selected_apis=selected_apis_list
        )

        # Step 1: 解析为预览
        preview = parse_to_preview(file_path, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 2: 与数据库对比
        preview = await analyze_diff(preview, query_db, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 3: 执行导入
        result = await execute_import(preview, query_db, config)

        # 清理临时文件
        try:
            os.remove(file_path)
        except:
            pass

        if result.success:
            return ResponseUtil.success(
                data=result.data.model_dump(by_alias=True),
                msg=f"导入成功：创建 {result.data.modules_created} 个模块，"
                    f"新增 {result.data.apis_created} 个接口，"
                    f"更新 {result.data.apis_updated} 个接口，"
                    f"跳过 {result.data.apis_skipped} 个接口"
            )
        else:
            return ResponseUtil.failure(msg=result.msg)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'导入失败: {str(e)}')


# ==================== HAR 文件导入接口 ====================

@test_casesController.post(
    '/har/preview',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='预览HAR文件接口'
)
async def preview_har_file(
        request: Request,
        file: UploadFile = File(..., description='HAR文件'),
        projectId: int = Form(..., description='目标项目ID'),
        targetModuleId: Optional[int] = Form(None, description='目标模块ID，为空则创建新模块'),
        moduleName: Optional[str] = Form(None, description='新模块名称'),
        importHeaders: bool = Form(True, description='是否导入headers'),
        importParams: bool = Form(True, description='是否导入params'),
        importBody: bool = Form(True, description='是否导入请求体'),
        importCookies: bool = Form(True, description='是否导入cookies'),
        filterStatic: bool = Form(True, description='是否过滤静态资源'),
        allowedMethods: Optional[str] = Form(None, description='允许的HTTP方法，逗号分隔'),
        includeDomains: Optional[str] = Form(None, description='只包含的域名，逗号分隔'),
        urlKeywords: Optional[str] = Form(None, description='URL关键词过滤，逗号分隔'),
        query_db: AsyncSession = Depends(get_db),
):
    """
    预览HAR文件接口列表

    - 支持标准 HAR 格式文件
    - 默认过滤静态资源（图片、CSS、JS等）
    - 返回接口列表供用户选择
    """
    try:
        # 验证文件类型
        if not file.filename.lower().endswith('.har'):
            return ResponseUtil.failure(msg='只支持 .har 格式文件')

        # 保存上传的文件到临时位置
        now = datetime.now()
        relative_path = f"temp/{now.strftime('%Y%m%d')}"
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        os.makedirs(dir_path, exist_ok=True)

        unique_name = f"har_{now.strftime('%Y%m%d%H%M%S')}_{UploadUtil.generate_random_number()}.har"
        file_path = os.path.join(dir_path, unique_name)

        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        # 解析参数列表
        allowed_methods_list = None
        if allowedMethods:
            allowed_methods_list = [m.strip().upper() for m in allowedMethods.split(',') if m.strip()]

        include_domains_list = None
        if includeDomains:
            include_domains_list = [d.strip() for d in includeDomains.split(',') if d.strip()]

        url_keywords_list = None
        if urlKeywords:
            url_keywords_list = [k.strip() for k in urlKeywords.split(',') if k.strip()]

        config = HarImportConfig(
            project_id=projectId,
            target_module_id=targetModuleId,
            module_name=moduleName,
            import_headers=importHeaders,
            import_params=importParams,
            import_body=importBody,
            import_cookies=importCookies,
            filter_static=filterStatic,
            allowed_methods=allowed_methods_list,
            include_domains=include_domains_list,
            url_keywords=url_keywords_list
        )

        # 解析预览
        preview = har_parse_to_preview(file_path, file.filename, config)

        # 清理临时文件
        try:
            os.remove(file_path)
        except:
            pass

        if preview.success:
            return ResponseUtil.success(data=preview.data, msg=preview.msg)
        else:
            return ResponseUtil.failure(msg=preview.msg)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'预览失败: {str(e)}')


@test_casesController.post(
    '/har/import',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='导入HAR文件接口'
)
async def import_har_file(
        request: Request,
        file: UploadFile = File(..., description='HAR文件'),
        projectId: int = Form(..., description='目标项目ID'),
        targetModuleId: Optional[int] = Form(None, description='目标模块ID，为空则创建新模块'),
        moduleName: Optional[str] = Form(None, description='新模块名称'),
        importHeaders: bool = Form(True, description='是否导入headers'),
        importParams: bool = Form(True, description='是否导入params'),
        importBody: bool = Form(True, description='是否导入请求体'),
        importCookies: bool = Form(True, description='是否导入cookies'),
        filterStatic: bool = Form(True, description='是否过滤静态资源'),
        allowedMethods: Optional[str] = Form(None, description='允许的HTTP方法，逗号分隔'),
        includeDomains: Optional[str] = Form(None, description='只包含的域名，逗号分隔'),
        urlKeywords: Optional[str] = Form(None, description='URL关键词过滤，逗号分隔'),
        selectedApis: Optional[str] = Form(None, description='选中的接口标识，逗号分隔（格式: name::method）'),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    导入HAR文件接口到数据库

    - 支持标准 HAR 格式文件
    - 支持选择性导入（通过 selectedApis）
    - 所有接口均为新增，不进行更新操作
    """
    try:
        # 验证文件类型
        if not file.filename.lower().endswith('.har'):
            return ResponseUtil.failure(msg='只支持 .har 格式文件')

        # 保存上传的文件到临时位置
        now = datetime.now()
        relative_path = f"temp/{now.strftime('%Y%m%d')}"
        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
        os.makedirs(dir_path, exist_ok=True)

        unique_name = f"har_{now.strftime('%Y%m%d%H%M%S')}_{UploadUtil.generate_random_number()}.har"
        file_path = os.path.join(dir_path, unique_name)

        content = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        # 解析参数列表
        allowed_methods_list = None
        if allowedMethods:
            allowed_methods_list = [m.strip().upper() for m in allowedMethods.split(',') if m.strip()]

        include_domains_list = None
        if includeDomains:
            include_domains_list = [d.strip() for d in includeDomains.split(',') if d.strip()]

        url_keywords_list = None
        if urlKeywords:
            url_keywords_list = [k.strip() for k in urlKeywords.split(',') if k.strip()]

        selected_apis_list = None
        if selectedApis:
            selected_apis_list = [s.strip() for s in selectedApis.split(',') if s.strip()]

        config = HarImportExecuteConfig(
            project_id=projectId,
            target_module_id=targetModuleId,
            module_name=moduleName,
            import_headers=importHeaders,
            import_params=importParams,
            import_body=importBody,
            import_cookies=importCookies,
            filter_static=filterStatic,
            allowed_methods=allowed_methods_list,
            include_domains=include_domains_list,
            url_keywords=url_keywords_list,
            selected_apis=selected_apis_list
        )

        # Step 1: 解析预览
        preview = har_parse_to_preview(file_path, file.filename, config)
        if not preview.success:
            return ResponseUtil.failure(msg=preview.msg)

        # Step 2: 执行导入
        result = await har_execute_import(preview, query_db, config)

        # 清理临时文件
        try:
            os.remove(file_path)
        except:
            pass

        if result.success:
            return ResponseUtil.success(
                data=result.data.model_dump(by_alias=True),
                msg=f"导入成功：新增 {result.data.apis_created} 个接口"
            )
        else:
            return ResponseUtil.failure(msg=result.msg)

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'导入失败: {str(e)}')


# ==================== cURL 导入接口 ====================

@test_casesController.post(
    '/curl/import',
    dependencies=[Depends(CheckUserInterfaceAuth('api_test_cases:test_cases:add'))],
    summary='从cURL命令导入接口'
)
async def import_curl_command(
        request: Request,
        curl_request: CurlImportRequest,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    从cURL命令导入接口

    - 支持 Bash 和 Windows CMD 两种格式
    - 自动识别请求方法、Headers、Cookies、请求体等
    - 创建后自动放入「快速创建」（无父模块）
    """
    try:
        # Step 1: 解析 cURL 命令
        parse_result = parse_curl_command(curl_request.curl_command)

        if not parse_result.success:
            return ResponseUtil.failure(msg=parse_result.msg)

        curl_data = parse_result.data

        # Step 2: 创建测试用例基础记录
        add_test_cases = Test_casesModel()
        add_test_cases.parent_submodule_id = None  # 直接放入快速创建
        add_test_cases.project_id = curl_request.project_id
        add_test_cases.case_type = "1"  # 接口类型
        add_test_cases.create_by = current_user.user.user_name
        add_test_cases.create_time = datetime.now()
        add_test_cases.update_by = current_user.user.user_name
        add_test_cases.update_time = datetime.now()

        add_result = await Test_casesService.add_test_cases_services(query_db, add_test_cases)

        # Step 3: 更新用例详细数据
        curl_data.case_id = add_result.get('caseId')
        await Test_casesService.edit_test_cases_services(query_db, curl_data)

        return ResponseUtil.success(
            data={'caseId': curl_data.case_id},
            msg=f'导入成功：创建接口「{curl_data.name}」'
        )

    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=f'cURL导入失败: {str(e)}')
