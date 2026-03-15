from sqlalchemy import Float, Column, Integer, DateTime, String, Text
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiCacheData(Base):
    """
    环境缓存表
    """

    __tablename__ = 'api_cache_data'
    __table_args__ = {'comment': '环境缓存表'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='缓存数据ID')
    cache_key = Column(String(255), nullable=True, comment='缓存键名')
    environment_id = Column(Integer, nullable=True, comment='关联的环境ID')
    cache_value = Column(Text, nullable=True, comment='缓存值')
    source_type = Column(String(50), nullable=True, comment='数据来源可以为空')
    user_id = Column(String(255), nullable=True, comment='用戶id')




