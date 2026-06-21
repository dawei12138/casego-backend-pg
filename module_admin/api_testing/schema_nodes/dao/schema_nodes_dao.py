from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_testing.schema_nodes.entity.do.schema_nodes_do import SchemaNode
from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel, Schema_nodesPageQueryModel, Schema_nodesQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time

def is_empty_generated_value(value):
    return value == '' or (isinstance(value, (list, dict)) and len(value) == 0)


def normalize_empty_values(data, field_names):
    normalized = data.copy()
    for field_name in field_names:
        if field_name in normalized and is_empty_generated_value(normalized.get(field_name)):
            normalized[field_name] = None
    return normalized


class Schema_nodesDao:
    """
    JSON Schema 可视化节点模块数据库操作层
    """

    @classmethod
    async def get_schema_nodes_detail_by_id(cls, db: AsyncSession, node_id: str):
        """
        根据节点ID获取JSON Schema 可视化节点详细信息

        :param db: orm对象
        :param node_id: 节点ID
        :return: JSON Schema 可视化节点信息对象
        """
        schema_nodes_info = (
            (
                await db.execute(
                    select(SchemaNode)
                    .where(
                        SchemaNode.node_id == node_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_nodes_info

    @classmethod
    async def get_schema_nodes_detail_by_info(cls, db: AsyncSession, schema_nodes: Schema_nodesModel):
        """
        根据JSON Schema 可视化节点参数获取JSON Schema 可视化节点信息

        :param db: orm对象
        :param schema_nodes: JSON Schema 可视化节点参数对象
        :return: JSON Schema 可视化节点信息对象
        """
        schema_nodes_info = (
            (
                await db.execute(
                    select(SchemaNode).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return schema_nodes_info

    @classmethod
    async def get_schema_nodes_list(cls, db: AsyncSession, query_object: Schema_nodesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取JSON Schema 可视化节点列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 可视化节点列表信息字典对象
        """
        query = (
            select(SchemaNode)
            .where(
                SchemaNode.model_id == query_object.model_id if query_object.model_id else True,
                SchemaNode.parent_id == query_object.parent_id if query_object.parent_id else True,
                SchemaNode.root_id == query_object.root_id if query_object.root_id else True,
                SchemaNode.node_kind == query_object.node_kind if query_object.node_kind else True,
                SchemaNode.field_name.like(f'%{query_object.field_name}%') if query_object.field_name else True,
                SchemaNode.display_name.like(f'%{query_object.display_name}%') if query_object.display_name else True,
                SchemaNode.alias == query_object.alias if query_object.alias else True,
                SchemaNode.source_field_name.like(f'%{query_object.source_field_name}%') if query_object.source_field_name else True,
                SchemaNode.source_field_type == query_object.source_field_type if query_object.source_field_type else True,
                SchemaNode.source_field_comment == query_object.source_field_comment if query_object.source_field_comment else True,
                SchemaNode.code_field_name.like(f'%{query_object.code_field_name}%') if query_object.code_field_name else True,
                SchemaNode.title == query_object.title if query_object.title else True,
                SchemaNode.type == query_object.type if query_object.type else True,
                SchemaNode.type_list == query_object.type_list if query_object.type_list else True,
                SchemaNode.nullable == query_object.nullable if query_object.nullable else True,
                SchemaNode.required == query_object.required if query_object.required else True,
                SchemaNode.deprecated == query_object.deprecated if query_object.deprecated else True,
                SchemaNode.access_mode == query_object.access_mode if query_object.access_mode else True,
                SchemaNode.format == query_object.format if query_object.format else True,
                SchemaNode.default_value == query_object.default_value if query_object.default_value else True,
                SchemaNode.example_value == query_object.example_value if query_object.example_value else True,
                SchemaNode.examples == query_object.examples if query_object.examples else True,
                SchemaNode.enum_enabled == query_object.enum_enabled if query_object.enum_enabled else True,
                SchemaNode.enum_values == query_object.enum_values if query_object.enum_values else True,
                SchemaNode.enum_meta == query_object.enum_meta if query_object.enum_meta else True,
                SchemaNode.const_enabled == query_object.const_enabled if query_object.const_enabled else True,
                SchemaNode.const_value == query_object.const_value if query_object.const_value else True,
                SchemaNode.mock_enabled == query_object.mock_enabled if query_object.mock_enabled else True,
                SchemaNode.mock_type == query_object.mock_type if query_object.mock_type else True,
                SchemaNode.mock_rule == query_object.mock_rule if query_object.mock_rule else True,
                SchemaNode.mock_value == query_object.mock_value if query_object.mock_value else True,
                SchemaNode.mock_config == query_object.mock_config if query_object.mock_config else True,
                SchemaNode.constraints == query_object.constraints if query_object.constraints else True,
                SchemaNode.composition == query_object.composition if query_object.composition else True,
                SchemaNode.ref_config == query_object.ref_config if query_object.ref_config else True,
                SchemaNode.xml_config == query_object.xml_config if query_object.xml_config else True,
                SchemaNode.source == query_object.source if query_object.source else True,
                SchemaNode.source_path == query_object.source_path if query_object.source_path else True,
                SchemaNode.import_hint == query_object.import_hint if query_object.import_hint else True,
                SchemaNode.raw_schema == query_object.raw_schema if query_object.raw_schema else True,
                SchemaNode.raw_schema_extras == query_object.raw_schema_extras if query_object.raw_schema_extras else True,
                SchemaNode.ui_state == query_object.ui_state if query_object.ui_state else True,
                SchemaNode.path == query_object.path if query_object.path else True,
                SchemaNode.json_pointer == query_object.json_pointer if query_object.json_pointer else True,
                SchemaNode.level == query_object.level if query_object.level else True,
                SchemaNode.expanded == query_object.expanded if query_object.expanded else True,
                SchemaNode.locked == query_object.locked if query_object.locked else True,
                SchemaNode.sort_no == query_object.sort_no if query_object.sort_no else True,
                SchemaNode.description == query_object.description if query_object.description else True,
            )
            .where(SchemaNode.del_flag == "0")
            .order_by(SchemaNode.node_id)
            #.distinct()
        )
        schema_nodes_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return schema_nodes_list

    @classmethod
    async def get_schema_nodes_orm_list(cls, db: AsyncSession, query_object: Schema_nodesQueryModel) -> List[Schema_nodesQueryModel]:
        """
        根据查询参数获取JSON Schema 可视化节点列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: JSON Schema 可视化节点列表信息orm对象
        """
        query = (
            select(SchemaNode)
            .where(
                SchemaNode.model_id == query_object.model_id if query_object.model_id else True,
                SchemaNode.parent_id == query_object.parent_id if query_object.parent_id else True,
                SchemaNode.root_id == query_object.root_id if query_object.root_id else True,
                SchemaNode.node_kind == query_object.node_kind if query_object.node_kind else True,
                SchemaNode.field_name.like(f'%{query_object.field_name}%') if query_object.field_name else True,
                SchemaNode.display_name.like(f'%{query_object.display_name}%') if query_object.display_name else True,
                SchemaNode.alias == query_object.alias if query_object.alias else True,
                SchemaNode.source_field_name.like(f'%{query_object.source_field_name}%') if query_object.source_field_name else True,
                SchemaNode.source_field_type == query_object.source_field_type if query_object.source_field_type else True,
                SchemaNode.source_field_comment == query_object.source_field_comment if query_object.source_field_comment else True,
                SchemaNode.code_field_name.like(f'%{query_object.code_field_name}%') if query_object.code_field_name else True,
                SchemaNode.title == query_object.title if query_object.title else True,
                SchemaNode.type == query_object.type if query_object.type else True,
                SchemaNode.type_list == query_object.type_list if query_object.type_list else True,
                SchemaNode.nullable == query_object.nullable if query_object.nullable else True,
                SchemaNode.required == query_object.required if query_object.required else True,
                SchemaNode.deprecated == query_object.deprecated if query_object.deprecated else True,
                SchemaNode.access_mode == query_object.access_mode if query_object.access_mode else True,
                SchemaNode.format == query_object.format if query_object.format else True,
                SchemaNode.default_value == query_object.default_value if query_object.default_value else True,
                SchemaNode.example_value == query_object.example_value if query_object.example_value else True,
                SchemaNode.examples == query_object.examples if query_object.examples else True,
                SchemaNode.enum_enabled == query_object.enum_enabled if query_object.enum_enabled else True,
                SchemaNode.enum_values == query_object.enum_values if query_object.enum_values else True,
                SchemaNode.enum_meta == query_object.enum_meta if query_object.enum_meta else True,
                SchemaNode.const_enabled == query_object.const_enabled if query_object.const_enabled else True,
                SchemaNode.const_value == query_object.const_value if query_object.const_value else True,
                SchemaNode.mock_enabled == query_object.mock_enabled if query_object.mock_enabled else True,
                SchemaNode.mock_type == query_object.mock_type if query_object.mock_type else True,
                SchemaNode.mock_rule == query_object.mock_rule if query_object.mock_rule else True,
                SchemaNode.mock_value == query_object.mock_value if query_object.mock_value else True,
                SchemaNode.mock_config == query_object.mock_config if query_object.mock_config else True,
                SchemaNode.constraints == query_object.constraints if query_object.constraints else True,
                SchemaNode.composition == query_object.composition if query_object.composition else True,
                SchemaNode.ref_config == query_object.ref_config if query_object.ref_config else True,
                SchemaNode.xml_config == query_object.xml_config if query_object.xml_config else True,
                SchemaNode.source == query_object.source if query_object.source else True,
                SchemaNode.source_path == query_object.source_path if query_object.source_path else True,
                SchemaNode.import_hint == query_object.import_hint if query_object.import_hint else True,
                SchemaNode.raw_schema == query_object.raw_schema if query_object.raw_schema else True,
                SchemaNode.raw_schema_extras == query_object.raw_schema_extras if query_object.raw_schema_extras else True,
                SchemaNode.ui_state == query_object.ui_state if query_object.ui_state else True,
                SchemaNode.path == query_object.path if query_object.path else True,
                SchemaNode.json_pointer == query_object.json_pointer if query_object.json_pointer else True,
                SchemaNode.level == query_object.level if query_object.level else True,
                SchemaNode.expanded == query_object.expanded if query_object.expanded else True,
                SchemaNode.locked == query_object.locked if query_object.locked else True,
                SchemaNode.sort_no == query_object.sort_no if query_object.sort_no else True,
                SchemaNode.description == query_object.description if query_object.description else True,
            )
            .where(SchemaNode.del_flag == "0")
            .order_by(SchemaNode.node_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Schema_nodesQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_schema_nodes_dao(cls, db: AsyncSession, schema_nodes: Schema_nodesModel):
        """
        新增JSON Schema 可视化节点数据库操作

        :param db: orm对象
        :param schema_nodes: JSON Schema 可视化节点对象
        :return:
        """
        payload = schema_nodes.model_dump(exclude_none=True, exclude={})
        payload = normalize_empty_values(
            payload,
            {
                'node_id',
                'parent_id',
                'root_id',
                'field_name',
                'display_name',
                'alias',
                'source_field_name',
                'source_field_type',
                'source_field_comment',
                'code_field_name',
                'title',
                'format',
                'mock_type',
                'mock_rule',
                'source',
                'source_path',
                'path',
                'json_pointer',
                'expanded',
                'locked',
                'create_by',
                'create_time',
                'update_by',
                'update_time',
                'remark',
                'description',
                'del_flag',
            },
        )
        db_schema_nodes = SchemaNode(**payload)
        db.add(db_schema_nodes)
        await db.flush()

        return db_schema_nodes

    @classmethod
    async def edit_schema_nodes_dao(cls, db: AsyncSession, schema_nodes: dict):
        """
        编辑JSON Schema 可视化节点数据库操作

        :param db: orm对象
        :param schema_nodes: 需要更新的JSON Schema 可视化节点字典
        :return:
        """
        schema_nodes = normalize_empty_values(
            schema_nodes,
            {
                'node_id',
                'parent_id',
                'root_id',
                'field_name',
                'display_name',
                'alias',
                'source_field_name',
                'source_field_type',
                'source_field_comment',
                'code_field_name',
                'title',
                'format',
                'mock_type',
                'mock_rule',
                'source',
                'source_path',
                'path',
                'json_pointer',
                'expanded',
                'locked',
                'create_by',
                'create_time',
                'update_by',
                'update_time',
                'remark',
                'description',
                'del_flag',
            },
        )
        await db.execute(update(SchemaNode), [schema_nodes])

    @classmethod
    async def delete_schema_nodes_dao(cls, db: AsyncSession, schema_nodes: Schema_nodesModel):
        """
        删除JSON Schema 可视化节点数据库操作

        :param db: orm对象
        :param schema_nodes: JSON Schema 可视化节点对象
        :return:
        """
        #await db.execute(delete(SchemaNode).where(SchemaNode.node_id.in_([schema_nodes.node_id])))
        await db.execute(update(SchemaNode).where(SchemaNode.node_id.in_([schema_nodes.node_id])).values(del_flag="1"))

    @classmethod
    async def delete_schema_nodes_by_model_id_dao(cls, db: AsyncSession, model_id: str):
        """
        根据模型ID软删除JSON Schema 可视化节点。

        :param db: orm对象
        :param model_id: 模型ID
        :return:
        """
        await db.execute(update(SchemaNode).where(SchemaNode.model_id == model_id).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio
    from config.get_db import get_db


    async def main():

        async for db in get_db():
            try:
                query = Schema_nodesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Schema_nodesDao.get_schema_nodes_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
