from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.cases.entity.do.cases_do import AppTestCases
from module_app.cases.entity.vo.cases_vo import CasesModel, CasesPageQueryModel, CasesQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class CasesDao:
    """
    测试用例模块数据库操作层
    """

    @classmethod
    async def get_cases_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取测试用例详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 测试用例信息对象
        """
        cases_info = (
            (
                await db.execute(
                    select(AppTestCases)
                    .where(
                        AppTestCases.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return cases_info

    @classmethod
    async def get_cases_detail_by_info(cls, db: AsyncSession, cases: CasesModel):
        """
        根据测试用例参数获取测试用例信息

        :param db: orm对象
        :param cases: 测试用例参数对象
        :return: 测试用例信息对象
        """
        cases_info = (
            (
                await db.execute(
                    select(AppTestCases).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return cases_info

    @classmethod
    async def get_cases_list(cls, db: AsyncSession, query_object: CasesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取测试用例列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试用例列表信息字典对象
        """
        query = (
            select(AppTestCases)
            .where(
                AppTestCases.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppTestCases.des == query_object.des if query_object.des else True,
                AppTestCases.designer == query_object.designer if query_object.designer else True,
                AppTestCases.platform == query_object.platform if query_object.platform else True,
                AppTestCases.project_id == query_object.project_id if query_object.project_id else True,
                AppTestCases.module_id == query_object.module_id if query_object.module_id else True,
                AppTestCases.version == query_object.version if query_object.version else True,
                AppTestCases.edit_time == query_object.edit_time if query_object.edit_time else True,
                AppTestCases.description == query_object.description if query_object.description else True,
                AppTestCases.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppTestCases.del_flag == "0")
            .order_by(AppTestCases.id)
            #.distinct()
        )
        cases_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return cases_list

    @classmethod
    async def get_cases_orm_list(cls, db: AsyncSession, query_object: CasesQueryModel) -> List[CasesQueryModel]:
        """
        根据查询参数获取测试用例列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 测试用例列表信息orm对象
        """
        query = (
            select(AppTestCases)
            .where(
                AppTestCases.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppTestCases.des == query_object.des if query_object.des else True,
                AppTestCases.designer == query_object.designer if query_object.designer else True,
                AppTestCases.platform == query_object.platform if query_object.platform else True,
                AppTestCases.project_id == query_object.project_id if query_object.project_id else True,
                AppTestCases.module_id == query_object.module_id if query_object.module_id else True,
                AppTestCases.version == query_object.version if query_object.version else True,
                AppTestCases.edit_time == query_object.edit_time if query_object.edit_time else True,
                AppTestCases.description == query_object.description if query_object.description else True,
                AppTestCases.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppTestCases.del_flag == "0")
            .order_by(AppTestCases.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [CasesQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_cases_dao(cls, db: AsyncSession, cases: CasesModel):
        """
        新增测试用例数据库操作

        :param db: orm对象
        :param cases: 测试用例对象
        :return:
        """
        db_cases = AppTestCases(**cases.model_dump(exclude={}))
        db.add(db_cases)
        await db.flush()

        return db_cases

    @classmethod
    async def edit_cases_dao(cls, db: AsyncSession, cases: dict):
        """
        编辑测试用例数据库操作

        :param db: orm对象
        :param cases: 需要更新的测试用例字典
        :return:
        """
        await db.execute(update(AppTestCases), [cases])

    @classmethod
    async def delete_cases_dao(cls, db: AsyncSession, cases: CasesModel):
        """
        删除测试用例数据库操作

        :param db: orm对象
        :param cases: 测试用例对象
        :return:
        """
        #await db.execute(delete(AppTestCases).where(AppTestCases.id.in_([cases.id])))
        await db.execute(update(AppTestCases).where(AppTestCases.id.in_([cases.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = CasesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await CasesDao.get_cases_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
