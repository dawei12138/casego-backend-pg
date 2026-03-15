from sqlalchemy import Column, Float, Text, String, BigInteger, DateTime, Integer, Index, JSON, Enum
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApiParamItem(Base):
    __tablename__ = "api_param_item"
    __table_args__ = (
        Index('ix_param_item_table_id', 'parameterization_id'),
        {'comment': '参数化数据表行'},
    )

    key_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='主键ID')
    parameterization_id = Column(BigInteger, nullable=True, comment='所属参数表ID')
    group_name = Column(String(100), nullable=True, comment='参数分组')
    key = Column(String(100), nullable=True, comment='参数键')
    value = Column(Text, nullable=True, comment='参数值')
    item = Column(JSONB, default={}, comment="节点配置信息")
