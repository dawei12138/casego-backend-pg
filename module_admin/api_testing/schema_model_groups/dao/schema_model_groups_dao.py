from sqlalchemy import or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from module_admin.api_testing.schema_model_groups.entity.do.schema_model_groups_do import SchemaModelGroup
from module_admin.api_testing.schema_model_groups.entity.vo.schema_model_groups_vo import (
    Schema_model_groupsModel,
    Schema_model_groupsPageQueryModel,
    Schema_model_groupsQueryModel,
)
from utils.page_util import PageUtil


def is_empty_generated_value(value):
    return value == '' or (isinstance(value, (list, dict)) and len(value) == 0)


def normalize_empty_values(data, field_names):
    normalized = data.copy()
    for field_name in field_names:
        if field_name in normalized and is_empty_generated_value(normalized.get(field_name)):
            normalized[field_name] = None
    return normalized


def build_group_keyword_filter(query_object):
    if not query_object.name:
        return True
    keyword = f'%{query_object.name}%'
    return or_(SchemaModelGroup.name.like(keyword), SchemaModelGroup.description.like(keyword))


class Schema_model_groupsDao:
    """
    JSON Schema 数据模型目录模块数据库操作层
    """

    @classmethod
    async def get_schema_model_groups_detail_by_id(cls, db: AsyncSession, group_id: str):
        group_info = (
            (
                await db.execute(
                    select(SchemaModelGroup).where(
                        SchemaModelGroup.group_id == group_id,
                        SchemaModelGroup.del_flag == '0',
                    )
                )
            )
            .scalars()
            .first()
        )

        return group_info

    @classmethod
    async def get_schema_model_groups_list(
        cls,
        db: AsyncSession,
        query_object: Schema_model_groupsPageQueryModel,
        is_page: bool = False,
    ):
        query = (
            select(SchemaModelGroup)
            .where(
                SchemaModelGroup.project_id == query_object.project_id if query_object.project_id else True,
                SchemaModelGroup.branch_id == query_object.branch_id if query_object.branch_id else True,
                SchemaModelGroup.parent_id == query_object.parent_id if query_object.parent_id else True,
                build_group_keyword_filter(query_object),
                SchemaModelGroup.del_flag == '0',
            )
            .order_by(SchemaModelGroup.sort_no, SchemaModelGroup.group_id)
        )
        return await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

    @classmethod
    async def get_schema_model_groups_orm_list(
        cls,
        db: AsyncSession,
        query_object: Schema_model_groupsQueryModel,
    ) -> List[Schema_model_groupsQueryModel]:
        query = (
            select(SchemaModelGroup)
            .where(
                SchemaModelGroup.project_id == query_object.project_id if query_object.project_id else True,
                SchemaModelGroup.branch_id == query_object.branch_id if query_object.branch_id else True,
                SchemaModelGroup.parent_id == query_object.parent_id if query_object.parent_id else True,
                build_group_keyword_filter(query_object),
                SchemaModelGroup.del_flag == '0',
            )
            .order_by(SchemaModelGroup.sort_no, SchemaModelGroup.group_id)
        )
        result = await db.execute(query)
        return [Schema_model_groupsQueryModel.model_validate(item) for item in result.scalars().all()]

    @classmethod
    async def add_schema_model_groups_dao(cls, db: AsyncSession, group: Schema_model_groupsModel):
        payload = group.model_dump(exclude_none=True)
        payload = normalize_empty_values(
            payload,
            {
                'group_id',
                'branch_id',
                'parent_id',
                'name',
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
        db_group = SchemaModelGroup(**payload)
        db.add(db_group)
        await db.flush()
        return db_group

    @classmethod
    async def edit_schema_model_groups_dao(cls, db: AsyncSession, group: dict):
        group = normalize_empty_values(
            group,
            {
                'group_id',
                'branch_id',
                'parent_id',
                'name',
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
        await db.execute(update(SchemaModelGroup), [group])

    @classmethod
    async def delete_schema_model_groups_dao(cls, db: AsyncSession, group: Schema_model_groupsModel):
        await db.execute(update(SchemaModelGroup).where(SchemaModelGroup.group_id == group.group_id).values(del_flag='1'))
