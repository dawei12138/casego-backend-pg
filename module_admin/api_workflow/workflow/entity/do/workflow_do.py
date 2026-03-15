from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Float, BigInteger, JSON, Index, Boolean, Text, Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from utils.api_workflow_tools.models import TriggerType


class ApiWorkflow(Base):
    """
    测试执行器主表
    """

    __tablename__ = "api_workflow"
    __table_args__ = (
        Index('ix_workflow_name', 'name'),
        {
            'comment': '测试执行器主表'
        }
    )

    workflow_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    name = Column(String(200), comment="执行器名称")
    # 执行配置
    execution_config = Column(JSONB, comment="执行配置")
    # 关联字段
    parent_submodule_id = Column(BigInteger, nullable=True, comment='父级模块ID')
    project_id = Column(BigInteger, nullable=True, comment='父级模块ID')


