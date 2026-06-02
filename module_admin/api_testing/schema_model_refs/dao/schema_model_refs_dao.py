from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_testing.schema_model_refs.entity.do.schema_model_refs_do import SchemaModelRef
from module_admin.api_testing.schema_model_refs.entity.vo.schema_model_refs_vo import Schema_model_refsModel, Schema_model_refsPageQueryModel, Schema_model_refsQueryModel
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


class Schema_model_refsDao:
    """
    JSON Schema 模型引用关系模块数据库操作层
    """

    @classmethod
    async def get_schema_model_refs_detail_by_id(cls, db: AsyncSession, ref_id: str):
        """
        根据引用ID获取JSON Schema 模型引用关系详细信息

        :param db: orm对象
        :param ref_id: 引用ID
        :return: JSON Schema 模型引用关系信息对象
        """
        schema_model_refs_info = (
            (
                await db.execute(
                    select(SchemaModelRef)
                    .where(
                        SchemaModelRef.ref_id == ref_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_model_refs_info

    @classmethod
    async def get_schema_model_refs_detail_by_info(cls, db: AsyncSession, schema_model_refs: Schema_model_refsModel):
        """
        根据JSON Schema 模型引用关系参数获取JSON Schema 模型引用关系信息

        :param db: orm对象
        :param schema_model_refs: JSON Schema 模型引用关系参数对象
        :return: JSON Schema 模型引用关系信息对象
        """
        schema_model_refs_info = (
            (
                await db.execute(
                    select(SchemaModelRef).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_model_refs_info

    @classmethod
    async def get_schema_model_refs_list(cls, db: AsyncSession, query_object: Schema_model_refsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取JSON Schema 模型引用关系列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 模型引用关系列表信息字典对象
        """
        query = (
            select(SchemaModelRef)
            .where(
                SchemaModelRef.model_id == query_object.model_id if query_object.model_id else True,
                SchemaModelRef.ref_model_id == query_object.ref_model_id if query_object.ref_model_id else True,
                SchemaModelRef.ref_path == query_object.ref_path if query_object.ref_path else True,
                SchemaModelRef.ref_version == query_object.ref_version if query_object.ref_version else True,
                SchemaModelRef.description == query_object.description if query_object.description else True,
                SchemaModelRef.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModelRef.del_flag == "0")
            .order_by(SchemaModelRef.ref_id)
            #.distinct()
        )
        schema_model_refs_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return schema_model_refs_list

    @classmethod
    async def get_schema_model_refs_orm_list(cls, db: AsyncSession, query_object: Schema_model_refsQueryModel) -> List[Schema_model_refsQueryModel]:
        """
        根据查询参数获取JSON Schema 模型引用关系列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: JSON Schema 模型引用关系列表信息orm对象
        """
        query = (
            select(SchemaModelRef)
            .where(
                SchemaModelRef.model_id == query_object.model_id if query_object.model_id else True,
                SchemaModelRef.ref_model_id == query_object.ref_model_id if query_object.ref_model_id else True,
                SchemaModelRef.ref_path == query_object.ref_path if query_object.ref_path else True,
                SchemaModelRef.ref_version == query_object.ref_version if query_object.ref_version else True,
                SchemaModelRef.description == query_object.description if query_object.description else True,
                SchemaModelRef.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModelRef.del_flag == "0")
            .order_by(SchemaModelRef.ref_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Schema_model_refsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_schema_model_refs_dao(cls, db: AsyncSession, schema_model_refs: Schema_model_refsModel):
        """
        新增JSON Schema 模型引用关系数据库操作

        :param db: orm对象
        :param schema_model_refs: JSON Schema 模型引用关系对象
        :return:
        """
        payload = schema_model_refs.model_dump(exclude_none=True, exclude={})
        payload = normalize_empty_values(
            payload,
            {
                'ref_id',
                'ref_path',
                'ref_version',
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
        db_schema_model_refs = SchemaModelRef(**payload)
        db.add(db_schema_model_refs)
        await db.flush()

        return db_schema_model_refs

    @classmethod
    async def edit_schema_model_refs_dao(cls, db: AsyncSession, schema_model_refs: dict):
        """
        编辑JSON Schema 模型引用关系数据库操作

        :param db: orm对象
        :param schema_model_refs: 需要更新的JSON Schema 模型引用关系字典
        :return:
        """
        schema_model_refs = normalize_empty_values(
            schema_model_refs,
            {
                'ref_id',
                'ref_path',
                'ref_version',
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
        await db.execute(update(SchemaModelRef), [schema_model_refs])

    @classmethod
    async def delete_schema_model_refs_dao(cls, db: AsyncSession, schema_model_refs: Schema_model_refsModel):
        """
        删除JSON Schema 模型引用关系数据库操作

        :param db: orm对象
        :param schema_model_refs: JSON Schema 模型引用关系对象
        :return:
        """
        #await db.execute(delete(SchemaModelRef).where(SchemaModelRef.ref_id.in_([schema_model_refs.ref_id])))
        await db.execute(update(SchemaModelRef).where(SchemaModelRef.ref_id.in_([schema_model_refs.ref_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Schema_model_refsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Schema_model_refsDao.get_schema_model_refs_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
