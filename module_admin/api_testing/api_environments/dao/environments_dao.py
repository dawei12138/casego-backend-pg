from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_admin.api_testing.api_environments.entity.do.environments_do import ApiEnvironments
from module_admin.api_testing.api_environments.entity.vo.environments_vo import EnvironmentsModel, \
    EnvironmentsPageQueryModel
from module_admin.api_testing.api_services.entity.do.services_do import ApiServices
from utils.page_util import PageUtil


class EnvironmentsDao:
    """
    环境配置模块数据库操作层
    """

    @classmethod
    async def get_environments_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据环境ID获取环境配置详细信息

        :param db: orm对象
        :param id: 环境ID
        :return: 环境配置信息对象
        """
        environments_info = (
            (
                await db.execute(
                    select(ApiEnvironments)
                    .where(
                        ApiEnvironments.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return environments_info

    @classmethod
    async def get_environments_detail_by_info(cls, db: AsyncSession, environments: EnvironmentsModel):
        """
        根据环境配置参数获取环境配置信息

        :param db: orm对象
        :param environments: 环境配置参数对象
        :return: 环境配置信息对象
        """
        environments_info = (
            (
                await db.execute(
                    select(ApiEnvironments).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return environments_info

    @classmethod
    async def get_environments_list(cls, db: AsyncSession, query_object: EnvironmentsPageQueryModel,
                                    is_page: bool = False):
        """
        根据查询参数获取环境配置列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境配置列表信息对象
        """
        query = (
            select(ApiEnvironments)
            .where(
                ApiEnvironments.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiEnvironments.project_id == query_object.project_id if query_object.project_id else True,
                ApiEnvironments.create_time == query_object.create_time if query_object.create_time else True,
            )
            .where(ApiEnvironments.del_flag == "0")
            .order_by(ApiEnvironments.id)
            #.distinct()
        )
        environments_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return environments_list

    @classmethod
    async def add_environments_dao(cls, db: AsyncSession, environments: EnvironmentsModel):
        """
        新增环境配置数据库操作

        :param db: orm对象
        :param environments: 环境配置对象
        :return:
        """
        db_environments = ApiEnvironments(**environments.model_dump(exclude={'description', 'sort_no', 'del_flag'}))
        db.add(db_environments)
        await db.flush()

        return db_environments

    @classmethod
    async def init_environments_dao(cls, db: AsyncSession, extra_dict: dict):
        """
        新增項目的時候初始化环境配置数据库操作

        :param extra_dict: project_id,user
        :param db: orm对象
        :return:
        """
        init_map = [
            {"name": "正式環境", }, {"name": "測試環境", "is_default": 1}, {"name": "灰度環境"}, {"name": "演示環境"}]
        inserted_ids = []
        for item in init_map:
            item.update(extra_dict)
            db_environments = ApiEnvironments(**item)
            db.add(db_environments)
            inserted_ids.append(db_environments)  # 保存对象
        await db.flush()
        ids = [env.id for env in inserted_ids]
        extra_dict.pop("project_id")
        init_service_map = {"name": "默認服務", "is_default": True, "url": " "}
        init_service_map.update(extra_dict)
        for env_id in ids:
            init_service_map.update({"environment_id": env_id})
            db_services = ApiServices(**init_service_map)
            db.add(db_services)
        await db.flush()

    @classmethod
    async def edit_environments_dao(cls, db: AsyncSession, environments: dict):
        """
        编辑环境配置数据库操作

        :param db: orm对象
        :param environments: 需要更新的环境配置字典
        :return:
        """
        await db.execute(update(ApiEnvironments), [environments])

    @classmethod
    async def edit_environments_isdefault_dao(cls, db: AsyncSession, environments: EnvironmentsModel):
        """
        操作是否默認為取消

        :param db: orm对象
        :param environments: 需要更新的环境配置字典
        :return:
        """
        await db.execute(update(ApiEnvironments).where(
            and_(ApiEnvironments.project_id.in_([environments.project_id]), ApiEnvironments.is_default == 1)
        ).values(is_default=0))

    @classmethod
    async def delete_environments_dao(cls, db: AsyncSession, environments: EnvironmentsModel):
        """
        删除环境配置数据库操作

        :param db: orm对象
        :param environments: 环境配置对象
        :return:
        """
        # await db.execute(delete(ApiEnvironments).where(ApiEnvironments.id.in_([environments.id])))
        await db.execute(update(ApiEnvironments).where(ApiEnvironments.id.in_([environments.id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:

                # 测试查询
                result = await EnvironmentsDao.init_environments_dao(db)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
