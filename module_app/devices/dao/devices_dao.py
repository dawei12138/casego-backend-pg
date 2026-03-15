from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_app.devices.entity.do.devices_do import AppDevices
from module_app.devices.entity.vo.devices_vo import DevicesModel, DevicesPageQueryModel, DevicesQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class DevicesDao:
    """
    设备模块数据库操作层
    """

    @classmethod
    async def get_devices_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据主键ID获取设备详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 设备信息对象
        """
        devices_info = (
            (
                await db.execute(
                    select(AppDevices)
                    .where(
                        AppDevices.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return devices_info

    @classmethod
    async def get_devices_detail_by_info(cls, db: AsyncSession, devices: DevicesModel):
        """
        根据设备参数获取设备信息

        :param db: orm对象
        :param devices: 设备参数对象
        :return: 设备信息对象
        """
        devices_info = (
            (
                await db.execute(
                    select(AppDevices).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return devices_info

    @classmethod
    async def get_devices_list(cls, db: AsyncSession, query_object: DevicesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取设备列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 设备列表信息字典对象
        """
        query = (
            select(AppDevices)
            .where(
                AppDevices.agent_id == query_object.agent_id if query_object.agent_id else True,
                AppDevices.ud_id == query_object.ud_id if query_object.ud_id else True,
                AppDevices.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppDevices.nick_name.like(f'%{query_object.nick_name}%') if query_object.nick_name else True,
                AppDevices.model == query_object.model if query_object.model else True,
                AppDevices.chi_name.like(f'%{query_object.chi_name}%') if query_object.chi_name else True,
                AppDevices.manufacturer == query_object.manufacturer if query_object.manufacturer else True,
                AppDevices.cpu == query_object.cpu if query_object.cpu else True,
                AppDevices.size == query_object.size if query_object.size else True,
                AppDevices.version == query_object.version if query_object.version else True,
                AppDevices.platform == query_object.platform if query_object.platform else True,
                AppDevices.is_hm == query_object.is_hm if query_object.is_hm else True,
                AppDevices.status == query_object.status if query_object.status else True,
                AppDevices.user == query_object.user if query_object.user else True,
                AppDevices.password == query_object.password if query_object.password else True,
                AppDevices.img_url == query_object.img_url if query_object.img_url else True,
                AppDevices.temperature == query_object.temperature if query_object.temperature else True,
                AppDevices.voltage == query_object.voltage if query_object.voltage else True,
                AppDevices.level == query_object.level if query_object.level else True,
                AppDevices.position == query_object.position if query_object.position else True,
                AppDevices.description == query_object.description if query_object.description else True,
                AppDevices.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppDevices.del_flag == "0")
            .order_by(AppDevices.id)
            #.distinct()
        )
        devices_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return devices_list

    @classmethod
    async def get_devices_orm_list(cls, db: AsyncSession, query_object: DevicesQueryModel) -> List[DevicesQueryModel]:
        """
        根据查询参数获取设备列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 设备列表信息orm对象
        """
        query = (
            select(AppDevices)
            .where(
                AppDevices.agent_id == query_object.agent_id if query_object.agent_id else True,
                AppDevices.ud_id == query_object.ud_id if query_object.ud_id else True,
                AppDevices.name.like(f'%{query_object.name}%') if query_object.name else True,
                AppDevices.nick_name.like(f'%{query_object.nick_name}%') if query_object.nick_name else True,
                AppDevices.model == query_object.model if query_object.model else True,
                AppDevices.chi_name.like(f'%{query_object.chi_name}%') if query_object.chi_name else True,
                AppDevices.manufacturer == query_object.manufacturer if query_object.manufacturer else True,
                AppDevices.cpu == query_object.cpu if query_object.cpu else True,
                AppDevices.size == query_object.size if query_object.size else True,
                AppDevices.version == query_object.version if query_object.version else True,
                AppDevices.platform == query_object.platform if query_object.platform else True,
                AppDevices.is_hm == query_object.is_hm if query_object.is_hm else True,
                AppDevices.status == query_object.status if query_object.status else True,
                AppDevices.user == query_object.user if query_object.user else True,
                AppDevices.password == query_object.password if query_object.password else True,
                AppDevices.img_url == query_object.img_url if query_object.img_url else True,
                AppDevices.temperature == query_object.temperature if query_object.temperature else True,
                AppDevices.voltage == query_object.voltage if query_object.voltage else True,
                AppDevices.level == query_object.level if query_object.level else True,
                AppDevices.position == query_object.position if query_object.position else True,
                AppDevices.description == query_object.description if query_object.description else True,
                AppDevices.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(AppDevices.del_flag == "0")
            .order_by(AppDevices.id)
            #.distinct()
        )

        result = await db.execute(query)
        return [DevicesQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_devices_dao(cls, db: AsyncSession, devices: DevicesModel):
        """
        新增设备数据库操作

        :param db: orm对象
        :param devices: 设备对象
        :return:
        """
        db_devices = AppDevices(**devices.model_dump(exclude={}))
        db.add(db_devices)
        await db.flush()

        return db_devices

    @classmethod
    async def edit_devices_dao(cls, db: AsyncSession, devices: dict):
        """
        编辑设备数据库操作

        :param db: orm对象
        :param devices: 需要更新的设备字典
        :return:
        """
        await db.execute(update(AppDevices), [devices])

    @classmethod
    async def delete_devices_dao(cls, db: AsyncSession, devices: DevicesModel):
        """
        删除设备数据库操作

        :param db: orm对象
        :param devices: 设备对象
        :return:
        """
        #await db.execute(delete(AppDevices).where(AppDevices.id.in_([devices.id])))
        await db.execute(update(AppDevices).where(AppDevices.id.in_([devices.id])).values(del_flag="1"))

    @classmethod
    async def find_by_ud_id(cls, db: AsyncSession, ud_id: str):
        """
        根据设备序列号查询设备 (Phase 2.1.1)

        :param db: orm对象
        :param ud_id: 设备序列号
        :return: 设备信息对象
        """
        device_info = (
            (
                await db.execute(
                    select(AppDevices)
                    .where(
                        AppDevices.ud_id == ud_id,
                        AppDevices.del_flag == "0"
                    )
                )
            )
            .scalars()
            .first()
        )

        return device_info

    @classmethod
    async def update_device_by_ud_id(cls, db: AsyncSession, agent_id: int, ud_id: str, detail: dict):
        """
        根据设备序列号更新设备详情 (Phase 2.1.2)

        :param db: orm对象
        :param agent_id: Agent ID
        :param ud_id: 设备序列号
        :param detail: 设备详情字典
        :return:
        """
        update_data = {
            'agent_id': agent_id,
            'ud_id': ud_id
        }

        # 提取详情中的字段
        if 'name' in detail:
            update_data['name'] = detail['name']
        if 'model' in detail:
            update_data['model'] = detail['model']
        if 'manufacturer' in detail:
            update_data['manufacturer'] = detail['manufacturer']
        if 'cpu' in detail:
            update_data['cpu'] = detail['cpu']
        if 'size' in detail:
            update_data['size'] = detail['size']
        if 'version' in detail:
            update_data['version'] = detail['version']
        if 'chiName' in detail:
            update_data['chi_name'] = detail['chiName']
        if 'isHm' in detail:
            from module_app.enums import BoolFlagEnum
            update_data['is_hm'] = BoolFlagEnum.YES if detail['isHm'] else BoolFlagEnum.NO

        await db.execute(
            update(AppDevices)
            .where(AppDevices.ud_id == ud_id)
            .values(**update_data)
        )

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = DevicesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await DevicesDao.get_devices_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
