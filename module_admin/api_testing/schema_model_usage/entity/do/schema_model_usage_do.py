from sqlalchemy import Column, DateTime, Float, String, Text, Index
from config.base import Base


class SchemaModelRef(Base):
    """
    JSON Schema 模型引用关系表
    """

    __tablename__ = 'schema_model_refs'
    __table_args__ = (
        Index('ix_schema_model_refs_model_id', 'model_id'),
        Index('ix_schema_model_refs_ref_model_id', 'ref_model_id'),
        {'comment': 'JSON Schema 模型引用关系表'},
    )

    ref_id = Column(String(64), primary_key=True, nullable=False, comment='引用ID')
    model_id = Column(String(64), nullable=False, comment='模型ID')
    ref_model_id = Column(String(64), nullable=False, comment='被引用模型ID')
    ref_path = Column(String(512), nullable=True, comment='引用路径')
    ref_version = Column(String(32), nullable=True, comment='引用版本')




