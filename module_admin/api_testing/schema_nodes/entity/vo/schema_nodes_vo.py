from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Any, Optional
from module_admin.annotation.pydantic_annotation import as_query


def is_empty_generated_value(value):
    return value == '' or (isinstance(value, (list, dict)) and len(value) == 0)


def normalize_empty_generated_values(values, field_alias_map):
    if not isinstance(values, dict):
        return values
    data = values.copy()
    for field_name, alias_name in field_alias_map.items():
        for key in {field_name, alias_name}:
            if key in data and is_empty_generated_value(data.get(key)):
                data[key] = None
    return data




class Schema_nodesModel(BaseModel):
    """
    JSON Schema 可视化节点表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    node_id: Optional[str] = Field(default=None, description='节点ID')
    model_id: Optional[str] = Field(default=None, description='所属模型ID')
    parent_id: Optional[str] = Field(default=None, description='父节点ID')
    root_id: Optional[str] = Field(default=None, description='根节点ID')
    node_kind: Optional[str] = Field(default=None, description='节点类型：root/property/items/composition/ref')
    field_name: Optional[str] = Field(default=None, description='字段名')
    display_name: Optional[str] = Field(default=None, description='展示名')
    alias: Optional[str] = Field(default=None, description='字段映射名或代码生成别名')
    source_field_name: Optional[str] = Field(default=None, description='来源字段名')
    source_field_type: Optional[str] = Field(default=None, description='来源字段类型')
    source_field_comment: Optional[str] = Field(default=None, description='来源字段注释')
    code_field_name: Optional[str] = Field(default=None, description='代码生成字段名')
    title: Optional[str] = Field(default=None, description='JSON Schema title')
    type: Optional[str] = Field(default=None, description='JSON Schema主类型')
    type_list: Optional[Any] = Field(default=None, description='多类型列表')
    nullable: Optional[bool] = Field(default=None, description='是否允许NULL')
    required: Optional[bool] = Field(default=None, description='是否必填')
    deprecated: Optional[bool] = Field(default=None, description='是否废弃')
    access_mode: Optional[str] = Field(default=None, description='读写行为')
    format: Optional[str] = Field(default=None, description='format')
    default_value: Optional[Any] = Field(default=None, description='默认值')
    example_value: Optional[Any] = Field(default=None, description='示例值')
    examples: Optional[Any] = Field(default=None, description='示例值列表')
    enum_enabled: Optional[bool] = Field(default=None, description='是否启用枚举')
    enum_values: Optional[Any] = Field(default=None, description='枚举值')
    enum_meta: Optional[Any] = Field(default=None, description='枚举元数据')
    const_enabled: Optional[bool] = Field(default=None, description='是否启用常量')
    const_value: Optional[Any] = Field(default=None, description='常量值')
    mock_enabled: Optional[bool] = Field(default=None, description='是否启用Mock')
    mock_type: Optional[str] = Field(default=None, description='Mock类型')
    mock_rule: Optional[str] = Field(default=None, description='Mock规则')
    mock_value: Optional[Any] = Field(default=None, description='固定Mock值')
    mock_config: Optional[Any] = Field(default=None, description='Mock配置')
    constraints: Optional[Any] = Field(default=None, description='类型约束')
    composition: Optional[Any] = Field(default=None, description='组合结构配置')
    ref_config: Optional[Any] = Field(default=None, description='引用配置')
    xml_config: Optional[Any] = Field(default=None, description='XML配置')
    source: Optional[str] = Field(default=None, description='节点来源')
    source_path: Optional[str] = Field(default=None, description='来源路径')
    import_hint: Optional[Any] = Field(default=None, description='导入推断信息')
    raw_schema: Optional[Any] = Field(default=None, description='当前节点原始Schema')
    raw_schema_extras: Optional[Any] = Field(default=None, description='不支持可视化的Schema关键字')
    ui_state: Optional[Any] = Field(default=None, description='前端临时状态')
    path: Optional[str] = Field(default=None, description='字段路径')
    json_pointer: Optional[str] = Field(default=None, description='JSON Pointer')
    level: Optional[int] = Field(default=None, description='层级')
    expanded: Optional[bool] = Field(default=None, description='是否展开')
    locked: Optional[bool] = Field(default=None, description='是否锁定')
    sort_no: Optional[float] = Field(default=None, description='排序号')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    description: Optional[str] = Field(default=None, description='')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='model_id', message='所属模型ID不能为空')
    def get_model_id(self):
        return self.model_id

    @NotBlank(field_name='node_kind', message='节点类型：root/property/items/composition/ref不能为空')
    def get_node_kind(self):
        return self.node_kind

    @NotBlank(field_name='type', message='JSON Schema主类型不能为空')
    def get_type(self):
        return self.type

    @NotBlank(field_name='nullable', message='是否允许NULL不能为空')
    def get_nullable(self):
        return self.nullable

    @NotBlank(field_name='required', message='是否必填不能为空')
    def get_required(self):
        return self.required

    @NotBlank(field_name='deprecated', message='是否废弃不能为空')
    def get_deprecated(self):
        return self.deprecated

    @NotBlank(field_name='access_mode', message='读写行为不能为空')
    def get_access_mode(self):
        return self.access_mode

    @NotBlank(field_name='enum_enabled', message='是否启用枚举不能为空')
    def get_enum_enabled(self):
        return self.enum_enabled

    @NotBlank(field_name='const_enabled', message='是否启用常量不能为空')
    def get_const_enabled(self):
        return self.const_enabled

    @NotBlank(field_name='mock_enabled', message='是否启用Mock不能为空')
    def get_mock_enabled(self):
        return self.mock_enabled

    @NotBlank(field_name='level', message='层级不能为空')
    def get_level(self):
        return self.level

    @NotBlank(field_name='sort_no', message='排序号不能为空')
    def get_sort_no(self):
        return self.sort_no


    def validate_fields(self):
        self.get_model_id()
        self.get_node_kind()
        self.get_type()
        self.get_nullable()
        self.get_required()
        self.get_deprecated()
        self.get_access_mode()
        self.get_enum_enabled()
        self.get_const_enabled()
        self.get_mock_enabled()
        self.get_level()
        self.get_sort_no()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'node_id': 'nodeId',
                'parent_id': 'parentId',
                'root_id': 'rootId',
                'field_name': 'fieldName',
                'display_name': 'displayName',
                'alias': 'alias',
                'source_field_name': 'sourceFieldName',
                'source_field_type': 'sourceFieldType',
                'source_field_comment': 'sourceFieldComment',
                'code_field_name': 'codeFieldName',
                'title': 'title',
                'format': 'format',
                'mock_type': 'mockType',
                'mock_rule': 'mockRule',
                'source': 'source',
                'source_path': 'sourcePath',
                'path': 'path',
                'json_pointer': 'jsonPointer',
                'expanded': 'expanded',
                'locked': 'locked',
                'create_by': 'createBy',
                'create_time': 'createTime',
                'update_by': 'updateBy',
                'update_time': 'updateTime',
                'remark': 'remark',
                'description': 'description',
                'del_flag': 'delFlag',
            },
        )




class Schema_nodesQueryModel(Schema_nodesModel):
    """
    JSON Schema 可视化节点不分页查询模型
    """
    pass


@as_query
class Schema_nodesPageQueryModel(Schema_nodesQueryModel):
    """
    JSON Schema 可视化节点分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSchema_nodesModel(BaseModel):
    """
    删除JSON Schema 可视化节点模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    node_ids: str = Field(description='需要删除的节点ID')
