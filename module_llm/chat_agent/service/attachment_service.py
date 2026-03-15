# -*- coding: utf-8 -*-
"""
聊天附件服务 —— 文件保存 + 多模态消息构造
"""
import base64
import mimetypes
import os
from datetime import datetime
from typing import List, Tuple

import aiofiles
from fastapi import UploadFile

from module_llm.chat_agent.entity.vo.chat_vo import (
    AttachmentMeta,
    CHAT_ATTACHMENT_MAX_SIZE,
    CHAT_ATTACHMENT_MAX_COUNT,
    CHAT_ATTACHMENT_ALLOWED_EXTS,
    CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS,
    CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS,
)
from module_llm.workspace.service.workspace_service import WorkspaceService
from utils.log_util import logger
from utils.sys_upload_util import UploadUtil

UPLOAD_SUBDIR = "upload"

# 文本文件最大读取字符数，超过则截断
MAX_TEXT_CHARS = 50_000


class AttachmentService:
    """聊天附件操作"""

    @staticmethod
    def _classify_extension(ext: str) -> str:
        """根据扩展名返回 'image' 或 'text'"""
        if ext in CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS:
            return "image"
        if ext in CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS:
            return "text"
        raise ValueError(f"不支持的文件类型: {ext}")

    @classmethod
    async def save_attachments(
        cls,
        user_id: int,
        thread_id: str,
        files: List[UploadFile],
    ) -> Tuple[List[AttachmentMeta], List[dict]]:
        """
        保存上传文件到 agent_workspace/{user_id}/{thread_id}/upload/

        :return: (成功列表, 失败列表)
        """
        if len(files) > CHAT_ATTACHMENT_MAX_COUNT:
            raise ValueError(f"每条消息最多附带 {CHAT_ATTACHMENT_MAX_COUNT} 个附件")

        workspace_path = WorkspaceService._resolve_workspace_path(user_id, thread_id)
        upload_dir = workspace_path / UPLOAD_SUBDIR
        upload_dir.mkdir(parents=True, exist_ok=True)

        successes: List[AttachmentMeta] = []
        failures: List[dict] = []

        for file in files:
            try:
                ext = UploadUtil.get_file_extension(file.filename or "")
                if ext not in CHAT_ATTACHMENT_ALLOWED_EXTS:
                    failures.append({"filename": file.filename, "error": f"不支持的文件类型: {ext}"})
                    continue

                file_type = cls._classify_extension(ext)

                content = await file.read()
                if len(content) > CHAT_ATTACHMENT_MAX_SIZE:
                    failures.append({"filename": file.filename, "error": "文件大小超过10MB限制"})
                    continue

                now = datetime.now()
                file_hash = UploadUtil.get_file_hash(content)[:8]
                random_suffix = UploadUtil.generate_random_number(4)
                stored_filename = f"{now.strftime('%Y%m%d%H%M%S')}_{file_hash}_{random_suffix}{ext}"
                stored_path = upload_dir / stored_filename

                async with aiofiles.open(stored_path, 'wb') as f:
                    await f.write(content)

                mime_type, _ = mimetypes.guess_type(file.filename or "")

                meta = AttachmentMeta(
                    filename=file.filename or stored_filename,
                    stored_name=f"{UPLOAD_SUBDIR}/{stored_filename}",
                    file_type=file_type,
                    mime_type=mime_type or "application/octet-stream",
                    size=len(content),
                )
                successes.append(meta)
                logger.info(f"附件保存成功: {file.filename} -> {stored_path}")

            except Exception as e:
                failures.append({"filename": file.filename, "error": str(e)})
                logger.warning(f"附件保存失败: {file.filename}, error={e}")

        return successes, failures

    @classmethod
    async def build_message_content(
        cls,
        message: str,
        attachments: List[AttachmentMeta],
        user_id: int,
        thread_id: str,
    ) -> Tuple[list, list]:
        """
        构造 LangChain 多模态 content blocks。

        - 图片 → base64 image_url block
        - 文本文件 → 内联 text block
        - 用户文本 → text block

        :return: (content_blocks, attachment_meta_dicts)
            content_blocks: 传给 HumanMessage.content
            attachment_meta_dicts: 传给 HumanMessage.additional_kwargs["attachments"]
        """
        blocks: list = []
        workspace_path = WorkspaceService._resolve_workspace_path(user_id, thread_id)
        meta_dicts: list = []

        for att in attachments:
            file_path = workspace_path / att.stored_name
            if not file_path.exists():
                logger.warning(f"附件文件不存在，跳过: {file_path}")
                continue

            try:
                if att.file_type == "image":
                    async with aiofiles.open(file_path, 'rb') as f:
                        raw = await f.read()
                    b64 = base64.b64encode(raw).decode('ascii')
                    blocks.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{att.mime_type};base64,{b64}"},
                    })

                elif att.file_type == "text":
                    async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        text_content = await f.read()
                    if len(text_content) > MAX_TEXT_CHARS:
                        text_content = text_content[:MAX_TEXT_CHARS] + f"\n... (truncated, {len(text_content)} chars total)"
                    blocks.append({
                        "type": "text",
                        "text": f"--- Content of {att.filename} ---\n{text_content}\n--- End of {att.filename} ---",
                    })

                meta_dicts.append(att.model_dump(by_alias=True))

            except Exception as e:
                logger.warning(f"处理附件失败: {att.filename}, error={e}")

        # 用户文本消息放最后
        if message:
            blocks.append({"type": "text", "text": message})

        return blocks, meta_dicts
