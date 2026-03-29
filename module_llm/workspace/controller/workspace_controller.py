# -*- coding: utf-8 -*-
"""
工作区文件管理 - 控制器
"""
import mimetypes
from typing import List

from fastapi import APIRouter, Depends, Query, File, UploadFile
from fastapi.responses import FileResponse

from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_llm.llm_run.entity.vo.attachment_vo import ChatAttachmentUploadResponse
from module_llm.llm_run.service.attachment_service import AttachmentService
from module_llm.workspace.entity.vo.workspace_vo import (
    CreateFileRequest, CreateFolderRequest, DeleteRequest,
)
from module_llm.workspace.service.workspace_service import WorkspaceService
from utils.log_util import logger
from utils.response_util import ResponseUtil

workspaceController = APIRouter(
    prefix='/llm/workspace',
    dependencies=[Depends(LoginService.get_current_user)],
)


@workspaceController.get('/files', summary='列出工作区文件')
async def list_files(
    session_id: str = Query(..., alias='sessionId', description='会话ID'),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    result = await WorkspaceService.list_files(current_user.user.user_id, session_id)
    return ResponseUtil.success(data=result.model_dump(by_alias=True))


@workspaceController.get('/files/content', summary='读取文件内容')
async def read_file(
    session_id: str = Query(..., alias='sessionId', description='会话ID'),
    path: str = Query(..., description='文件相对路径'),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        result = await WorkspaceService.read_file(current_user.user.user_id, session_id, path)
        return ResponseUtil.success(data=result.model_dump(by_alias=True))
    except (FileNotFoundError, ValueError) as e:
        return ResponseUtil.failure(msg=str(e))


@workspaceController.get('/files/download', summary='下载文件')
async def download_file(
    session_id: str = Query(..., alias='sessionId', description='会话ID'),
    path: str = Query(..., description='文件相对路径'),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        file_path = WorkspaceService._resolve_workspace_path(
            current_user.user.user_id, session_id, path
        )
        if not file_path.exists() or not file_path.is_file():
            return ResponseUtil.failure(msg=f'文件不存在: {path}')

        mime_type, _ = mimetypes.guess_type(str(file_path))
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type=mime_type or 'application/octet-stream',
        )
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))


@workspaceController.post('/files', summary='创建文件')
async def create_file(
    request: CreateFileRequest,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        await WorkspaceService.create_file(
            current_user.user.user_id, request.session_id, request.path, request.content
        )
        return ResponseUtil.success(msg='文件创建成功')
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))


@workspaceController.delete('/files', summary='删除文件')
async def delete_file(
    request: DeleteRequest,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        await WorkspaceService.delete_file(
            current_user.user.user_id, request.session_id, request.path
        )
        return ResponseUtil.success(msg='文件删除成功')
    except (FileNotFoundError, ValueError) as e:
        return ResponseUtil.failure(msg=str(e))


@workspaceController.post('/folders', summary='创建文件夹')
async def create_folder(
    request: CreateFolderRequest,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        await WorkspaceService.create_folder(
            current_user.user.user_id, request.session_id, request.path
        )
        return ResponseUtil.success(msg='文件夹创建成功')
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))


@workspaceController.delete('/folders', summary='删除文件夹')
async def delete_folder(
    request: DeleteRequest,
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        await WorkspaceService.delete_folder(
            current_user.user.user_id, request.session_id, request.path
        )
        return ResponseUtil.success(msg='文件夹删除成功')
    except (FileNotFoundError, ValueError) as e:
        return ResponseUtil.failure(msg=str(e))


@workspaceController.post('/attachments/upload', summary='上传聊天附件')
async def upload_chat_attachments(
    session_id: str = Query(..., alias='sessionId', description='会话ID'),
    files: List[UploadFile] = File(..., description='附件文件列表，最多5个'),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        successes, failures = await AttachmentService.save_attachments(
            user_id=current_user.user.user_id,
            thread_id=session_id,
            files=files,
        )
        response = ChatAttachmentUploadResponse(
            attachments=successes,
            failed=failures,
        )
        return ResponseUtil.success(data=response.model_dump(by_alias=True))
    except ValueError as e:
        return ResponseUtil.failure(msg=str(e))
    except Exception as e:
        logger.error(f'附件上传失败: {e}')
        return ResponseUtil.failure(msg=f'附件上传失败: {str(e)}')
