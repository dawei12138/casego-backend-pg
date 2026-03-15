from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.public_steps_steps.entity.do.public_steps_steps_do import AppPublicStepsSteps
from module_app.public_steps_steps.entity.vo.public_steps_steps_vo import Public_steps_stepsModel, Public_steps_stepsPageQueryModel, Public_steps_stepsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Public_steps_stepsDao:
    """
    公共步骤-步骤关联模块数据库操作层
    """

    @classmethod
    async def get_public_steps_steps_detail_by_id(cls, db: AsyncSession, public_steps_id: int):
        """
        根据公共步骤ID获取公共步骤-步骤关联详细信息

        :param db: orm对象
        :param public_steps_id: 公共步骤ID
        :return: 公共步骤-步骤关联信息对象
        """
        public_steps_steps_info = (
            (
                await db.execute(
                    select(AppPublicStepsSteps)
                    .where(
                        AppPublicStepsSteps.public_steps_id == public_steps_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return public_steps_steps_info

    @classmethod
    async def get_public_steps_steps_detail_by_info(cls, db: AsyncSession, public_steps_steps: Public_steps_stepsModel):
        """
        根据公共步骤-步骤关联参数获取公共步骤-步骤关联信息

        :param db: orm对象
        :param public_steps_steps: 公共步骤-步骤关联参数对象
        :return: 公共步骤-步骤关联信息对象
        """
        public_steps_steps_info = (
            (
                await db.execute(
                    select(AppPublicStepsSteps).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return public_steps_steps_info

    @classmethod
    async def get_public_steps_steps_list(cls, db: AsyncSession, query_object: Public_steps_stepsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取公共步骤-步骤关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公共步骤-步骤关联列表信息字典对象
        """
        query = (
            select(AppPublicStepsSteps)
            .where(
                AppPublicStepsSteps.description == query_object.description if query_object.description else True,
                AppPublicStepsSteps.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppPublicStepsSteps.del_flag == "0")
            .order_by(AppPublicStepsSteps.public_steps_id)
            #.distinct()
        )
        public_steps_steps_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return public_steps_steps_list

    @classmethod
    async def get_public_steps_steps_orm_list(cls, db: AsyncSession, query_object: Public_steps_stepsQueryModel) -> List[Public_steps_stepsQueryModel]:
        """
        根据查询参数获取公共步骤-步骤关联列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 公共步骤-步骤关联列表信息orm对象
        """
        query = (
            select(AppPublicStepsSteps)
            .where(
                AppPublicStepsSteps.description == query_object.description if query_object.description else True,
                AppPublicStepsSteps.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppPublicStepsSteps.del_flag == "0")
            .order_by(AppPublicStepsSteps.public_steps_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Public_steps_stepsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_public_steps_steps_dao(cls, db: AsyncSession, public_steps_steps: Public_steps_stepsModel):
        """
        新增公共步骤-步骤关联数据库操作

        :param db: orm对象
        :param public_steps_steps: 公共步骤-步骤关联对象
        :return:
        """
        db_public_steps_steps = AppPublicStepsSteps(**public_steps_steps.model_dump(exclude={}))
        db.add(db_public_steps_steps)
        await db.flush()

        return db_public_steps_steps

    @classmethod
    async def edit_public_steps_steps_dao(cls, db: AsyncSession, public_steps_steps: dict):
        """
        编辑公共步骤-步骤关联数据库操作

        :param db: orm对象
        :param public_steps_steps: 需要更新的公共步骤-步骤关联字典
        :return:
        """
        await db.execute(update(AppPublicStepsSteps), [public_steps_steps])

    @classmethod
    async def delete_public_steps_steps_dao(cls, db: AsyncSession, public_steps_steps: Public_steps_stepsModel):
        """
        删除公共步骤-步骤关联数据库操作

        :param db: orm对象
        :param public_steps_steps: 公共步骤-步骤关联对象
        :return:
        """
        #await db.execute(delete(AppPublicStepsSteps).where(AppPublicStepsSteps.public_steps_id.in_([public_steps_steps.public_steps_id])))
        await db.execute(update(AppPublicStepsSteps).where(AppPublicStepsSteps.public_steps_id.in_([public_steps_steps.public_steps_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Public_steps_stepsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Public_steps_stepsDao.get_public_steps_steps_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
