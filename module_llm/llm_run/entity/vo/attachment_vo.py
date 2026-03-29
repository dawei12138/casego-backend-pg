from pydantic import BaseModel
from typing import List

CHAT_ATTACHMENT_MAX_SIZE = 10 * 1024 * 1024
CHAT_ATTACHMENT_MAX_COUNT = 5
CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS = {'.txt', '.json', '.csv', '.md', '.log', '.xml', '.yaml', '.yml'}
CHAT_ATTACHMENT_ALLOWED_EXTS = CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS | CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS


class AttachmentMeta(BaseModel):
    filename: str
    stored_name: str
    file_type: str
    mime_type: str
    size: int


class ChatAttachmentUploadResponse(BaseModel):
    attachments: List[AttachmentMeta]
    failed: List[dict] = []
