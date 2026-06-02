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
