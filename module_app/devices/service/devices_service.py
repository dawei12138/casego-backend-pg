from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.devices.dao.devices_dao import DevicesDao
from module_app.devices.entity.vo.devices_vo import DeleteDevicesModel, DevicesModel, DevicesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class DevicesService:
    """
    设备模块服务层
    """

    @classmethod
    async def get_devices_list_services(
        cls, query_db: AsyncSession, query_object: DevicesPageQueryModel, is_page: bool = False
    ):
        """
        获取设备列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 设备列表信息对象
        """
        devices_list_result = await DevicesDao.get_devices_list(query_db, query_object, is_page)

        return devices_list_result


    @classmethod
    async def add_devices_services(cls, query_db: AsyncSession, page_object: DevicesModel):
        """
        新增设备信息service

        :param query_db: orm对象
        :param page_object: 新增设备对象
        :return: 新增设备校验结果
        """
        try:
            await DevicesDao.add_devices_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_devices_services(cls, query_db: AsyncSession, page_object: DevicesModel):
        """
        编辑设备信息service

        :param query_db: orm对象
        :param page_object: 编辑设备对象
        :return: 编辑设备校验结果
        """
        edit_devices = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        devices_info = await cls.devices_detail_services(query_db, page_object.id)
        if devices_info.id:
            try:
                await DevicesDao.edit_devices_dao(query_db, edit_devices)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='设备不存在')

    @classmethod
    async def delete_devices_services(cls, query_db: AsyncSession, page_object: DeleteDevicesModel):
        """
        删除设备信息service

        :param query_db: orm对象
        :param page_object: 删除设备对象
        :return: 删除设备校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await DevicesDao.delete_devices_dao(query_db, DevicesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def devices_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取设备详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        devices = await DevicesDao.get_devices_detail_by_id(query_db, id=id)
        if devices:
            result = DevicesModel(**CamelCaseUtil.transform_result(devices))
        else:
            result = DevicesModel(**dict())

        return result

    @staticmethod
    async def export_devices_list_services(devices_list: List):
        """
        导出设备信息service

        :param devices_list: 设备信息列表
        :return: 设备信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'agentId': '所属Agent的ID',
            'udId': '设备序列号(唯一标识)',
            'name': '设备名称',
            'nickName': '设备备注名',
            'model': '设备型号',
            'chiName': '设备中文名',
            'manufacturer': '制造商',
            'cpu': 'CPU架构',
            'size': '屏幕分辨率',
            'version': '系统版本',
            'platform': '平台类型',
            'isHm': '是否鸿蒙',
            'status': '设备状态',
            'user': '当前占用者用户名',
            'password': '设备安装App的密码',
            'imgUrl': '设备封面图URL',
            'temperature': '设备温度',
            'voltage': '电池电压',
            'level': '电量百分比',
            'position': 'Hub位置',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(devices_list, mapping_dict)

        return binary_data

    @classmethod
    async def find_by_ud_id(cls, query_db: AsyncSession, ud_id: str):
        """
        通过设备序列号查询设备信息 (Phase 2.1.1)

        :param query_db: orm对象
        :param ud_id: 设备序列号
        :return: 设备信息对象，如果不存在则返回 None
        """
        device = await DevicesDao.find_by_ud_id(query_db, ud_id)
        if device:
            result = DevicesModel(**CamelCaseUtil.transform_result(device))
        else:
            result = None

        return result

    @classmethod
    async def update_device(cls, query_db: AsyncSession, agent_id: int, ud_id: str, detail: dict):
        """
        更新设备详情 (Phase 2.1.2)

        :param query_db: orm对象
        :param agent_id: Agent ID
        :param ud_id: 设备序列号
        :param detail: 设备详情字典
        :return: 更新结果
        """
        try:
            await DevicesDao.update_device_by_ud_id(query_db, agent_id, ud_id, detail)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='设备详情更新成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def occupy(cls, query_db: AsyncSession, ud_id: str, user: str):
        """
        占用设备 (Phase 2.1.3)

        :param query_db: orm对象
        :param ud_id: 设备序列号
        :param user: 占用者用户名
        :return: Agent连接信息（包含 host, port, wsUrl）
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from module_app.agents.entity.do.agents_do import AppAgents
        from module_app.enums import DeviceStatusEnum
        from sqlalchemy import select, update

        # 1. 查询设备信息
        result = await query_db.execute(
            select(AppDevices).where(
                AppDevices.ud_id == ud_id,
                AppDevices.del_flag == "0"
            )
        )
        device = result.scalars().first()

        if not device:
            raise ServiceException(message=f'设备不存在: {ud_id}')

        # 2. 检查设备是否已被占用
        if device.status == DeviceStatusEnum.DEBUGGING and device.user:
            raise ServiceException(message=f'设备已被占用: {device.user}')

        # 3. 查询Agent信息
        agent_result = await query_db.execute(
            select(AppAgents).where(AppAgents.id == device.agent_id)
        )
        agent = agent_result.scalars().first()

        if not agent:
            raise ServiceException(message=f'Agent不存在: {device.agent_id}')

        # 4. 更新设备状态为占用
        try:
            await query_db.execute(
                update(AppDevices)
                .where(AppDevices.ud_id == ud_id)
                .values(status=DeviceStatusEnum.DEBUGGING, user=user)
            )
            await query_db.commit()

            # 5. 返回Agent连接信息
            platform_path = 'android' if device.platform.value == 1 else 'ios'
            ws_url = f'ws://{agent.host}:{agent.port}/websockets/{platform_path}/{ud_id}'

            return {
                'agentHost': agent.host,
                'agentPort': agent.port,
                'wsUrl': ws_url
            }

        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def release(cls, query_db: AsyncSession, ud_id: str):
        """
        释放设备 (Phase 2.1.4)

        :param query_db: orm对象
        :param ud_id: 设备序列号
        :return: 释放结果
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from module_app.enums import DeviceStatusEnum
        from sqlalchemy import update

        try:
            # 查询设备是否存在
            result = await query_db.execute(
                select(AppDevices).where(
                    AppDevices.ud_id == ud_id,
                    AppDevices.del_flag == "0"
                )
            )
            device = result.scalars().first()

            if not device:
                raise ServiceException(message=f'设备不存在: {ud_id}')

            # 更新设备状态为在线，清空占用者
            await query_db.execute(
                update(AppDevices)
                .where(AppDevices.ud_id == ud_id)
                .values(status=DeviceStatusEnum.ONLINE, user='')
            )
            await query_db.commit()

            return CrudResponseModel(is_success=True, message='设备释放成功')

        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def update_battery(cls, query_db: AsyncSession, ud_id: str, level: int, voltage: int, temperature: int):
        """
        更新设备电量信息 (Phase 2.1.5)

        :param query_db: orm对象
        :param ud_id: 设备序列号
        :param level: 电量百分比
        :param voltage: 电池电压
        :param temperature: 设备温度
        :return: 更新结果
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from sqlalchemy import update

        try:
            await query_db.execute(
                update(AppDevices)
                .where(AppDevices.ud_id == ud_id, AppDevices.del_flag == "0")
                .values(level=level, voltage=voltage, temperature=temperature)
            )
            await query_db.commit()

            return CrudResponseModel(is_success=True, message='电量信息更新成功')

        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def list_by_agent(cls, query_db: AsyncSession, agent_id: int):
        """
        获取Agent下的所有设备 (Phase 2.1.6)

        :param query_db: orm对象
        :param agent_id: Agent ID
        :return: 设备列表
        """
        from module_app.devices.entity.do.devices_do import AppDevices
        from sqlalchemy import select

        result = await query_db.execute(
            select(AppDevices)
            .where(AppDevices.agent_id == agent_id, AppDevices.del_flag == "0")
            .order_by(AppDevices.id)
        )
        devices = result.scalars().all()

        # 转换为VO模型
        device_list = [DevicesModel(**CamelCaseUtil.transform_result(device)) for device in devices]

        return device_list
