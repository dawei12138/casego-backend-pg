from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_headers.entity.do.headers_do import ApiHeaders
from module_admin.api_testing.api_headers.entity.vo.headers_vo import HeadersModel, HeadersPageQueryModel, \
    HeadersQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db

class HeadersDao:
    """
    接口请求头模块数据库操作层
    """

    @classmethod
    async def get_headers_detail_by_id(cls, db: AsyncSession, header_id: int):
        """
        根据ID获取接口请求头详细信息

        :param db: orm对象
        :param header_id: ID
        :return: 接口请求头信息对象
        """
        headers_info = (
            (
                await db.execute(
                    select(ApiHeaders)
                    .where(
                        ApiHeaders.header_id == header_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return headers_info

    @classmethod
    async def get_headers_detail_by_info(cls, db: AsyncSession, headers: HeadersModel):
        """
        根据接口请求头参数获取接口请求头信息

        :param db: orm对象
        :param headers: 接口请求头参数对象
        :return: 接口请求头信息对象
        """
        headers_info = (
            (
                await db.execute(
                    select(ApiHeaders).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return headers_info

    @classmethod
    async def get_headers_list(cls, db: AsyncSession, query_object: HeadersPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口请求头列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口请求头列表信息对象
        """
        query = (
            select(ApiHeaders)
            .where(
                ApiHeaders.case_id == query_object.case_id if query_object.case_id else True,
                ApiHeaders.key == query_object.key if query_object.key else True,
                ApiHeaders.value == query_object.value if query_object.value else True,
                ApiHeaders.is_run == query_object.is_run if query_object.is_run else True,
                ApiHeaders.description == query_object.description if query_object.description else True,
                ApiHeaders.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiHeaders.del_flag == "0")
            .order_by(ApiHeaders.header_id)
            #.distinct()
        )
        headers_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return headers_list

    @classmethod
    async def get_headers_orm_list(cls, db: AsyncSession, query_object: HeadersQueryModel):
        """
        根据查询参数获取接口请求头列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口请求头列表信息orm对象
        """
        query = (
            select(ApiHeaders)
            .where(
                ApiHeaders.case_id == query_object.case_id if query_object.case_id else True,
                ApiHeaders.key == query_object.key if query_object.key else True,
                ApiHeaders.value == query_object.value if query_object.value else True,
                ApiHeaders.is_run == query_object.is_run if query_object.is_run else True,
                ApiHeaders.description == query_object.description if query_object.description else True,
                ApiHeaders.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiHeaders.del_flag == "0")
            .order_by(ApiHeaders.header_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [HeadersQueryModel.model_validate(i) for i in result.scalars().all()]
    @classmethod
    async def add_headers_dao(cls, db: AsyncSession, headers: HeadersModel):
        """
        新增接口请求头数据库操作

        :param db: orm对象
        :param headers: 接口请求头对象
        :return:
        """
        db_headers = ApiHeaders(**headers.model_dump(exclude={}))
        db.add(db_headers)
        await db.flush()

        return db_headers



    @classmethod
    async def edit_headers_dao(cls, db: AsyncSession, headers: dict):
        """
        编辑接口请求头数据库操作

        :param db: orm对象
        :param headers: 需要更新的接口请求头字典
        :return:
        """
        await db.execute(update(ApiHeaders), [headers])

    @classmethod
    async def delete_headers_dao(cls, db: AsyncSession, headers: HeadersModel):
        """
        删除接口请求头数据库操作

        :param db: orm对象
        :param headers: 接口请求头对象
        :return:
        """
        #await db.execute(delete(ApiHeaders).where(ApiHeaders.header_id.in_([headers.header_id])))
        await db.execute(update(ApiHeaders).where(ApiHeaders.header_id.in_([headers.header_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = HeadersPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await HeadersDao.get_headers_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
