from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception import ServiceException
from module_admin.api_testing.schema_model_groups.dao.schema_model_groups_dao import Schema_model_groupsDao
from module_admin.api_testing.schema_model_groups.entity.vo.schema_model_groups_vo import (
    DeleteSchema_model_groupsModel,
    Schema_model_groupsModel,
    Schema_model_groupsPageQueryModel,
)
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from utils.common_util import CamelCaseUtil


class Schema_model_groupsService:
    """
    JSON Schema 数据模型目录模块服务层
    """

    @classmethod
    async def get_schema_model_groups_list_services(
        cls,
        query_db: AsyncSession,
        query_object: Schema_model_groupsPageQueryModel,
        is_page: bool = False,
    ):
        return await Schema_model_groupsDao.get_schema_model_groups_list(query_db, query_object, is_page)

    @classmethod
    async def add_schema_model_groups_services(cls, query_db: AsyncSession, page_object: Schema_model_groupsModel):
        page_object = Schema_model_groupsModel.model_validate(page_object.model_dump())
        page_object.group_id = page_object.group_id or cls._new_group_id()
        page_object.del_flag = page_object.del_flag or '0'
        page_object.sort_no = page_object.sort_no if page_object.sort_no is not None else 0
        page_object.validate_fields()
        try:
            await Schema_model_groupsDao.add_schema_model_groups_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(
                is_success=True,
                message='新增成功',
                result=page_object.model_dump(by_alias=True),
            )
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_schema_model_groups_services(cls, query_db: AsyncSession, page_object: Schema_model_groupsModel):
        page_object = Schema_model_groupsModel.model_validate(page_object.model_dump())
        page_object.validate_fields()
        group_info = await cls.schema_model_groups_detail_services(query_db, page_object.group_id)
        if not group_info.group_id:
            raise ServiceException(message='JSON Schema 数据模型目录不存在')

        edit_group = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        try:
            await Schema_model_groupsDao.edit_schema_model_groups_dao(query_db, edit_group)
            await query_db.commit()
            result_payload = group_info.model_dump()
            result_payload.update(edit_group)
            return CrudResponseModel(
                is_success=True,
                message='更新成功',
                result=Schema_model_groupsModel.model_validate(result_payload).model_dump(by_alias=True),
            )
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_schema_model_groups_services(
        cls,
        query_db: AsyncSession,
        page_object: DeleteSchema_model_groupsModel,
    ):
        if not page_object.group_ids:
            raise ServiceException(message='传入目录ID为空')
        try:
            for group_id in page_object.group_ids.split(','):
                group_id_obj = Schema_model_groupsModel.model_validate({'group_id': group_id}).group_id
                await Schema_model_groupsDao.delete_schema_model_groups_dao(
                    query_db,
                    Schema_model_groupsModel(groupId=group_id_obj),
                )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def schema_model_groups_detail_services(cls, query_db: AsyncSession, group_id: str):
        group_info = await Schema_model_groupsDao.get_schema_model_groups_detail_by_id(query_db, group_id=group_id)
        if isinstance(group_info, Schema_model_groupsModel):
            return group_info
        if group_info:
            return Schema_model_groupsModel(**CamelCaseUtil.transform_result(group_info))
        return Schema_model_groupsModel(**dict())

    @staticmethod
    def _new_group_id() -> str:
        return f'group_{uuid4().hex[:12]}'
