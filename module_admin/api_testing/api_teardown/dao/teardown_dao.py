from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_teardown.entity.do.teardown_do import ApiTeardown
from module_admin.api_testing.api_teardown.entity.vo.teardown_vo import TeardownModel, TeardownPageQueryModel, \
    TeardownQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db

class TeardownDao:
    """
    接口后置操作模块数据库操作层
    """

    @classmethod
    async def get_teardown_detail_by_id(cls, db: AsyncSession, teardown_id: int):
        """
        根据操作ID获取接口后置操作详细信息

        :param db: orm对象
        :param teardown_id: 操作ID
        :return: 接口后置操作信息对象
        """
        teardown_info = (
            (
                await db.execute(
                    select(ApiTeardown)
                    .where(
                        ApiTeardown.teardown_id == teardown_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return teardown_info

    @classmethod
    async def get_teardown_detail_by_info(cls, db: AsyncSession, teardown: TeardownModel):
        """
        根据接口后置操作参数获取接口后置操作信息

        :param db: orm对象
        :param teardown: 接口后置操作参数对象
        :return: 接口后置操作信息对象
        """
        teardown_info = (
            (
                await db.execute(
                    select(ApiTeardown).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return teardown_info

    @classmethod
    async def get_teardown_list(cls, db: AsyncSession, query_object: TeardownPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口后置操作列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口后置操作列表信息对象
        """
        query = (
            select(ApiTeardown)
            .where(
                ApiTeardown.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiTeardown.case_id == query_object.case_id if query_object.case_id else True,
                ApiTeardown.teardown_type == query_object.teardown_type if query_object.teardown_type else True,
                ApiTeardown.extract_variable_method == query_object.extract_variable_method if query_object.extract_variable_method else True,
                ApiTeardown.jsonpath == query_object.jsonpath if query_object.jsonpath else True,
                ApiTeardown.extract_index == query_object.extract_index if query_object.extract_index else True,
                ApiTeardown.extract_index_is_run == query_object.extract_index_is_run if query_object.extract_index_is_run else True,
                ApiTeardown.variable_name.like(f'%{query_object.variable_name}%') if query_object.variable_name else True,
                ApiTeardown.database_id == query_object.database_id if query_object.database_id else True,
                ApiTeardown.db_operation == query_object.db_operation if query_object.db_operation else True,
                ApiTeardown.script == query_object.script if query_object.script else True,
                ApiTeardown.wait_time == query_object.wait_time if query_object.wait_time else True,
                ApiTeardown.is_run == query_object.is_run if query_object.is_run else True,
                ApiTeardown.description == query_object.description if query_object.description else True,
                ApiTeardown.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiTeardown.del_flag == "0")
            .order_by(ApiTeardown.teardown_id)
            #.distinct()
        )
        teardown_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return teardown_list

    @classmethod
    async def get_teardown_orm_list(cls, db: AsyncSession, query_object: TeardownQueryModel):
        """
        根据查询参数获取接口后置操作列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口后置操作列表信息orm对象
        """
        query = (
            select(ApiTeardown)
            .where(
                ApiTeardown.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiTeardown.case_id == query_object.case_id if query_object.case_id else True,
                ApiTeardown.teardown_type == query_object.teardown_type if query_object.teardown_type else True,
                ApiTeardown.extract_variable_method == query_object.extract_variable_method if query_object.extract_variable_method else True,
                ApiTeardown.jsonpath == query_object.jsonpath if query_object.jsonpath else True,
                ApiTeardown.extract_index == query_object.extract_index if query_object.extract_index else True,
                ApiTeardown.extract_index_is_run == query_object.extract_index_is_run if query_object.extract_index_is_run else True,
                ApiTeardown.variable_name.like(f'%{query_object.variable_name}%') if query_object.variable_name else True,
                ApiTeardown.database_id == query_object.database_id if query_object.database_id else True,
                ApiTeardown.db_operation == query_object.db_operation if query_object.db_operation else True,
                ApiTeardown.script == query_object.script if query_object.script else True,
                ApiTeardown.wait_time == query_object.wait_time if query_object.wait_time else True,
                ApiTeardown.is_run == query_object.is_run if query_object.is_run else True,
                ApiTeardown.description == query_object.description if query_object.description else True,
                ApiTeardown.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiTeardown.del_flag == "0")
            .order_by(ApiTeardown.teardown_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [TeardownQueryModel.model_validate(i) for i in result.scalars().all()]

    @classmethod
    async def add_teardown_dao(cls, db: AsyncSession, teardown: TeardownModel):
        """
        新增接口后置操作数据库操作

        :param db: orm对象
        :param teardown: 接口后置操作对象
        :return:
        """
        db_teardown = ApiTeardown(**teardown.model_dump(exclude={}))
        db.add(db_teardown)
        await db.flush()

        return db_teardown

    @classmethod
    async def edit_teardown_dao(cls, db: AsyncSession, teardown: dict):
        """
        编辑接口后置操作数据库操作

        :param db: orm对象
        :param teardown: 需要更新的接口后置操作字典
        :return:
        """
        await db.execute(update(ApiTeardown), [teardown])

    @classmethod
    async def delete_teardown_dao(cls, db: AsyncSession, teardown: TeardownModel):
        """
        删除接口后置操作数据库操作

        :param db: orm对象
        :param teardown: 接口后置操作对象
        :return:
        """
        #await db.execute(delete(ApiTeardown).where(ApiTeardown.teardown_id.in_([teardown.teardown_id])))
        await db.execute(update(ApiTeardown).where(ApiTeardown.teardown_id.in_([teardown.teardown_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = TeardownPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await TeardownDao.get_teardown_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
