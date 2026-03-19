# -*- coding: utf-8 -*-
"""
技能文件系统同步服务
负责将数据库中的技能内容同步到 CaseGo/skills/ 目录，
使 deepagents 框架能够通过 FilesystemBackend 读取技能文件
"""

import os
import shutil
import asyncio
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from module_llm.skills.dao.skill_dao import SkillDao
from module_llm.skills.dao.skill_file_dao import SkillFileDao
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
