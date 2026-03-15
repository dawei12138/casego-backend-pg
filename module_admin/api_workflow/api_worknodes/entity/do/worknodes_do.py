import enum

from sqlalchemy import Integer, JSON, Column, DateTime, Enum, String, SmallInteger, Float, Index, BigInteger, Boolean, \
    Text
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class NodeTypeEnum(str, enum.Enum):
    """节点类型枚举"""
    IF = "if"  # 条件判断节点
    ELSE = "else"  # 条件判断else节点
    FOR = "for"  # 循环节点
    FOREACH = "foreach"  # 遍历节点
    GROUP = "group"  # 分组节点
    TASK = "task"  # 任务节点


class ApiWorknodes(Base):
    __tablename__ = "api_worknodes"
    __table_args__ = (
        Index('ix_executor_nodes_parent_id', 'parent_id'),
        Index('ix_executor_nodes_type', 'type'),
        {
            'comment': '执行器节点表'
        }
    )

    node_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    workflow_id = Column(BigInteger, nullable=True, comment="所属执行器ID")
    parent_id = Column(String(50), nullable=True, comment="父节点ID")

    # 节点基本信息
    name = Column(String(200), comment="节点名称")
    type = Column(Enum(NodeTypeEnum, name="NodeTypeEnum"), comment="节点类型")
    is_run = Column(Boolean, default=True, comment="是否启用执行")

    children_ids = Column(JSONB, comment="子结点列表")
    # 节点配置 - 根据不同类型存储不同配置
    config = Column(JSONB, comment="节点配置信息")



