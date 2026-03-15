import hashlib
import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import aiofiles
from starlette.responses import FileResponse
from fastapi import APIRouter, Depends, Form, Request, UploadFile, File, HTTPException
from pydantic import BaseModel
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.system.service.file_service import FileService
from module_admin.system.entity.vo.file_vo import DeleteFileModel, FileModel, FilePageQueryModel
from utils.common_util import bytes2file_response, ensure_path_sep
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.sys_upload_util import UploadResponse, UploadConfig, UploadUtil, FileInfo

fileController = APIRouter(prefix='/system/file', dependencies=[Depends(LoginService.get_current_user)])


@fileController.post("/upload", response_model=UploadResponse,
                     dependencies=[Depends(CheckUserInterfaceAuth('system:file:add'))])
async def upload_files(
        request: Request,
        query_db: AsyncSession = Depends(get_db),
        files: Optional[List[UploadFile]] = File(None),  # 原有 form-data 上传
        file_type: Optional[str] = None,  # 可选：指定文件类型限制
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
        filename: Optional[str] = None,  # binary 上传时必须提供文件名（可通过 query 传）
):
    """
    批量文件上传接口，支持 multipart/form-data 和 binary/octet-stream
    """
    try:
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
            if not files:
                raise HTTPException(status_code=400, detail="没有上传文件")

            if len(files) > 20:
                raise HTTPException(status_code=400, detail="批量上传文件数量不能超过20个")

            for file in files:
                try:
                    content = await file.read()

                    # 检查大小
                    if len(content) > UploadConfig.MAX_FILE_SIZE:
                        failed_files.append({"filename": file.filename, "error": "文件大小超过限制"})
                        continue

                    # 检查类型
                    if file_type and not UploadUtil.is_allowed_file(file.filename, file_type):
                        failed_files.append({"filename": file.filename, "error": "不支持的文件类型"})
                        continue

                    # 保存文件
                    file_ext = UploadUtil.get_file_extension(file.filename)
                    file_hash = UploadUtil.get_file_hash(content)[:8]
                    unique_name = f"file_{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{UploadUtil.generate_random_number()}{file_ext}"
                    file_path = os.path.join(dir_path, unique_name)
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(content)

                    file_url = f"{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{unique_name}"
                    mime_type, _ = mimetypes.guess_type(file.filename)

                    file_info = FileInfo(
                        filename=unique_name,
                        original_name=file.filename,
                        file_path=file_path.replace('\\', '/'),
                        file_url=file_url,
                        file_size=len(content),
                        file_type=mime_type or "application/octet-stream",
                        upload_time=now.isoformat()
                    )

                    add_file = FileModel(
                        original_name=file.filename,
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

                except Exception as e:
                    failed_files.append({"filename": file.filename, "error": str(e)})

        # ========= 2. binary/octet-stream =========
        # elif "application/octet-stream" in content_type or "binary/octet-stream" in content_type:
        else:
            content = await request.body()

            if not filename:
                raise HTTPException(status_code=400, detail="binary 上传必须提供 filename 参数")

            if len(content) > UploadConfig.MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="文件大小超过限制")

            if file_type and not UploadUtil.is_allowed_file(filename, file_type):
                raise HTTPException(status_code=400, detail="不支持的文件类型")

            # 保存文件
            file_ext = UploadUtil.get_file_extension(filename)
            file_hash = UploadUtil.get_file_hash(content)[:8]
            unique_name = f"file_{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{UploadUtil.generate_random_number()}{file_ext}"
            file_path = os.path.join(dir_path, unique_name)
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)

            file_url = f"{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{unique_name}"
            mime_type, _ = mimetypes.guess_type(filename)

            file_info = FileInfo(
                filename=unique_name,
                original_name=filename,
                file_path=file_path.replace('\\', '/'),
                file_url=file_url,
                file_size=len(content),
                file_type=mime_type or "application/octet-stream",
                upload_time=now.isoformat()
            )

            add_file = FileModel(
                original_name=filename,
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

        # else:
        #     raise HTTPException(status_code=415, detail="不支持的 Content-Type")

        # ========= 返回结果 =========
        if uploaded_files:
            message = f"成功上传 {len(uploaded_files)} 个文件"
            if failed_files:
                message += f"，{len(failed_files)} 个文件上传失败"
            return UploadResponse(success=True, message=message, data={
                "uploadedFiles": uploaded_files,
                "failedFiles": failed_files,
                "totalCount": (len(files) if files else 1),
                "successCount": len(uploaded_files),
                "failureCount": len(failed_files)
            })
        else:
            return UploadResponse(success=False, message="所有文件上传失败", data={
                "failedFiles": failed_files,
                "totalCount": (len(files) if files else 1),
                "successCount": 0,
                "failureCount": len(failed_files)
            })

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"批量上传失败: {str(e)}")


# @fileController.post("/upload", response_model=UploadResponse,
#                      dependencies=[Depends(CheckUserInterfaceAuth('system:file:add'))])
# async def upload_files(
#         request: Request,
#         query_db: AsyncSession = Depends(get_db),
#         files: List[UploadFile] = File(...),
#         file_type: Optional[str] = None,  # 可选：指定文件类型限制
#         current_user: CurrentUserModel = Depends(LoginService.get_current_user),
# ):
#     """
#     批量文件上传接口
#     """
#     try:
#         if not files:
#             raise HTTPException(status_code=400, detail="没有上传文件")
#
#         if len(files) > 20:  # 限制批量上传数量
#             raise HTTPException(status_code=400, detail="批量上传文件数量不能超过20个")
#
#         uploaded_files = []
#         failed_files = []
#
#         # 创建日期目录
#         now = datetime.now()
#         relative_path = f"files/{now.strftime('%Y')}/{now.strftime('%m')}/{now.strftime('%d')}"
#         dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)
#
#         try:
#             os.makedirs(dir_path, exist_ok=True)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"创建目录失败: {str(e)}")
#
#         for file in files:
#             try:
#                 # 读取文件内容
#                 content = await file.read()
#
#                 # 检查文件大小
#                 if len(content) > UploadConfig.MAX_FILE_SIZE:
#                     failed_files.append({
#                         "filename": file.filename,
#                         "error": "文件大小超过限制"
#                     })
#                     continue
#
#                 # 检查文件类型
#                 if file_type and not UploadUtil.is_allowed_file(file.filename, file_type):
#                     failed_files.append({
#                         "filename": file.filename,
#                         "error": "不支持的文件类型"
#                     })
#                     continue
#
#                 # 生成唯一文件名
#                 file_ext = UploadUtil.get_file_extension(file.filename)
#                 file_hash = UploadUtil.get_file_hash(content)[:8]  # 使用文件hash前8位
#                 unique_name = f"file_{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{UploadUtil.generate_random_number()}{file_ext}"
#                 file_path = os.path.join(dir_path, unique_name)
#
#                 # 保存文件
#                 async with aiofiles.open(file_path, 'wb') as f:
#                     await f.write(content)
#                 uniform_path = file_path.replace('\\', '/')
#
#                 # 构建文件信息
#                 file_url = f"{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{unique_name}"
#                 mime_type, _ = mimetypes.guess_type(file.filename)
#
#                 file_info = FileInfo(
#                     filename=unique_name,
#                     original_name=file.filename,
#                     file_path=uniform_path,
#                     file_url=file_url,
#                     file_size=len(content),
#                     file_type=mime_type or "application/octet-stream",
#                     upload_time=now.isoformat()
#                 )
#                 add_file = FileModel(original_name=file.filename, stored_name=unique_name, mime_type=mime_type,
#                                      file_size=len(content), file_path=uniform_path, file_url=file_url, )
#                 add_file.create_by = current_user.user.user_name
#                 add_file.create_time = datetime.now()
#                 add_file.update_by = current_user.user.user_name
#                 add_file.update_time = datetime.now()
#                 add_file_result = await FileService.add_file_services(query_db, add_file)
#                 uploaded_files.append(file_info.dict())
#
#             except Exception as e:
#                 failed_files.append({
#                     "filename": file.filename,
#                     "error": str(e)
#                 })
#
#         # 返回结果
#         if uploaded_files:
#             message = f"成功上传 {len(uploaded_files)} 个文件"
#             if failed_files:
#                 message += f"，{len(failed_files)} 个文件上传失败"
#
#             return UploadResponse(
#                 success=True,
#                 message=message,
#                 data={
#                     "uploadedFiles": uploaded_files,
#                     "failedFiles": failed_files,
#                     "totalCount": len(files),
#                     "successCount": len(uploaded_files),
#                     "failureCount": len(failed_files)
#                 }
#             )
#         else:
#             return UploadResponse(
#                 success=False,
#                 message="所有文件上传失败",
#                 data={
#                     "failedFiles": failed_files,
#                     "totalCount": len(files),
#                     "successCount": 0,
#                     "failureCount": len(failed_files)
#                 }
#             )
#
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"批量上传失败: {str(e)}")


@fileController.post("/upload/single", response_model=UploadResponse,
                     dependencies=[Depends(CheckUserInterfaceAuth('system:file:add'))])
async def upload_single_file(
        request: Request,
        file: UploadFile = File(...),
        file_type: Optional[str] = None,
        custom_path: Optional[str] = None  # 自定义保存路径
):
    """
    通用单文件上传接口
    """
    try:
        # 读取文件内容
        content = await file.read()

        # 检查文件大小
        if len(content) > UploadConfig.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="文件大小超过限制")

        # 检查文件类型
        if file_type and not UploadUtil.is_allowed_file(file.filename, file_type):
            raise HTTPException(status_code=400, detail="不支持的文件类型")

        # 创建目录
        now = datetime.now()
        if custom_path:
            relative_path = f"{custom_path}/{now.strftime('%Y')}/{now.strftime('%m')}"
        else:
            relative_path = f"files/{now.strftime('%Y')}/{now.strftime('%m')}/{now.strftime('%d')}"

        dir_path = os.path.join(UploadConfig.UPLOAD_PATH, relative_path)

        try:
            os.makedirs(dir_path, exist_ok=True)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建目录失败: {str(e)}")

        # 生成唯一文件名
        file_ext = UploadUtil.get_file_extension(file.filename)
        file_hash = UploadUtil.get_file_hash(content)[:8]
        unique_name = f"file_{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{UploadUtil.generate_random_number()}{file_ext}"
        file_path = os.path.join(dir_path, unique_name)

        # 保存文件
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        # 构建访问URL
        file_url = f"{UploadConfig.UPLOAD_PREFIX}/{relative_path}/{unique_name}"
        mime_type, _ = mimetypes.guess_type(file.filename)

        return UploadResponse(
            success=True,
            message="文件上传成功",
            data={
                "fileName": unique_name,
                "originalName": file.filename,
                "fileUrl": file_url,
                "filePath": file_path,
                "fileSize": len(content),
                "fileType": mime_type or "application/octet-stream",
                "uploadTime": now.isoformat()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")


# 配置
BASE_STORAGE_PATH = ensure_path_sep("/CaseGo/upload_path/files")  # 你的文件存储根目录


@fileController.get("/CaseGo/upload_path/files/{file_path:path}",
                    dependencies=[Depends(CheckUserInterfaceAuth('system:file:add'))])
async def serve_file(file_path: str, request: Request):
    """
    安全的文件访问服务

    Args:
        file_path: 文件相对路径
        request: FastAPI请求对象

    Returns:
        FileResponse: 文件响应
    """
    try:
        # 构建安全的文件路径
        requested_path = Path(file_path)

        # 防止路径遍历攻击
        if ".." in requested_path.parts:
            logger.warning(f"Path traversal attack attempted: {file_path}")
            raise HTTPException(status_code=400, detail="Invalid path")

        # 构建完整路径
        full_path = Path(BASE_STORAGE_PATH) / requested_path

        # 规范化路径并确保它在允许的目录内
        full_path = full_path.resolve()
        base_path = Path(BASE_STORAGE_PATH).resolve()

        if not str(full_path).startswith(str(base_path)):
            logger.warning(f"Access denied for path: {full_path}")
            raise HTTPException(status_code=403, detail="Access denied")

        # 检查文件是否存在且是文件
        if not full_path.exists():
            logger.info(f"File not found: {full_path}")
            raise HTTPException(status_code=404, detail="File not found")

        if not full_path.is_file():
            logger.warning(f"Not a file: {full_path}")
            raise HTTPException(status_code=400, detail="Not a file")

        # 获取文件信息
        file_size = full_path.stat().st_size
        file_name = full_path.name

        # 检查文件大小
        if file_size == 0:
            logger.warning(f"Empty file: {full_path}")
            raise HTTPException(status_code=404, detail="File is empty")

        # 自动检测MIME类型
        mime_type, _ = mimetypes.guess_type(str(full_path))
        if mime_type is None:
            mime_type = "application/octet-stream"

        # 打印调试信息
        logger.info(f"Serving file: {full_path}, size: {file_size}, mime_type: {mime_type}")

        # 检查是否支持Range请求（断点续传）
        range_header = request.headers.get('range')

        if range_header:
            return await serve_file_with_range(full_path, range_header, file_size, mime_type)

        # 返回完整文件 - 修复：确保所有必要参数都设置
        return FileResponse(
            path=str(full_path),  # 确保路径是字符串
            filename=file_name,  # 必须设置filename
            media_type=mime_type,  # 必须设置media_type
            headers={
                "Content-Length": str(file_size),
                "Accept-Ranges": "bytes",
                "Cache-Control": "public, max-age=3600",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error serving file {file_path}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def serve_file_with_range(
        file_path: Path,
        range_header: str,
        file_size: int,
        mime_type: str
) -> StreamingResponse:
    """
    处理Range请求（断点续传）
    """
    try:
        # 解析Range头
        range_match = range_header.replace('bytes=', '').split('-')
        start = int(range_match[0]) if range_match[0] else 0
        end = int(range_match[1]) if range_match[1] else file_size - 1

        # 验证范围
        if start >= file_size or end >= file_size or start > end:
            raise HTTPException(
                status_code=416,
                detail="Requested Range Not Satisfiable",
                headers={"Content-Range": f"bytes */{file_size}"}
            )

        content_length = end - start + 1

        async def file_streamer():
            async with aiofiles.open(file_path, 'rb') as file:
                await file.seek(start)
                remaining = content_length
                chunk_size = 8192

                while remaining > 0:
                    read_size = min(chunk_size, remaining)
                    chunk = await file.read(read_size)
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk

        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Cache-Control": "public, max-age=3600",
        }

        return StreamingResponse(
            file_streamer(),
            status_code=206,  # Partial Content
            media_type=mime_type,
            headers=headers
        )

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Range header")


@fileController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:file:list'))]
)
async def get_system_file_list(
        request: Request,
        file_page_query: FilePageQueryModel = Depends(FilePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(file_page_query.model_dump())
    # 参数交换，前端参数穿的有问题
    file_page_query.original_name, file_page_query.stored_name = file_page_query.stored_name, file_page_query.original_name

    # 获取分页数据
    file_page_query_result = await FileService.get_file_list_services(query_db, file_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=file_page_query_result)


@fileController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:file:add'))])
@ValidateFields(validate_model='add_file')
# @Log(title='附件管理', business_type=BusinessType.INSERT)
async def add_system_file(
        request: Request,
        add_file: FileModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_file.create_by = current_user.user.user_name
    add_file.create_time = datetime.now()
    add_file.update_by = current_user.user.user_name
    add_file.update_time = datetime.now()
    logger.info(add_file.model_dump())
    add_file_result = await FileService.add_file_services(query_db, add_file)
    logger.info(add_file_result.message)

    return ResponseUtil.success(msg=add_file_result.message)


@fileController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:file:edit'))])
@ValidateFields(validate_model='edit_file')
# @Log(title='附件管理', business_type=BusinessType.UPDATE)
async def edit_system_file(
        request: Request,
        edit_file: FileModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_file.model_dump())
    edit_file.update_by = current_user.user.user_name
    edit_file.update_time = datetime.now()
    edit_file_result = await FileService.edit_file_services(query_db, edit_file)
    logger.info(edit_file_result.message)

    return ResponseUtil.success(msg=edit_file_result.message)


@fileController.delete('/{file_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:file:remove'))])
# @Log(title='附件管理', business_type=BusinessType.DELETE)
async def delete_system_file(request: Request, file_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_file = DeleteFileModel(fileIds=file_ids)
    logger.info(delete_file.model_dump())
    delete_file_result = await FileService.delete_file_services(query_db, delete_file)
    logger.info(delete_file_result.message)

    return ResponseUtil.success(msg=delete_file_result.message)


# @fileController.get(
#     '/{file_id}', response_model=FileModel, dependencies=[Depends(CheckUserInterfaceAuth('system:file:query'))]
# )
# async def query_detail_system_file(request: Request, file_id: int, query_db: AsyncSession = Depends(get_db)):
#     logger.info(f"id:{id}")
#     file_detail_result = await FileService.file_detail_services(query_db, file_id)
#     logger.info(f'获取file_id为{file_id}的信息成功')
#
#     return ResponseUtil.success(data=file_detail_result)
@fileController.get(
    '/{file_id}', response_model=FileModel, dependencies=[Depends(CheckUserInterfaceAuth('system:file:query'))]
)
async def query_detail_system_file(request: Request, file_id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    file_detail_result = await FileService.file_detail_services(query_db, file_id)
    logger.info(f'获取file_id为{file_id}的信息成功')

    return ResponseUtil.success(data=file_detail_result)


@fileController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('system:file:export'))])
# @Log(title='附件管理', business_type=BusinessType.EXPORT)
async def export_system_file_list(
        request: Request,
        file_page_query: FilePageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    file_query_result = await FileService.get_file_list_services(query_db, file_page_query, is_page=False)
    file_export_result = await FileService.export_file_list_services(file_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(file_export_result))
