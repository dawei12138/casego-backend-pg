from uuid import UUID as PyUUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_llm.skills.entity.do.skill_file_do import LlmSkillFile
from module_llm.skills.entity.vo.skill_vo import SkillFileModel


class SkillFileDao:
    """
    AI技能文件模块数据库操作层
    """

    @classmethod
    async def get_files_by_skill_id(cls, db: AsyncSession, skill_id) -> List[LlmSkillFile]:
        """
        获取技能下所有文件

        :param db: orm对象
        :param skill_id: 技能ID
        :return: 文件列表
        """
        result = await db.execute(
            select(LlmSkillFile)
            .where(
                LlmSkillFile.skill_id == skill_id,
                LlmSkillFile.del_flag == "0",
            )
            .order_by(LlmSkillFile.file_path)
        )
        return list(result.scalars().all())

    @classmethod
    async def get_file_by_id(cls, db: AsyncSession, file_id):
        """
        根据文件ID获取文件信息

        :param db: orm对象
        :param file_id: 文件ID
        :return: 文件信息对象
        """
        file_info = (
            (
                await db.execute(
                    select(LlmSkillFile)
                    .where(
                        LlmSkillFile.file_id == file_id,
                        LlmSkillFile.del_flag == "0",
                    )
                )
            )
            .scalars()
            .first()
        )
        return file_info

    @classmethod
    async def get_file_by_path(cls, db: AsyncSession, skill_id, file_path: str):
        """
        根据技能ID和文件路径获取文件信息

        :param db: orm对象
        :param skill_id: 技能ID
        :param file_path: 文件相对路径
        :return: 文件信息对象
        """
        file_info = (
            (
                await db.execute(
                    select(LlmSkillFile)
                    .where(
                        LlmSkillFile.skill_id == skill_id,
                        LlmSkillFile.file_path == file_path,
                        LlmSkillFile.del_flag == "0",
                    )
                )
            )
            .scalars()
            .first()
        )
        return file_info

    @classmethod
    async def add_file_dao(cls, db: AsyncSession, file: SkillFileModel):
        """
        新增技能文件数据库操作

        :param db: orm对象
        :param file: 文件对象
        :return: 新增的文件ORM对象
        """
        db_file = LlmSkillFile(**file.model_dump(exclude={}))
        db.add(db_file)
        await db.flush()
        return db_file

    @classmethod
    async def edit_file_dao(cls, db: AsyncSession, file: dict):
        """
        编辑技能文件数据库操作

        :param db: orm对象
        :param file: 需要更新的文件字典
        :return:
        """
        await db.execute(update(LlmSkillFile), [file])

    @classmethod
    async def delete_file_dao(cls, db: AsyncSession, file_id):
        """
        删除技能文件数据库操作（软删除）

        :param db: orm对象
        :param file_id: 文件ID
        :return:
        """
        await db.execute(
            update(LlmSkillFile)
            .where(LlmSkillFile.file_id == file_id)
            .values(del_flag="1")
        )

    @classmethod
    async def delete_files_by_skill_id(cls, db: AsyncSession, skill_id):
        """
        删除技能下所有文件（软删除，用于删除技能时）

        :param db: orm对象
        :param skill_id: 技能ID
        :return:
        """
        await db.execute(
            update(LlmSkillFile)
            .where(LlmSkillFile.skill_id == skill_id)
            .values(del_flag="1")
        )
