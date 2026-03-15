from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_setup.entity.do.setup_do import ApiSetup
from module_admin.api_testing.api_setup.entity.vo.setup_vo import SetupModel, SetupPageQueryModel, SetupQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db

class SetupDao:
    """
    接口前置操作模块数据库操作层
    """

    @classmethod
    async def get_setup_detail_by_id(cls, db: AsyncSession, setup_id: int):
        """
        根据操作ID获取接口前置操作详细信息

        :param db: orm对象
        :param setup_id: 操作ID
        :return: 接口前置操作信息对象
        """
        setup_info = (
            (
                await db.execute(
                    select(ApiSetup)
                    .where(
                        ApiSetup.setup_id == setup_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return setup_info

    @classmethod
    async def get_setup_detail_by_info(cls, db: AsyncSession, setup: SetupModel):
        """
        根据接口前置操作参数获取接口前置操作信息

        :param db: orm对象
        :param setup: 接口前置操作参数对象
        :return: 接口前置操作信息对象
        """
        setup_info = (
            (
                await db.execute(
                    select(ApiSetup).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return setup_info

    @classmethod
    async def get_setup_list(cls, db: AsyncSession, query_object: SetupPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口前置操作列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口前置操作列表信息对象
        """
        query = (
            select(ApiSetup)
            .where(
                ApiSetup.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiSetup.case_id == query_object.case_id if query_object.case_id else True,
                ApiSetup.setup_type == query_object.setup_type if query_object.setup_type else True,
                ApiSetup.db_connection_id == query_object.db_connection_id if query_object.db_connection_id else True,
                ApiSetup.script == query_object.script if query_object.script else True,
                ApiSetup.jsonpath == query_object.jsonpath if query_object.jsonpath else True,
                ApiSetup.variable_name.like(f'%{query_object.variable_name}%') if query_object.variable_name else True,
                ApiSetup.wait_time == query_object.wait_time if query_object.wait_time else True,
                ApiSetup.extract_index == query_object.extract_index if query_object.extract_index else True,
                ApiSetup.extract_index_is_run == query_object.extract_index_is_run if query_object.extract_index_is_run else True,
                ApiSetup.is_run == query_object.is_run if query_object.is_run else True,
                ApiSetup.description == query_object.description if query_object.description else True,
                ApiSetup.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiSetup.del_flag == "0")
            .order_by(ApiSetup.setup_id)
            #.distinct()
        )
        setup_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return setup_list

    @classmethod
    async def get_setup_orm_list(cls, db: AsyncSession, query_object: SetupQueryModel):
        """
        根据查询参数获取接口前置操作列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口前置操作列表信息orm对象
        """
        query = (
            select(ApiSetup)
            .where(
                ApiSetup.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiSetup.case_id == query_object.case_id if query_object.case_id else True,
                ApiSetup.setup_type == query_object.setup_type if query_object.setup_type else True,
                ApiSetup.db_connection_id == query_object.db_connection_id if query_object.db_connection_id else True,
                ApiSetup.script == query_object.script if query_object.script else True,
                ApiSetup.jsonpath == query_object.jsonpath if query_object.jsonpath else True,
                ApiSetup.variable_name.like(f'%{query_object.variable_name}%') if query_object.variable_name else True,
                ApiSetup.wait_time == query_object.wait_time if query_object.wait_time else True,
                ApiSetup.extract_index == query_object.extract_index if query_object.extract_index else True,
                ApiSetup.extract_index_is_run == query_object.extract_index_is_run if query_object.extract_index_is_run else True,
                ApiSetup.is_run == query_object.is_run if query_object.is_run else True,
                ApiSetup.description == query_object.description if query_object.description else True,
                ApiSetup.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiSetup.del_flag == "0")
            .order_by(ApiSetup.setup_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [SetupQueryModel.model_validate(i) for i in result.scalars().all()]

    @classmethod
    async def add_setup_dao(cls, db: AsyncSession, setup: SetupModel):
        """
        新增接口前置操作数据库操作

        :param db: orm对象
        :param setup: 接口前置操作对象
        :return:
        """
        db_setup = ApiSetup(**setup.model_dump(exclude={}))
        db.add(db_setup)
        await db.flush()

        return db_setup

    @classmethod
    async def edit_setup_dao(cls, db: AsyncSession, setup: dict):
        """
        编辑接口前置操作数据库操作

        :param db: orm对象
        :param setup: 需要更新的接口前置操作字典
        :return:
        """
        await db.execute(update(ApiSetup), [setup])

    @classmethod
    async def delete_setup_dao(cls, db: AsyncSession, setup: SetupModel):
        """
        删除接口前置操作数据库操作

        :param db: orm对象
        :param setup: 接口前置操作对象
        :return:
        """
        #await db.execute(delete(ApiSetup).where(ApiSetup.setup_id.in_([setup.setup_id])))
        await db.execute(update(ApiSetup).where(ApiSetup.setup_id.in_([setup.setup_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = SetupPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await SetupDao.get_setup_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
