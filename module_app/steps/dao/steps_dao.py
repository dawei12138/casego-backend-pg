from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.steps.entity.do.steps_do import AppSteps
from module_app.steps.entity.vo.steps_vo import StepsModel, StepsPageQueryModel, StepsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class StepsDao:
    """
    测试步骤模块数据库操作层
    """

    @classmethod
    async def get_steps_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取测试步骤详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 测试步骤信息对象
        """
        steps_info = (
            (
                await db.execute(
                    select(AppSteps)
                    .where(
                        AppSteps.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return steps_info

    @classmethod
    async def get_steps_detail_by_info(cls, db: AsyncSession, steps: StepsModel):
        """
        根据测试步骤参数获取测试步骤信息

        :param db: orm对象
        :param steps: 测试步骤参数对象
        :return: 测试步骤信息对象
        """
        steps_info = (
            (
                await db.execute(
                    select(AppSteps).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return steps_info

    @classmethod
    async def get_steps_list(cls, db: AsyncSession, query_object: StepsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取测试步骤列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试步骤列表信息字典对象
        """
        query = (
            select(AppSteps)
            .where(
                AppSteps.case_id == query_object.case_id if query_object.case_id else True,
                AppSteps.project_id == query_object.project_id if query_object.project_id else True,
                AppSteps.parent_id == query_object.parent_id if query_object.parent_id else True,
                AppSteps.step_type == query_object.step_type if query_object.step_type else True,
                AppSteps.content == query_object.content if query_object.content else True,
                AppSteps.text == query_object.text if query_object.text else True,
                AppSteps.platform == query_object.platform if query_object.platform else True,
                AppSteps.error == query_object.error if query_object.error else True,
                AppSteps.condition_type == query_object.condition_type if query_object.condition_type else True,
                AppSteps.disabled == query_object.disabled if query_object.disabled else True,
                AppSteps.description == query_object.description if query_object.description else True,
                AppSteps.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppSteps.del_flag == "0")
            .order_by(AppSteps.id)
            #.distinct()
        )
        steps_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return steps_list

    @classmethod
    async def get_steps_orm_list(cls, db: AsyncSession, query_object: StepsQueryModel) -> List[StepsQueryModel]:
        """
        根据查询参数获取测试步骤列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 测试步骤列表信息orm对象
        """
        query = (
            select(AppSteps)
            .where(
                AppSteps.case_id == query_object.case_id if query_object.case_id else True,
                AppSteps.project_id == query_object.project_id if query_object.project_id else True,
                AppSteps.parent_id == query_object.parent_id if query_object.parent_id else True,
                AppSteps.step_type == query_object.step_type if query_object.step_type else True,
                AppSteps.content == query_object.content if query_object.content else True,
                AppSteps.text == query_object.text if query_object.text else True,
                AppSteps.platform == query_object.platform if query_object.platform else True,
                AppSteps.error == query_object.error if query_object.error else True,
                AppSteps.condition_type == query_object.condition_type if query_object.condition_type else True,
                AppSteps.disabled == query_object.disabled if query_object.disabled else True,
                AppSteps.description == query_object.description if query_object.description else True,
                AppSteps.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppSteps.del_flag == "0")
            .order_by(AppSteps.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [StepsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_steps_dao(cls, db: AsyncSession, steps: StepsModel):
        """
        新增测试步骤数据库操作

        :param db: orm对象
        :param steps: 测试步骤对象
        :return:
        """
        db_steps = AppSteps(**steps.model_dump(exclude={}))
        db.add(db_steps)
        await db.flush()

        return db_steps

    @classmethod
    async def edit_steps_dao(cls, db: AsyncSession, steps: dict):
        """
        编辑测试步骤数据库操作

        :param db: orm对象
        :param steps: 需要更新的测试步骤字典
        :return:
        """
        await db.execute(update(AppSteps), [steps])

    @classmethod
    async def delete_steps_dao(cls, db: AsyncSession, steps: StepsModel):
        """
        删除测试步骤数据库操作

        :param db: orm对象
        :param steps: 测试步骤对象
        :return:
        """
        #await db.execute(delete(AppSteps).where(AppSteps.id.in_([steps.id])))
        await db.execute(update(AppSteps).where(AppSteps.id.in_([steps.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = StepsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await StepsDao.get_steps_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
