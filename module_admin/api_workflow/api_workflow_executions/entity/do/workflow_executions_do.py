from sqlalchemy import JSON, Integer, Column, Float, String, DateTime, Text, BigInteger
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiWorkflowExecutions(Base):
    """
    执行器执行记录表
    """

    __tablename__ = "api_workflow_executions"
    __table_args__ = {
        'comment': '执行器执行记录表'
    }

    workflow_execution_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    workflow_id = Column(BigInteger, nullable=True, comment="执行器ID")
    workflow_name = Column(BigInteger, comment="执行名称")

    # 执行状态
    status = Column(String(20), nullable=False, default="pending", comment="执行状态")

    # 执行时间
    start_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    duration = Column(Integer, comment="执行时长(秒)")

    # 执行数据
    input_data = Column(JSONB, comment="输入数据")
    output_data = Column(JSONB, comment="输出数据")
    context_data = Column(JSONB, comment="上下文数据")

    # 执行结果统计
    total_nodes = Column(Integer, default=0, comment="总节点数")
    success_nodes = Column(Integer, default=0, comment="成功节点数")
    failed_nodes = Column(Integer, default=0, comment="失败节点数")
    skipped_nodes = Column(Integer, default=0, comment="跳过节点数")

    # 错误信息
    error_message = Column(Text, comment="错误信息")
    error_details = Column(JSONB, comment="错误详情")




