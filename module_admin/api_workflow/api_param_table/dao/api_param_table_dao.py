from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_workflow.api_param_table.entity.do.api_param_table_do import ApiParamTable
from module_admin.api_workflow.api_param_table.entity.vo.api_param_table_vo import Api_param_tableModel, Api_param_tablePageQueryModel, Api_param_tableQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Api_param_tableDao:
    """
    参数化数据主模块数据库操作层
    """

    @classmethod
    async def get_api_param_table_detail_by_id(cls, db: AsyncSession, parameterization_id: int):
        """
        根据主键ID获取参数化数据主详细信息

        :param db: orm对象
        :param parameterization_id: 主键ID
        :return: 参数化数据主信息对象
        """
        api_param_table_info = (
            (
                await db.execute(
                    select(ApiParamTable)
                    .where(
                        ApiParamTable.parameterization_id == parameterization_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_param_table_info

    @classmethod
    async def get_api_param_table_detail_by_info(cls, db: AsyncSession, api_param_table: Api_param_tableModel):
        """
        根据参数化数据主参数获取参数化数据主信息

        :param db: orm对象
        :param api_param_table: 参数化数据主参数对象
        :return: 参数化数据主信息对象
        """
        api_param_table_info = (
            (
                await db.execute(
                    select(ApiParamTable).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_param_table_info

    @classmethod
    async def get_api_param_table_list(cls, db: AsyncSession, query_object: Api_param_tablePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取参数化数据主列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 参数化数据主列表信息字典对象
        """
        query = (
            select(ApiParamTable)
            .where(
                ApiParamTable.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiParamTable.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiParamTable.description == query_object.description if query_object.description else True,
                ApiParamTable.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiParamTable.del_flag == "0")
            .order_by(ApiParamTable.parameterization_id)
            #.distinct()
        )
        api_param_table_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return api_param_table_list

    @classmethod
    async def get_api_param_table_orm_list(cls, db: AsyncSession, query_object: Api_param_tableQueryModel):
        """
        根据查询参数获取参数化数据主列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 参数化数据主列表信息orm对象
        """
        query = (
            select(ApiParamTable)
            .where(
                ApiParamTable.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiParamTable.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiParamTable.description == query_object.description if query_object.description else True,
                ApiParamTable.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiParamTable.del_flag == "0")
            .order_by(ApiParamTable.parameterization_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_api_param_table_dao(cls, db: AsyncSession, api_param_table: Api_param_tableModel):
        """
        新增参数化数据主数据库操作

        :param db: orm对象
        :param api_param_table: 参数化数据主对象
        :return:
        """
        db_api_param_table = ApiParamTable(**api_param_table.model_dump(exclude={}))
        db.add(db_api_param_table)
        await db.flush()

        return db_api_param_table

    @classmethod
    async def edit_api_param_table_dao(cls, db: AsyncSession, api_param_table: dict):
        """
        编辑参数化数据主数据库操作

        :param db: orm对象
        :param api_param_table: 需要更新的参数化数据主字典
        :return:
        """
        await db.execute(update(ApiParamTable), [api_param_table])

    @classmethod
    async def delete_api_param_table_dao(cls, db: AsyncSession, api_param_table: Api_param_tableModel):
        """
        删除参数化数据主数据库操作

        :param db: orm对象
        :param api_param_table: 参数化数据主对象
        :return:
        """
        #await db.execute(delete(ApiParamTable).where(ApiParamTable.parameterization_id.in_([api_param_table.parameterization_id])))
        await db.execute(update(ApiParamTable).where(ApiParamTable.parameterization_id.in_([api_param_table.parameterization_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Api_param_tablePageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Api_param_tableDao.get_api_param_table_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
