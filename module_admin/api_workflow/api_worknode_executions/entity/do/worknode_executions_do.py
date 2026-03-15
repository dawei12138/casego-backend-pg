from sqlalchemy import JSON, Column, DateTime, Integer, Text, SmallInteger, Float, String, Boolean, BigInteger, Index, \
    Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.enums import NotificationType


class ApiWorknodeExecutions(Base):
    __tablename__ = "api_worknode_executions"
    __table_args__ = (
        Index('ix_node_execution_id', 'node_execution_id'),
        Index('ix_node_executions_node_id', 'node_id'),
        {
            'comment': '节点执行记录表'
        }
    )

    node_execution_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    workflow_execution_id = Column(BigInteger, nullable=False, comment="执行器执行记录ID")
    node_id = Column(BigInteger, nullable=False, comment="节点ID")

    # 执行状态和时间
    status = Column(String(20), nullable=False, default="pending", comment="执行状态")
    start_time = Column(DateTime, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    duration = Column(Integer, comment="执行时长(毫秒)")

    # 执行数据
    input_data = Column(JSONB, comment="输入数据")
    output_data = Column(JSONB, comment="输出数据")
    context_snapshot = Column(JSONB, comment="执行时上下文快照")

    # 循环相关
    loop_index = Column(Integer, comment="循环索引")
    loop_item = Column(JSONB, comment="循环项数据")

    # 条件判断相关
    condition_result = Column(Boolean, comment="条件判断结果")

    # 错误信息
    error_message = Column(Text, comment="错误信息")
    error_details = Column(JSONB, comment="错误详情")

    # 执行次数(重试)
    retry_count = Column(Integer, default=0, comment="重试次数")


