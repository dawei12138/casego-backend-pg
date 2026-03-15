from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class AppGlobalParams(Base):
    """
    全局参数表
    """

    __tablename__ = 'app_global_params'
    __table_args__ = {'comment': '全局参数表'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='主键ID')
    params_key = Column(String(255), nullable=True, comment='参数键名')
    params_value = Column(Text, nullable=True, comment='参数值')
    project_id = Column(Integer, nullable=True, comment='所属项目ID')




