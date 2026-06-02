from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_testing.schema_models.entity.do.schema_models_do import SchemaModel
from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel, Schema_modelsPageQueryModel, Schema_modelsQueryModel
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


class Schema_modelsDao:
    """
    JSON Schema 数据模型主模块数据库操作层
    """

    @classmethod
    async def get_schema_models_detail_by_id(cls, db: AsyncSession, model_id: str):
        """
        根据模型ID获取JSON Schema 数据模型主详细信息

        :param db: orm对象
        :param model_id: 模型ID
        :return: JSON Schema 数据模型主信息对象
        """
        schema_models_info = (
            (
                await db.execute(
                    select(SchemaModel)
                    .where(
                        SchemaModel.model_id == model_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_models_info

    @classmethod
    async def get_schema_models_detail_by_info(cls, db: AsyncSession, schema_models: Schema_modelsModel):
        """
        根据JSON Schema 数据模型主参数获取JSON Schema 数据模型主信息

        :param db: orm对象
        :param schema_models: JSON Schema 数据模型主参数对象
        :return: JSON Schema 数据模型主信息对象
        """
        schema_models_info = (
            (
                await db.execute(
                    select(SchemaModel).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_models_info

    @classmethod
    async def get_schema_models_list(cls, db: AsyncSession, query_object: Schema_modelsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取JSON Schema 数据模型主列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 数据模型主列表信息字典对象
        """
        query = (
            select(SchemaModel)
            .where(
                SchemaModel.project_id == query_object.project_id if query_object.project_id else True,
                SchemaModel.case_id == query_object.case_id if query_object.case_id else True,
                SchemaModel.group_id == query_object.group_id if query_object.group_id else True,
                SchemaModel.name.like(f'%{query_object.name}%') if query_object.name else True,
                SchemaModel.display_name.like(f'%{query_object.display_name}%') if query_object.display_name else True,
                SchemaModel.title == query_object.title if query_object.title else True,
                SchemaModel.schema_draft == query_object.schema_draft if query_object.schema_draft else True,
                SchemaModel.root_node_id == query_object.root_node_id if query_object.root_node_id else True,
                SchemaModel.model_category == query_object.model_category if query_object.model_category else True,
                SchemaModel.model_role == query_object.model_role if query_object.model_role else True,
                SchemaModel.parent_model_id == query_object.parent_model_id if query_object.parent_model_id else True,
                SchemaModel.source_model_name.like(f'%{query_object.source_model_name}%') if query_object.source_model_name else True,
                SchemaModel.code_class_name.like(f'%{query_object.code_class_name}%') if query_object.code_class_name else True,
                SchemaModel.code_file_name.like(f'%{query_object.code_file_name}%') if query_object.code_file_name else True,
                SchemaModel.source_table_name.like(f'%{query_object.source_table_name}%') if query_object.source_table_name else True,
                SchemaModel.visibility == query_object.visibility if query_object.visibility else True,
                SchemaModel.status == query_object.status if query_object.status else True,
                SchemaModel.version == query_object.version if query_object.version else True,
                SchemaModel.revision == query_object.revision if query_object.revision else True,
                SchemaModel.source_type == query_object.source_type if query_object.source_type else True,
                SchemaModel.source_id == query_object.source_id if query_object.source_id else True,
                SchemaModel.raw_schema == query_object.raw_schema if query_object.raw_schema else True,
                SchemaModel.raw_schema_extras == query_object.raw_schema_extras if query_object.raw_schema_extras else True,
                SchemaModel.generated_schema == query_object.generated_schema if query_object.generated_schema else True,
                SchemaModel.tags == query_object.tags if query_object.tags else True,
                SchemaModel.description == query_object.description if query_object.description else True,
                SchemaModel.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModel.del_flag == "0")
            .order_by(SchemaModel.model_id)
            #.distinct()
        )
        schema_models_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return schema_models_list

    @classmethod
    async def get_schema_models_orm_list(cls, db: AsyncSession, query_object: Schema_modelsQueryModel) -> List[Schema_modelsQueryModel]:
        """
        根据查询参数获取JSON Schema 数据模型主列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: JSON Schema 数据模型主列表信息orm对象
        """
        query = (
            select(SchemaModel)
            .where(
                SchemaModel.project_id == query_object.project_id if query_object.project_id else True,
                SchemaModel.case_id == query_object.case_id if query_object.case_id else True,
                SchemaModel.group_id == query_object.group_id if query_object.group_id else True,
                SchemaModel.name.like(f'%{query_object.name}%') if query_object.name else True,
                SchemaModel.display_name.like(f'%{query_object.display_name}%') if query_object.display_name else True,
                SchemaModel.title == query_object.title if query_object.title else True,
                SchemaModel.schema_draft == query_object.schema_draft if query_object.schema_draft else True,
                SchemaModel.root_node_id == query_object.root_node_id if query_object.root_node_id else True,
                SchemaModel.model_category == query_object.model_category if query_object.model_category else True,
                SchemaModel.model_role == query_object.model_role if query_object.model_role else True,
                SchemaModel.parent_model_id == query_object.parent_model_id if query_object.parent_model_id else True,
                SchemaModel.source_model_name.like(f'%{query_object.source_model_name}%') if query_object.source_model_name else True,
                SchemaModel.code_class_name.like(f'%{query_object.code_class_name}%') if query_object.code_class_name else True,
                SchemaModel.code_file_name.like(f'%{query_object.code_file_name}%') if query_object.code_file_name else True,
                SchemaModel.source_table_name.like(f'%{query_object.source_table_name}%') if query_object.source_table_name else True,
                SchemaModel.visibility == query_object.visibility if query_object.visibility else True,
                SchemaModel.status == query_object.status if query_object.status else True,
                SchemaModel.version == query_object.version if query_object.version else True,
                SchemaModel.revision == query_object.revision if query_object.revision else True,
                SchemaModel.source_type == query_object.source_type if query_object.source_type else True,
                SchemaModel.source_id == query_object.source_id if query_object.source_id else True,
                SchemaModel.raw_schema == query_object.raw_schema if query_object.raw_schema else True,
                SchemaModel.raw_schema_extras == query_object.raw_schema_extras if query_object.raw_schema_extras else True,
                SchemaModel.generated_schema == query_object.generated_schema if query_object.generated_schema else True,
                SchemaModel.tags == query_object.tags if query_object.tags else True,
                SchemaModel.description == query_object.description if query_object.description else True,
                SchemaModel.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(SchemaModel.del_flag == "0")
            .order_by(SchemaModel.model_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Schema_modelsQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_schema_models_dao(cls, db: AsyncSession, schema_models: Schema_modelsModel):
        """
        新增JSON Schema 数据模型主数据库操作

        :param db: orm对象
        :param schema_models: JSON Schema 数据模型主对象
        :return:
        """
        payload = schema_models.model_dump(exclude_none=True, exclude={})
        payload = normalize_empty_values(
            payload,
            {
                'model_id',
                'case_id',
                'group_id',
                'name',
                'display_name',
                'title',
                'schema_draft',
                'root_node_id',
                'model_category',
                'model_role',
                'parent_model_id',
                'source_model_name',
                'code_class_name',
                'code_file_name',
                'source_table_name',
                'revision',
                'source_id',
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
        db_schema_models = SchemaModel(**payload)
        db.add(db_schema_models)
        await db.flush()

        return db_schema_models

    @classmethod
    async def edit_schema_models_dao(cls, db: AsyncSession, schema_models: dict):
        """
        编辑JSON Schema 数据模型主数据库操作

        :param db: orm对象
        :param schema_models: 需要更新的JSON Schema 数据模型主字典
        :return:
        """
        schema_models = normalize_empty_values(
            schema_models,
            {
                'model_id',
                'case_id',
                'group_id',
                'name',
                'display_name',
                'title',
                'schema_draft',
                'root_node_id',
                'model_category',
                'model_role',
                'parent_model_id',
                'source_model_name',
                'code_class_name',
                'code_file_name',
                'source_table_name',
                'revision',
                'source_id',
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
        await db.execute(update(SchemaModel), [schema_models])

    @classmethod
    async def delete_schema_models_dao(cls, db: AsyncSession, schema_models: Schema_modelsModel):
        """
        删除JSON Schema 数据模型主数据库操作

        :param db: orm对象
        :param schema_models: JSON Schema 数据模型主对象
        :return:
        """
        #await db.execute(delete(SchemaModel).where(SchemaModel.model_id.in_([schema_models.model_id])))
        await db.execute(update(SchemaModel).where(SchemaModel.model_id.in_([schema_models.model_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Schema_modelsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Schema_modelsDao.get_schema_models_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
