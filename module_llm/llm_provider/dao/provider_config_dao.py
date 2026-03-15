from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_llm.llm_provider.entity.do.provider_config_do import LlmProvider
from module_llm.llm_provider.entity.vo.provider_config_vo import Provider_configModel, Provider_configPageQueryModel, Provider_configQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Provider_configDao:
    """
    LLM提供商配置模块数据库操作层
    """

    @classmethod
    async def get_provider_config_detail_by_id(cls, db: AsyncSession, provider_id: int):
        """
        根据提供商配置ID获取LLM提供商配置详细信息

        :param db: orm对象
        :param provider_id: 提供商配置ID
        :return: LLM提供商配置信息对象
        """
        provider_config_info = (
            (
                await db.execute(
                    select(LlmProvider)
                    .where(
                        LlmProvider.provider_id == provider_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return provider_config_info

    @classmethod
    async def get_provider_config_by_key(cls, db: AsyncSession, provider_key: str):
        """
        根据提供商标识获取LLM提供商配置详细信息

        :param db: orm对象
        :param provider_key: 提供商标识(如openai/anthropic/deepseek等)
        :return: LLM提供商配置信息对象
        """
        provider_config_info = (
            (
                await db.execute(
                    select(LlmProvider)
                    .where(
                        LlmProvider.provider_key == provider_key,
                        LlmProvider.del_flag == "0",
                    )
                )
            )
            .scalars()
            .first()
        )

        return provider_config_info

    @classmethod
    async def get_provider_config_detail_by_info(cls, db: AsyncSession, provider_config: Provider_configModel):
        """
        根据LLM提供商配置参数获取LLM提供商配置信息

        :param db: orm对象
        :param provider_config: LLM提供商配置参数对象
        :return: LLM提供商配置信息对象
        """
        provider_config_info = (
            (
                await db.execute(
                    select(LlmProvider).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return provider_config_info

    @classmethod
    async def get_provider_config_list(cls, db: AsyncSession, query_object: Provider_configPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取LLM提供商配置列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: LLM提供商配置列表信息字典对象
        """
        query = (
            select(LlmProvider)
            .where(
            )
            .where(LlmProvider.del_flag == "0")
            .order_by(LlmProvider.provider_id)
            #.distinct()
        )
        provider_config_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return provider_config_list

    @classmethod
    async def get_provider_config_orm_list(cls, db: AsyncSession, query_object: Provider_configQueryModel) -> List[Provider_configQueryModel]:
        """
        根据查询参数获取LLM提供商配置列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: LLM提供商配置列表信息orm对象
        """
        query = (
            select(LlmProvider)
            .where(
            )
            .where(LlmProvider.del_flag == "0")
            .order_by(LlmProvider.provider_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Provider_configQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_provider_config_dao(cls, db: AsyncSession, provider_config: Provider_configModel):
        """
        新增LLM提供商配置数据库操作

        :param db: orm对象
        :param provider_config: LLM提供商配置对象
        :return:
        """
        db_provider_config = LlmProvider(**provider_config.model_dump(exclude={}))
        db.add(db_provider_config)
        await db.flush()

        return db_provider_config

    @classmethod
    async def edit_provider_config_dao(cls, db: AsyncSession, provider_config: dict):
        """
        编辑LLM提供商配置数据库操作

        :param db: orm对象
        :param provider_config: 需要更新的LLM提供商配置字典
        :return:
        """
        await db.execute(update(LlmProvider), [provider_config])

    @classmethod
    async def delete_provider_config_dao(cls, db: AsyncSession, provider_config: Provider_configModel):
        """
        删除LLM提供商配置数据库操作

        :param db: orm对象
        :param provider_config: LLM提供商配置对象
        :return:
        """
        #await db.execute(delete(LlmProvider).where(LlmProvider.provider_id.in_([provider_config.provider_id])))
        await db.execute(update(LlmProvider).where(LlmProvider.provider_id.in_([provider_config.provider_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Provider_configPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Provider_configDao.get_provider_config_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
