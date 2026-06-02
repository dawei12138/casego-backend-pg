from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_testing.schema_model_versions.entity.do.versions_do import SchemaModelVersion
from module_admin.api_testing.schema_model_versions.entity.vo.versions_vo import VersionsModel, VersionsPageQueryModel, VersionsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

def is_empty_generated_value(value):
    return value == '' or (isinstance(value, (list, dict)) and len(value) == 0)


def normalize_empty_values(data, field_names):
    normalized = data.copy()
    for field_name in field_names:
        if field_name in normalized and is_empty_generated_value(normalized.get(field_name)):
            normalized[field_name] = None
    return normalized


class VersionsDao:
    """
    JSON Schema 模型版本模块数据库操作层
    """

    @classmethod
    async def get_versions_detail_by_id(cls, db: AsyncSession, version_id: str):
        """
        根据版本ID获取JSON Schema 模型版本详细信息

        :param db: orm对象
        :param version_id: 版本ID
        :return: JSON Schema 模型版本信息对象
        """
        versions_info = (
            (
                await db.execute(
                    select(SchemaModelVersion)
                    .where(
                        SchemaModelVersion.version_id == version_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return versions_info

    @classmethod
    async def get_versions_detail_by_info(cls, db: AsyncSession, versions: VersionsModel):
        """
        根据JSON Schema 模型版本参数获取JSON Schema 模型版本信息

        :param db: orm对象
        :param versions: JSON Schema 模型版本参数对象
        :return: JSON Schema 模型版本信息对象
        """
        versions_info = (
            (
                await db.execute(
                    select(SchemaModelVersion).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return versions_info

    @classmethod
    async def get_versions_list(cls, db: AsyncSession, query_object: VersionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取JSON Schema 模型版本列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 模型版本列表信息字典对象
        """
        query = (
            select(SchemaModelVersion)
            .where(
                SchemaModelVersion.model_id == query_object.model_id if query_object.model_id else True,
                SchemaModelVersion.version == query_object.version if query_object.version else True,
                SchemaModelVersion.revision == query_object.revision if query_object.revision else True,
                SchemaModelVersion.schema_snapshot == query_object.schema_snapshot if query_object.schema_snapshot else True,
                SchemaModelVersion.nodes_snapshot == query_object.nodes_snapshot if query_object.nodes_snapshot else True,
                SchemaModelVersion.change_log == query_object.change_log if query_object.change_log else True,
                SchemaModelVersion.description == query_object.description if query_object.description else True,
                SchemaModelVersion.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModelVersion.del_flag == "0")
            .order_by(SchemaModelVersion.version_id)
            #.distinct()
        )
        versions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return versions_list

    @classmethod
    async def get_versions_orm_list(cls, db: AsyncSession, query_object: VersionsQueryModel) -> List[VersionsQueryModel]:
        """
        根据查询参数获取JSON Schema 模型版本列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: JSON Schema 模型版本列表信息orm对象
        """
        query = (
            select(SchemaModelVersion)
            .where(
                SchemaModelVersion.model_id == query_object.model_id if query_object.model_id else True,
                SchemaModelVersion.version == query_object.version if query_object.version else True,
                SchemaModelVersion.revision == query_object.revision if query_object.revision else True,
                SchemaModelVersion.schema_snapshot == query_object.schema_snapshot if query_object.schema_snapshot else True,
                SchemaModelVersion.nodes_snapshot == query_object.nodes_snapshot if query_object.nodes_snapshot else True,
                SchemaModelVersion.change_log == query_object.change_log if query_object.change_log else True,
                SchemaModelVersion.description == query_object.description if query_object.description else True,
                SchemaModelVersion.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModelVersion.del_flag == "0")
            .order_by(SchemaModelVersion.version_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [VersionsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_versions_dao(cls, db: AsyncSession, versions: VersionsModel):
        """
        新增JSON Schema 模型版本数据库操作

        :param db: orm对象
        :param versions: JSON Schema 模型版本对象
        :return:
        """
        payload = versions.model_dump(exclude_none=True, exclude={})
        payload = normalize_empty_values(
            payload,
            {
                'version_id',
                'revision',
                'change_log',
                'create_by',
                'create_time',
                'update_by',
                'update_time',
                'remark',
                'description',
                'sort_no',
                'del_flag',
            },
        )
        db_versions = SchemaModelVersion(**payload)
        db.add(db_versions)
        await db.flush()

        return db_versions

    @classmethod
    async def edit_versions_dao(cls, db: AsyncSession, versions: dict):
        """
        编辑JSON Schema 模型版本数据库操作

        :param db: orm对象
        :param versions: 需要更新的JSON Schema 模型版本字典
        :return:
        """
        versions = normalize_empty_values(
            versions,
            {
                'version_id',
                'revision',
                'change_log',
                'create_by',
                'create_time',
                'update_by',
                'update_time',
                'remark',
                'description',
                'sort_no',
                'del_flag',
            },
        )
        await db.execute(update(SchemaModelVersion), [versions])

    @classmethod
    async def delete_versions_dao(cls, db: AsyncSession, versions: VersionsModel):
        """
        删除JSON Schema 模型版本数据库操作

        :param db: orm对象
        :param versions: JSON Schema 模型版本对象
        :return:
        """
        #await db.execute(delete(SchemaModelVersion).where(SchemaModelVersion.version_id.in_([versions.version_id])))
        await db.execute(update(SchemaModelVersion).where(SchemaModelVersion.version_id.in_([versions.version_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = VersionsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await VersionsDao.get_versions_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
