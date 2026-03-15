from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_services.entity.do.services_do import ApiServices
from module_admin.api_testing.api_services.entity.vo.services_vo import ServicesModel, ServicesPageQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db


class ServicesDao:
    """
    环境服务地址模块数据库操作层
    """

    @classmethod
    async def get_services_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据服务ID获取环境服务地址详细信息

        :param db: orm对象
        :param id: 服务ID
        :return: 环境服务地址信息对象
        """
        services_info = (
            (
                await db.execute(
                    select(ApiServices)
                    .where(
                        ApiServices.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return services_info

    @classmethod
    async def get_services_detail_by_info(cls, db: AsyncSession, services: ServicesModel):
        """
        根据环境服务地址参数获取环境服务地址信息

        :param db: orm对象
        :param services: 环境服务地址参数对象
        :return: 环境服务地址信息对象
        """
        services_info = (
            (
                await db.execute(
                    select(ApiServices).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return services_info

    @classmethod
    async def get_services_list(cls, db: AsyncSession, query_object: ServicesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取环境服务地址列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境服务地址列表信息对象
        """
        query = (
            select(ApiServices)
            .where(
                ApiServices.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiServices.url.like(f'%{query_object.url}%') if query_object.url else True,
                ApiServices.environment_id == query_object.environment_id if query_object.environment_id else True,
                ApiServices.is_default == query_object.is_default if query_object.is_default else True,
            )
            .where(ApiServices.del_flag == "0")
            .order_by(ApiServices.id)
            #.distinct()
        )
        services_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return services_list

    @classmethod
    async def add_services_dao(cls, db: AsyncSession, services: ServicesModel):
        """
        新增环境服务地址数据库操作

        :param db: orm对象
        :param services: 环境服务地址对象
        :return:
        """
        db_services = ApiServices(**services.model_dump(exclude={'remark', 'description', 'sort_no', 'del_flag'}))
        db.add(db_services)
        await db.flush()

        return db_services

    @classmethod
    async def edit_services_dao(cls, db: AsyncSession, services: dict):
        """
        编辑环境服务地址数据库操作

        :param db: orm对象
        :param services: 需要更新的环境服务地址字典
        :return:
        """
        await db.execute(update(ApiServices), [services])

    @classmethod
    async def delete_services_dao(cls, db: AsyncSession, services: ServicesModel):
        """
        删除环境服务地址数据库操作

        :param db: orm对象
        :param services: 环境服务地址对象
        :return:
        """
        # await db.execute(delete(ApiServices).where(ApiServices.id.in_([services.id])))
        await db.execute(update(ApiServices).where(ApiServices.id.in_([services.id])).values(del_flag="1"))

    @classmethod
    async def update_service_default(cls, db: AsyncSession, services: ServicesModel):
        """
        修改环境服务地址默认为全部取消

        :param db: orm对象
        :param services: 环境服务地址对象
        :return:
        """
        await db.execute(
            update(ApiServices).where(ApiServices.environment_id.in_([services.environment_id])).values(is_default=False))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = ServicesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await ServicesDao.get_services_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
