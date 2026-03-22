# -*- coding: utf-8 -*-
"""
技能文件系统同步服务
负责将数据库中的技能内容同步到 CaseGo/skills/ 目录，
以及从文件系统反向扫描导入技能到数据库，
使 deepagents 框架能够通过 FilesystemBackend 读取技能文件
"""

import os
import shutil
import asyncio
from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from module_llm.skills.dao.skill_dao import SkillDao
from module_llm.skills.dao.skill_file_dao import SkillFileDao
from module_llm.skills.entity.vo.skill_vo import SkillModel, SkillFileModel
from utils.log_util import logger


# 与 deepagent_factory.py 中的 SKILLS_ROOT 保持一致
SKILLS_ROOT = os.path.join("CaseGo", "skills")

# 每个 skill_name 一个锁，防止并发写入冲突
_sync_locks: dict[str, asyncio.Lock] = {}


def _get_lock(skill_name: str) -> asyncio.Lock:
    """获取或创建 skill_name 对应的异步锁"""
    if skill_name not in _sync_locks:
        _sync_locks[skill_name] = asyncio.Lock()
    return _sync_locks[skill_name]


class SkillSyncService:
    """
    技能文件系统同步服务
    DB(source of truth) → CaseGo/skills/ (filesystem)
    """

    @classmethod
    async def sync_all(cls, db: AsyncSession):
        """
        全量同步：从数据库重建所有启用技能到文件系统
        在应用启动时调用

        :param db: orm对象
        """
        try:
            enabled_skills = await SkillDao.get_all_enabled_skills(db)
            synced_names = set()

            for skill in enabled_skills:
                try:
                    files = await SkillFileDao.get_files_by_skill_id(db, skill.skill_id)
                    await cls._write_skill_to_disk(skill.skill_name, files)
                    synced_names.add(skill.skill_name)
                except Exception as e:
                    logger.error(f'同步技能 {skill.skill_name} 失败: {e}')

            logger.info(f'技能文件系统同步完成，共同步 {len(synced_names)} 个技能')
        except Exception as e:
            logger.error(f'技能全量同步失败: {e}')

    @classmethod
    async def sync_skill(cls, db: AsyncSession, skill_name: str):
        """
        单个技能同步：将指定技能从数据库同步到文件系统
        在创建/更新技能后调用

        :param db: orm对象
        :param skill_name: 技能目录名
        """
        lock = _get_lock(skill_name)
        async with lock:
            skill = await SkillDao.get_skill_by_name(db, skill_name)
            if not skill or not skill.enabled:
                await cls.remove_skill(skill_name)
                return

            files = await SkillFileDao.get_files_by_skill_id(db, skill.skill_id)
            await cls._write_skill_to_disk(skill_name, files)
            logger.info(f'技能 {skill_name} 已同步到文件系统，共 {len(files)} 个文件')

    @classmethod
    async def remove_skill(cls, skill_name: str):
        """
        移除技能目录
        在删除/禁用技能时调用

        :param skill_name: 技能目录名
        """
        skill_dir = os.path.join(SKILLS_ROOT, skill_name)
        if os.path.exists(skill_dir):
            shutil.rmtree(skill_dir, ignore_errors=True)
            logger.info(f'已移除技能目录: {skill_dir}')

    @classmethod
    async def _write_skill_to_disk(cls, skill_name: str, files: list):
        """
        将技能文件写入磁盘

        :param skill_name: 技能目录名
        :param files: LlmSkillFile ORM 对象列表
        """
        skill_dir = os.path.join(SKILLS_ROOT, skill_name)

        # 清空并重建目录，确保与数据库一致
        if os.path.exists(skill_dir):
            shutil.rmtree(skill_dir)
        os.makedirs(skill_dir, exist_ok=True)

        for file_obj in files:
            if file_obj.is_binary or file_obj.content is None:
                continue

            file_path = os.path.join(skill_dir, file_obj.file_path)

            # 防止路径遍历
            real_path = os.path.realpath(file_path)
            real_skill_dir = os.path.realpath(skill_dir)
            if not real_path.startswith(real_skill_dir):
                logger.warning(f'跳过路径遍历文件: {file_obj.file_path}')
                continue

            # 创建子目录
            file_dir = os.path.dirname(file_path)
            if file_dir:
                os.makedirs(file_dir, exist_ok=True)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_obj.content)

    @classmethod
    async def scan_and_import(cls, db: AsyncSession):
        """
        反向同步：扫描 CaseGo/skills/ 目录，将文件系统中存在但数据库中不存在的技能导入数据库。

        应在 sync_all 之前调用，确保本地 clone 或手动放入的技能也能被系统管理。
        """
        from module_llm.skills.service.skill_import_service import SkillImportService

        if not os.path.isdir(SKILLS_ROOT):
            return

        imported_count = 0
        for entry in os.scandir(SKILLS_ROOT):
            if not entry.is_dir() or entry.name.startswith('.') or entry.name == 'node_modules':
                continue

            skill_name = entry.name

            # 目录名不合法时自动 slugify 并重命名目录
            if not SkillImportService.validate_skill_name(skill_name):
                slugified = SkillImportService.slugify_skill_name(skill_name)
                if not slugified or not SkillImportService.validate_skill_name(slugified):
                    logger.debug(f'跳过不合法的目录名（无法自动转换）: {skill_name}')
                    continue
                old_path = os.path.join(SKILLS_ROOT, skill_name)
                new_path = os.path.join(SKILLS_ROOT, slugified)
                if os.path.exists(new_path):
                    logger.debug(f'跳过: 转换后目录已存在: {slugified}（原: {skill_name}）')
                    continue
                try:
                    os.rename(old_path, new_path)
                    logger.info(f'重命名技能目录: {skill_name} → {slugified}')
                except OSError as e:
                    logger.warning(f'重命名技能目录失败: {skill_name} → {slugified}: {e}')
                    continue
                skill_name = slugified

            # 已存在于数据库则跳过
            existing = await SkillDao.get_skill_by_name(db, skill_name)
            if existing:
                continue

            try:
                await cls._import_skill_dir(db, skill_name)
                imported_count += 1
            except Exception as e:
                logger.warning(f'从文件系统导入技能 {skill_name} 失败: {e}')

        if imported_count > 0:
            logger.info(f'从文件系统反向导入 {imported_count} 个技能到数据库')

    @classmethod
    async def _import_skill_dir(cls, db: AsyncSession, skill_name: str):
        """
        将单个技能目录导入数据库

        :param db: orm对象
        :param skill_name: 技能目录名
        """
        from module_llm.skills.service.skill_import_service import SkillImportService

        skill_dir = os.path.join(SKILLS_ROOT, skill_name)
        now = datetime.now()

        # 读取 SKILL.md 解析元数据
        metadata = {}
        skill_md_path = os.path.join(skill_dir, 'SKILL.md')
        if os.path.isfile(skill_md_path):
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                skill_md_content = f.read()
            metadata = SkillImportService.parse_skill_md_frontmatter(skill_md_content)

        # 创建技能记录
        skill_model = SkillModel(
            skill_name=skill_name,
            display_name=metadata.get('name', skill_name),
            description=metadata.get('description', ''),
            enabled=True,
            source_type='local',
            allowed_tools=metadata.get('allowed-tools', ''),
            license_info=metadata.get('license', ''),
            create_by='system',
            create_time=now,
            update_by='system',
            update_time=now,
        )
        db_skill = await SkillDao.add_skill_dao(db, skill_model)

        # 递归读取所有文件
        file_count = 0
        for root, _dirs, files in os.walk(skill_dir):
            for fname in files:
                abs_path = os.path.join(root, fname)
                rel_path = os.path.relpath(abs_path, skill_dir).replace('\\', '/')

                # 跳过隐藏文件和 node_modules
                if any(part.startswith('.') or part == 'node_modules' for part in rel_path.split('/')):
                    continue

                try:
                    with open(abs_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    is_binary = False
                except (UnicodeDecodeError, ValueError):
                    content = None
                    is_binary = True

                file_model = SkillFileModel(
                    skill_id=db_skill.skill_id,
                    file_path=rel_path,
                    content=content,
                    is_binary=is_binary,
                    create_by='system',
                    create_time=now,
                    update_by='system',
                    update_time=now,
                )
                await SkillFileDao.add_file_dao(db, file_model)
                file_count += 1

        await db.commit()
        logger.info(f'从文件系统导入技能: {skill_name}，共 {file_count} 个文件')
