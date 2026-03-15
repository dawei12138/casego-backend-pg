from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.globalparams.entity.do.globalparams_do import AppGlobalParams
from module_app.globalparams.entity.vo.globalparams_vo import GlobalparamsModel, GlobalparamsPageQueryModel, GlobalparamsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class GlobalparamsDao:
    """
    全局参数模块数据库操作层
    """

    @classmethod
    async def get_globalparams_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取全局参数详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 全局参数信息对象
        """
        globalparams_info = (
            (
                await db.execute(
                    select(AppGlobalParams)
                    .where(
                        AppGlobalParams.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return globalparams_info

    @classmethod
    async def get_globalparams_detail_by_info(cls, db: AsyncSession, globalparams: GlobalparamsModel):
        """
        根据全局参数参数获取全局参数信息

        :param db: orm对象
        :param globalparams: 全局参数参数对象
        :return: 全局参数信息对象
        """
        globalparams_info = (
            (
                await db.execute(
                    select(AppGlobalParams).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return globalparams_info

    @classmethod
    async def get_globalparams_list(cls, db: AsyncSession, query_object: GlobalparamsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取全局参数列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 全局参数列表信息字典对象
        """
        query = (
            select(AppGlobalParams)
            .where(
                AppGlobalParams.params_key == query_object.params_key if query_object.params_key else True,
                AppGlobalParams.params_value == query_object.params_value if query_object.params_value else True,
                AppGlobalParams.project_id == query_object.project_id if query_object.project_id else True,
                AppGlobalParams.description == query_object.description if query_object.description else True,
                AppGlobalParams.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppGlobalParams.del_flag == "0")
            .order_by(AppGlobalParams.id)
            #.distinct()
        )
        globalparams_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return globalparams_list

    @classmethod
    async def get_globalparams_orm_list(cls, db: AsyncSession, query_object: GlobalparamsQueryModel) -> List[GlobalparamsQueryModel]:
        """
        根据查询参数获取全局参数列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 全局参数列表信息orm对象
        """
        query = (
            select(AppGlobalParams)
            .where(
                AppGlobalParams.params_key == query_object.params_key if query_object.params_key else True,
                AppGlobalParams.params_value == query_object.params_value if query_object.params_value else True,
                AppGlobalParams.project_id == query_object.project_id if query_object.project_id else True,
                AppGlobalParams.description == query_object.description if query_object.description else True,
                AppGlobalParams.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppGlobalParams.del_flag == "0")
            .order_by(AppGlobalParams.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [GlobalparamsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_globalparams_dao(cls, db: AsyncSession, globalparams: GlobalparamsModel):
        """
        新增全局参数数据库操作

        :param db: orm对象
        :param globalparams: 全局参数对象
        :return:
        """
        db_globalparams = AppGlobalParams(**globalparams.model_dump(exclude={}))
        db.add(db_globalparams)
        await db.flush()

        return db_globalparams

    @classmethod
    async def edit_globalparams_dao(cls, db: AsyncSession, globalparams: dict):
        """
        编辑全局参数数据库操作

        :param db: orm对象
        :param globalparams: 需要更新的全局参数字典
        :return:
        """
        await db.execute(update(AppGlobalParams), [globalparams])

    @classmethod
    async def delete_globalparams_dao(cls, db: AsyncSession, globalparams: GlobalparamsModel):
        """
        删除全局参数数据库操作

        :param db: orm对象
        :param globalparams: 全局参数对象
        :return:
        """
        #await db.execute(delete(AppGlobalParams).where(AppGlobalParams.id.in_([globalparams.id])))
        await db.execute(update(AppGlobalParams).where(AppGlobalParams.id.in_([globalparams.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = GlobalparamsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await GlobalparamsDao.get_globalparams_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
