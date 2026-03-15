from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_assertions.entity.do.assertions_do import ApiAssertions
from module_admin.api_testing.api_assertions.entity.vo.assertions_vo import AssertionsModel, AssertionsPageQueryModel, \
    AssertionsQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db

class AssertionsDao:
    """
    接口断言模块数据库操作层
    """

    @classmethod
    async def get_assertions_detail_by_id(cls, db: AsyncSession, assertion_id: int):
        """
        根据断言ID获取接口断言详细信息

        :param db: orm对象
        :param assertion_id: 断言ID
        :return: 接口断言信息对象
        """
        assertions_info = (
            (
                await db.execute(
                    select(ApiAssertions)
                    .where(
                        ApiAssertions.assertion_id == assertion_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return assertions_info

    @classmethod
    async def get_assertions_detail_by_info(cls, db: AsyncSession, assertions: AssertionsModel):
        """
        根据接口断言参数获取接口断言信息

        :param db: orm对象
        :param assertions: 接口断言参数对象
        :return: 接口断言信息对象
        """
        assertions_info = (
            (
                await db.execute(
                    select(ApiAssertions).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return assertions_info

    @classmethod
    async def get_assertions_list(cls, db: AsyncSession, query_object: AssertionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口断言列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口断言列表信息对象
        """
        query = (
            select(ApiAssertions)
            .where(
                ApiAssertions.case_id == query_object.case_id if query_object.case_id else True,
                ApiAssertions.jsonpath == query_object.jsonpath if query_object.jsonpath else True,
                ApiAssertions.jsonpath_index == query_object.jsonpath_index if query_object.jsonpath_index else True,
                ApiAssertions.assertion_method == query_object.assertion_method if query_object.assertion_method else True,
                ApiAssertions.value == query_object.value if query_object.value else True,
                ApiAssertions.assert_type == query_object.assert_type if query_object.assert_type else True,
                ApiAssertions.is_run == query_object.is_run if query_object.is_run else True,
                ApiAssertions.description == query_object.description if query_object.description else True,
                ApiAssertions.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiAssertions.del_flag == "0")
            .order_by(ApiAssertions.assertion_id)
            #.distinct()
        )
        assertions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return assertions_list


    @classmethod
    async def get_assertions_orm_list(cls, db: AsyncSession, query_object: AssertionsQueryModel):
        """
        根据查询参数获取接口断言列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口断言列表信息orm对象
        """
        query = (
            select(ApiAssertions)
            .where(
                ApiAssertions.case_id == query_object.case_id if query_object.case_id else True,
                ApiAssertions.jsonpath == query_object.jsonpath if query_object.jsonpath else True,
                ApiAssertions.jsonpath_index == query_object.jsonpath_index if query_object.jsonpath_index else True,
                ApiAssertions.assertion_method == query_object.assertion_method if query_object.assertion_method else True,
                ApiAssertions.value == query_object.value if query_object.value else True,
                ApiAssertions.assert_type == query_object.assert_type if query_object.assert_type else True,
                ApiAssertions.is_run == query_object.is_run if query_object.is_run else True,
                ApiAssertions.description == query_object.description if query_object.description else True,
                ApiAssertions.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiAssertions.del_flag == "0")
            .order_by(ApiAssertions.assertion_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [AssertionsQueryModel.model_validate(i) for i in result.scalars().all()]
    @classmethod
    async def add_assertions_dao(cls, db: AsyncSession, assertions: AssertionsModel):
        """
        新增接口断言数据库操作

        :param db: orm对象
        :param assertions: 接口断言对象
        :return:
        """
        db_assertions = ApiAssertions(**assertions.model_dump(exclude={}))
        db.add(db_assertions)
        await db.flush()

        return db_assertions

    @classmethod
    async def edit_assertions_dao(cls, db: AsyncSession, assertions: dict):
        """
        编辑接口断言数据库操作

        :param db: orm对象
        :param assertions: 需要更新的接口断言字典
        :return:
        """
        await db.execute(update(ApiAssertions), [assertions])

    @classmethod
    async def delete_assertions_dao(cls, db: AsyncSession, assertions: AssertionsModel):
        """
        删除接口断言数据库操作

        :param db: orm对象
        :param assertions: 接口断言对象
        :return:
        """
        #await db.execute(delete(ApiAssertions).where(ApiAssertions.assertion_id.in_([assertions.assertion_id])))
        await db.execute(update(ApiAssertions).where(ApiAssertions.assertion_id.in_([assertions.assertion_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = AssertionsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await AssertionsDao.get_assertions_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
