# -*- coding: utf-8 -*-
"""
AI???????
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from pathlib import PurePosixPath

from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_llm.llm_skill.dao.skill_dao import SkillDao
from module_llm.llm_skill.dao.skill_file_dao import SkillFileDao
from module_llm.llm_skill.entity.vo.skill_vo import (
    DeleteSkillModel, SkillModel, SkillPageQueryModel,
    SkillFileModel, SkillDetailModel, SkillImportUrlModel,
    SkillFileContentSaveModel, SkillFilesBatchSaveModel,
    SkillFolderCreateModel, SkillFolderRenameModel,
    SkillFolderDeleteModel, SkillFileMoveModel,
)
from module_llm.llm_skill.service.skill_sync_service import SkillSyncService
from module_llm.llm_skill.service.skill_import_service import SkillImportService
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil
from utils.log_util import logger


class SkillService:
    """
    AI???????
    """

    # ==================== ???? ====================

    @classmethod
    async def get_skill_list_services(
        cls, query_db: AsyncSession, query_object: SkillPageQueryModel, is_page: bool = False
    ):
        """
        ????????service

        :param query_db: orm??
        :param query_object: ??????
        :param is_page: ??????
        :return: ????????
        """
        skill_list_result = await SkillDao.get_skill_list(query_db, query_object, is_page)
        return skill_list_result

    @classmethod
    async def get_skill_all_list_services(
        cls, query_db: AsyncSession, query_object: SkillPageQueryModel
    ):
        """
        ????????????????

        :param query_db: orm??
        :param query_object: ??????
        :return: ??????
        """
        skill_list_result = await SkillDao.get_skill_list(query_db, query_object, is_page=False)
        skill_list = []
        for item in skill_list_result:
            skill_list.append({
                'skillId': str(item.get('skillId', '')),
                'skillName': item.get('skillName', ''),
                'displayName': item.get('displayName', ''),
                'enabled': item.get('enabled', False),
            })
        return skill_list

    # ==================== ?? ====================

    @classmethod
    async def skill_detail_services(cls, query_db: AsyncSession, skill_id):
        """
        ???????????????

        :param query_db: orm??
        :param skill_id: ??ID
        :return: ??????
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id=skill_id)
        if skill:
            skill_dict = CamelCaseUtil.transform_result(skill)
            files = await SkillFileDao.get_files_by_skill_id(query_db, skill_id)
            file_list = []
            for f in files:
                file_dict = CamelCaseUtil.transform_result(f)
                # ????????????????
                file_dict.pop('content', None)
                file_list.append(SkillFileModel(**file_dict))
            result = SkillDetailModel(**skill_dict, files=file_list)
        else:
            result = SkillDetailModel(**dict())
        return result

    # ==================== ?? ====================

    @classmethod
    async def add_skill_services(cls, query_db: AsyncSession, page_object: SkillModel):
        """
        ????service

        :param query_db: orm??
        :param page_object: ??????
        :return: ????
        """
        # ????????
        if not SkillImportService.validate_skill_name(page_object.skill_name):
            raise ServiceException(
                message=f'技能名称不合法: {page_object.skill_name}（仅允许小写字母、数字和连字符）'
            )

        # ?????
        existing = await SkillDao.get_skill_by_name(query_db, page_object.skill_name)
        if existing:
            raise ServiceException(message=f'技能 {page_object.skill_name} 已存在')

        try:
            db_skill = await SkillDao.add_skill_dao(query_db, page_object)

            # ?????? SKILL.md???????
            files = await SkillFileDao.get_files_by_skill_id(query_db, db_skill.skill_id)
            if not files:
                now = datetime.now()
                frontmatter = f"""---
name: {page_object.skill_name}
description: {page_object.description or ''}
"""
                if page_object.allowed_tools:
                    frontmatter += f"allowed-tools: {page_object.allowed_tools}\n"
                if page_object.license_info:
                    frontmatter += f"license: {page_object.license_info}\n"
                frontmatter += "---\n\n"
                if page_object.description:
                    frontmatter += f"# {page_object.display_name or page_object.skill_name}\n\n{page_object.description}\n"

                file_model = SkillFileModel(
                    skill_id=db_skill.skill_id,
                    file_path='SKILL.md',
                    content=frontmatter,
                    is_binary=False,
                    create_by=page_object.create_by,
                    create_time=now,
                    update_by=page_object.update_by,
                    update_time=now,
                )
                await SkillFileDao.add_file_dao(query_db, file_model)

            await query_db.commit()

            # ???????
            if page_object.enabled is not False:
                await SkillSyncService.sync_skill(query_db, page_object.skill_name)

            return CrudResponseModel(is_success=True, message='新增技能成功')
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    # ==================== ?? ====================

    @classmethod
    async def edit_skill_services(cls, query_db: AsyncSession, page_object: SkillModel):
        """
        ??????service

        :param query_db: orm??
        :param page_object: ??????
        :return: ????
        """
        edit_skill = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        skill_info = await cls.skill_detail_services(query_db, page_object.skill_id)
        if skill_info.skill_id:
            old_skill_name = skill_info.skill_name
            try:
                # ????? skill_name????????
                if page_object.skill_name and page_object.skill_name != old_skill_name:
                    if not SkillImportService.validate_skill_name(page_object.skill_name):
                        raise ServiceException(
                            message=f'技能名称不合法: {page_object.skill_name}（仅允许小写字母、数字和连字符）'
                        )
                    existing = await SkillDao.get_skill_by_name(query_db, page_object.skill_name)
                    if existing:
                        raise ServiceException(message=f'技能 {page_object.skill_name} 已存在')

                await SkillDao.edit_skill_dao(query_db, edit_skill)
                await query_db.commit()

                # ??????????????
                new_skill_name = page_object.skill_name or old_skill_name
                if page_object.skill_name and page_object.skill_name != old_skill_name:
                    await SkillSyncService.remove_skill(old_skill_name)

                # ???????
                await SkillSyncService.sync_skill(query_db, new_skill_name)

                return CrudResponseModel(is_success=True, message='????')
            except ServiceException:
                await query_db.rollback()
                raise
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='?????')

    # ==================== ?? ====================

    @classmethod
    async def delete_skill_services(cls, query_db: AsyncSession, page_object: DeleteSkillModel):
        """
        ????service

        :param query_db: orm??
        :param page_object: ??????
        :return: ????
        """
        if page_object.skill_ids:
            skill_id_list = page_object.skill_ids.split(',')
            try:
                skill_names = []
                for skill_id in skill_id_list:
                    skill_id_obj = SkillModel.model_validate({'skill_id': skill_id}).skill_id
                    # ????????????????
                    skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id_obj)
                    if skill:
                        skill_names.append(skill.skill_name)
                    # ??????????
                    await SkillDao.delete_skill_dao(query_db, SkillModel(skill_id=skill_id_obj))
                    await SkillFileDao.delete_files_by_skill_id(query_db, skill_id_obj)

                await query_db.commit()

                # ????????????
                for name in skill_names:
                    await SkillSyncService.remove_skill(name)

                return CrudResponseModel(is_success=True, message='????')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='????ID??')

    # ==================== ???? ====================

    @classmethod
    async def get_skill_files_services(cls, query_db: AsyncSession, skill_id):
        """
        ??????????????

        :param query_db: orm??
        :param skill_id: ??ID
        :return: ????
        """
        files = await SkillFileDao.get_files_by_skill_id(query_db, skill_id)
        result = []
        for f in files:
            file_dict = CamelCaseUtil.transform_result(f)
            file_dict.pop('content', None)
            result.append(file_dict)
        return result

    @classmethod
    async def get_skill_file_content_services(cls, query_db: AsyncSession, skill_id, file_path: str):
        """
        ??????????

        :param query_db: orm??
        :param skill_id: ??ID
        :param file_path: ??????
        :return: ??????
        """
        file_obj = await SkillFileDao.get_file_by_path(query_db, skill_id, file_path)
        if file_obj:
            return SkillFileModel(**CamelCaseUtil.transform_result(file_obj))
        else:
            return SkillFileModel(**dict())

    @staticmethod
    def _normalize_skill_file_path(file_path: str) -> str:
        """
        Normalize and validate a skill-relative file path.
        """
        if file_path is None:
            raise ServiceException(message='file_path cannot be empty')

        raw_path = str(file_path).strip().replace('\\', '/')
        if not raw_path:
            raise ServiceException(message='file_path cannot be empty')
        if raw_path.startswith('/'):
            raise ServiceException(message='file_path must be relative to skill directory')
        if raw_path.endswith('/'):
            raise ServiceException(message='file_path must point to a file')

        normalized = str(PurePosixPath(raw_path))
        parts = [part for part in normalized.split('/') if part and part != '.']
        if not parts:
            raise ServiceException(message='file_path cannot be empty')
        if any(part == '..' for part in parts):
            raise ServiceException(message=f'illegal file path: {file_path}')
        if ':' in parts[0]:
            raise ServiceException(message=f'illegal file path: {file_path}')

        return '/'.join(parts)

    @classmethod
    async def save_skill_file_content_services(
        cls,
        query_db: AsyncSession,
        skill_id,
        file_model: SkillFileContentSaveModel,
        operator: str,
    ):
        """
        Save a single skill file (upsert by file_path).
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
        if not skill:
            raise ServiceException(message='Skill not found')
        skill_name = skill.skill_name
        skill_enabled = bool(skill.enabled)

        normalized_path = cls._normalize_skill_file_path(file_model.file_path)
        content = file_model.content or ''
        if normalized_path == 'SKILL.md':
            content = content.removeprefix('\ufeff')

        now = datetime.now()
        existing = await SkillFileDao.get_file_by_path(query_db, skill_id, normalized_path)
        do_sync_all = bool(file_model.sync_all)

        try:
            if existing:
                await SkillFileDao.edit_file_dao(
                    query_db,
                    {
                        'file_id': existing.file_id,
                        'file_path': normalized_path,
                        'content': content,
                        'is_binary': bool(file_model.is_binary),
                        'update_by': operator,
                        'update_time': now,
                    },
                )
                action = 'updated'
            else:
                await SkillFileDao.add_file_dao(
                    query_db,
                    SkillFileModel(
                        skill_id=skill_id,
                        file_path=normalized_path,
                        content=content,
                        is_binary=bool(file_model.is_binary),
                        create_by=operator,
                        create_time=now,
                        update_by=operator,
                        update_time=now,
                    ),
                )
                action = 'created'

            await query_db.commit()

            sync_result = None
            if do_sync_all:
                sync_result = await SkillSyncService.sync_all(query_db)
            elif skill_enabled:
                await SkillSyncService.sync_skill(query_db, skill_name)

            return {
                'skillId': str(skill_id),
                'filePath': normalized_path,
                'action': action,
                'syncAll': do_sync_all,
                'syncResult': sync_result,
            }
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def save_skill_files_batch_services(
        cls,
        query_db: AsyncSession,
        skill_id,
        batch_model: SkillFilesBatchSaveModel,
        operator: str,
    ):
        """
        Save batch skill files (upsert by file_path).
        """
        if not batch_model.files:
            raise ServiceException(message='files cannot be empty')

        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
        if not skill:
            raise ServiceException(message='Skill not found')
        skill_name = skill.skill_name
        skill_enabled = bool(skill.enabled)

        now = datetime.now()
        created = 0
        updated = 0
        seen_paths = set()
        do_sync_all = bool(batch_model.sync_all)

        try:
            for file_item in batch_model.files:
                normalized_path = cls._normalize_skill_file_path(file_item.file_path)
                if normalized_path in seen_paths:
                    raise ServiceException(message=f'Duplicate file path in request: {normalized_path}')
                seen_paths.add(normalized_path)

                content = file_item.content or ''
                if normalized_path == 'SKILL.md':
                    content = content.removeprefix('\ufeff')

                existing = await SkillFileDao.get_file_by_path(query_db, skill_id, normalized_path)
                if existing:
                    await SkillFileDao.edit_file_dao(
                        query_db,
                        {
                            'file_id': existing.file_id,
                            'file_path': normalized_path,
                            'content': content,
                            'is_binary': bool(file_item.is_binary),
                            'update_by': operator,
                            'update_time': now,
                        },
                    )
                    updated += 1
                else:
                    await SkillFileDao.add_file_dao(
                        query_db,
                        SkillFileModel(
                            skill_id=skill_id,
                            file_path=normalized_path,
                            content=content,
                            is_binary=bool(file_item.is_binary),
                            create_by=operator,
                            create_time=now,
                            update_by=operator,
                            update_time=now,
                        ),
                    )
                    created += 1

            await query_db.commit()

            sync_result = None
            if do_sync_all:
                sync_result = await SkillSyncService.sync_all(query_db)
            elif skill_enabled:
                await SkillSyncService.sync_skill(query_db, skill_name)

            return {
                'skillId': str(skill_id),
                'total': len(batch_model.files),
                'created': created,
                'updated': updated,
                'syncAll': do_sync_all,
                'syncResult': sync_result,
            }
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def sync_all_skills_services(cls, query_db: AsyncSession):
        """
        Full sync all enabled skills from DB to filesystem.
        """
        return await SkillSyncService.sync_all(query_db)

    @classmethod
    async def add_skill_file_services(cls, query_db: AsyncSession, file_model: SkillFileModel):
        """
        ??????

        :param query_db: orm??
        :param file_model: ????
        :return: ????
        """
        # ?????????
        existing = await SkillFileDao.get_file_by_path(query_db, file_model.skill_id, file_model.file_path)
        if existing:
            raise ServiceException(message=f'?? {file_model.file_path} ???')

        try:
            await SkillFileDao.add_file_dao(query_db, file_model)
            await query_db.commit()

            # ???????
            skill = await SkillDao.get_skill_detail_by_id(query_db, file_model.skill_id)
            if skill and skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return CrudResponseModel(is_success=True, message='??????')
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_skill_file_services(cls, query_db: AsyncSession, file_model: SkillFileModel):
        """
        ????????

        :param query_db: orm??
        :param file_model: ????
        :return: ????
        """
        edit_file = file_model.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        file_obj = await SkillFileDao.get_file_by_id(query_db, file_model.file_id)
        if file_obj:
            file_skill_id = file_obj.skill_id
            try:
                await SkillFileDao.edit_file_dao(query_db, edit_file)
                await query_db.commit()

                # ???????
                skill = await SkillDao.get_skill_detail_by_id(query_db, file_skill_id)
                if skill and skill.enabled:
                    await SkillSyncService.sync_skill(query_db, skill.skill_name)

                return CrudResponseModel(is_success=True, message='??????')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='?????')

    @classmethod
    async def delete_skill_file_services(cls, query_db: AsyncSession, skill_id, file_id):
        """
        ??????

        :param query_db: orm??
        :param skill_id: ??ID
        :param file_id: ??ID
        :return: ????
        """
        try:
            await SkillFileDao.delete_file_dao(query_db, file_id)
            await query_db.commit()

            # ???????
            skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
            if skill and skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return CrudResponseModel(is_success=True, message='删除文件成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    # ==================== 文件夹管理 ====================

    @classmethod
    def _normalize_folder_path(cls, folder_path: str) -> str:
        """
        Normalize and validate a folder path. Returns path WITH trailing slash stripped.
        """
        if not folder_path:
            raise ServiceException(message='folder_path cannot be empty')
        raw = folder_path.strip().replace('\\', '/')
        # Strip leading/trailing slashes
        raw = raw.strip('/')
        if not raw:
            raise ServiceException(message='folder_path cannot be empty')
        parts = [p for p in raw.split('/') if p and p != '.']
        if not parts:
            raise ServiceException(message='folder_path cannot be empty')
        if any(part == '..' for part in parts):
            raise ServiceException(message=f'illegal folder path: {folder_path}')
        if ':' in parts[0]:
            raise ServiceException(message=f'illegal folder path: {folder_path}')
        return '/'.join(parts)

    @classmethod
    async def create_skill_folder_services(
        cls, query_db: AsyncSession, skill_id, folder_model: SkillFolderCreateModel, operator: str
    ):
        """
        Create a subfolder by adding a .gitkeep placeholder file.
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
        if not skill:
            raise ServiceException(message='Skill not found')

        folder_path = cls._normalize_folder_path(folder_model.folder_path)
        gitkeep_path = f'{folder_path}/.gitkeep'

        # Check if folder already has files
        existing_files = await SkillFileDao.get_files_by_path_prefix(
            query_db, skill_id, f'{folder_path}/'
        )
        if existing_files:
            raise ServiceException(message=f'文件夹 {folder_path} 已存在')

        now = datetime.now()
        try:
            await SkillFileDao.add_file_dao(
                query_db,
                SkillFileModel(
                    skill_id=skill_id,
                    file_path=gitkeep_path,
                    content='',
                    is_binary=False,
                    create_by=operator,
                    create_time=now,
                    update_by=operator,
                    update_time=now,
                ),
            )
            await query_db.commit()

            if skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return {'skillId': str(skill_id), 'folderPath': folder_path, 'action': 'created'}
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def rename_skill_folder_services(
        cls, query_db: AsyncSession, skill_id, folder_model: SkillFolderRenameModel, operator: str
    ):
        """
        Rename a subfolder by updating all file paths with the old prefix to the new prefix.
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
        if not skill:
            raise ServiceException(message='Skill not found')

        old_path = cls._normalize_folder_path(folder_model.old_path)
        new_path = cls._normalize_folder_path(folder_model.new_path)

        if old_path == new_path:
            raise ServiceException(message='新旧文件夹路径相同')

        old_prefix = f'{old_path}/'
        new_prefix = f'{new_path}/'

        # Check source folder has files
        source_files = await SkillFileDao.get_files_by_path_prefix(query_db, skill_id, old_prefix)
        if not source_files:
            raise ServiceException(message=f'文件夹 {old_path} 不存在或为空')

        # Check target folder doesn't already exist
        target_files = await SkillFileDao.get_files_by_path_prefix(query_db, skill_id, new_prefix)
        if target_files:
            raise ServiceException(message=f'目标文件夹 {new_path} 已存在')

        now = datetime.now()
        try:
            for file_obj in source_files:
                new_file_path = new_prefix + file_obj.file_path[len(old_prefix):]
                await SkillFileDao.edit_file_dao(
                    query_db,
                    {
                        'file_id': file_obj.file_id,
                        'file_path': new_file_path,
                        'update_by': operator,
                        'update_time': now,
                    },
                )
            await query_db.commit()

            if skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return {
                'skillId': str(skill_id),
                'oldPath': old_path,
                'newPath': new_path,
                'filesRenamed': len(source_files),
            }
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_skill_folder_services(
        cls, query_db: AsyncSession, skill_id, folder_model: SkillFolderDeleteModel
    ):
        """
        Delete a subfolder and all files inside it.
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
        if not skill:
            raise ServiceException(message='Skill not found')

        folder_path = cls._normalize_folder_path(folder_model.folder_path)
        prefix = f'{folder_path}/'

        # Check folder has files
        files = await SkillFileDao.get_files_by_path_prefix(query_db, skill_id, prefix)
        if not files:
            raise ServiceException(message=f'文件夹 {folder_path} 不存在或为空')

        try:
            await SkillFileDao.batch_delete_by_path_prefix(query_db, skill_id, prefix)
            await query_db.commit()

            if skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return {
                'skillId': str(skill_id),
                'folderPath': folder_path,
                'filesDeleted': len(files),
            }
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def move_skill_file_services(
        cls, query_db: AsyncSession, skill_id, move_model: SkillFileMoveModel, operator: str
    ):
        """
        Move a file to a new path within the same skill.
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
        if not skill:
            raise ServiceException(message='Skill not found')

        old_path = cls._normalize_skill_file_path(move_model.old_path)
        new_path = cls._normalize_skill_file_path(move_model.new_path)

        if old_path == new_path:
            raise ServiceException(message='新旧文件路径相同')

        # Check source file exists
        source_file = await SkillFileDao.get_file_by_path(query_db, skill_id, old_path)
        if not source_file:
            raise ServiceException(message=f'文件 {old_path} 不存在')

        # Check target path not occupied
        target_file = await SkillFileDao.get_file_by_path(query_db, skill_id, new_path)
        if target_file:
            raise ServiceException(message=f'目标路径 {new_path} 已有文件')

        now = datetime.now()
        try:
            await SkillFileDao.edit_file_dao(
                query_db,
                {
                    'file_id': source_file.file_id,
                    'file_path': new_path,
                    'update_by': operator,
                    'update_time': now,
                },
            )

            # If old folder is now empty, clean up .gitkeep if it was the only remaining file
            old_dir = '/'.join(old_path.split('/')[:-1])
            if old_dir:
                remaining = await SkillFileDao.get_files_by_path_prefix(
                    query_db, skill_id, f'{old_dir}/'
                )
                # If only .gitkeep remains and it's the only file, keep it for empty folder tracking
                # No auto-cleanup needed - user can delete folder explicitly

            await query_db.commit()

            if skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return {
                'skillId': str(skill_id),
                'oldPath': old_path,
                'newPath': new_path,
                'action': 'moved',
            }
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def upload_skill_services(cls, query_db: AsyncSession, file_bytes: bytes, filename: str, user_name: str):
        """
        ??????????? ZIP ? MD?

        :param query_db: orm??
        :param file_bytes: ????
        :param filename: ?????
        :param user_name: ?????
        :return: ????
        """
        lower_name = (filename or '').lower()
        if lower_name.endswith('.md'):
            try:
                md_content = file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                raise ValueError('MD?????????UTF-8??')
            result = await SkillImportService.import_from_md(query_db, md_content, filename, user_name)
        else:
            result = await SkillImportService.import_from_zip(query_db, file_bytes, user_name)
        return CrudResponseModel(
            is_success=True,
            message=f'????: {result["skill_name"]}?? {result["file_count"]} ???'
        )

    @classmethod
    async def import_url_skill_services(
        cls, query_db: AsyncSession, import_model: SkillImportUrlModel, user_name: str
    ):
        """
        ?URL????

        :param query_db: orm??
        :param import_model: URL????
        :param user_name: ?????
        :return: ????
        """
        result = await SkillImportService.import_from_url(
            query_db, import_model.url, import_model.skill_name, user_name
        )
        return CrudResponseModel(
            is_success=True,
            message=f'????: {result["skill_name"]}?? {result["file_count"]} ???'
        )

    # ==================== ?? ====================

    @staticmethod
    async def export_skill_list_services(skill_list: List):
        """
        ??????

        :param skill_list: ????
        :return: excel?????
        """
        mapping_dict = {
            'skillId': '??ID',
            'skillName': '?????',
            'displayName': '????',
            'description': '??',
            'enabled': '????',
            'sourceType': '????',
            'sourceUrl': '??URL',
            'allowedTools': '?????',
            'licenseInfo': '???',
            'createBy': '???',
            'createTime': '????',
            'updateBy': '???',
            'updateTime': '????',
        }
        binary_data = ExcelUtil.export_list2excel(skill_list, mapping_dict)
        return binary_data
