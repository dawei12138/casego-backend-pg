from uuid import UUID as PyUUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_llm.skills.entity.do.skill_do import LlmSkill
from module_llm.skills.entity.vo.skill_vo import SkillModel, SkillPageQueryModel, SkillQueryModel
from utils.page_util import PageUtil


class SkillDao:
    """
    AI技能模块数据库操作层
    """

    @classmethod
    async def get_skill_by_ids(cls, db: AsyncSession, skill_ids: List[str]) -> List[LlmSkill]:
        """
        根据技能ID列表批量获取技能配置

        :param db: orm对象
        :param skill_ids: 技能ID字符串列表
        :return: LlmSkill ORM对象列表
        """
        uuid_ids = [PyUUID(sid) for sid in skill_ids]
        result = await db.execute(
            select(LlmSkill)
            .where(
                LlmSkill.skill_id.in_(uuid_ids),
                LlmSkill.del_flag == "0",
            )
        )
        return list(result.scalars().all())

    @classmethod
    async def get_skill_detail_by_id(cls, db: AsyncSession, skill_id):
        """
        根据技能ID获取技能详细信息

        :param db: orm对象
        :param skill_id: 技能唯一标识符(UUID)
        :return: 技能信息对象
        """
        skill_info = (
            (
                await db.execute(
                    select(LlmSkill)
                    .where(
                        LlmSkill.skill_id == skill_id,
                        LlmSkill.del_flag == "0",
                    )
                )
            )
            .scalars()
            .first()
        )
        return skill_info

    @classmethod
    async def get_skill_by_name(cls, db: AsyncSession, skill_name: str):
        """
        根据技能目录名获取技能信息（用于唯一性检查）

        :param db: orm对象
        :param skill_name: 技能目录名
        :return: 技能信息对象
        """
        skill_info = (
            (
                await db.execute(
                    select(LlmSkill)
                    .where(
                        LlmSkill.skill_name == skill_name,
                        LlmSkill.del_flag == "0",
                    )
                )
            )
            .scalars()
            .first()
        )
        return skill_info

    @classmethod
    async def get_skill_list(cls, db: AsyncSession, query_object: SkillPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取技能列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 技能列表信息字典对象
        """
        query = (
            select(LlmSkill)
            .where(
                LlmSkill.skill_name.like(f'%{query_object.skill_name}%') if query_object.skill_name else True,
                LlmSkill.enabled == query_object.enabled if query_object.enabled is not None else True,
            )
            .where(LlmSkill.del_flag == "0")
            .order_by(LlmSkill.sort_no, LlmSkill.create_time.desc())
        )
        skill_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return skill_list

    @classmethod
    async def get_all_enabled_skills(cls, db: AsyncSession) -> List[LlmSkill]:
        """
        获取所有启用的技能（用于启动时文件系统同步）

        :param db: orm对象
        :return: 启用的技能列表
        """
        result = await db.execute(
            select(LlmSkill)
            .where(
                LlmSkill.enabled == True,
                LlmSkill.del_flag == "0",
            )
            .order_by(LlmSkill.sort_no)
        )
        return list(result.scalars().all())

    @classmethod
    async def add_skill_dao(cls, db: AsyncSession, skill: SkillModel):
        """
        新增技能数据库操作

        :param db: orm对象
        :param skill: 技能对象
        :return: 新增的技能ORM对象
        """
        db_skill = LlmSkill(**skill.model_dump(exclude={}))
        db.add(db_skill)
        await db.flush()
        return db_skill

    @classmethod
    async def edit_skill_dao(cls, db: AsyncSession, skill: dict):
        """
        编辑技能数据库操作

        :param db: orm对象
        :param skill: 需要更新的技能字典
        :return:
        """
        await db.execute(update(LlmSkill), [skill])

    @classmethod
    async def delete_skill_dao(cls, db: AsyncSession, skill: SkillModel):
        """
        删除技能数据库操作（软删除）

        :param db: orm对象
        :param skill: 技能对象
        :return:
        """
        await db.execute(
            update(LlmSkill)
            .where(LlmSkill.skill_id.in_([skill.skill_id]))
            .values(del_flag="1")
        )
