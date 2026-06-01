from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.module_demo.module_uuid_demo.entity.do.module_uuid_demo_do import ModuleUuidDemo
from module_admin.module_demo.module_uuid_demo.entity.vo.module_uuid_demo_vo import Module_uuid_demoModel, Module_uuid_demoPageQueryModel, Module_uuid_demoQueryModel
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


class Module_uuid_demoDao:
    """
    UUID主键业务示例模块数据库操作层
    """

    @classmethod
    async def get_module_uuid_demo_detail_by_id(cls, db: AsyncSession, id: str):
        """
        根据主键ID-uuid获取UUID主键业务示例详细信息

        :param db: orm对象
        :param id: 主键ID-uuid
        :return: UUID主键业务示例信息对象
        """
        module_uuid_demo_info = (
            (
                await db.execute(
                    select(ModuleUuidDemo)
                    .where(
                        ModuleUuidDemo.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return module_uuid_demo_info

    @classmethod
    async def get_module_uuid_demo_detail_by_info(cls, db: AsyncSession, module_uuid_demo: Module_uuid_demoModel):
        """
        根据UUID主键业务示例参数获取UUID主键业务示例信息

        :param db: orm对象
        :param module_uuid_demo: UUID主键业务示例参数对象
        :return: UUID主键业务示例信息对象
        """
        module_uuid_demo_info = (
            (
                await db.execute(
                    select(ModuleUuidDemo).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return module_uuid_demo_info

    @classmethod
    async def get_module_uuid_demo_list(cls, db: AsyncSession, query_object: Module_uuid_demoPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取UUID主键业务示例列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: UUID主键业务示例列表信息字典对象
        """
        query = (
            select(ModuleUuidDemo)
            .where(
                ModuleUuidDemo.title == query_object.title if query_object.title else True,
                ModuleUuidDemo.business_code == query_object.business_code if query_object.business_code else True,
                ModuleUuidDemo.customer_name.like(f'%{query_object.customer_name}%') if query_object.customer_name else True,
                ModuleUuidDemo.status == query_object.status if query_object.status else True,
                ModuleUuidDemo.priority == query_object.priority if query_object.priority else True,
                ModuleUuidDemo.amount == query_object.amount if query_object.amount else True,
                ModuleUuidDemo.enabled == query_object.enabled if query_object.enabled else True,
                ModuleUuidDemo.occurred_date == query_object.occurred_date if query_object.occurred_date else True,
                ModuleUuidDemo.closed_time == query_object.closed_time if query_object.closed_time else True,
                ModuleUuidDemo.extra_info == query_object.extra_info if query_object.extra_info else True,
                ModuleUuidDemo.description == query_object.description if query_object.description else True,
                ModuleUuidDemo.sort_no == query_object.sort_no if query_object.sort_no else True,
                ModuleUuidDemo.type == query_object.type if query_object.type else True,
            )
            .where(ModuleUuidDemo.del_flag == "0")
            .order_by(ModuleUuidDemo.id)
            #.distinct()
        )
        module_uuid_demo_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return module_uuid_demo_list

    @classmethod
    async def get_module_uuid_demo_orm_list(cls, db: AsyncSession, query_object: Module_uuid_demoQueryModel) -> List[Module_uuid_demoQueryModel]:
        """
        根据查询参数获取UUID主键业务示例列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: UUID主键业务示例列表信息orm对象
        """
        query = (
            select(ModuleUuidDemo)
            .where(
                ModuleUuidDemo.title == query_object.title if query_object.title else True,
                ModuleUuidDemo.business_code == query_object.business_code if query_object.business_code else True,
                ModuleUuidDemo.customer_name.like(f'%{query_object.customer_name}%') if query_object.customer_name else True,
                ModuleUuidDemo.status == query_object.status if query_object.status else True,
                ModuleUuidDemo.priority == query_object.priority if query_object.priority else True,
                ModuleUuidDemo.amount == query_object.amount if query_object.amount else True,
                ModuleUuidDemo.enabled == query_object.enabled if query_object.enabled else True,
                ModuleUuidDemo.occurred_date == query_object.occurred_date if query_object.occurred_date else True,
                ModuleUuidDemo.closed_time == query_object.closed_time if query_object.closed_time else True,
                ModuleUuidDemo.extra_info == query_object.extra_info if query_object.extra_info else True,
                ModuleUuidDemo.description == query_object.description if query_object.description else True,
                ModuleUuidDemo.sort_no == query_object.sort_no if query_object.sort_no else True,
                ModuleUuidDemo.type == query_object.type if query_object.type else True,
            )
            .where(ModuleUuidDemo.del_flag == "0")
            .order_by(ModuleUuidDemo.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Module_uuid_demoQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_module_uuid_demo_dao(cls, db: AsyncSession, module_uuid_demo: Module_uuid_demoModel):
        """
        新增UUID主键业务示例数据库操作

        :param db: orm对象
        :param module_uuid_demo: UUID主键业务示例对象
        :return:
        """
        payload = module_uuid_demo.model_dump(exclude_none=True, exclude={})
        payload = normalize_empty_values(
            payload,
            {
                'id',
                'business_code',
                'customer_name',
                'status',
                'priority',
                'amount',
                'enabled',
                'occurred_date',
                'closed_time',
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
        db_module_uuid_demo = ModuleUuidDemo(**payload)
        db.add(db_module_uuid_demo)
        await db.flush()

        return db_module_uuid_demo

    @classmethod
    async def edit_module_uuid_demo_dao(cls, db: AsyncSession, module_uuid_demo: dict):
        """
        编辑UUID主键业务示例数据库操作

        :param db: orm对象
        :param module_uuid_demo: 需要更新的UUID主键业务示例字典
        :return:
        """
        module_uuid_demo = normalize_empty_values(
            module_uuid_demo,
            {
                'id',
                'business_code',
                'customer_name',
                'status',
                'priority',
                'amount',
                'enabled',
                'occurred_date',
                'closed_time',
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
        await db.execute(update(ModuleUuidDemo), [module_uuid_demo])

    @classmethod
    async def delete_module_uuid_demo_dao(cls, db: AsyncSession, module_uuid_demo: Module_uuid_demoModel):
        """
        删除UUID主键业务示例数据库操作

        :param db: orm对象
        :param module_uuid_demo: UUID主键业务示例对象
        :return:
        """
        #await db.execute(delete(ModuleUuidDemo).where(ModuleUuidDemo.id.in_([module_uuid_demo.id])))
        await db.execute(update(ModuleUuidDemo).where(ModuleUuidDemo.id.in_([module_uuid_demo.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Module_uuid_demoPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Module_uuid_demoDao.get_module_uuid_demo_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
