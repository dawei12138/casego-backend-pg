from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_cookies.entity.do.cookies_do import ApiCookies
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import CookiesModel, CookiesPageQueryModel, \
    CookiesQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db


class CookiesDao:
    """
    接口请求Cookie模块数据库操作层
    """

    @classmethod
    async def get_cookies_detail_by_id(cls, db: AsyncSession, cookie_id: int):
        """
        根据ID获取接口请求Cookie详细信息

        :param db: orm对象
        :param cookie_id: ID
        :return: 接口请求Cookie信息对象
        """
        cookies_info = (
            (
                await db.execute(
                    select(ApiCookies)
                    .where(
                        ApiCookies.cookie_id == cookie_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return cookies_info

    @classmethod
    async def get_cookies_detail_by_info(cls, db: AsyncSession, cookies: CookiesModel):
        """
        根据接口请求Cookie参数获取接口请求Cookie信息

        :param db: orm对象
        :param cookies: 接口请求Cookie参数对象
        :return: 接口请求Cookie信息对象
        """
        cookies_info = (
            (
                await db.execute(
                    select(ApiCookies).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return cookies_info

    @classmethod
    async def get_cookies_list(cls, db: AsyncSession, query_object: CookiesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口请求Cookie列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口请求Cookie列表信息对象
        """
        query = (
            select(ApiCookies)
            .where(
                ApiCookies.case_id == query_object.case_id if query_object.case_id else True,
                ApiCookies.key == query_object.key if query_object.key else True,
                ApiCookies.value == query_object.value if query_object.value else True,
                ApiCookies.domain == query_object.domain if query_object.domain else True,
                ApiCookies.path == query_object.path if query_object.path else True,
                ApiCookies.is_run == query_object.is_run if query_object.is_run else True,
                ApiCookies.description == query_object.description if query_object.description else True,
                ApiCookies.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiCookies.del_flag == "0")
            .order_by(ApiCookies.cookie_id)
            #.distinct()
        )
        cookies_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return cookies_list

    @classmethod
    async def get_cookies_orm_list(cls, db: AsyncSession, query_object: CookiesQueryModel):
        """
        根据查询参数获取接口请求Cookie列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口请求Cookie列表信息orm对象
        """
        query = (
            select(ApiCookies)
            .where(
                ApiCookies.case_id == query_object.case_id if query_object.case_id else True,
                ApiCookies.key == query_object.key if query_object.key else True,
                ApiCookies.value == query_object.value if query_object.value else True,
                ApiCookies.domain == query_object.domain if query_object.domain else True,
                ApiCookies.path == query_object.path if query_object.path else True,
                ApiCookies.is_run == query_object.is_run if query_object.is_run else True,
                ApiCookies.description == query_object.description if query_object.description else True,
                ApiCookies.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiCookies.del_flag == "0")
            .order_by(ApiCookies.cookie_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [CookiesQueryModel.model_validate(i) for i in result.scalars().all()]  # 返回 ORM 对象列表

    @classmethod
    async def add_cookies_dao(cls, db: AsyncSession, cookies: CookiesModel):
        """
        新增接口请求Cookie数据库操作

        :param db: orm对象
        :param cookies: 接口请求Cookie对象
        :return:
        """
        db_cookies = ApiCookies(**cookies.model_dump(exclude={}))
        db.add(db_cookies)
        await db.flush()

        return db_cookies

    @classmethod
    async def edit_cookies_dao(cls, db: AsyncSession, cookies: dict):
        """
        编辑接口请求Cookie数据库操作

        :param db: orm对象
        :param cookies: 需要更新的接口请求Cookie字典
        :return:
        """
        await db.execute(update(ApiCookies), [cookies])

    @classmethod
    async def delete_cookies_dao(cls, db: AsyncSession, cookies: CookiesModel):
        """
        删除接口请求Cookie数据库操作

        :param db: orm对象
        :param cookies: 接口请求Cookie对象
        :return:
        """
        # await db.execute(delete(ApiCookies).where(ApiCookies.cookie_id.in_([cookies.cookie_id])))
        await db.execute(update(ApiCookies).where(ApiCookies.cookie_id.in_([cookies.cookie_id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = CookiesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await CookiesDao.get_cookies_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
