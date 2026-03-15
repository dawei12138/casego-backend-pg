from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.agents.entity.do.agents_do import AppAgents
from module_app.agents.entity.vo.agents_vo import AgentsModel, AgentsPageQueryModel, AgentsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class AgentsDao:
    """
    Agent代理模块数据库操作层
    """

    @classmethod
    async def get_agents_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取Agent代理详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: Agent代理信息对象
        """
        agents_info = (
            (
                await db.execute(
                    select(AppAgents)
                    .where(
                        AppAgents.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return agents_info

    @classmethod
    async def get_agents_detail_by_info(cls, db: AsyncSession, agents: AgentsModel):
        """
        根据Agent代理参数获取Agent代理信息

        :param db: orm对象
        :param agents: Agent代理参数对象
        :return: Agent代理信息对象
        """
        agents_info = (
            (
                await db.execute(
                    select(AppAgents).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return agents_info

    @classmethod
    async def get_agents_list(cls, db: AsyncSession, query_object: AgentsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取Agent代理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: Agent代理列表信息字典对象
        """
        query = (
            select(AppAgents)
            .where(
                AppAgents.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppAgents.host == query_object.host if query_object.host else True,
                AppAgents.port == query_object.port if query_object.port else True,
                AppAgents.secret_key == query_object.secret_key if query_object.secret_key else True,
                AppAgents.status == query_object.status if query_object.status else True,
                AppAgents.system_type == query_object.system_type if query_object.system_type else True,
                AppAgents.version == query_object.version if query_object.version else True,
                AppAgents.lock_version == query_object.lock_version if query_object.lock_version else True,
                AppAgents.high_temp == query_object.high_temp if query_object.high_temp else True,
                AppAgents.high_temp_time == query_object.high_temp_time if query_object.high_temp_time else True,
                AppAgents.has_hub == query_object.has_hub if query_object.has_hub else True,
                AppAgents.description == query_object.description if query_object.description else True,
                AppAgents.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppAgents.del_flag == "0")
            .order_by(AppAgents.id)
            #.distinct()
        )
        agents_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return agents_list

    @classmethod
    async def get_agents_orm_list(cls, db: AsyncSession, query_object: AgentsQueryModel) -> List[AgentsQueryModel]:
        """
        根据查询参数获取Agent代理列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: Agent代理列表信息orm对象
        """
        query = (
            select(AppAgents)
            .where(
                AppAgents.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppAgents.host == query_object.host if query_object.host else True,
                AppAgents.port == query_object.port if query_object.port else True,
                AppAgents.secret_key == query_object.secret_key if query_object.secret_key else True,
                AppAgents.status == query_object.status if query_object.status else True,
                AppAgents.system_type == query_object.system_type if query_object.system_type else True,
                AppAgents.version == query_object.version if query_object.version else True,
                AppAgents.lock_version == query_object.lock_version if query_object.lock_version else True,
                AppAgents.high_temp == query_object.high_temp if query_object.high_temp else True,
                AppAgents.high_temp_time == query_object.high_temp_time if query_object.high_temp_time else True,
                AppAgents.has_hub == query_object.has_hub if query_object.has_hub else True,
                AppAgents.description == query_object.description if query_object.description else True,
                AppAgents.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppAgents.del_flag == "0")
            .order_by(AppAgents.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [AgentsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_agents_dao(cls, db: AsyncSession, agents: AgentsModel):
        """
        新增Agent代理数据库操作

        :param db: orm对象
        :param agents: Agent代理对象
        :return:
        """
        db_agents = AppAgents(**agents.model_dump(exclude={}))
        db.add(db_agents)
        await db.flush()

        return db_agents

    @classmethod
    async def edit_agents_dao(cls, db: AsyncSession, agents: dict):
        """
        编辑Agent代理数据库操作

        :param db: orm对象
        :param agents: 需要更新的Agent代理字典
        :return:
        """
        await db.execute(update(AppAgents), [agents])

    @classmethod
    async def delete_agents_dao(cls, db: AsyncSession, agents: AgentsModel):
        """
        删除Agent代理数据库操作

        :param db: orm对象
        :param agents: Agent代理对象
        :return:
        """
        #await db.execute(delete(AppAgents).where(AppAgents.id.in_([agents.id])))
        await db.execute(update(AppAgents).where(AppAgents.id.in_([agents.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = AgentsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await AgentsDao.get_agents_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
