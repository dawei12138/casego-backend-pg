import mimetypes
from datetime import datetime
from typing import List, Tuple

import aiofiles
from fastapi import UploadFile

from module_llm.llm_run.entity.vo.attachment_vo import (
    AttachmentMeta,
    CHAT_ATTACHMENT_ALLOWED_EXTS,
    CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS,
    CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS,
    CHAT_ATTACHMENT_MAX_COUNT,
    CHAT_ATTACHMENT_MAX_SIZE,
)
from module_llm.workspace.service.workspace_service import WorkspaceService
from utils.log_util import logger
from utils.sys_upload_util import UploadUtil

UPLOAD_SUBDIR = 'upload'


class AttachmentService:
    @staticmethod
    def _classify_extension(ext: str) -> str:
        if ext in CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS:
            return 'image'
        if ext in CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS:
            return 'text'
        raise ValueError(f'不支持的文件类型: {ext}')

    @classmethod
    async def save_attachments(
        cls,
        user_id: int,
        thread_id: str,
        files: List[UploadFile],
    ) -> Tuple[List[AttachmentMeta], List[dict]]:
        if len(files) > CHAT_ATTACHMENT_MAX_COUNT:
            raise ValueError(f'每条消息最多附带 {CHAT_ATTACHMENT_MAX_COUNT} 个附件')

        workspace_path = WorkspaceService._resolve_workspace_path(user_id, thread_id)
        upload_dir = workspace_path / UPLOAD_SUBDIR
        upload_dir.mkdir(parents=True, exist_ok=True)

        successes: List[AttachmentMeta] = []
        failures: List[dict] = []

        for file in files:
            try:
                ext = UploadUtil.get_file_extension(file.filename or '')
                if ext not in CHAT_ATTACHMENT_ALLOWED_EXTS:
                    failures.append({'filename': file.filename, 'error': f'不支持的文件类型: {ext}'})
                    continue

                file_type = cls._classify_extension(ext)
                content = await file.read()
                if len(content) > CHAT_ATTACHMENT_MAX_SIZE:
                    failures.append({'filename': file.filename, 'error': '文件大小超过10MB限制'})
                    continue

                now = datetime.now()
                file_hash = UploadUtil.get_file_hash(content)[:8]
                random_suffix = UploadUtil.generate_random_number(4)
                stored_filename = f"{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{random_suffix}{ext}"
                stored_path = upload_dir / stored_filename

                async with aiofiles.open(stored_path, 'wb') as f:
                    await f.write(content)

                mime_type, _ = mimetypes.guess_type(file.filename or '')
                successes.append(
                    AttachmentMeta(
                        filename=file.filename or stored_filename,
                        stored_name=f'{UPLOAD_SUBDIR}/{stored_filename}',
                        file_type=file_type,
                        mime_type=mime_type or 'application/octet-stream',
                        size=len(content),
                    )
                )
            except Exception as e:
                failures.append({'filename': file.filename, 'error': str(e)})
                logger.warning(f'附件保存失败: {file.filename}, error={e}')

        return successes, failures
