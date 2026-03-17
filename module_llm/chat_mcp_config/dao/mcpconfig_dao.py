from uuid import UUID as PyUUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_llm.chat_mcp_config.entity.do.mcpconfig_do import LlmMcpConfig
from module_llm.chat_mcp_config.entity.vo.mcpconfig_vo import McpconfigModel, McpconfigPageQueryModel, \
    McpconfigQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db


class McpconfigDao:
    """
    MCP服务器配置模块数据库操作层
    """

    @classmethod
    async def get_mcpconfig_by_ids(cls, db: AsyncSession, config_ids: List[str]) -> List[LlmMcpConfig]:
        """
        根据配置ID列表批量获取MCP服务器配置

        :param db: orm对象
        :param config_ids: 配置ID字符串列表
        :return: LlmMcpConfig ORM对象列表
        """
        uuid_ids = [PyUUID(cid) for cid in config_ids]
        result = await db.execute(
            select(LlmMcpConfig)
            .where(
                LlmMcpConfig.config_id.in_(uuid_ids),
                LlmMcpConfig.del_flag == "0",
            )
        )
        return list(result.scalars().all())

    @classmethod
    async def get_mcpconfig_detail_by_id(cls, db: AsyncSession, config_id: int):
        """
        根据配置唯一标识符(UUID)获取MCP服务器配置详细信息

        :param db: orm对象
        :param config_id: 配置唯一标识符(UUID)
        :return: MCP服务器配置信息对象
        """
        mcpconfig_info = (
            (
                await db.execute(
                    select(LlmMcpConfig)
                    .where(
                        LlmMcpConfig.config_id == config_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return mcpconfig_info

    @classmethod
    async def get_mcpconfig_detail_by_info(cls, db: AsyncSession, mcpconfig: McpconfigModel):
        """
        根据MCP服务器配置参数获取MCP服务器配置信息

        :param db: orm对象
        :param mcpconfig: MCP服务器配置参数对象
        :return: MCP服务器配置信息对象
        """
        mcpconfig_info = (
            (
                await db.execute(
                    select(LlmMcpConfig).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return mcpconfig_info

    @classmethod
    async def get_mcpconfig_list(cls, db: AsyncSession, query_object: McpconfigPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取MCP服务器配置列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: MCP服务器配置列表信息字典对象
        """
        query = (
            select(LlmMcpConfig)
            .where(
                LlmMcpConfig.server_name.like(f'%{query_object.server_name}%') if query_object.server_name else True,
            )
            .where(LlmMcpConfig.del_flag == "0")
            .order_by(LlmMcpConfig.config_id)
            # .distinct()
        )
        mcpconfig_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return mcpconfig_list

    @classmethod
    async def get_mcpconfig_orm_list(cls, db: AsyncSession, query_object: McpconfigQueryModel) -> List[
        McpconfigQueryModel]:
        """
        根据查询参数获取MCP服务器配置列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: MCP服务器配置列表信息orm对象
        """
        query = (
            select(LlmMcpConfig)
            .where(
                LlmMcpConfig.server_name.like(f'%{query_object.server_name}%') if query_object.server_name else True,
            )
            .where(LlmMcpConfig.del_flag == "0")
            .order_by(LlmMcpConfig.config_id)
            # .distinct()
        )

        result = await db.execute(query)
        return [McpconfigQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_mcpconfig_dao(cls, db: AsyncSession, mcpconfig: McpconfigModel):
        """
        新增MCP服务器配置数据库操作

        :param db: orm对象
        :param mcpconfig: MCP服务器配置对象
        :return:
        """
        db_mcpconfig = LlmMcpConfig(**mcpconfig.model_dump(exclude={}))
        db.add(db_mcpconfig)
        await db.flush()

        return db_mcpconfig

    @classmethod
    async def edit_mcpconfig_dao(cls, db: AsyncSession, mcpconfig: dict):
        """
        编辑MCP服务器配置数据库操作

        :param db: orm对象
        :param mcpconfig: 需要更新的MCP服务器配置字典
        :return:
        """
        await db.execute(update(LlmMcpConfig), [mcpconfig])

    @classmethod
    async def delete_mcpconfig_dao(cls, db: AsyncSession, mcpconfig: McpconfigModel):
        """
        删除MCP服务器配置数据库操作

        :param db: orm对象
        :param mcpconfig: MCP服务器配置对象
        :return:
        """
        # await db.execute(delete(LlmMcpConfig).where(LlmMcpConfig.config_id.in_([mcpconfig.config_id])))
        await db.execute(
            update(LlmMcpConfig).where(LlmMcpConfig.config_id.in_([mcpconfig.config_id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = McpconfigPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await McpconfigDao.get_mcpconfig_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
