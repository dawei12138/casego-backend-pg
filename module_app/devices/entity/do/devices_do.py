from sqlalchemy import Float, Enum, Integer, DateTime, String, Column
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from module_app.enums import PlatformEnum, DeviceStatusEnum, BoolFlagEnum


class AppDevices(Base):
    """
    设备表
    """

    __tablename__ = 'app_devices'
    __table_args__ = {'comment': '设备表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    agent_id = Column(Integer, nullable=False, index=True, comment='所属Agent的ID')
    ud_id = Column(String(255), nullable=False, index=True, comment='设备序列号(唯一标识)')
    name = Column(String(255), nullable=True, default='', comment='设备名称')
    nick_name = Column(String(255), nullable=True, default='', comment='设备备注名')
    model = Column(String(100), nullable=True, default='', comment='设备型号')
    chi_name = Column(String(100), nullable=True, default='', comment='设备中文名')
    manufacturer = Column(String(100), nullable=True, default='', comment='制造商')
    cpu = Column(String(50), nullable=True, default='', comment='CPU架构')
    size = Column(String(50), nullable=True, default='', comment='屏幕分辨率')
    version = Column(String(50), nullable=True, default='', comment='系统版本')
    platform = Column(Enum(PlatformEnum, name="PlatformEnum"), nullable=False, default=PlatformEnum.ANDROID,
                      comment='平台类型')
    is_hm = Column(Enum(BoolFlagEnum, name="BoolFlagEnum"), nullable=False, default=BoolFlagEnum.NO, comment='是否鸿蒙')
    status = Column(Enum(DeviceStatusEnum, name="DeviceStatusEnum"), nullable=True, default=DeviceStatusEnum.OFFLINE,
                    comment='设备状态')
    user = Column(String(100), nullable=True, default='', comment='当前占用者用户名')
    password = Column(String(255), nullable=True, default='', comment='设备安装App的密码')
    img_url = Column(String(500), nullable=True, default='', comment='设备封面图URL')
    temperature = Column(Integer, nullable=True, default=0, comment='设备温度')
    voltage = Column(Integer, nullable=True, default=0, comment='电池电压')
    level = Column(Integer, nullable=True, default=0, comment='电量百分比')
    position = Column(Integer, nullable=True, default=0, comment='Hub位置')

