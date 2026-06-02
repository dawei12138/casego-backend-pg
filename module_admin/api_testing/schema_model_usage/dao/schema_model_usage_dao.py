from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_testing.schema_model_usage.entity.do.schema_model_usage_do import SchemaModelUsage
from module_admin.api_testing.schema_model_usage.entity.vo.schema_model_usage_vo import Schema_model_usageModel, Schema_model_usagePageQueryModel, Schema_model_usageQueryModel
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


class Schema_model_usageDao:
    """
    JSON Schema 模型使用关系模块数据库操作层
    """

    @classmethod
    async def get_schema_model_usage_detail_by_id(cls, db: AsyncSession, usage_id: str):
        """
        根据使用关系ID获取JSON Schema 模型使用关系详细信息

        :param db: orm对象
        :param usage_id: 使用关系ID
        :return: JSON Schema 模型使用关系信息对象
        """
        schema_model_usage_info = (
            (
                await db.execute(
                    select(SchemaModelUsage)
                    .where(
                        SchemaModelUsage.usage_id == usage_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_model_usage_info

    @classmethod
    async def get_schema_model_usage_detail_by_info(cls, db: AsyncSession, schema_model_usage: Schema_model_usageModel):
        """
        根据JSON Schema 模型使用关系参数获取JSON Schema 模型使用关系信息

        :param db: orm对象
        :param schema_model_usage: JSON Schema 模型使用关系参数对象
        :return: JSON Schema 模型使用关系信息对象
        """
        schema_model_usage_info = (
            (
                await db.execute(
                    select(SchemaModelUsage).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_model_usage_info

    @classmethod
    async def get_schema_model_usage_list(cls, db: AsyncSession, query_object: Schema_model_usagePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取JSON Schema 模型使用关系列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 模型使用关系列表信息字典对象
        """
        query = (
            select(SchemaModelUsage)
            .where(
                SchemaModelUsage.model_id == query_object.model_id if query_object.model_id else True,
                SchemaModelUsage.usage_type == query_object.usage_type if query_object.usage_type else True,
                SchemaModelUsage.usage_target_id == query_object.usage_target_id if query_object.usage_target_id else True,
                SchemaModelUsage.usage_target_name.like(f'%{query_object.usage_target_name}%') if query_object.usage_target_name else True,
                SchemaModelUsage.description == query_object.description if query_object.description else True,
                SchemaModelUsage.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModelUsage.del_flag == "0")
            .order_by(SchemaModelUsage.usage_id)
            #.distinct()
        )
        schema_model_usage_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return schema_model_usage_list

    @classmethod
    async def get_schema_model_usage_orm_list(cls, db: AsyncSession, query_object: Schema_model_usageQueryModel) -> List[Schema_model_usageQueryModel]:
        """
        根据查询参数获取JSON Schema 模型使用关系列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: JSON Schema 模型使用关系列表信息orm对象
        """
        query = (
            select(SchemaModelUsage)
            .where(
                SchemaModelUsage.model_id == query_object.model_id if query_object.model_id else True,
                SchemaModelUsage.usage_type == query_object.usage_type if query_object.usage_type else True,
                SchemaModelUsage.usage_target_id == query_object.usage_target_id if query_object.usage_target_id else True,
                SchemaModelUsage.usage_target_name.like(f'%{query_object.usage_target_name}%') if query_object.usage_target_name else True,
                SchemaModelUsage.description == query_object.description if query_object.description else True,
                SchemaModelUsage.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModelUsage.del_flag == "0")
            .order_by(SchemaModelUsage.usage_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Schema_model_usageQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_schema_model_usage_dao(cls, db: AsyncSession, schema_model_usage: Schema_model_usageModel):
        """
        新增JSON Schema 模型使用关系数据库操作

        :param db: orm对象
        :param schema_model_usage: JSON Schema 模型使用关系对象
        :return:
        """
        payload = schema_model_usage.model_dump(exclude_none=True, exclude={})
        payload = normalize_empty_values(
            payload,
            {
                'usage_id',
                'usage_target_name',
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
        db_schema_model_usage = SchemaModelUsage(**payload)
        db.add(db_schema_model_usage)
        await db.flush()

        return db_schema_model_usage

    @classmethod
    async def edit_schema_model_usage_dao(cls, db: AsyncSession, schema_model_usage: dict):
        """
        编辑JSON Schema 模型使用关系数据库操作

        :param db: orm对象
        :param schema_model_usage: 需要更新的JSON Schema 模型使用关系字典
        :return:
        """
        schema_model_usage = normalize_empty_values(
            schema_model_usage,
            {
                'usage_id',
                'usage_target_name',
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
        await db.execute(update(SchemaModelUsage), [schema_model_usage])

    @classmethod
    async def delete_schema_model_usage_dao(cls, db: AsyncSession, schema_model_usage: Schema_model_usageModel):
        """
        删除JSON Schema 模型使用关系数据库操作

        :param db: orm对象
        :param schema_model_usage: JSON Schema 模型使用关系对象
        :return:
        """
        #await db.execute(delete(SchemaModelUsage).where(SchemaModelUsage.usage_id.in_([schema_model_usage.usage_id])))
        await db.execute(update(SchemaModelUsage).where(SchemaModelUsage.usage_id.in_([schema_model_usage.usage_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Schema_model_usagePageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Schema_model_usageDao.get_schema_model_usage_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
