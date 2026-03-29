# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class FileType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"


class FileEntryModel(BaseModel):
    """文件/目录条目"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    name: str = Field(description='文件或目录名')
    path: str = Field(description='相对于会话工作区根目录的路径')
    type: FileType = Field(description='类型: file / directory')
    size: int = Field(default=0, description='文件大小(字节), 目录为0')
    mime_type: Optional[str] = Field(default=None, description='MIME类型, 目录为null')
    created_time: datetime = Field(description='创建时间')
    modified_time: datetime = Field(description='最后修改时间')


class FileTreeResponse(BaseModel):
    """文件树响应"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    session_id: str = Field(alias='sessionId', description='会话ID')
    files: List[FileEntryModel] = Field(default_factory=list, description='扁平文件列表')
    total: int = Field(default=0, description='条目总数')


class FileContentResponse(BaseModel):
    """文件内容响应"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    name: str = Field(description='文件名')
    path: str = Field(description='相对路径')
    content: str = Field(description='文件内容(文本或base64)')
    is_binary: bool = Field(default=False, description='是否为base64编码的二进制文件')
    mime_type: str = Field(default='text/plain', description='MIME类型')
    size: int = Field(default=0, description='文件大小(字节)')


class CreateFileRequest(BaseModel):
    """创建文件请求"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    session_id: str = Field(alias='sessionId', description='会话ID')
    path: str = Field(description='新文件的相对路径')
    content: str = Field(default='', description='文件内容')


class CreateFolderRequest(BaseModel):
    """创建文件夹请求"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    session_id: str = Field(alias='sessionId', description='会话ID')
    path: str = Field(description='新文件夹的相对路径')


class DeleteRequest(BaseModel):
    """删除文件或文件夹请求"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    session_id: str = Field(alias='sessionId', description='会话ID')
    path: str = Field(description='要删除的文件/文件夹的相对路径')
