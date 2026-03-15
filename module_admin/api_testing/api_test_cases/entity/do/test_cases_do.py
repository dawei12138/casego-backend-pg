from typing import Optional

from sqlalchemy import String, Integer, DateTime, Text, Float, SmallInteger, Column, BigInteger, ForeignKey, JSON, Enum, \
    Boolean, Index
from sqlalchemy.orm import relationship

from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.enums import Request_Type, Request_method


# from module_admin.api_project_submodules.entity.do.project_submodules_do import ApiProjectSubmodules


class ApiTestCases(Base):
    __tablename__ = 'api_test_cases'
    __table_args__ = (
        # 优化查询父用例：按模块ID + 用例类型 + 删除标记
        Index('idx_cases_submodule_type', 'parent_submodule_id', 'case_type', 'del_flag'),
        # 优化查询子用例：按父用例ID + 用例类型 + 删除标记
        Index('idx_cases_parent_type', 'parent_case_id', 'case_type', 'del_flag'),
        # 优化按项目ID查询
        Index('idx_cases_project', 'project_id', 'del_flag'),
        {'comment': '接口用例表'}
    )

    case_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment='测试用例ID')
    name = Column(String(255), nullable=True, comment='测试用例名称')
    case_type = Column(String(50), default="1", nullable=False, comment='测试用例类型')
    copy_id = Column(Integer, nullable=True, comment='复制用例ID')
    parent_case_id = Column(Integer, nullable=True, comment='父级测试接口ID')
    project_id = Column(Integer, nullable=True, comment='项目ID')
    parent_submodule_id = Column(BigInteger, nullable=True,
                                 comment='父级模块ID')
    path = Column(Text, nullable=True, comment='请求路径')
    method = Column(Enum(Request_method, name="Request_method"), default=Request_method.GET, comment='请求方法')
    request_type = Column(Enum(Request_Type, name="Request_Type"), default=Request_Type.NONE, nullable=False, comment='请求类型')
    json_data = Column(JSONB, nullable=True, default={}, comment='请求json，xml，raw数据')
    is_run = Column(SmallInteger, default=1, comment='是否执行')
    status_code = Column(Integer, default=200, comment='预期状态码')
    sleep = Column(Integer, default=0, comment='执行前等待时间')
    case_file_config = Column(JSONB, default={}, comment='用例的文件配置')
    response_example = Column(JSONB, nullable=True, comment='返回示例')


