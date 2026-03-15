from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query
from module_app.enums import DeviceStatusEnum, BoolFlagEnum, PlatformEnum


class DevicesModel(BaseModel):
    """
    设备表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='主键ID')
    agent_id: Optional[int] = Field(default=None, description='所属Agent的ID')
    ud_id: Optional[str] = Field(default=None, description='设备序列号(唯一标识)')
    name: Optional[str] = Field(default=None, description='设备名称')
    nick_name: Optional[str] = Field(default=None, description='设备备注名')
    model: Optional[str] = Field(default=None, description='设备型号')
    chi_name: Optional[str] = Field(default=None, description='设备中文名')
    manufacturer: Optional[str] = Field(default=None, description='制造商')
    cpu: Optional[str] = Field(default=None, description='CPU架构')
    size: Optional[str] = Field(default=None, description='屏幕分辨率')
    version: Optional[str] = Field(default=None, description='系统版本')
    platform: Optional[PlatformEnum] = Field(default=None, description='平台类型')
    is_hm: Optional[BoolFlagEnum] = Field(default=None, description='是否鸿蒙')
    status: Optional[DeviceStatusEnum] = Field(default=None, description='设备状态')
    user: Optional[str] = Field(default=None, description='当前占用者用户名')
    password: Optional[str] = Field(default=None, description='设备安装App的密码')
    img_url: Optional[str] = Field(default=None, description='设备封面图URL')
    temperature: Optional[int] = Field(default=None, description='设备温度')
    voltage: Optional[int] = Field(default=None, description='电池电压')
    level: Optional[int] = Field(default=None, description='电量百分比')
    position: Optional[int] = Field(default=None, description='Hub位置')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')






class DevicesQueryModel(DevicesModel):
    """
    设备不分页查询模型
    """
    pass


@as_query
class DevicesPageQueryModel(DevicesQueryModel):
    """
    设备分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDevicesModel(BaseModel):
    """
    删除设备模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID')


class OccupyDeviceModel(BaseModel):
    """
    占用设备请求模型 (Phase 2.2.1)
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ud_id: str = Field(description='设备序列号')


class OccupyDeviceResponseModel(BaseModel):
    """
    占用设备响应模型 (Phase 2.2.1)
    """

    model_config = ConfigDict(alias_generator=to_camel)

    agent_host: str = Field(description='Agent的IP地址')
    agent_port: int = Field(description='Agent的端口')
    ws_url: str = Field(description='WebSocket连接地址')
