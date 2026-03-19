# -*- coding: utf-8 -*-
"""
技能导入服务
支持从 ZIP 文件上传和 URL 导入技能
"""

import io
import os
import re
import uuid
import zipfile
from datetime import datetime
from typing import Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from module_llm.skills.dao.skill_dao import SkillDao
from module_llm.skills.dao.skill_file_dao import SkillFileDao
from module_llm.skills.entity.vo.skill_vo import SkillModel, SkillFileModel
from module_llm.skills.service.skill_sync_service import SkillSyncService
from utils.log_util import logger

# 合法的技能目录名：小写字母、数字、连字符
SKILL_NAME_PATTERN = re.compile(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$')


class SkillImportService:
    """
    技能导入服务 - 处理 ZIP 上传和 URL 导入
    """

    @staticmethod
    def validate_skill_name(skill_name: str) -> bool:
        """
        验证技能目录名是否合法

        :param skill_name: 技能目录名
        :return: 是否合法
        """
        if not skill_name or len(skill_name) > 128:
            return False
        # 单字符也允许
        if len(skill_name) == 1:
            return skill_name.isalnum()
        return bool(SKILL_NAME_PATTERN.match(skill_name))

    @staticmethod
    def parse_skill_md_frontmatter(content: str) -> dict:
        """
        解析 SKILL.md 的 YAML frontmatter

        :param content: SKILL.md 文件内容
        :return: 元数据字典 {name, description, allowed-tools, license}
        """
        match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}

        result = {}
        for line in match.group(1).strip().split('\n'):
            line = line.strip()
            if ':' in line:
                key, _, value = line.partition(':')
                result[key.strip()] = value.strip()
        return result

    @classmethod
    async def import_from_zip(
        cls,
        db: AsyncSession,
        zip_bytes: bytes,
        user_name: str,
    ) -> dict:
        """
        从 ZIP 文件导入技能

        :param db: orm对象
        :param zip_bytes: ZIP 文件字节内容
        :param user_name: 当前用户名
        :return: 导入结果 {skill_name, skill_id, file_count}
        """
        with zipfile.ZipFile(io.BytesIO(zip_bytes), 'r') as zf:
            # 检测技能目录结构
            names = zf.namelist()
            skill_root, files_map = cls._detect_skill_root(zf, names)

            if not files_map:
                raise ValueError('ZIP文件中未找到有效的技能文件（需包含SKILL.md）')

            # 读取 SKILL.md 解析元数据
            skill_md_path = None
            for path in files_map:
                if path == 'SKILL.md' or path.endswith('/SKILL.md'):
                    normalized = path[len(skill_root):] if skill_root else path
                    if normalized == 'SKILL.md':
                        skill_md_path = path
                        break

            if not skill_md_path:
                raise ValueError('ZIP文件中未找到SKILL.md文件')

            skill_md_content = zf.read(skill_md_path).decode('utf-8')
            metadata = cls.parse_skill_md_frontmatter(skill_md_content)

            # 确定技能名称
            skill_name = metadata.get('name', '')
            if not skill_name and skill_root:
                skill_name = skill_root.rstrip('/')
            if not skill_name:
                raise ValueError('无法从ZIP中推断技能名称，请在SKILL.md frontmatter中指定name字段')

            if not cls.validate_skill_name(skill_name):
                raise ValueError(f'技能名称不合法: {skill_name}（只允许小写字母、数字和连字符）')

            # 检查是否已存在
            existing = await SkillDao.get_skill_by_name(db, skill_name)
            if existing:
                raise ValueError(f'技能 {skill_name} 已存在')

            # 创建技能记录
            now = datetime.now()
            skill_model = SkillModel(
                skill_name=skill_name,
                display_name=metadata.get('name', skill_name),
                description=metadata.get('description', ''),
                enabled=True,
                source_type='upload',
                allowed_tools=metadata.get('allowed-tools', ''),
                license_info=metadata.get('license', ''),
                create_by=user_name,
                create_time=now,
                update_by=user_name,
                update_time=now,
            )
            db_skill = await SkillDao.add_skill_dao(db, skill_model)

            # 创建文件记录
            file_count = 0
            for zip_path in sorted(files_map.keys()):
                rel_path = zip_path[len(skill_root):] if skill_root else zip_path
                if not rel_path or rel_path.endswith('/'):
                    continue

                try:
                    file_content = zf.read(zip_path).decode('utf-8')
                    is_binary = False
                except (UnicodeDecodeError, ValueError):
                    file_content = None
                    is_binary = True

                file_model = SkillFileModel(
                    skill_id=db_skill.skill_id,
                    file_path=rel_path,
                    content=file_content,
                    is_binary=is_binary,
                    create_by=user_name,
                    create_time=now,
                    update_by=user_name,
                    update_time=now,
                )
                await SkillFileDao.add_file_dao(db, file_model)
                file_count += 1

            await db.commit()

            # 同步到文件系统
            await SkillSyncService.sync_skill(db, skill_name)

            return {
                'skill_name': skill_name,
                'skill_id': str(db_skill.skill_id),
                'file_count': file_count,
            }

    @classmethod
    async def import_from_url(
        cls,
        db: AsyncSession,
        url: str,
        skill_name: Optional[str] = None,
        user_name: str = 'system',
    ) -> dict:
        """
        从 URL 导入技能

        :param db: orm对象
        :param url: 导入URL
        :param skill_name: 技能目录名（可选）
        :param user_name: 当前用户名
        :return: 导入结果 {skill_name, skill_id, file_count}
        """
        async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        content_bytes = response.content

        # 判断是否为ZIP文件
        is_zip = (
            'zip' in content_type.lower()
            or url.lower().endswith('.zip')
            or content_bytes[:4] == b'PK\x03\x04'
        )

        if is_zip:
            result = await cls.import_from_zip(db, content_bytes, user_name)
            # 更新来源信息
            skill = await SkillDao.get_skill_by_name(db, result['skill_name'])
            if skill:
                await SkillDao.edit_skill_dao(db, {
                    'skill_id': skill.skill_id,
                    'source_type': 'url',
                    'source_url': url,
                    'update_by': user_name,
                    'update_time': datetime.now(),
                })
                await db.commit()
            return result

        # 当作单个 SKILL.md 文本处理
        try:
            text_content = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('URL内容无法解码为文本，且不是有效的ZIP文件')

        metadata = cls.parse_skill_md_frontmatter(text_content)

        # 确定技能名称
        if not skill_name:
            skill_name = metadata.get('name', '')
        if not skill_name:
            # 尝试从URL路径推断
            url_path = url.rstrip('/').split('/')[-1]
            if url_path.endswith('.md'):
                url_path = url_path[:-3]
            skill_name = url_path.lower().replace('_', '-').replace(' ', '-')

        if not cls.validate_skill_name(skill_name):
            raise ValueError(f'技能名称不合法: {skill_name}，请手动指定skill_name')

        # 检查是否已存在
        existing = await SkillDao.get_skill_by_name(db, skill_name)
        if existing:
            raise ValueError(f'技能 {skill_name} 已存在')

        # 创建技能记录
        now = datetime.now()
        skill_model = SkillModel(
            skill_name=skill_name,
            display_name=metadata.get('name', skill_name),
            description=metadata.get('description', ''),
            enabled=True,
            source_type='url',
            source_url=url,
            allowed_tools=metadata.get('allowed-tools', ''),
            license_info=metadata.get('license', ''),
            create_by=user_name,
            create_time=now,
            update_by=user_name,
            update_time=now,
        )
        db_skill = await SkillDao.add_skill_dao(db, skill_model)

        # 创建 SKILL.md 文件记录
        file_model = SkillFileModel(
            skill_id=db_skill.skill_id,
            file_path='SKILL.md',
            content=text_content,
            is_binary=False,
            create_by=user_name,
            create_time=now,
            update_by=user_name,
            update_time=now,
        )
        await SkillFileDao.add_file_dao(db, file_model)

        await db.commit()

        # 同步到文件系统
        await SkillSyncService.sync_skill(db, skill_name)

        return {
            'skill_name': skill_name,
            'skill_id': str(db_skill.skill_id),
            'file_count': 1,
        }

    @classmethod
    def _detect_skill_root(cls, zf: zipfile.ZipFile, names: list) -> tuple:
        """
        检测ZIP中的技能根目录

        :return: (skill_root_prefix, files_map)
        """
        # 情况1: 根目录直接有 SKILL.md
        if 'SKILL.md' in names:
            return '', {n: n for n in names if not n.endswith('/')}

        # 情况2: 单个子目录包含 SKILL.md
        top_dirs = set()
        for name in names:
            parts = name.split('/')
            if len(parts) > 1 and parts[0]:
                top_dirs.add(parts[0])

        for top_dir in top_dirs:
            skill_md = f'{top_dir}/SKILL.md'
            if skill_md in names:
                prefix = f'{top_dir}/'
                files_map = {
                    n: n for n in names
                    if n.startswith(prefix) and not n.endswith('/')
                }
                return prefix, files_map

        return '', {}
