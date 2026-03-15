from sqlalchemy import Float, Integer, String, Column, DateTime, Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from module_app.enums import PlatformEnum


class AppPublicSteps(Base):
    """
    公共步骤表
    """

    __tablename__ = 'app_public_steps'
    __table_args__ = {'comment': '公共步骤表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(255), nullable=False, comment='公共步骤名称')
    platform = Column(Enum(PlatformEnum, name="PlatformEnum"), nullable=False, default=PlatformEnum.ANDROID, comment='平台类型')
    project_id = Column(Integer, nullable=False, index=True, comment='所属项目ID')




