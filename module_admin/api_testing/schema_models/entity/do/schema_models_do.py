from sqlalchemy import Boolean, Column, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from config.base import Base


class SchemaModel(Base):
    """
    JSON Schema 数据模型主表
    """

    __tablename__ = 'schema_models'
    __table_args__ = (
        Index('ix_schema_models_project_id', 'project_id'),
        Index('ix_schema_models_group_id', 'group_id'),
        Index('ix_schema_models_name', 'name'),
        Index('ix_schema_models_status', 'status'),
        {'comment': 'JSON Schema 数据模型主表'},
    )

    model_id = Column(String(64), primary_key=True, nullable=False, comment='模型ID')
    project_id = Column(Integer, nullable=False, comment='所属项目ID')
    case_id = Column(Integer, nullable=True, comment='关联的测试用例ID')
    group_id = Column(String(64), nullable=True, comment='所属分组ID')
    name = Column(String(128), nullable=True, comment='模型唯一名称')
    display_name = Column(String(128), nullable=True, comment='展示名称')
    title = Column(String(256), nullable=True, comment='JSON Schema标题')
    schema_draft = Column(String(32), nullable=True, default='draft-07', comment='JSON Schema版本')
    root_node_id = Column(String(64), nullable=True, comment='根节点ID')
    model_category = Column(String(32), nullable=True, comment='模型分类：request/response/common/enum/dto')
    model_role = Column(String(32), nullable=True, comment='模型角色：input/output/entity/enum')
    parent_model_id = Column(String(64), nullable=True, comment='派生来源模型ID')
    source_model_name = Column(String(128), nullable=True, comment='来源模型名称')
    code_class_name = Column(String(128), nullable=True, comment='代码生成类名')
    code_file_name = Column(String(256), nullable=True, comment='代码生成文件名')
    source_table_name = Column(String(128), nullable=True, comment='来源数据库表名')
    visibility = Column(String(32), nullable=False, default='project', comment='可见性：private/project/public')
    status = Column(String(32), nullable=False, default='draft', comment='状态：draft/published/deprecated')
    version = Column(Integer, nullable=False, default=1, comment='内部版本号')
    revision = Column(String(32), nullable=True, comment='语义版本号')
    source_type = Column(String(32), nullable=False, default='manual', comment='来源类型：manual/json/openapi/database/code')
    source_id = Column(String(128), nullable=True, comment='来源业务ID')
    raw_schema = Column(JSONB, nullable=True, comment='原始JSON Schema')
    raw_schema_extras = Column(JSONB, nullable=True, comment='模型级扩展Schema关键字')
    generated_schema = Column(JSONB, nullable=True, comment='生成后的JSON Schema')
    tags = Column(JSONB, nullable=True, comment='标签')


