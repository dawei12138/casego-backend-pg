from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_testing.api_formdata.entity.do.formdata_do import ApiFormdata
from module_admin.api_testing.api_formdata.entity.vo.formdata_vo import FormdataModel, FormdataPageQueryModel, \
    FormdataQueryModel
from utils.page_util import PageUtil
from config.get_db import get_db


class FormdataDao:
    """
    接口单body模块数据库操作层
    """

    @classmethod
    async def get_formdata_detail_by_id(cls, db: AsyncSession, formdata_id: int):
        """
        根据ID获取接口单body详细信息

        :param db: orm对象
        :param formdata_id: ID
        :return: 接口单body信息对象
        """
        formdata_info = (
            (
                await db.execute(
                    select(ApiFormdata)
                    .where(
                        ApiFormdata.formdata_id == formdata_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return formdata_info

    @classmethod
    async def get_formdata_detail_by_info(cls, db: AsyncSession, formdata: FormdataModel):
        """
        根据接口单body参数获取接口单body信息

        :param db: orm对象
        :param formdata: 接口单body参数对象
        :return: 接口单body信息对象
        """
        formdata_info = (
            (
                await db.execute(
                    select(ApiFormdata).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return formdata_info

    @classmethod
    async def get_formdata_list(cls, db: AsyncSession, query_object: FormdataPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口单body列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口单body列表信息对象
        """
        query = (
            select(ApiFormdata)
            .where(
                ApiFormdata.case_id == query_object.case_id if query_object.case_id else True,
                ApiFormdata.key == query_object.key if query_object.key else True,
            )
            .where(ApiFormdata.del_flag == "0")
            .order_by(ApiFormdata.formdata_id)
            #.distinct()
        )
        formdata_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return formdata_list

    @classmethod
    async def del_case_form(cls, db: AsyncSession, query_object: FormdataPageQueryModel):
        """
        批量删除用例的关联表单

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口单body列表信息对象
        """
        conditions = []
        if query_object.case_id:
            conditions.append(ApiFormdata.case_id == query_object.case_id)
        if query_object.key:
            conditions.append(ApiFormdata.key == query_object.key)
        stmt = (
            update(ApiFormdata)
            .where(*conditions)
            .values(del_flag="1")
        )

        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount

    @classmethod
    async def get_formdata_orm_list(cls, db: AsyncSession, query_object: FormdataQueryModel):
        """
        根据查询参数获取接口单body列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 接口单body列表信息orm对象
        """
        query = (
            select(ApiFormdata)
            .where(
                ApiFormdata.case_id == query_object.case_id if query_object.case_id else True,
                ApiFormdata.key == query_object.key if query_object.key else True,
            )
            .where(ApiFormdata.del_flag == "0")
            .order_by(ApiFormdata.formdata_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [FormdataQueryModel.model_validate(i) for i in result.scalars().all()]

    @classmethod
    async def add_formdata_dao(cls, db: AsyncSession, formdata: FormdataModel):
        """
        新增接口单body数据库操作

        :param db: orm对象
        :param formdata: 接口单body对象
        :return:
        """
        db_formdata = ApiFormdata(**formdata.model_dump(exclude={'remark', }))
        db.add(db_formdata)
        await db.flush()

        return db_formdata

    @classmethod
    async def edit_formdata_dao(cls, db: AsyncSession, formdata: dict):
        """
        编辑接口单body数据库操作

        :param db: orm对象
        :param formdata: 需要更新的接口单body字典
        :return:
        """
        await db.execute(update(ApiFormdata), [formdata])

    @classmethod
    async def delete_formdata_dao(cls, db: AsyncSession, formdata: FormdataModel):
        """
        删除接口单body数据库操作

        :param db: orm对象
        :param formdata: 接口单body对象
        :return:
        """
        # await db.execute(delete(ApiFormdata).where(ApiFormdata.formdata_id.in_([formdata.formdata_id])))
        await db.execute(
            update(ApiFormdata).where(ApiFormdata.formdata_id.in_([formdata.formdata_id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = FormdataPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await FormdataDao.get_formdata_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
