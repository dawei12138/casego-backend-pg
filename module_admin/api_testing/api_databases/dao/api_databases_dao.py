from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_databases.entity.do.api_databases_do import ApiDatabases
from module_admin.api_testing.api_databases.entity.vo.api_databases_vo import Api_databasesModel, Api_databasesPageQueryModel
from utils.page_util import PageUtil


class Api_databasesDao:
    """
    数据库配置模块数据库操作层
    """

    @classmethod
    async def get_api_databases_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据数据库ID获取数据库配置详细信息

        :param db: orm对象
        :param id: 数据库ID
        :return: 数据库配置信息对象
        """
        api_databases_info = (
            (
                await db.execute(
                    select(ApiDatabases)
                    .where(
                        ApiDatabases.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_databases_info

    @classmethod
    async def get_api_databases_detail_by_info(cls, db: AsyncSession, api_databases: Api_databasesModel):
        """
        根据数据库配置参数获取数据库配置信息

        :param db: orm对象
        :param api_databases: 数据库配置参数对象
        :return: 数据库配置信息对象
        """
        api_databases_info = (
            (
                await db.execute(
                    select(ApiDatabases).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_databases_info

    @classmethod
    async def get_api_databases_list(cls, db: AsyncSession, query_object: Api_databasesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取数据库配置列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据库配置列表信息对象
        """
        query = (
            select(ApiDatabases)
            .where(
                ApiDatabases.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiDatabases.db_type == query_object.db_type if query_object.db_type else True,
                ApiDatabases.del_flag == "0",
                ApiDatabases.project_id==query_object.project_id if query_object.project_id else True,
            )
            .order_by(ApiDatabases.id)
            #.distinct()
        )
        api_databases_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        # 对 password 进行模糊化处理（rows 是字典列表）
        for item in api_databases_list.rows:
            if "password" in item and item["password"]:
                item["password"] = item["password"][:2] + "****"  # 或者部分隐藏，如
        return api_databases_list

    @classmethod
    async def add_api_databases_dao(cls, db: AsyncSession, api_databases: Api_databasesModel):
        """
        新增数据库配置数据库操作

        :param db: orm对象
        :param api_databases: 数据库配置对象
        :return:
        """
        db_api_databases = ApiDatabases(**api_databases.model_dump(exclude={'description', 'sort_no', 'del_flag'}))
        db.add(db_api_databases)
        await db.flush()

        return db_api_databases

    @classmethod
    async def edit_api_databases_dao(cls, db: AsyncSession, api_databases: dict):
        """
        编辑数据库配置数据库操作

        :param db: orm对象
        :param api_databases: 需要更新的数据库配置字典
        :return:
        """
        await db.execute(update(ApiDatabases), [api_databases])

    @classmethod
    async def delete_api_databases_dao(cls, db: AsyncSession, api_databases: Api_databasesModel):
        """
        删除数据库配置数据库操作

        :param db: orm对象
        :param api_databases: 数据库配置对象
        :return:
        """
        # await db.execute(delete(ApiDatabases).where(ApiDatabases.id.in_([api_databases.id])))
        await db.execute(update(ApiDatabases).where(ApiDatabases.id.in_([api_databases.id])).values(del_flag="1"))
