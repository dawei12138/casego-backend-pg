from sqlalchemy import Boolean, Column, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from config.base import Base


class SchemaNode(Base):
    """
    JSON Schema 可视化节点表
    """

    __tablename__ = 'schema_nodes'
    __table_args__ = (
        Index('ix_schema_nodes_model_id', 'model_id'),
        Index('ix_schema_nodes_parent_id', 'parent_id'),
        Index('ix_schema_nodes_json_pointer', 'json_pointer'),
        Index('ix_schema_nodes_path', 'path'),
        {'comment': 'JSON Schema 可视化节点表'},
    )

    node_id = Column(String(64), primary_key=True, nullable=False, comment='节点ID')
    model_id = Column(String(64), nullable=False, comment='所属模型ID')
    parent_id = Column(String(64), nullable=True, comment='父节点ID')
    root_id = Column(String(64), nullable=True, comment='根节点ID')
    node_kind = Column(String(32), nullable=False, comment='节点类型：root/property/items/composition/ref')
    field_name = Column(String(128), nullable=True, comment='字段名')
    display_name = Column(String(128), nullable=True, comment='展示名')
    alias = Column(String(128), nullable=True, comment='字段映射名或代码生成别名')
    source_field_name = Column(String(128), nullable=True, comment='来源字段名')
    source_field_type = Column(String(128), nullable=True, comment='来源字段类型')
    source_field_comment = Column(Text, nullable=True, comment='来源字段注释')
    code_field_name = Column(String(128), nullable=True, comment='代码生成字段名')
    title = Column(String(256), nullable=True, comment='JSON Schema title')
    type = Column(String(32), nullable=False, comment='JSON Schema主类型')
    type_list = Column(JSONB, nullable=True, comment='多类型列表')
    nullable = Column(Boolean, nullable=False, default=False, comment='是否允许NULL')
    required = Column(Boolean, nullable=False, default=False, comment='是否必填')
    deprecated = Column(Boolean, nullable=False, default=False, comment='是否废弃')
    access_mode = Column(String(32), nullable=False, default='readWrite', comment='读写行为')
    format = Column(String(64), nullable=True, comment='format')
    default_value = Column(JSONB, nullable=True, comment='默认值')
    example_value = Column(JSONB, nullable=True, comment='示例值')
    examples = Column(JSONB, nullable=True, comment='示例值列表')
    enum_enabled = Column(Boolean, nullable=False, default=False, comment='是否启用枚举')
    enum_values = Column(JSONB, nullable=True, comment='枚举值')
    enum_meta = Column(JSONB, nullable=True, comment='枚举元数据')
    const_enabled = Column(Boolean, nullable=False, default=False, comment='是否启用常量')
    const_value = Column(JSONB, nullable=True, comment='常量值')
    mock_enabled = Column(Boolean, nullable=False, default=False, comment='是否启用Mock')
    mock_type = Column(String(32), nullable=True, comment='Mock类型')
    mock_rule = Column(String(256), nullable=True, comment='Mock规则')
    mock_value = Column(JSONB, nullable=True, comment='固定Mock值')
    mock_config = Column(JSONB, nullable=True, comment='Mock配置')
    constraints = Column(JSONB, nullable=True, comment='类型约束')
    composition = Column(JSONB, nullable=True, comment='组合结构配置')
    ref_config = Column(JSONB, nullable=True, comment='引用配置')
    xml_config = Column(JSONB, nullable=True, comment='XML配置')
    source = Column(String(32), nullable=True, comment='节点来源')
    source_path = Column(String(1024), nullable=True, comment='来源路径')
    import_hint = Column(JSONB, nullable=True, comment='导入推断信息')
    raw_schema = Column(JSONB, nullable=True, comment='当前节点原始Schema')
    raw_schema_extras = Column(JSONB, nullable=True, comment='不支持可视化的Schema关键字')
    ui_state = Column(JSONB, nullable=True, comment='前端临时状态')
    path = Column(String(1024), nullable=True, comment='字段路径')
    json_pointer = Column(String(1024), nullable=True, comment='JSON Pointer')
    level = Column(Integer, nullable=False, default=0, comment='层级')
    expanded = Column(Boolean, nullable=True, default=False, comment='是否展开')
    locked = Column(Boolean, nullable=True, default=False, comment='是否锁定')
    sort_no = Column(Float, nullable=False, default=0, comment='排序号')
