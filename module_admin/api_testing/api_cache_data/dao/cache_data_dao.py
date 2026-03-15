from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_cache_data.entity.do.cache_data_do import ApiCacheData
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataModel, Cache_dataPageQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db


class Cache_dataDao:
    """
    环境缓存模块数据库操作层
    """

    @classmethod
    async def get_cache_data_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据缓存数据ID获取环境缓存详细信息

        :param db: orm对象
        :param id: 缓存数据ID
        :return: 环境缓存信息对象
        """
        cache_data_info = (
            (
                await db.execute(
                    select(ApiCacheData)
                    .where(
                        ApiCacheData.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return cache_data_info

    @classmethod
    async def get_cache_data_detail_by_info(cls, db: AsyncSession, cache_data: Cache_dataModel):
        """
        根据环境缓存参数获取环境缓存信息

        :param db: orm对象
        :param cache_data: 环境缓存参数对象
        :return: 环境缓存信息对象
        """
        cache_data_info = (
            (
                await db.execute(
                    select(ApiCacheData).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return cache_data_info


    @classmethod
    async def get_cache_data_list(cls, db: AsyncSession, query_object: Cache_dataPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取环境缓存列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境缓存列表信息对象
        """
        query = (
            select(ApiCacheData)
            .where(
                ApiCacheData.cache_key == query_object.cache_key if query_object.cache_key else True,
                ApiCacheData.environment_id == query_object.environment_id if query_object.environment_id else True,
                ApiCacheData.cache_value == query_object.cache_value if query_object.cache_value else True,
                ApiCacheData.user_id == query_object.user_id if query_object.user_id else True,
            )
            .where(ApiCacheData.del_flag == "0")
            .order_by(ApiCacheData.id)
            #.distinct()
        )
        cache_data_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return cache_data_list

    @classmethod
    async def add_cache_data_dao(cls, db: AsyncSession, cache_data: Cache_dataModel):
        """
        新增环境缓存数据库操作

        :param db: orm对象
        :param cache_data: 环境缓存对象
        :return:
        """
        db_cache_data = ApiCacheData(
            **cache_data.model_dump(exclude={'source_type', 'remark', 'description', 'sort_no', 'del_flag', }))
        db.add(db_cache_data)
        await db.flush()

        return db_cache_data

    @classmethod
    async def edit_cache_data_dao(cls, db: AsyncSession, cache_data: dict):
        """
        编辑环境缓存数据库操作

        :param db: orm对象
        :param cache_data: 需要更新的环境缓存字典
        :return:
        """
        await db.execute(update(ApiCacheData), [cache_data])

    @classmethod
    async def delete_cache_data_dao(cls, db: AsyncSession, cache_data: Cache_dataModel):
        """
        删除环境缓存数据库操作

        :param db: orm对象
        :param cache_data: 环境缓存对象
        :return:
        """
        # await db.execute(delete(ApiCacheData).where(ApiCacheData.id.in_([cache_data.id])))
        await db.execute(update(ApiCacheData).where(ApiCacheData.id.in_([cache_data.id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Cache_dataPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Cache_dataDao.get_cache_data_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
