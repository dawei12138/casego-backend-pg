from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.steps_elements.entity.do.steps_elements_do import AppStepsElements
from module_app.steps_elements.entity.vo.steps_elements_vo import Steps_elementsModel, Steps_elementsPageQueryModel, Steps_elementsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Steps_elementsDao:
    """
    步骤-元素关联模块数据库操作层
    """

    @classmethod
    async def get_steps_elements_detail_by_id(cls, db: AsyncSession, steps_id: int):
        """
        根据步骤ID获取步骤-元素关联详细信息

        :param db: orm对象
        :param steps_id: 步骤ID
        :return: 步骤-元素关联信息对象
        """
        steps_elements_info = (
            (
                await db.execute(
                    select(AppStepsElements)
                    .where(
                        AppStepsElements.steps_id == steps_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return steps_elements_info

    @classmethod
    async def get_steps_elements_detail_by_info(cls, db: AsyncSession, steps_elements: Steps_elementsModel):
        """
        根据步骤-元素关联参数获取步骤-元素关联信息

        :param db: orm对象
        :param steps_elements: 步骤-元素关联参数对象
        :return: 步骤-元素关联信息对象
        """
        steps_elements_info = (
            (
                await db.execute(
                    select(AppStepsElements).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return steps_elements_info

    @classmethod
    async def get_steps_elements_list(cls, db: AsyncSession, query_object: Steps_elementsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取步骤-元素关联列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 步骤-元素关联列表信息字典对象
        """
        query = (
            select(AppStepsElements)
            .where(
                AppStepsElements.description == query_object.description if query_object.description else True,
                AppStepsElements.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppStepsElements.del_flag == "0")
            .order_by(AppStepsElements.steps_id)
            #.distinct()
        )
        steps_elements_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return steps_elements_list

    @classmethod
    async def get_steps_elements_orm_list(cls, db: AsyncSession, query_object: Steps_elementsQueryModel) -> List[Steps_elementsQueryModel]:
        """
        根据查询参数获取步骤-元素关联列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 步骤-元素关联列表信息orm对象
        """
        query = (
            select(AppStepsElements)
            .where(
                AppStepsElements.description == query_object.description if query_object.description else True,
                AppStepsElements.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppStepsElements.del_flag == "0")
            .order_by(AppStepsElements.steps_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Steps_elementsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_steps_elements_dao(cls, db: AsyncSession, steps_elements: Steps_elementsModel):
        """
        新增步骤-元素关联数据库操作

        :param db: orm对象
        :param steps_elements: 步骤-元素关联对象
        :return:
        """
        db_steps_elements = AppStepsElements(**steps_elements.model_dump(exclude={}))
        db.add(db_steps_elements)
        await db.flush()

        return db_steps_elements

    @classmethod
    async def edit_steps_elements_dao(cls, db: AsyncSession, steps_elements: dict):
        """
        编辑步骤-元素关联数据库操作

        :param db: orm对象
        :param steps_elements: 需要更新的步骤-元素关联字典
        :return:
        """
        await db.execute(update(AppStepsElements), [steps_elements])

    @classmethod
    async def delete_steps_elements_dao(cls, db: AsyncSession, steps_elements: Steps_elementsModel):
        """
        删除步骤-元素关联数据库操作

        :param db: orm对象
        :param steps_elements: 步骤-元素关联对象
        :return:
        """
        #await db.execute(delete(AppStepsElements).where(AppStepsElements.steps_id.in_([steps_elements.steps_id])))
        await db.execute(update(AppStepsElements).where(AppStepsElements.steps_id.in_([steps_elements.steps_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Steps_elementsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Steps_elementsDao.get_steps_elements_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
