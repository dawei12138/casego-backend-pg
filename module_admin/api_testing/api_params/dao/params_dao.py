from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_params.entity.do.params_do import ApiParams
from module_admin.api_testing.api_params.entity.vo.params_vo import ParamsModel, ParamsPageQueryModel, ParamsQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db

class ParamsDao:
    """
    接口请求参数模块数据库操作层
    """

    @classmethod
    async def get_params_detail_by_id(cls, db: AsyncSession, param_id: int):
        """
        根据ID获取接口请求参数详细信息

        :param db: orm对象
        :param param_id: ID
        :return: 接口请求参数信息对象
        """
        params_info = (
            (
                await db.execute(
                    select(ApiParams)
                    .where(
                        ApiParams.param_id == param_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return params_info

    @classmethod
    async def get_params_detail_by_info(cls, db: AsyncSession, params: ParamsModel):
        """
        根据接口请求参数参数获取接口请求参数信息

        :param db: orm对象
        :param params: 接口请求参数参数对象
        :return: 接口请求参数信息对象
        """
        params_info = (
            (
                await db.execute(
                    select(ApiParams).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return params_info

    @classmethod
    async def get_params_list(cls, db: AsyncSession, query_object: ParamsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口请求参数列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口请求参数列表信息对象
        """
        query = (
            select(ApiParams)
            .where(
                ApiParams.case_id == query_object.case_id if query_object.case_id else True,
                ApiParams.key == query_object.key if query_object.key else True,
                ApiParams.value == query_object.value if query_object.value else True,
                ApiParams.is_run == query_object.is_run if query_object.is_run else True,
                ApiParams.description == query_object.description if query_object.description else True,
                ApiParams.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiParams.del_flag == "0")
            .order_by(ApiParams.param_id)
            #.distinct()
        )
        params_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return params_list

    @classmethod
    async def get_params_orm_list(cls, db: AsyncSession, query_object: ParamsQueryModel):
        """
        根据查询参数获取接口请求参数列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口请求参数列表信息orm对象
        """
        query = (
            select(ApiParams)
            .where(
                ApiParams.case_id == query_object.case_id if query_object.case_id else True,
                ApiParams.key == query_object.key if query_object.key else True,
                ApiParams.value == query_object.value if query_object.value else True,
                ApiParams.is_run == query_object.is_run if query_object.is_run else True,
                ApiParams.description == query_object.description if query_object.description else True,
                ApiParams.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiParams.del_flag == "0")
            .order_by(ApiParams.param_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [ParamsQueryModel.model_validate(i) for i in result.scalars().all()]
    @classmethod
    async def add_params_dao(cls, db: AsyncSession, params: ParamsModel):
        """
        新增接口请求参数数据库操作

        :param db: orm对象
        :param params: 接口请求参数对象
        :return:
        """
        db_params = ApiParams(**params.model_dump(exclude={}))
        db.add(db_params)
        await db.flush()

        return db_params

    @classmethod
    async def edit_params_dao(cls, db: AsyncSession, params: dict):
        """
        编辑接口请求参数数据库操作

        :param db: orm对象
        :param params: 需要更新的接口请求参数字典
        :return:
        """
        await db.execute(update(ApiParams), [params])

    @classmethod
    async def delete_params_dao(cls, db: AsyncSession, params: ParamsModel):
        """
        删除接口请求参数数据库操作

        :param db: orm对象
        :param params: 接口请求参数对象
        :return:
        """
        #await db.execute(delete(ApiParams).where(ApiParams.param_id.in_([params.param_id])))
        await db.execute(update(ApiParams).where(ApiParams.param_id.in_([params.param_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = ParamsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await ParamsDao.get_params_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
