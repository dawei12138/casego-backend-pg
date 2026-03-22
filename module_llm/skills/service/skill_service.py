# -*- coding: utf-8 -*-
"""
AI技能模块服务层
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime

from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_llm.skills.dao.skill_dao import SkillDao
from module_llm.skills.dao.skill_file_dao import SkillFileDao
from module_llm.skills.entity.vo.skill_vo import (
    DeleteSkillModel, SkillModel, SkillPageQueryModel,
    SkillFileModel, SkillDetailModel, SkillImportUrlModel,
)
from module_llm.skills.service.skill_sync_service import SkillSyncService
from module_llm.skills.service.skill_import_service import SkillImportService
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil
from utils.log_util import logger


class SkillService:
    """
    AI技能模块服务层
    """

    # ==================== 列表查询 ====================

    @classmethod
    async def get_skill_list_services(
        cls, query_db: AsyncSession, query_object: SkillPageQueryModel, is_page: bool = False
    ):
        """
        获取技能列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 技能列表信息对象
        """
        skill_list_result = await SkillDao.get_skill_list(query_db, query_object, is_page)
        return skill_list_result

    @classmethod
    async def get_skill_all_list_services(
        cls, query_db: AsyncSession, query_object: SkillPageQueryModel
    ):
        """
        获取所有技能列表（用于下拉选择）

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :return: 技能简要列表
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

    # ==================== 详情 ====================

    @classmethod
    async def skill_detail_services(cls, query_db: AsyncSession, skill_id):
        """
        获取技能详细信息（含文件列表）

        :param query_db: orm对象
        :param skill_id: 技能ID
        :return: 技能详情对象
        """
        skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id=skill_id)
        if skill:
            skill_dict = CamelCaseUtil.transform_result(skill)
            files = await SkillFileDao.get_files_by_skill_id(query_db, skill_id)
            file_list = []
            for f in files:
                file_dict = CamelCaseUtil.transform_result(f)
                # 列表中不返回文件内容，减少传输量
                file_dict.pop('content', None)
                file_list.append(SkillFileModel(**file_dict))
            result = SkillDetailModel(**skill_dict, files=file_list)
        else:
            result = SkillDetailModel(**dict())
        return result

    # ==================== 新增 ====================

    @classmethod
    async def add_skill_services(cls, query_db: AsyncSession, page_object: SkillModel):
        """
        新增技能service

        :param query_db: orm对象
        :param page_object: 新增技能对象
        :return: 新增结果
        """
        # 验证技能名合法性
        if not SkillImportService.validate_skill_name(page_object.skill_name):
            raise ServiceException(message=f'技能目录名不合法: {page_object.skill_name}（只允许小写字母、数字和连字符）')

        # 检查唯一性
        existing = await SkillDao.get_skill_by_name(query_db, page_object.skill_name)
        if existing:
            raise ServiceException(message=f'技能 {page_object.skill_name} 已存在')

        try:
            db_skill = await SkillDao.add_skill_dao(query_db, page_object)

            # 如果没有提交 SKILL.md，自动生成一个
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

            # 同步到文件系统
            if page_object.enabled is not False:
                await SkillSyncService.sync_skill(query_db, page_object.skill_name)

            return CrudResponseModel(is_success=True, message='新增成功')
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    # ==================== 编辑 ====================

    @classmethod
    async def edit_skill_services(cls, query_db: AsyncSession, page_object: SkillModel):
        """
        编辑技能信息service

        :param query_db: orm对象
        :param page_object: 编辑技能对象
        :return: 编辑结果
        """
        edit_skill = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        skill_info = await cls.skill_detail_services(query_db, page_object.skill_id)
        if skill_info.skill_id:
            old_skill_name = skill_info.skill_name
            try:
                # 如果修改了 skill_name，需要验证新名称
                if page_object.skill_name and page_object.skill_name != old_skill_name:
                    if not SkillImportService.validate_skill_name(page_object.skill_name):
                        raise ServiceException(
                            message=f'技能目录名不合法: {page_object.skill_name}'
                        )
                    existing = await SkillDao.get_skill_by_name(query_db, page_object.skill_name)
                    if existing:
                        raise ServiceException(message=f'技能 {page_object.skill_name} 已存在')

                await SkillDao.edit_skill_dao(query_db, edit_skill)
                await query_db.commit()

                # 如果修改了名称，先移除旧目录
                new_skill_name = page_object.skill_name or old_skill_name
                if page_object.skill_name and page_object.skill_name != old_skill_name:
                    await SkillSyncService.remove_skill(old_skill_name)

                # 同步到文件系统
                await SkillSyncService.sync_skill(query_db, new_skill_name)

                return CrudResponseModel(is_success=True, message='更新成功')
            except ServiceException:
                await query_db.rollback()
                raise
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='技能不存在')

    # ==================== 删除 ====================

    @classmethod
    async def delete_skill_services(cls, query_db: AsyncSession, page_object: DeleteSkillModel):
        """
        删除技能service

        :param query_db: orm对象
        :param page_object: 删除技能对象
        :return: 删除结果
        """
        if page_object.skill_ids:
            skill_id_list = page_object.skill_ids.split(',')
            try:
                skill_names = []
                for skill_id in skill_id_list:
                    skill_id_obj = SkillModel.model_validate({'skill_id': skill_id}).skill_id
                    # 获取技能名称用于后续文件系统清理
                    skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id_obj)
                    if skill:
                        skill_names.append(skill.skill_name)
                    # 软删除技能和关联文件
                    await SkillDao.delete_skill_dao(query_db, SkillModel(skill_id=skill_id_obj))
                    await SkillFileDao.delete_files_by_skill_id(query_db, skill_id_obj)

                await query_db.commit()

                # 移除文件系统中的技能目录
                for name in skill_names:
                    await SkillSyncService.remove_skill(name)

                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入技能ID为空')

    # ==================== 文件操作 ====================

    @classmethod
    async def get_skill_files_services(cls, query_db: AsyncSession, skill_id):
        """
        获取技能文件列表（不含内容）

        :param query_db: orm对象
        :param skill_id: 技能ID
        :return: 文件列表
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
        获取技能指定文件内容

        :param query_db: orm对象
        :param skill_id: 技能ID
        :param file_path: 文件相对路径
        :return: 文件内容对象
        """
        file_obj = await SkillFileDao.get_file_by_path(query_db, skill_id, file_path)
        if file_obj:
            return SkillFileModel(**CamelCaseUtil.transform_result(file_obj))
        else:
            return SkillFileModel(**dict())

    @classmethod
    async def add_skill_file_services(cls, query_db: AsyncSession, file_model: SkillFileModel):
        """
        新增技能文件

        :param query_db: orm对象
        :param file_model: 文件对象
        :return: 新增结果
        """
        # 检查文件是否已存在
        existing = await SkillFileDao.get_file_by_path(query_db, file_model.skill_id, file_model.file_path)
        if existing:
            raise ServiceException(message=f'文件 {file_model.file_path} 已存在')

        try:
            await SkillFileDao.add_file_dao(query_db, file_model)
            await query_db.commit()

            # 同步到文件系统
            skill = await SkillDao.get_skill_detail_by_id(query_db, file_model.skill_id)
            if skill and skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return CrudResponseModel(is_success=True, message='新增文件成功')
        except ServiceException:
            await query_db.rollback()
            raise
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_skill_file_services(cls, query_db: AsyncSession, file_model: SkillFileModel):
        """
        编辑技能文件内容

        :param query_db: orm对象
        :param file_model: 文件对象
        :return: 编辑结果
        """
        edit_file = file_model.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        file_obj = await SkillFileDao.get_file_by_id(query_db, file_model.file_id)
        if file_obj:
            try:
                await SkillFileDao.edit_file_dao(query_db, edit_file)
                await query_db.commit()

                # 同步到文件系统
                skill = await SkillDao.get_skill_detail_by_id(query_db, file_obj.skill_id)
                if skill and skill.enabled:
                    await SkillSyncService.sync_skill(query_db, skill.skill_name)

                return CrudResponseModel(is_success=True, message='更新文件成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='文件不存在')

    @classmethod
    async def delete_skill_file_services(cls, query_db: AsyncSession, skill_id, file_id):
        """
        删除技能文件

        :param query_db: orm对象
        :param skill_id: 技能ID
        :param file_id: 文件ID
        :return: 删除结果
        """
        try:
            await SkillFileDao.delete_file_dao(query_db, file_id)
            await query_db.commit()

            # 同步到文件系统
            skill = await SkillDao.get_skill_detail_by_id(query_db, skill_id)
            if skill and skill.enabled:
                await SkillSyncService.sync_skill(query_db, skill.skill_name)

            return CrudResponseModel(is_success=True, message='删除文件成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    # ==================== 导入 ====================

    @classmethod
    async def upload_skill_services(cls, query_db: AsyncSession, file_bytes: bytes, filename: str, user_name: str):
        """
        上传文件导入技能（支持 ZIP 和 MD）

        :param query_db: orm对象
        :param file_bytes: 文件字节
        :param filename: 原始文件名
        :param user_name: 当前用户名
        :return: 导入结果
        """
        lower_name = (filename or '').lower()
        if lower_name.endswith('.md'):
            try:
                md_content = file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                raise ValueError('MD文件内容无法解码为UTF-8文本')
            result = await SkillImportService.import_from_md(query_db, md_content, filename, user_name)
        else:
            result = await SkillImportService.import_from_zip(query_db, file_bytes, user_name)
        return CrudResponseModel(
            is_success=True,
            message=f'导入成功: {result["skill_name"]}，共 {result["file_count"]} 个文件'
        )

    @classmethod
    async def import_url_skill_services(
        cls, query_db: AsyncSession, import_model: SkillImportUrlModel, user_name: str
    ):
        """
        从URL导入技能

        :param query_db: orm对象
        :param import_model: URL导入模型
        :param user_name: 当前用户名
        :return: 导入结果
        """
        result = await SkillImportService.import_from_url(
            query_db, import_model.url, import_model.skill_name, user_name
        )
        return CrudResponseModel(
            is_success=True,
            message=f'导入成功: {result["skill_name"]}，共 {result["file_count"]} 个文件'
        )

    # ==================== 导出 ====================

    @staticmethod
    async def export_skill_list_services(skill_list: List):
        """
        导出技能列表

        :param skill_list: 技能列表
        :return: excel二进制数据
        """
        mapping_dict = {
            'skillId': '技能ID',
            'skillName': '技能目录名',
            'displayName': '显示名称',
            'description': '描述',
            'enabled': '是否启用',
            'sourceType': '来源类型',
            'sourceUrl': '来源URL',
            'allowedTools': '允许的工具',
            'licenseInfo': '许可证',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
        }
        binary_data = ExcelUtil.export_list2excel(skill_list, mapping_dict)
        return binary_data
