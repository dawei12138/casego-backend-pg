from sqlalchemy import DateTime, Float, String, Column, Text, Integer, SmallInteger, Boolean, JSON
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiTeardown(Base):
    """
    接口后置操作表
    """

    __tablename__ = 'api_teardown'
    __table_args__ = {'comment': '接口后置操作表'}

    teardown_id = Column(Integer, primary_key=True, comment='操作ID')
    name = Column(String(255), nullable=True, comment='操作名称')
    case_id = Column(Integer, nullable=False, comment='关联的测试用例ID')
    teardown_type = Column(String(255), nullable=False,
                           comment='操作类型 (extract_variable, db_operation, custom_script, wait_time)')
    extract_variable_method = Column(String(255), nullable=True,
                                     comment='提取响应的方法： response_text''response_json''response_xml''response_header''response_cookie')
    jsonpath = Column(Text, nullable=True, comment='jsonpath提取表达式（用于提取变量）')
    extract_variables = Column(JSONB, default=[{"variable_name": None, "jsonpath": None}],
                               comment='提取额外参数的KEY-VALUE')
    extract_index = Column(Integer, default=0, nullable=True, comment='提取索引')
    extract_index_is_run = Column(Boolean, default=True, comment='是否执行提取索引操作')
    regular_expression = Column(Text, nullable=True, comment='正则表达式（用于提取text）')
    xpath_expression = Column(Text, nullable=True, comment='正则表达式（用于提取xml）')
    response_header = Column(Text, nullable=True, comment='正则表达式（用于提取响应头）')
    response_cookie = Column(Text, nullable=True, comment='正则表达式（用于提取cookie）')
    variable_name = Column(String(255), nullable=True, comment='变量名称（用于存储提取的数据）')
    database_id = Column(Integer, nullable=True, comment='数据库连接ID')
    db_operation = Column(Text, nullable=True, comment='数据库操作语句（用于数据库操作）')
    script = Column(Text, nullable=True, comment='自定义脚本语句（用于自定义脚本）')
    wait_time = Column(Integer, nullable=True, comment='等待时间（毫秒，用于等待时间）')
    is_run = Column(Boolean, default=True, comment='是否执行该后置操作')




