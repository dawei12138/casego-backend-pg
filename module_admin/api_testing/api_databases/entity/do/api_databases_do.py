from sqlalchemy import String, Integer, Float, DateTime, Column
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiDatabases(Base):
    """
    数据库配置表
    """
    __tablename__ = 'api_databases'
    __table_args__ = {'comment': '数据库配置表'}

    id = Column(Integer, primary_key=True, comment='数据库ID')
    name = Column(String(100), nullable=True, comment='数据库名称')
    db_type = Column(String(50), nullable=True, comment='数据库类型（如1 MySQL、2Redis，）')
    host = Column(String(100), nullable=True, comment='数据库主机')
    port = Column(Integer, nullable=True, comment='数据库端口')
    username = Column(String(100), nullable=True, comment='数据库用户名')
    password = Column(String(100), nullable=True, comment='数据库密码')
    project_id = Column(Integer, nullable=True, comment='所属项目ID')




