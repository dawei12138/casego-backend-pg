#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：sys_upload_util.py
@Author  ：david
@Date    ：2025-11-17 14:04 
"""
import hashlib
from typing import Optional
from pathlib import Path
from pydantic import BaseModel


class UploadConfig:
    UPLOAD_PATH = "./CaseGo/upload_path"  # 本地上传路径
    UPLOAD_PREFIX = "/CaseGo/upload_path"  # 访问URL前缀
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
        'document': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'],
        'audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg']
    }


# 响应模型
class UploadResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class FileInfo(BaseModel):
    filename: str
    original_name: str
    file_path: str
    file_url: str
    file_size: int
    file_type: str
    upload_time: str


# 工具类
class UploadUtil:
    @staticmethod
    def generate_random_number(length: int = 6) -> str:
        """生成随机数字字符串"""
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])

    @staticmethod
    def get_file_hash(content: bytes) -> str:
        """计算文件MD5哈希值"""
        return hashlib.md5(content).hexdigest()

    @staticmethod
    def get_file_extension(filename: str) -> str:
        """获取文件扩展名"""
        return Path(filename).suffix.lower()

    @staticmethod
    def is_allowed_file(filename: str, file_type: str = None) -> bool:
        """检查文件类型是否允许"""
        ext = UploadUtil.get_file_extension(filename)

        if file_type and file_type in UploadConfig.ALLOWED_EXTENSIONS:
            return ext in UploadConfig.ALLOWED_EXTENSIONS[file_type]

        # 如果没有指定类型，检查是否在所有允许的扩展名中
        all_extensions = []
        for extensions in UploadConfig.ALLOWED_EXTENSIONS.values():
            all_extensions.extend(extensions)

        return ext in all_extensions


# 创建目录
def ensure_upload_directory():
    """确保上传目录存在"""
    Path(UploadConfig.UPLOAD_PATH).mkdir(parents=True, exist_ok=True)


