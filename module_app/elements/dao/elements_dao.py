from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.elements.entity.do.elements_do import AppElements
from module_app.elements.entity.vo.elements_vo import ElementsModel, ElementsPageQueryModel, ElementsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class ElementsDao:
    """
    控件元素模块数据库操作层
    """

    @classmethod
    async def get_elements_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取控件元素详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 控件元素信息对象
        """
        elements_info = (
            (
                await db.execute(
                    select(AppElements)
                    .where(
                        AppElements.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return elements_info

    @classmethod
    async def get_elements_detail_by_info(cls, db: AsyncSession, elements: ElementsModel):
        """
        根据控件元素参数获取控件元素信息

        :param db: orm对象
        :param elements: 控件元素参数对象
        :return: 控件元素信息对象
        """
        elements_info = (
            (
                await db.execute(
                    select(AppElements).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return elements_info

    @classmethod
    async def get_elements_list(cls, db: AsyncSession, query_object: ElementsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取控件元素列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 控件元素列表信息字典对象
        """
        query = (
            select(AppElements)
            .where(
                AppElements.ele_name.like(f'%{query_object.ele_name}%') if query_object.ele_name else True,
                AppElements.description == query_object.description if query_object.description else True,
                AppElements.sort_no == query_object.sort_no if query_object.sort_no else True,
                AppElements.ele_type == query_object.ele_type if query_object.ele_type else True,
                AppElements.ele_value == query_object.ele_value if query_object.ele_value else True,
                AppElements.project_id == query_object.project_id if query_object.project_id else True,
                AppElements.module_id == query_object.module_id if query_object.module_id else True,
            )
            .where(AppElements.del_flag == "0")
            .order_by(AppElements.id)
            #.distinct()
        )
        elements_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return elements_list

    @classmethod
    async def get_elements_orm_list(cls, db: AsyncSession, query_object: ElementsQueryModel) -> List[ElementsQueryModel]:
        """
        根据查询参数获取控件元素列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 控件元素列表信息orm对象
        """
        query = (
            select(AppElements)
            .where(
                AppElements.ele_name.like(f'%{query_object.ele_name}%') if query_object.ele_name else True,
                AppElements.description == query_object.description if query_object.description else True,
                AppElements.sort_no == query_object.sort_no if query_object.sort_no else True,
                AppElements.ele_type == query_object.ele_type if query_object.ele_type else True,
                AppElements.ele_value == query_object.ele_value if query_object.ele_value else True,
                AppElements.project_id == query_object.project_id if query_object.project_id else True,
                AppElements.module_id == query_object.module_id if query_object.module_id else True,
            )
            .where(AppElements.del_flag == "0")
            .order_by(AppElements.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [ElementsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_elements_dao(cls, db: AsyncSession, elements: ElementsModel):
        """
        新增控件元素数据库操作

        :param db: orm对象
        :param elements: 控件元素对象
        :return:
        """
        db_elements = AppElements(**elements.model_dump(exclude={}))
        db.add(db_elements)
        await db.flush()

        return db_elements

    @classmethod
    async def edit_elements_dao(cls, db: AsyncSession, elements: dict):
        """
        编辑控件元素数据库操作

        :param db: orm对象
        :param elements: 需要更新的控件元素字典
        :return:
        """
        await db.execute(update(AppElements), [elements])

    @classmethod
    async def delete_elements_dao(cls, db: AsyncSession, elements: ElementsModel):
        """
        删除控件元素数据库操作

        :param db: orm对象
        :param elements: 控件元素对象
        :return:
        """
        #await db.execute(delete(AppElements).where(AppElements.id.in_([elements.id])))
        await db.execute(update(AppElements).where(AppElements.id.in_([elements.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = ElementsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await ElementsDao.get_elements_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
