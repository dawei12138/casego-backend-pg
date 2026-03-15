from datetime import datetime

from sqlalchemy import Enum, String, BigInteger, Column, JSON, SmallInteger, Float, Integer, DateTime, Boolean, Index
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from utils.api_workflow_tools.models import TriggerType


class ApiWorkflowReport(Base):
    """
    测试报告主表
    """
    __tablename__ = "api_workflow_report"
    __table_args__ = (
        Index('ix_report_workflow_id', 'workflow_id'),
        {
            'comment': '自动化测试执行报告表'
        }
    )

    # 主键 ID
    report_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='报告ID')

    # 所属执行器 workflow
    workflow_id = Column(BigInteger, nullable=False, comment='执行器ID')

    # 报告名称（可自定义，如 “2025-01-01 10:00 定时任务报告”）
    name = Column(String(255), nullable=True, comment='报告名称')

    # 执行时间
    start_time = Column(DateTime, nullable=True, default=datetime.now, comment='开始时间')
    end_time = Column(DateTime, nullable=True, comment='结束时间')

    # 聚合统计信息
    total_cases = Column(Integer, default=0, comment='总用例数')
    success_cases = Column(Integer, default=0, comment='成功用例数')
    failed_cases = Column(Integer, default=0, comment='失败用例数')

    # 时间耗时 （秒）
    duration = Column(Float, nullable=True, comment='总耗时(秒)')

    # 报告整体状态
    is_success = Column(Boolean, default=True, comment="是否全部成功")

    # 原始报告数据（包含所有步骤、日志结构等）
    report_data = Column(JSONB, default={}, comment='完整报告JSON数据')

    # 执行来源（定时任务、手动触发、API触发等）
    trigger_type = Column(
        Enum(
            TriggerType,
            values_callable=lambda x: [e.value for e in x],
            name="trigger_type_enum"
        ),
        nullable=True,
        comment="触发类型"
    )




