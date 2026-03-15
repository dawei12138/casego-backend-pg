from sqlalchemy import SmallInteger, Integer, String, DateTime, Column, Float, Text, Boolean, JSON
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiSetup(Base):
    """
    接口前置操作表
    """

    __tablename__ = 'api_setup'
    __table_args__ = {'comment': '接口前置操作表'}

    setup_id = Column(Integer, primary_key=True, comment='操作ID')
    name = Column(String(255), nullable=True, comment='操作名称')
    case_id = Column(Integer, nullable=False, comment='关联的测试用例ID')
    setup_type = Column(String(255), nullable=False, comment='操作类型 (db_connection, execute_script, wait_time)')
    db_connection_id = Column(Integer, nullable=True, comment='数据库连接ID')
    script = Column(Text, nullable=True, comment='脚本语句')
    extract_variables = Column(JSONB, default=[{"variable_name": None, "jsonpath": None}], comment='提取额外参数的KEY-VALUE')
    jsonpath = Column(Text, nullable=True, comment='jsonpath提取表达式')
    variable_name = Column(String(255), nullable=True, comment='变量名称（用于存储提取的数据）')
    wait_time = Column(Integer, nullable=True, comment='等待时间（毫秒）')
    extract_index = Column(Integer, default=0, nullable=True, comment='提取索引')
    extract_index_is_run = Column(Boolean, default=True, comment='是否执行提取索引操作')
    is_run = Column(Boolean, default=True, comment='是否执行该前置操作')
