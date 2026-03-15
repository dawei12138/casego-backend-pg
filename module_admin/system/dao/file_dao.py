from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.system.entity.do.file_do import SysFile
from module_admin.system.entity.vo.file_vo import FileModel, FilePageQueryModel, FileQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class FileDao:
    """
    附件管理模块数据库操作层
    """

    @classmethod
    async def get_file_detail_by_id(cls, db: AsyncSession, file_id: int):
        """
        根据获取附件管理详细信息

        :param db: orm对象
        :param file_id: 
        :return: 附件管理信息对象
        """
        file_info = (
            (
                await db.execute(
                    select(SysFile)
                    .where(
                        SysFile.file_id == file_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return file_info

    @classmethod
    async def get_file_detail_by_info(cls, db: AsyncSession, file: FileModel):
        """
        根据附件管理参数获取附件管理信息

        :param db: orm对象
        :param file: 附件管理参数对象
        :return: 附件管理信息对象
        """
        file_info = (
            (
                await db.execute(
                    select(SysFile).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return file_info

    @classmethod
    async def get_file_list(cls, db: AsyncSession, query_object: FilePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取附件管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 附件管理列表信息字典对象
        """
        query = (
            select(SysFile)
            .where(
                SysFile.original_name.like(f'%{query_object.original_name}%') if query_object.original_name else True,
                SysFile.stored_name.like(f'%{query_object.stored_name}%') if query_object.stored_name else True,
                SysFile.file_ext == query_object.file_ext if query_object.file_ext else True,
                SysFile.mime_type == query_object.mime_type if query_object.mime_type else True,
                SysFile.file_size == query_object.file_size if query_object.file_size else True,
                SysFile.file_path == query_object.file_path if query_object.file_path else True,
                SysFile.file_url == query_object.file_url if query_object.file_url else True,
                SysFile.storage_type == query_object.storage_type if query_object.storage_type else True,
                SysFile.is_temp == query_object.is_temp if query_object.is_temp else True,
                SysFile.file_hash == query_object.file_hash if query_object.file_hash else True,
                SysFile.biz_tag == query_object.biz_tag if query_object.biz_tag else True,
                SysFile.description == query_object.description if query_object.description else True,
                SysFile.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SysFile.del_flag == "0")
            .order_by(SysFile.file_id)
            #.distinct()
        )
        file_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return file_list

    @classmethod
    async def get_file_orm_list(cls, db: AsyncSession, query_object: FileQueryModel):
        """
        根据查询参数获取附件管理列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 附件管理列表信息orm对象
        """
        query = (
            select(SysFile)
            .where(
                SysFile.original_name.like(f'%{query_object.original_name}%') if query_object.original_name else True,
                SysFile.stored_name.like(f'%{query_object.stored_name}%') if query_object.stored_name else True,
                SysFile.file_ext == query_object.file_ext if query_object.file_ext else True,
                SysFile.mime_type == query_object.mime_type if query_object.mime_type else True,
                SysFile.file_size == query_object.file_size if query_object.file_size else True,
                SysFile.file_path == query_object.file_path if query_object.file_path else True,
                SysFile.file_url == query_object.file_url if query_object.file_url else True,
                SysFile.storage_type == query_object.storage_type if query_object.storage_type else True,
                SysFile.is_temp == query_object.is_temp if query_object.is_temp else True,
                SysFile.file_hash == query_object.file_hash if query_object.file_hash else True,
                SysFile.biz_tag == query_object.biz_tag if query_object.biz_tag else True,
                SysFile.description == query_object.description if query_object.description else True,
                SysFile.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SysFile.del_flag == "0")
            .order_by(SysFile.file_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_file_dao(cls, db: AsyncSession, file: FileModel):
        """
        新增附件管理数据库操作

        :param db: orm对象
        :param file: 附件管理对象
        :return:
        """
        db_file = SysFile(**file.model_dump(exclude={'sort_no', 'del_flag'}))
        db.add(db_file)
        await db.flush()

        return db_file

    @classmethod
    async def edit_file_dao(cls, db: AsyncSession, file: dict):
        """
        编辑附件管理数据库操作

        :param db: orm对象
        :param file: 需要更新的附件管理字典
        :return:
        """
        await db.execute(update(SysFile), [file])

    @classmethod
    async def delete_file_dao(cls, db: AsyncSession, file: FileModel):
        """
        删除附件管理数据库操作

        :param db: orm对象
        :param file: 附件管理对象
        :return:
        """
        #await db.execute(delete(SysFile).where(SysFile.file_id.in_([file.file_id])))
        await db.execute(update(SysFile).where(SysFile.file_id.in_([file.file_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = FilePageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await FileDao.get_file_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
