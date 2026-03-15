from sqlalchemy import Column, Integer, DateTime, Float, String, SmallInteger, JSON
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import JSONB



class ApiEnvironments(Base):
    """
    环境配置表
    """

    __tablename__ = 'api_environments'
    __table_args__ = {'comment': '环境配置表'}

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='环境ID')
    name = Column(String(100), nullable=False, comment='环境名称')
    project_id = Column(Integer, nullable=True, comment='所属项目ID')
    is_default = Column(SmallInteger, nullable=True, comment='是否为默认环境')
    request_timeout = Column(Integer, default=5000, nullable=True, comment='请求超时(ms)')
    global_headers = Column(JSONB, default=[], nullable=True, comment='全局请求头json字典')
    global_cookies = Column(JSONB, default=[], nullable=True, comment='全局cookies字典')
