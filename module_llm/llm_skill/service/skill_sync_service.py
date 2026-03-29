# -*- coding: utf-8 -*-
"""
Skill sync service.

Source of truth is database records (skills + skill files).
This service syncs DB content to CaseGo/skills on filesystem.
"""

import asyncio
import os
import shutil
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from module_llm.llm_skill.dao.skill_dao import SkillDao
from module_llm.llm_skill.dao.skill_file_dao import SkillFileDao
from module_llm.llm_skill.entity.vo.skill_vo import SkillFileModel, SkillModel
from utils.log_util import logger


_PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
SKILLS_ROOT = os.path.join(_PROJECT_ROOT, "CaseGo", "skills")

_sync_locks: dict[str, asyncio.Lock] = {}


def _get_lock(skill_name: str) -> asyncio.Lock:
    """Get per-skill async lock for sync operations."""
    if skill_name not in _sync_locks:
        _sync_locks[skill_name] = asyncio.Lock()
    return _sync_locks[skill_name]


class SkillSyncService:
    """
    Sync service between database and filesystem.
    """

    @classmethod
    async def sync_all(cls, db: AsyncSession):
        """
        Full sync: write all enabled skills to filesystem.
        """
        try:
            enabled_skills = await SkillDao.get_all_enabled_skills(db)
            synced_names = set()
            failed_skills = []

            for skill in enabled_skills:
                try:
                    files = await SkillFileDao.get_files_by_skill_id(db, skill.skill_id)
                    await cls._write_skill_to_disk(skill.skill_name, files)
                    synced_names.add(skill.skill_name)
                except Exception as e:
                    failed_skills.append({"skillName": skill.skill_name, "error": str(e)})
                    logger.error(f"Sync skill failed: {skill.skill_name}, error: {e}")

            logger.info(
                f"Skill sync all finished: total={len(enabled_skills)}, synced={len(synced_names)}, failed={len(failed_skills)}"
            )
            return {
                "total": len(enabled_skills),
                "synced": len(synced_names),
                "failed": failed_skills,
            }
        except Exception as e:
            logger.error(f"Skill sync all crashed: {e}")
            return {
                "total": 0,
                "synced": 0,
                "failed": [{"skillName": "*", "error": str(e)}],
            }

    @classmethod
    async def sync_skill(cls, db: AsyncSession, skill_name: str):
        """
        Sync one skill to filesystem.
        If skill is absent or disabled, remove its directory from filesystem.
        """
        lock = _get_lock(skill_name)
        async with lock:
            skill = await SkillDao.get_skill_by_name(db, skill_name)
            if not skill or not skill.enabled:
                await cls.remove_skill(skill_name)
                return

            files = await SkillFileDao.get_files_by_skill_id(db, skill.skill_id)
            await cls._write_skill_to_disk(skill_name, files)
            logger.info(f"Skill synced: {skill_name}, files={len(files)}")

    @classmethod
    async def remove_skill(cls, skill_name: str):
        """
        Remove one skill directory from filesystem.
        """
        skill_dir = os.path.join(SKILLS_ROOT, skill_name)
        if os.path.exists(skill_dir):
            shutil.rmtree(skill_dir, ignore_errors=True)
            logger.info(f"Skill directory removed: {skill_dir}")

    @classmethod
    async def _write_skill_to_disk(cls, skill_name: str, files: list):
        """
        Rewrite one skill directory from DB file records.

        Strategy:
        1. Upsert all text files from DB to disk.
        2. Best-effort cleanup stale files not in DB.
        3. Never fail the whole sync due to one locked stale file.
        """
        skill_dir = os.path.join(SKILLS_ROOT, skill_name)
        os.makedirs(SKILLS_ROOT, exist_ok=True)
        os.makedirs(skill_dir, exist_ok=True)

        real_skill_dir = os.path.realpath(skill_dir)
        expected_rel_paths: set[str] = set()
        write_errors: list[str] = []

        for file_obj in files:
            if file_obj.is_binary or file_obj.content is None:
                continue

            rel_path = (file_obj.file_path or "").strip().replace("\\", "/")
            if not rel_path:
                continue

            target_path = os.path.join(skill_dir, rel_path)
            real_target_path = os.path.realpath(target_path)

            try:
                if os.path.commonpath([real_skill_dir, real_target_path]) != real_skill_dir:
                    logger.warning(f"Skip unsafe file path: {rel_path}")
                    continue
            except ValueError:
                logger.warning(f"Skip invalid file path: {rel_path}")
                continue

            expected_rel_paths.add(rel_path)
            target_dir = os.path.dirname(target_path)
            if target_dir:
                os.makedirs(target_dir, exist_ok=True)

            try:
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(file_obj.content)
            except OSError as e:
                write_errors.append(rel_path)
                logger.warning(f"Write skill file failed: {rel_path}, error: {e}")

        # Best-effort cleanup for files removed from DB.
        # This avoids full-directory deletion (rmtree) that is fragile on Windows file locks.
        for root, dirs, file_names in os.walk(skill_dir, topdown=False):
            for file_name in file_names:
                abs_path = os.path.join(root, file_name)
                rel = os.path.relpath(abs_path, skill_dir).replace("\\", "/")
                if rel in expected_rel_paths:
                    continue
                try:
                    os.remove(abs_path)
                except OSError as e:
                    logger.warning(f"Skip removing stale file (in use or denied): {rel}, error: {e}")

            for dir_name in dirs:
                abs_dir = os.path.join(root, dir_name)
                try:
                    if not os.listdir(abs_dir):
                        os.rmdir(abs_dir)
                except OSError:
                    # Ignore directory cleanup failures (in use / not empty).
                    pass

        if write_errors:
            logger.warning(
                f"Skill sync completed with write errors: skill={skill_name}, errorFiles={len(write_errors)}"
            )

    @classmethod
    async def scan_and_import(cls, db: AsyncSession):
        """
        Scan filesystem skills directory and import missing skills to DB.

        This only imports skills that do not already exist in DB.
        """
        from module_llm.llm_skill.service.skill_import_service import SkillImportService

        if not os.path.isdir(SKILLS_ROOT):
            return

        imported_count = 0
        for entry in os.scandir(SKILLS_ROOT):
            if not entry.is_dir() or entry.name.startswith(".") or entry.name == "node_modules":
                continue

            skill_name = entry.name

            if not SkillImportService.validate_skill_name(skill_name):
                slugified = SkillImportService.slugify_skill_name(skill_name)
                if not slugified or not SkillImportService.validate_skill_name(slugified):
                    logger.debug(f"Skip invalid skill directory name: {skill_name}")
                    continue

                old_path = os.path.join(SKILLS_ROOT, skill_name)
                new_path = os.path.join(SKILLS_ROOT, slugified)
                if os.path.exists(new_path):
                    logger.debug(
                        f"Skip rename because target exists: from={skill_name}, to={slugified}"
                    )
                    continue
                try:
                    os.rename(old_path, new_path)
                    logger.info(f"Renamed skill directory: from={skill_name}, to={slugified}")
                except OSError as e:
                    logger.warning(
                        f"Rename skill directory failed: from={skill_name}, to={slugified}, error={e}"
                    )
                    continue
                skill_name = slugified

            existing = await SkillDao.get_skill_by_name(db, skill_name)
            if existing:
                continue

            try:
                await cls._import_skill_dir(db, skill_name)
                imported_count += 1
            except Exception as e:
                logger.warning(f"Import local skill directory failed: {skill_name}, error: {e}")

        if imported_count > 0:
            logger.info(f"Imported local skills count: {imported_count}")

    @classmethod
    async def _import_skill_dir(cls, db: AsyncSession, skill_name: str):
        """
        Import a single local skill directory into DB.
        """
        from module_llm.llm_skill.service.skill_import_service import SkillImportService

        skill_dir = os.path.join(SKILLS_ROOT, skill_name)
        now = datetime.now()

        metadata = {}
        skill_md_path = os.path.join(skill_dir, "SKILL.md")
        if os.path.isfile(skill_md_path):
            with open(skill_md_path, "r", encoding="utf-8") as f:
                skill_md_content = f.read()
            metadata = SkillImportService.parse_skill_md_frontmatter(skill_md_content)

        skill_model = SkillModel(
            skill_name=skill_name,
            display_name=metadata.get("name", skill_name),
            description=metadata.get("description", ""),
            enabled=True,
            source_type="local",
            allowed_tools=metadata.get("allowed-tools", ""),
            license_info=metadata.get("license", ""),
            create_by="system",
            create_time=now,
            update_by="system",
            update_time=now,
        )
        db_skill = await SkillDao.add_skill_dao(db, skill_model)

        file_count = 0
        for root, _dirs, files in os.walk(skill_dir):
            for fname in files:
                abs_path = os.path.join(root, fname)
                rel_path = os.path.relpath(abs_path, skill_dir).replace("\\", "/")

                if any(part.startswith(".") or part == "node_modules" for part in rel_path.split("/")):
                    continue

                try:
                    with open(abs_path, "r", encoding="utf-8") as f:
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
                    create_by="system",
                    create_time=now,
                    update_by="system",
                    update_time=now,
                )
                await SkillFileDao.add_file_dao(db, file_model)
                file_count += 1

        await db.commit()
        logger.info(f"Imported local skill: {skill_name}, files={file_count}")
