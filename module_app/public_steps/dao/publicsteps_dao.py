from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.public_steps.entity.do.publicsteps_do import AppPublicSteps
from module_app.public_steps.entity.vo.publicsteps_vo import PublicstepsModel, PublicstepsPageQueryModel, PublicstepsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class PublicstepsDao:
    """
    公共步骤模块数据库操作层
    """

    @classmethod
    async def get_publicsteps_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取公共步骤详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 公共步骤信息对象
        """
        publicsteps_info = (
            (
                await db.execute(
                    select(AppPublicSteps)
                    .where(
                        AppPublicSteps.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return publicsteps_info

    @classmethod
    async def get_publicsteps_detail_by_info(cls, db: AsyncSession, publicsteps: PublicstepsModel):
        """
        根据公共步骤参数获取公共步骤信息

        :param db: orm对象
        :param publicsteps: 公共步骤参数对象
        :return: 公共步骤信息对象
        """
        publicsteps_info = (
            (
                await db.execute(
                    select(AppPublicSteps).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return publicsteps_info

    @classmethod
    async def get_publicsteps_list(cls, db: AsyncSession, query_object: PublicstepsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取公共步骤列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公共步骤列表信息字典对象
        """
        query = (
            select(AppPublicSteps)
            .where(
                AppPublicSteps.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppPublicSteps.platform == query_object.platform if query_object.platform else True,
                AppPublicSteps.project_id == query_object.project_id if query_object.project_id else True,
                AppPublicSteps.description == query_object.description if query_object.description else True,
                AppPublicSteps.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppPublicSteps.del_flag == "0")
            .order_by(AppPublicSteps.id)
            #.distinct()
        )
        publicsteps_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return publicsteps_list

    @classmethod
    async def get_publicsteps_orm_list(cls, db: AsyncSession, query_object: PublicstepsQueryModel) -> List[PublicstepsQueryModel]:
        """
        根据查询参数获取公共步骤列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 公共步骤列表信息orm对象
        """
        query = (
            select(AppPublicSteps)
            .where(
                AppPublicSteps.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppPublicSteps.platform == query_object.platform if query_object.platform else True,
                AppPublicSteps.project_id == query_object.project_id if query_object.project_id else True,
                AppPublicSteps.description == query_object.description if query_object.description else True,
                AppPublicSteps.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppPublicSteps.del_flag == "0")
            .order_by(AppPublicSteps.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [PublicstepsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_publicsteps_dao(cls, db: AsyncSession, publicsteps: PublicstepsModel):
        """
        新增公共步骤数据库操作

        :param db: orm对象
        :param publicsteps: 公共步骤对象
        :return:
        """
        db_publicsteps = AppPublicSteps(**publicsteps.model_dump(exclude={}))
        db.add(db_publicsteps)
        await db.flush()

        return db_publicsteps

    @classmethod
    async def edit_publicsteps_dao(cls, db: AsyncSession, publicsteps: dict):
        """
        编辑公共步骤数据库操作

        :param db: orm对象
        :param publicsteps: 需要更新的公共步骤字典
        :return:
        """
        await db.execute(update(AppPublicSteps), [publicsteps])

    @classmethod
    async def delete_publicsteps_dao(cls, db: AsyncSession, publicsteps: PublicstepsModel):
        """
        删除公共步骤数据库操作

        :param db: orm对象
        :param publicsteps: 公共步骤对象
        :return:
        """
        #await db.execute(delete(AppPublicSteps).where(AppPublicSteps.id.in_([publicsteps.id])))
        await db.execute(update(AppPublicSteps).where(AppPublicSteps.id.in_([publicsteps.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = PublicstepsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await PublicstepsDao.get_publicsteps_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
