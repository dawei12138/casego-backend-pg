from typing import List

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_workflow.api_param_item.entity.do.api_param_item_do import ApiParamItem
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemModel, \
    Api_param_itemPageQueryModel, Api_param_itemQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db


class Api_param_itemDao:
    """
    参数化数据行模块数据库操作层
    """

    @classmethod
    async def get_api_param_item_detail_by_id(cls, db: AsyncSession, key_id: int):
        """
        根据主键ID获取参数化数据行详细信息

        :param db: orm对象
        :param key_id: 主键ID
        :return: 参数化数据行信息对象
        """
        api_param_item_info = (
            (
                await db.execute(
                    select(ApiParamItem)
                    .where(
                        ApiParamItem.key_id == key_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_param_item_info

    @classmethod
    async def get_api_param_item_detail_by_info(cls, db: AsyncSession, api_param_item: Api_param_itemModel):
        """
        根据参数化数据行参数获取参数化数据行信息

        :param db: orm对象
        :param api_param_item: 参数化数据行参数对象
        :return: 参数化数据行信息对象
        """
        api_param_item_info = (
            (
                await db.execute(
                    select(ApiParamItem).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_param_item_info

    @classmethod
    async def get_api_param_item_list(cls, db: AsyncSession, query_object: Api_param_itemPageQueryModel,
                                      is_page: bool = False):
        """
        根据查询参数获取参数化数据行列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 参数化数据行列表信息字典对象
        """
        query = (
            select(ApiParamItem)
            .where(
                ApiParamItem.parameterization_id == query_object.parameterization_id if query_object.parameterization_id else True,
                ApiParamItem.group_name == query_object.group_name if query_object.group_name else True,
                ApiParamItem.key == query_object.key if query_object.key else True,
                ApiParamItem.value == query_object.value if query_object.value else True,
                ApiParamItem.description == query_object.description if query_object.description else True,
                ApiParamItem.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiParamItem.del_flag == "0")
            .order_by(ApiParamItem.key_id)
            #.distinct()
        )
        api_param_item_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return api_param_item_list

    @classmethod
    async def get_api_param_item_orm_list(cls, db: AsyncSession, query_object: Api_param_itemQueryModel) -> List[Api_param_itemQueryModel]:
        """
        根据查询参数获取参数化数据行列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 参数化数据行列表信息orm对象
        """
        query = (
            select(ApiParamItem)
            .where(
                ApiParamItem.parameterization_id == query_object.parameterization_id if query_object.parameterization_id else True,
                ApiParamItem.group_name == query_object.group_name if query_object.group_name else True,
                ApiParamItem.key == query_object.key if query_object.key else True,
                ApiParamItem.value == query_object.value if query_object.value else True,
                ApiParamItem.description == query_object.description if query_object.description else True,
                ApiParamItem.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiParamItem.del_flag == "0")
            .order_by(ApiParamItem.key_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Api_param_itemQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表
    @classmethod
    async def add_api_param_item_dao(cls, db: AsyncSession, api_param_item: Api_param_itemModel):
        """
        新增参数化数据行数据库操作

        :param db: orm对象
        :param api_param_item: 参数化数据行对象
        :return:
        """
        db_api_param_item = ApiParamItem(**api_param_item.model_dump(exclude={}))
        db.add(db_api_param_item)
        await db.flush()

        return db_api_param_item

    @classmethod
    async def edit_api_param_item_dao(cls, db: AsyncSession, api_param_item: dict):
        """
        编辑参数化数据行数据库操作

        :param db: orm对象
        :param api_param_item: 需要更新的参数化数据行字典
        :return:
        """
        await db.execute(update(ApiParamItem), [api_param_item])

    @classmethod
    async def delete_api_param_item_dao(cls, db: AsyncSession, api_param_item: Api_param_itemModel):
        """
        删除参数化数据行数据库操作

        :param db: orm对象
        :param api_param_item: 参数化数据行对象
        :return:
        """
        # await db.execute(delete(ApiParamItem).where(ApiParamItem.key_id.in_([api_param_item.key_id])))
        await db.execute(
            update(ApiParamItem).where(ApiParamItem.key_id.in_([api_param_item.key_id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Api_param_itemPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Api_param_itemDao.get_api_param_item_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
