from sqlalchemy import String, JSON, Float, DateTime, Column, Integer, SmallInteger, Boolean, Enum, Text, BigInteger
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime

from config.enums import Request_method
from utils.api_workflow_tools.models import StreamEventType


class ApiTestExecutionLog(Base):
    __tablename__ = 'api_test_execution_log'
    __table_args__ = {'comment': '接口测试执行日志表'}

    log_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='执行日志ID')
    case_id = Column(Integer, nullable=True, comment='测试用例ID')
    execution_time = Column(DateTime, default=datetime.now, nullable=False, comment='执行时间')
    is_success = Column(Boolean, default=True, comment='是否执行成功')

    # 所有执行数据存储在一个JSON字段中
    execution_data = Column(JSONB, default={}, comment='完整执行数据')

    # 为了方便查询，提取关键字段
    response_status_code = Column(Integer, nullable=True, comment='响应状态码')
    response_time = Column(Float, nullable=True, comment='响应时间(秒)')
    assertion_success = Column(Boolean, default=True, comment='断言是否成功')
    method = Column(Enum(Request_method, name="Request_method"), default=Request_method.GET, comment='请求方法')
    path = Column(Text, nullable=True, comment='请求路径')
    name = Column(Text, nullable=True, comment='测试用例名称')

    # 工作流相关
    workflow_id = Column(BigInteger, comment='workflow_id')
    report_id = Column(BigInteger, comment='report_id')
    event_type = Column(Enum(StreamEventType, name="StreamEventType"), default=StreamEventType.LOG, comment='类型')
