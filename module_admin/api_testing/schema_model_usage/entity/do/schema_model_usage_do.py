from sqlalchemy import Column, Index, String
from config.base import Base


class SchemaModelUsage(Base):
    """
    JSON Schema 模型使用关系表
    """

    __tablename__ = 'schema_model_usage'
    __table_args__ = (
        Index('ix_schema_model_usage_model_id', 'model_id'),
        Index('ix_schema_model_usage_target', 'usage_type', 'usage_target_id'),
        {'comment': 'JSON Schema 模型使用关系表'},
    )

    usage_id = Column(String(64), primary_key=True, nullable=False, comment='使用关系ID')
    model_id = Column(String(64), nullable=False, comment='模型ID')
    usage_type = Column(String(32), nullable=False, comment='使用类型')
    usage_target_id = Column(String(64), nullable=False, comment='使用目标ID')
    usage_target_name = Column(String(256), nullable=True, comment='使用目标名称')



