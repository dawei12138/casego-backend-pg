from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.module_demo.entity.do.module_demo_do import ModuleDemoAllTypes
from module_admin.module_demo.entity.vo.module_demo_vo import Module_demoModel, Module_demoPageQueryModel, Module_demoQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Module_demoDao:
    """
    Demo全类型测试模块数据库操作层
    """

    @classmethod
    async def get_module_demo_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID-bigint获取Demo全类型测试详细信息

        :param db: orm对象
        :param id: 主键ID-bigint
        :return: Demo全类型测试信息对象
        """
        module_demo_info = (
            (
                await db.execute(
                    select(ModuleDemoAllTypes)
                    .where(
                        ModuleDemoAllTypes.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return module_demo_info

    @classmethod
    async def get_module_demo_detail_by_info(cls, db: AsyncSession, module_demo: Module_demoModel):
        """
        根据Demo全类型测试参数获取Demo全类型测试信息

        :param db: orm对象
        :param module_demo: Demo全类型测试参数对象
        :return: Demo全类型测试信息对象
        """
        module_demo_info = (
            (
                await db.execute(
                    select(ModuleDemoAllTypes).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return module_demo_info

    @classmethod
    async def get_module_demo_list(cls, db: AsyncSession, query_object: Module_demoPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取Demo全类型测试列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: Demo全类型测试列表信息字典对象
        """
        query = (
            select(ModuleDemoAllTypes)
            .where(
                ModuleDemoAllTypes.string_value == query_object.string_value if query_object.string_value else True,
                ModuleDemoAllTypes.fixed_char_value == query_object.fixed_char_value if query_object.fixed_char_value else True,
                ModuleDemoAllTypes.unicode_value == query_object.unicode_value if query_object.unicode_value else True,
                ModuleDemoAllTypes.text_value == query_object.text_value if query_object.text_value else True,
                ModuleDemoAllTypes.unicode_text_value == query_object.unicode_text_value if query_object.unicode_text_value else True,
                ModuleDemoAllTypes.small_integer_value == query_object.small_integer_value if query_object.small_integer_value else True,
                ModuleDemoAllTypes.integer_value == query_object.integer_value if query_object.integer_value else True,
                ModuleDemoAllTypes.big_integer_value == query_object.big_integer_value if query_object.big_integer_value else True,
                ModuleDemoAllTypes.numeric_value == query_object.numeric_value if query_object.numeric_value else True,
                ModuleDemoAllTypes.decimal_value == query_object.decimal_value if query_object.decimal_value else True,
                ModuleDemoAllTypes.money_value == query_object.money_value if query_object.money_value else True,
                ModuleDemoAllTypes.float_value == query_object.float_value if query_object.float_value else True,
                ModuleDemoAllTypes.real_value == query_object.real_value if query_object.real_value else True,
                ModuleDemoAllTypes.double_value == query_object.double_value if query_object.double_value else True,
                ModuleDemoAllTypes.boolean_value == query_object.boolean_value if query_object.boolean_value else True,
                ModuleDemoAllTypes.date_value == query_object.date_value if query_object.date_value else True,
                ModuleDemoAllTypes.time_value == query_object.time_value if query_object.time_value else True,
                ModuleDemoAllTypes.time_tz_value == query_object.time_tz_value if query_object.time_tz_value else True,
                ModuleDemoAllTypes.datetime_value == query_object.datetime_value if query_object.datetime_value else True,
                ModuleDemoAllTypes.datetime_tz_value == query_object.datetime_tz_value if query_object.datetime_tz_value else True,
                ModuleDemoAllTypes.interval_value == query_object.interval_value if query_object.interval_value else True,
                ModuleDemoAllTypes.json_value == query_object.json_value if query_object.json_value else True,
                ModuleDemoAllTypes.jsonb_object_value == query_object.jsonb_object_value if query_object.jsonb_object_value else True,
                ModuleDemoAllTypes.jsonb_array_value == query_object.jsonb_array_value if query_object.jsonb_array_value else True,
                ModuleDemoAllTypes.jsonpath_value == query_object.jsonpath_value if query_object.jsonpath_value else True,
                ModuleDemoAllTypes.binary_value == query_object.binary_value if query_object.binary_value else True,
                ModuleDemoAllTypes.enum_value == query_object.enum_value if query_object.enum_value else True,
                ModuleDemoAllTypes.uuid_value == query_object.uuid_value if query_object.uuid_value else True,
                ModuleDemoAllTypes.string_array_value == query_object.string_array_value if query_object.string_array_value else True,
                ModuleDemoAllTypes.integer_array_value == query_object.integer_array_value if query_object.integer_array_value else True,
                ModuleDemoAllTypes.jsonb_array_items_value == query_object.jsonb_array_items_value if query_object.jsonb_array_items_value else True,
                ModuleDemoAllTypes.inet_value == query_object.inet_value if query_object.inet_value else True,
                ModuleDemoAllTypes.cidr_value == query_object.cidr_value if query_object.cidr_value else True,
                ModuleDemoAllTypes.macaddr_value == query_object.macaddr_value if query_object.macaddr_value else True,
                ModuleDemoAllTypes.macaddr8_value == query_object.macaddr8_value if query_object.macaddr8_value else True,
                ModuleDemoAllTypes.bit_value == query_object.bit_value if query_object.bit_value else True,
                ModuleDemoAllTypes.bit_varying_value == query_object.bit_varying_value if query_object.bit_varying_value else True,
                ModuleDemoAllTypes.tsvector_value == query_object.tsvector_value if query_object.tsvector_value else True,
                ModuleDemoAllTypes.tsquery_value == query_object.tsquery_value if query_object.tsquery_value else True,
                ModuleDemoAllTypes.int4_range_value == query_object.int4_range_value if query_object.int4_range_value else True,
                ModuleDemoAllTypes.int8_range_value == query_object.int8_range_value if query_object.int8_range_value else True,
                ModuleDemoAllTypes.numeric_range_value == query_object.numeric_range_value if query_object.numeric_range_value else True,
                ModuleDemoAllTypes.date_range_value == query_object.date_range_value if query_object.date_range_value else True,
                ModuleDemoAllTypes.timestamp_range_value == query_object.timestamp_range_value if query_object.timestamp_range_value else True,
                ModuleDemoAllTypes.timestamp_tz_range_value == query_object.timestamp_tz_range_value if query_object.timestamp_tz_range_value else True,
                ModuleDemoAllTypes.int4_multirange_value == query_object.int4_multirange_value if query_object.int4_multirange_value else True,
                ModuleDemoAllTypes.int8_multirange_value == query_object.int8_multirange_value if query_object.int8_multirange_value else True,
                ModuleDemoAllTypes.numeric_multirange_value == query_object.numeric_multirange_value if query_object.numeric_multirange_value else True,
                ModuleDemoAllTypes.date_multirange_value == query_object.date_multirange_value if query_object.date_multirange_value else True,
                ModuleDemoAllTypes.timestamp_multirange_value == query_object.timestamp_multirange_value if query_object.timestamp_multirange_value else True,
                ModuleDemoAllTypes.timestamp_tz_multirange_value == query_object.timestamp_tz_multirange_value if query_object.timestamp_tz_multirange_value else True,
                ModuleDemoAllTypes.oid_value == query_object.oid_value if query_object.oid_value else True,
                ModuleDemoAllTypes.regclass_value == query_object.regclass_value if query_object.regclass_value else True,
                ModuleDemoAllTypes.regconfig_value == query_object.regconfig_value if query_object.regconfig_value else True,
                ModuleDemoAllTypes.description == query_object.description if query_object.description else True,
                ModuleDemoAllTypes.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ModuleDemoAllTypes.del_flag == "0")
            .order_by(ModuleDemoAllTypes.id)
            #.distinct()
        )
        module_demo_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return module_demo_list

    @classmethod
    async def get_module_demo_orm_list(cls, db: AsyncSession, query_object: Module_demoQueryModel) -> List[Module_demoQueryModel]:
        """
        根据查询参数获取Demo全类型测试列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: Demo全类型测试列表信息orm对象
        """
        query = (
            select(ModuleDemoAllTypes)
            .where(
                ModuleDemoAllTypes.string_value == query_object.string_value if query_object.string_value else True,
                ModuleDemoAllTypes.fixed_char_value == query_object.fixed_char_value if query_object.fixed_char_value else True,
                ModuleDemoAllTypes.unicode_value == query_object.unicode_value if query_object.unicode_value else True,
                ModuleDemoAllTypes.text_value == query_object.text_value if query_object.text_value else True,
                ModuleDemoAllTypes.unicode_text_value == query_object.unicode_text_value if query_object.unicode_text_value else True,
                ModuleDemoAllTypes.small_integer_value == query_object.small_integer_value if query_object.small_integer_value else True,
                ModuleDemoAllTypes.integer_value == query_object.integer_value if query_object.integer_value else True,
                ModuleDemoAllTypes.big_integer_value == query_object.big_integer_value if query_object.big_integer_value else True,
                ModuleDemoAllTypes.numeric_value == query_object.numeric_value if query_object.numeric_value else True,
                ModuleDemoAllTypes.decimal_value == query_object.decimal_value if query_object.decimal_value else True,
                ModuleDemoAllTypes.money_value == query_object.money_value if query_object.money_value else True,
                ModuleDemoAllTypes.float_value == query_object.float_value if query_object.float_value else True,
                ModuleDemoAllTypes.real_value == query_object.real_value if query_object.real_value else True,
                ModuleDemoAllTypes.double_value == query_object.double_value if query_object.double_value else True,
                ModuleDemoAllTypes.boolean_value == query_object.boolean_value if query_object.boolean_value else True,
                ModuleDemoAllTypes.date_value == query_object.date_value if query_object.date_value else True,
                ModuleDemoAllTypes.time_value == query_object.time_value if query_object.time_value else True,
                ModuleDemoAllTypes.time_tz_value == query_object.time_tz_value if query_object.time_tz_value else True,
                ModuleDemoAllTypes.datetime_value == query_object.datetime_value if query_object.datetime_value else True,
                ModuleDemoAllTypes.datetime_tz_value == query_object.datetime_tz_value if query_object.datetime_tz_value else True,
                ModuleDemoAllTypes.interval_value == query_object.interval_value if query_object.interval_value else True,
                ModuleDemoAllTypes.json_value == query_object.json_value if query_object.json_value else True,
                ModuleDemoAllTypes.jsonb_object_value == query_object.jsonb_object_value if query_object.jsonb_object_value else True,
                ModuleDemoAllTypes.jsonb_array_value == query_object.jsonb_array_value if query_object.jsonb_array_value else True,
                ModuleDemoAllTypes.jsonpath_value == query_object.jsonpath_value if query_object.jsonpath_value else True,
                ModuleDemoAllTypes.binary_value == query_object.binary_value if query_object.binary_value else True,
                ModuleDemoAllTypes.enum_value == query_object.enum_value if query_object.enum_value else True,
                ModuleDemoAllTypes.uuid_value == query_object.uuid_value if query_object.uuid_value else True,
                ModuleDemoAllTypes.string_array_value == query_object.string_array_value if query_object.string_array_value else True,
                ModuleDemoAllTypes.integer_array_value == query_object.integer_array_value if query_object.integer_array_value else True,
                ModuleDemoAllTypes.jsonb_array_items_value == query_object.jsonb_array_items_value if query_object.jsonb_array_items_value else True,
                ModuleDemoAllTypes.inet_value == query_object.inet_value if query_object.inet_value else True,
                ModuleDemoAllTypes.cidr_value == query_object.cidr_value if query_object.cidr_value else True,
                ModuleDemoAllTypes.macaddr_value == query_object.macaddr_value if query_object.macaddr_value else True,
                ModuleDemoAllTypes.macaddr8_value == query_object.macaddr8_value if query_object.macaddr8_value else True,
                ModuleDemoAllTypes.bit_value == query_object.bit_value if query_object.bit_value else True,
                ModuleDemoAllTypes.bit_varying_value == query_object.bit_varying_value if query_object.bit_varying_value else True,
                ModuleDemoAllTypes.tsvector_value == query_object.tsvector_value if query_object.tsvector_value else True,
                ModuleDemoAllTypes.tsquery_value == query_object.tsquery_value if query_object.tsquery_value else True,
                ModuleDemoAllTypes.int4_range_value == query_object.int4_range_value if query_object.int4_range_value else True,
                ModuleDemoAllTypes.int8_range_value == query_object.int8_range_value if query_object.int8_range_value else True,
                ModuleDemoAllTypes.numeric_range_value == query_object.numeric_range_value if query_object.numeric_range_value else True,
                ModuleDemoAllTypes.date_range_value == query_object.date_range_value if query_object.date_range_value else True,
                ModuleDemoAllTypes.timestamp_range_value == query_object.timestamp_range_value if query_object.timestamp_range_value else True,
                ModuleDemoAllTypes.timestamp_tz_range_value == query_object.timestamp_tz_range_value if query_object.timestamp_tz_range_value else True,
                ModuleDemoAllTypes.int4_multirange_value == query_object.int4_multirange_value if query_object.int4_multirange_value else True,
                ModuleDemoAllTypes.int8_multirange_value == query_object.int8_multirange_value if query_object.int8_multirange_value else True,
                ModuleDemoAllTypes.numeric_multirange_value == query_object.numeric_multirange_value if query_object.numeric_multirange_value else True,
                ModuleDemoAllTypes.date_multirange_value == query_object.date_multirange_value if query_object.date_multirange_value else True,
                ModuleDemoAllTypes.timestamp_multirange_value == query_object.timestamp_multirange_value if query_object.timestamp_multirange_value else True,
                ModuleDemoAllTypes.timestamp_tz_multirange_value == query_object.timestamp_tz_multirange_value if query_object.timestamp_tz_multirange_value else True,
                ModuleDemoAllTypes.oid_value == query_object.oid_value if query_object.oid_value else True,
                ModuleDemoAllTypes.regclass_value == query_object.regclass_value if query_object.regclass_value else True,
                ModuleDemoAllTypes.regconfig_value == query_object.regconfig_value if query_object.regconfig_value else True,
                ModuleDemoAllTypes.description == query_object.description if query_object.description else True,
                ModuleDemoAllTypes.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ModuleDemoAllTypes.del_flag == "0")
            .order_by(ModuleDemoAllTypes.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Module_demoQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_module_demo_dao(cls, db: AsyncSession, module_demo: Module_demoModel):
        """
        新增Demo全类型测试数据库操作

        :param db: orm对象
        :param module_demo: Demo全类型测试对象
        :return:
        """
        db_module_demo = ModuleDemoAllTypes(**module_demo.model_dump(exclude={}))
        db.add(db_module_demo)
        await db.flush()

        return db_module_demo

    @classmethod
    async def edit_module_demo_dao(cls, db: AsyncSession, module_demo: dict):
        """
        编辑Demo全类型测试数据库操作

        :param db: orm对象
        :param module_demo: 需要更新的Demo全类型测试字典
        :return:
        """
        await db.execute(update(ModuleDemoAllTypes), [module_demo])

    @classmethod
    async def delete_module_demo_dao(cls, db: AsyncSession, module_demo: Module_demoModel):
        """
        删除Demo全类型测试数据库操作

        :param db: orm对象
        :param module_demo: Demo全类型测试对象
        :return:
        """
        #await db.execute(delete(ModuleDemoAllTypes).where(ModuleDemoAllTypes.id.in_([module_demo.id])))
        await db.execute(update(ModuleDemoAllTypes).where(ModuleDemoAllTypes.id.in_([module_demo.id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Module_demoPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Module_demoDao.get_module_demo_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
