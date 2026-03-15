from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_app.devices.service.devices_service import DevicesService
from module_app.devices.entity.vo.devices_vo import (
    DeleteDevicesModel,
    DevicesModel,
    DevicesPageQueryModel,
    OccupyDeviceModel,
    OccupyDeviceResponseModel
)
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil


devicesController = APIRouter(prefix='/app/devices', dependencies=[Depends(LoginService.get_current_user)])


@devicesController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:list'))],
    summary='获取设备列表',
    description='根据查询条件获取设备分页列表数据',
)
async def get_app_devices_list(
    request: Request,
devices_page_query: DevicesPageQueryModel = Depends(DevicesPageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
):
    logger.info(devices_page_query.model_dump())
    # 获取分页数据
    devices_page_query_result = await DevicesService.get_devices_list_services(query_db, devices_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=devices_page_query_result)


@devicesController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:add'))],
    summary='新增设备',
    description='创建一条新的设备记录',
)
@ValidateFields(validate_model='add_devices')
# @Log(title='设备', business_type=BusinessType.INSERT)
async def add_app_devices(
    request: Request,
    add_devices: DevicesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_devices.create_by = current_user.user.user_name
    add_devices.create_time = datetime.now()
    add_devices.update_by = current_user.user.user_name
    add_devices.update_time = datetime.now()
    logger.info(add_devices.model_dump())
    add_devices_result = await DevicesService.add_devices_services(query_db, add_devices)
    logger.info(add_devices_result.message)

    return ResponseUtil.success(msg=add_devices_result.message)


@devicesController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:edit'))],
    summary='修改设备',
    description='根据主键更新设备信息',
)
@ValidateFields(validate_model='edit_devices')
# @Log(title='设备', business_type=BusinessType.UPDATE)
async def edit_app_devices(
    request: Request,
    edit_devices: DevicesModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_devices.model_dump())
    edit_devices.update_by = current_user.user.user_name
    edit_devices.update_time = datetime.now()
    edit_devices_result = await DevicesService.edit_devices_services(query_db, edit_devices)
    logger.info(edit_devices_result.message)

    return ResponseUtil.success(msg=edit_devices_result.message)


@devicesController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:remove'))],
    summary='删除设备',
    description='根据主键批量删除设备记录，多个主键以逗号分隔',
)
# @Log(title='设备', business_type=BusinessType.DELETE)
async def delete_app_devices(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):

    delete_devices = DeleteDevicesModel(ids=ids)
    logger.info(delete_devices.model_dump())
    delete_devices_result = await DevicesService.delete_devices_services(query_db, delete_devices)
    logger.info(delete_devices_result.message)

    return ResponseUtil.success(msg=delete_devices_result.message)


@devicesController.get(
    '/{id}',
    response_model=DevicesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:query'))],
    summary='获取设备详情',
    description='根据主键获取设备详细信息',
)
async def query_detail_app_devices(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    devices_detail_result = await DevicesService.devices_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=devices_detail_result)


@devicesController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:export'))],
    summary='导出设备',
    description='根据查询条件导出设备列表数据到Excel文件',
)
# @Log(title='设备', business_type=BusinessType.EXPORT)
async def export_app_devices_list(
    request: Request,
    devices_page_query: DevicesPageQueryModel = Form(),
    query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    devices_query_result = await DevicesService.get_devices_list_services(query_db, devices_page_query, is_page=False)
    devices_export_result = await DevicesService.export_devices_list_services(devices_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(devices_export_result))


@devicesController.post(
    '/occupy',
    response_model=OccupyDeviceResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:occupy'))],
    summary='占用设备',
    description='占用指定设备进行调试，返回Agent连接信息 (Phase 2.2.1)',
)
async def occupy_device(
    request: Request,
    occupy_request: OccupyDeviceModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    占用设备接口

    请求参数:
    - ud_id: 设备序列号

    返回:
    - agentHost: Agent的IP地址
    - agentPort: Agent的端口
    - wsUrl: WebSocket连接地址
    """
    logger.info(f'用户 {current_user.user.user_name} 尝试占用设备 {occupy_request.ud_id}')

    try:
        result = await DevicesService.occupy(
            query_db,
            occupy_request.ud_id,
            current_user.user.user_name
        )
        logger.info(f'设备 {occupy_request.ud_id} 占用成功')

        return ResponseUtil.success(data=result)

    except Exception as e:
        logger.error(f'设备 {occupy_request.ud_id} 占用失败: {e}')
        raise e


@devicesController.get(
    '/release',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:release'))],
    summary='释放设备',
    description='释放指定设备，将设备状态设置为在线 (Phase 2.2.2)',
)
async def release_device(
    request: Request,
    ud_id: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    释放设备接口

    请求参数:
    - ud_id: 设备序列号
    """
    logger.info(f'用户 {current_user.user.user_name} 尝试释放设备 {ud_id}')

    try:
        result = await DevicesService.release(query_db, ud_id)
        logger.info(f'设备 {ud_id} 释放成功')

        return ResponseUtil.success(msg=result.message)

    except Exception as e:
        logger.error(f'设备 {ud_id} 释放失败: {e}')
        raise e


@devicesController.get(
    '/stopDebug',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:stopDebug'))],
    summary='强制停止调试',
    description='强制停止指定设备的调试，将设备状态设置为在线 (Phase 2.2.3)',
)
async def stop_debug_device(
    request: Request,
    ud_id: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    强制停止调试接口

    请求参数:
    - ud_id: 设备序列号
    """
    logger.info(f'用户 {current_user.user.user_name} 强制停止设备 {ud_id} 的调试')

    try:
        # 停止调试本质上就是释放设备
        result = await DevicesService.release(query_db, ud_id)
        logger.info(f'设备 {ud_id} 调试已停止')

        return ResponseUtil.success(msg=result.message)

    except Exception as e:
        logger.error(f'停止设备 {ud_id} 调试失败: {e}')
        raise e


@devicesController.get(
    '/listByAgentId',
    dependencies=[Depends(CheckUserInterfaceAuth('app:devices:list'))],
    summary='按Agent查询设备',
    description='获取指定Agent下的所有设备列表 (Phase 2.2.4)',
)
async def list_devices_by_agent_id(
    request: Request,
    agent_id: int,
    query_db: AsyncSession = Depends(get_db),
):
    """
    按Agent查询设备接口

    请求参数:
    - agent_id: Agent ID
    """
    logger.info(f'查询 Agent {agent_id} 下的设备列表')

    try:
        device_list = await DevicesService.list_by_agent(query_db, agent_id)
        logger.info(f'查询 Agent {agent_id} 设备列表成功，共 {len(device_list)} 台设备')

        return ResponseUtil.success(data=device_list)

    except Exception as e:
        logger.error(f'查询 Agent {agent_id} 设备列表失败: {e}')
        raise e
