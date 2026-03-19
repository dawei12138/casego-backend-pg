# -*- coding: utf-8 -*-
"""
工作区文件管理 - 服务层
"""
import base64
import mimetypes
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Union

import aiofiles

from module_admin.websocket.service.websocket_service import WebSocketService
from module_llm.workspace.entity.vo.workspace_vo import (
    FileEntryModel, FileTreeResponse, FileContentResponse, FileType,
)
from utils.log_util import logger

WORKSPACE_ROOT = os.path.join("CaseGo", "agent_workspace")

# 额外的文本 MIME 类型
_TEXT_MIME_EXTRAS = {
    'application/json', 'application/xml', 'application/javascript',
    'application/x-python-code', 'application/x-sh', 'application/sql',
    'application/yaml', 'application/x-yaml', 'application/toml',
}

# 文本文件扩展名（MIME 检测失败时的回退）
_TEXT_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.xml', '.yaml', '.yml',
    '.toml', '.md', '.txt', '.csv', '.sql', '.sh', '.bat', '.cmd',
    '.html', '.htm', '.css', '.scss', '.less', '.svg', '.ini', '.cfg',
    '.conf', '.env', '.gitignore', '.dockerfile', '.rs', '.go', '.java',
    '.c', '.cpp', '.h', '.hpp', '.rb', '.php', '.lua', '.r', '.swift',
    '.kt', '.kts', '.gradle', '.properties', '.log', '.vue',
}


class WorkspaceService:
    """工作区文件操作服务（含路径安全检查和 WebSocket 通知）"""

    @staticmethod
    def _resolve_workspace_path(user_id: int, thread_id: str, relative_path: str = '') -> Path:
        """
        解析并校验工作区路径，防止目录穿越。
        返回保证位于用户线程工作区内的绝对路径。
        """
        workspace = Path(WORKSPACE_ROOT) / str(user_id) / thread_id
        workspace = workspace.resolve()

        if relative_path:
            if '..' in relative_path.replace('\\', '/').split('/'):
                raise ValueError('路径不合法：不允许使用 ..')
            target = (workspace / relative_path).resolve()
        else:
            target = workspace

        if not str(target).startswith(str(workspace)):
            raise ValueError('路径不合法：超出工作区范围')

        return target

    @staticmethod
    def _is_text_file(file_path: str) -> bool:
        """判断文件是否为文本类型"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith('text/'):
                return True
            if mime_type in _TEXT_MIME_EXTRAS:
                return True
        ext = Path(file_path).suffix.lower()
        return ext in _TEXT_EXTENSIONS

    # ============ 查询操作 ============

    @classmethod
    async def list_files(cls, user_id: int, thread_id: str) -> FileTreeResponse:
        """列出线程工作区所有文件和目录（扁平列表）"""
        workspace = cls._resolve_workspace_path(user_id, thread_id)

        if not workspace.exists():
            return FileTreeResponse(thread_id=thread_id, files=[], total=0)

        entries = []
        for item in sorted(workspace.rglob('*')):
            rel_path = str(item.relative_to(workspace)).replace('\\', '/')
            stat = item.stat()
            is_file = item.is_file()
            mime_type = None
            if is_file:
                mime_type, _ = mimetypes.guess_type(str(item))
                mime_type = mime_type or 'application/octet-stream'
            entries.append(FileEntryModel(
                name=item.name,
                path=rel_path,
                type=FileType.DIRECTORY if item.is_dir() else FileType.FILE,
                size=stat.st_size if is_file else 0,
                mime_type=mime_type,
                created_time=datetime.fromtimestamp(stat.st_ctime),
                modified_time=datetime.fromtimestamp(stat.st_mtime),
            ))

        return FileTreeResponse(thread_id=thread_id, files=entries, total=len(entries))

    @classmethod
    async def read_file(cls, user_id: int, thread_id: str, path: str) -> FileContentResponse:
        """读取文件内容。文本文件返回 UTF-8 字符串，二进制文件返回 base64。"""
        file_path = cls._resolve_workspace_path(user_id, thread_id, path)

        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f'文件不存在: {path}')

        stat = file_path.stat()
        mime_type, _ = mimetypes.guess_type(str(file_path))
        mime_type = mime_type or 'application/octet-stream'
        is_binary = not cls._is_text_file(str(file_path))

        if is_binary:
            async with aiofiles.open(file_path, 'rb') as f:
                raw = await f.read()
            content = base64.b64encode(raw).decode('ascii')
        else:
            async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = await f.read()

        return FileContentResponse(
            name=file_path.name,
            path=path,
            content=content,
            is_binary=is_binary,
            mime_type=mime_type,
            size=stat.st_size,
        )

    # ============ 写操作（含 WebSocket 通知）============

    @classmethod
    async def create_file(cls, user_id: int, thread_id: str, path: str, content: str) -> None:
        """创建文件，自动创建父目录"""
        file_path = cls._resolve_workspace_path(user_id, thread_id, path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)

        await cls._notify_workspace_change(user_id, thread_id, 'file_created', path)

    @classmethod
    async def delete_file(cls, user_id: int, thread_id: str, path: str) -> None:
        """删除文件"""
        file_path = cls._resolve_workspace_path(user_id, thread_id, path)

        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f'文件不存在: {path}')

        file_path.unlink()
        await cls._notify_workspace_change(user_id, thread_id, 'file_deleted', path)

    @classmethod
    async def create_folder(cls, user_id: int, thread_id: str, path: str) -> None:
        """创建文件夹（含中间目录）"""
        dir_path = cls._resolve_workspace_path(user_id, thread_id, path)
        dir_path.mkdir(parents=True, exist_ok=True)
        await cls._notify_workspace_change(user_id, thread_id, 'folder_created', path)

    @classmethod
    async def delete_folder(cls, user_id: int, thread_id: str, path: str) -> None:
        """递归删除文件夹"""
        dir_path = cls._resolve_workspace_path(user_id, thread_id, path)

        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f'目录不存在: {path}')

        workspace = cls._resolve_workspace_path(user_id, thread_id)
        if dir_path == workspace:
            raise ValueError('不允许删除工作区根目录')

        shutil.rmtree(dir_path)
        await cls._notify_workspace_change(user_id, thread_id, 'folder_deleted', path)

    # ============ WebSocket 通知 ============

    @classmethod
    async def _notify_workspace_change(
        cls,
        user_id: Union[int, str],
        thread_id: str,
        action: str,
        path: str,
    ) -> None:
        """发送工作区文件变更 WebSocket 通知"""
        try:
            await WebSocketService.send_to_user(user_id, {
                'type': 'workspace_changed',
                'threadId': thread_id,
                'action': action,
                'path': path,
            })
        except Exception as e:
            logger.warning(f'工作区通知发送失败: {e}')

    @classmethod
    async def notify_agent_file_change(
        cls,
        user_id: Union[int, str],
        thread_id: str,
        tool_name: str = '',
    ) -> None:
        """
        Agent 工具执行后的文件变更通知（供 chat_controller 调用）。
        不需要精确路径，前端收到后刷新整个文件树即可。
        """
        try:
            await WebSocketService.send_to_user(user_id, {
                'type': 'workspace_changed',
                'threadId': thread_id,
                'action': 'agent_file_changed',
                'tool': tool_name,
            })
        except Exception as e:
            logger.warning(f'Agent 文件变更通知失败: {e}')
