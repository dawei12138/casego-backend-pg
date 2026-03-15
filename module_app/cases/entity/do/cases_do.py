# -*- coding: utf-8 -*-
"""
测试用例表
对应 Java: org.cloud.sonic.controller.models.domain.TestCases
"""
from sqlalchemy import String, Column, Text, Integer, DateTime, Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from module_app.enums import PlatformEnum


class AppTestCases(Base):
    """
    测试用例表 - 存储自动化测试用例
    """

    __tablename__ = 'app_test_cases'
    __table_args__ = {'comment': '测试用例表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    name = Column(String(255), nullable=False, comment='用例名称')
    des = Column(Text, nullable=True, comment='用例描述')
    designer = Column(String(100), nullable=True, comment='设计者')
    platform = Column(Enum(PlatformEnum, name="PlatformEnum",), nullable=False, default=PlatformEnum.ANDROID, comment='平台类型')
    project_id = Column(Integer, nullable=False, index=True, comment='所属项目ID')
    module_id = Column(Integer, nullable=True, default=0, index=True, comment='所属模块ID')
    version = Column(String(50), nullable=True, comment='版本号')
    edit_time = Column(DateTime, nullable=True, comment='最后编辑时间')
