from sqlalchemy import Integer, DateTime, SmallInteger, Column, String, Float, Boolean
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiAssertions(Base):
    """
    接口断言表
    """

    __tablename__ = 'api_assertions'
    __table_args__ = {'comment': '接口断言表'}

    assertion_id = Column(Integer, primary_key=True, comment='断言ID')
    case_id = Column(Integer, nullable=False, comment='关联的测试用例ID')
    jsonpath = Column(String(255), comment='JSONPath表达式OR提取方法')
    jsonpath_index = Column(Integer, comment='JSONPath提取索引')
    assertion_method = Column(String(255), nullable=True, comment='断言 (==, !=, >等)')
    value = Column(String(255), nullable=True, comment='预期值')
    assert_type = Column(String(255), nullable=True, comment='断言类型 (可选)')
    is_run = Column(Boolean, default=True, comment='是否执行该断言')
    extract_index_is_run = Column(Boolean, default=True, comment='是否执行提取索引操作')



