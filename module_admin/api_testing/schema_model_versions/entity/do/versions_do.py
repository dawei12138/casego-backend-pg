from sqlalchemy import Boolean, Column, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from config.base import Base


class SchemaModelVersion(Base):
    """
    JSON Schema 模型版本表
    """

    __tablename__ = 'schema_model_versions'
    __table_args__ = (
        Index('ix_schema_model_versions_model_id', 'model_id'),
        Index('ix_schema_model_versions_revision', 'revision'),
        {'comment': 'JSON Schema 模型版本表'},
    )

    version_id = Column(String(64), primary_key=True, nullable=False, comment='版本ID')
    model_id = Column(String(64), nullable=False, comment='模型ID')
    version = Column(Integer, nullable=False, comment='内部版本号')
    revision = Column(String(32), nullable=True, comment='语义版本号')
    schema_snapshot = Column(JSONB, nullable=False, comment='Schema快照')
    nodes_snapshot = Column(JSONB, nullable=True, comment='节点快照')
    change_log = Column(Text, nullable=True, comment='变更说明')



