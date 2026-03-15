from sqlalchemy import String, DateTime, Float, Column, Integer, SmallInteger, Boolean
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiServices(Base):
    __tablename__ = 'api_services'
    __table_args__ = {'comment': '环境服务地址表'}

    id = Column(Integer, primary_key=True, comment='服务ID')
    name = Column(String(100), nullable=True, comment='服务名称')
    url = Column(String(200), nullable=True, comment='服务地址')
    environment_id = Column(Integer, nullable=False, comment='所属环境ID')
    is_default = Column(Boolean, default=False, nullable=False, comment='是否为默认服务')





