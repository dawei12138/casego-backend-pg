from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_testing.api_script_library.entity.do.script_library_do import ApiScriptLibrary
from module_admin.api_testing.api_script_library.entity.vo.script_library_vo import Script_libraryModel, Script_libraryPageQueryModel, Script_libraryQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Script_libraryDao:
    """
    公共脚本库模块数据库操作层
    """

    @classmethod
    async def get_script_library_detail_by_id(cls, db: AsyncSession, script_id: int):
        """
        根据脚本ID获取公共脚本库详细信息

        :param db: orm对象
        :param script_id: 脚本ID
        :return: 公共脚本库信息对象
        """
        script_library_info = (
            (
                await db.execute(
                    select(ApiScriptLibrary)
                    .where(
                        ApiScriptLibrary.script_id == script_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return script_library_info

    @classmethod
    async def get_script_library_detail_by_info(cls, db: AsyncSession, script_library: Script_libraryModel):
        """
        根据公共脚本库参数获取公共脚本库信息

        :param db: orm对象
        :param script_library: 公共脚本库参数对象
        :return: 公共脚本库信息对象
        """
        script_library_info = (
            (
                await db.execute(
                    select(ApiScriptLibrary).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return script_library_info

    @classmethod
    async def get_script_library_list(cls, db: AsyncSession, query_object: Script_libraryPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取公共脚本库列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公共脚本库列表信息字典对象
        """
        query = (
            select(ApiScriptLibrary)
            .where(
                ApiScriptLibrary.script_name.like(f'%{query_object.script_name}%') if query_object.script_name else True,
                ApiScriptLibrary.script_type == query_object.script_type if query_object.script_type else True,
                ApiScriptLibrary.script_content == query_object.script_content if query_object.script_content else True,
                ApiScriptLibrary.status == query_object.status if query_object.status else True,
                ApiScriptLibrary.description == query_object.description if query_object.description else True,
                ApiScriptLibrary.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiScriptLibrary.del_flag == "0")
            .order_by(ApiScriptLibrary.script_id)
            #.distinct()
        )
        script_library_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return script_library_list

    @classmethod
    async def get_script_library_orm_list(cls, db: AsyncSession, query_object: Script_libraryQueryModel) -> List[Script_libraryQueryModel]:
        """
        根据查询参数获取公共脚本库列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 公共脚本库列表信息orm对象
        """
        query = (
            select(ApiScriptLibrary)
            .where(
                ApiScriptLibrary.script_name.like(f'%{query_object.script_name}%') if query_object.script_name else True,
                ApiScriptLibrary.script_type == query_object.script_type if query_object.script_type else True,
                ApiScriptLibrary.script_content == query_object.script_content if query_object.script_content else True,
                ApiScriptLibrary.status == query_object.status if query_object.status else True,
                ApiScriptLibrary.description == query_object.description if query_object.description else True,
                ApiScriptLibrary.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiScriptLibrary.del_flag == "0")
            .order_by(ApiScriptLibrary.script_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Script_libraryQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_script_library_dao(cls, db: AsyncSession, script_library: Script_libraryModel):
        """
        新增公共脚本库数据库操作

        :param db: orm对象
        :param script_library: 公共脚本库对象
        :return:
        """
        db_script_library = ApiScriptLibrary(**script_library.model_dump(exclude={}))
        db.add(db_script_library)
        await db.flush()

        return db_script_library

    @classmethod
    async def edit_script_library_dao(cls, db: AsyncSession, script_library: dict):
        """
        编辑公共脚本库数据库操作

        :param db: orm对象
        :param script_library: 需要更新的公共脚本库字典
        :return:
        """
        await db.execute(update(ApiScriptLibrary), [script_library])

    @classmethod
    async def delete_script_library_dao(cls, db: AsyncSession, script_library: Script_libraryModel):
        """
        删除公共脚本库数据库操作

        :param db: orm对象
        :param script_library: 公共脚本库对象
        :return:
        """
        #await db.execute(delete(ApiScriptLibrary).where(ApiScriptLibrary.script_id.in_([script_library.script_id])))
        await db.execute(update(ApiScriptLibrary).where(ApiScriptLibrary.script_id.in_([script_library.script_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Script_libraryPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Script_libraryDao.get_script_library_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
