from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Any, List, Optional
from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel


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




class Schema_modelsModel(BaseModel):
    """
    JSON Schema 数据模型主表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    model_id: Optional[str] = Field(default=None, description='模型ID')
    project_id: Optional[int] = Field(default=None, description='所属项目ID')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    group_id: Optional[str] = Field(default=None, description='所属分组ID')
    name: Optional[str] = Field(default=None, description='模型唯一名称')
    display_name: Optional[str] = Field(default=None, description='展示名称')
    title: Optional[str] = Field(default=None, description='JSON Schema标题')
    schema_draft: Optional[str] = Field(default=None, description='JSON Schema版本')
    root_node_id: Optional[str] = Field(default=None, description='根节点ID')
    model_category: Optional[str] = Field(default=None, description='模型分类：request/response/common/enum/dto')
    model_role: Optional[str] = Field(default=None, description='模型角色：input/output/entity/enum')
    parent_model_id: Optional[str] = Field(default=None, description='派生来源模型ID')
    source_model_name: Optional[str] = Field(default=None, description='来源模型名称')
    code_class_name: Optional[str] = Field(default=None, description='代码生成类名')
    code_file_name: Optional[str] = Field(default=None, description='代码生成文件名')
    source_table_name: Optional[str] = Field(default=None, description='来源数据库表名')
    visibility: Optional[str] = Field(default=None, description='可见性：private/project/public')
    status: Optional[str] = Field(default=None, description='状态：draft/published/deprecated')
    version: Optional[int] = Field(default=None, description='内部版本号')
    revision: Optional[str] = Field(default=None, description='语义版本号')
    source_type: Optional[str] = Field(default=None, description='来源类型：manual/json/openapi/database/code')
    source_id: Optional[str] = Field(default=None, description='来源业务ID')
    raw_schema: Optional[Any] = Field(default=None, description='原始JSON Schema')
    raw_schema_extras: Optional[Any] = Field(default=None, description='模型级扩展Schema关键字')
    generated_schema: Optional[Any] = Field(default=None, description='生成后的JSON Schema')
    tags: Optional[Any] = Field(default=None, description='标签')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    description: Optional[str] = Field(default=None, description='')
    sort_no: Optional[float] = Field(default=None, description='')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='project_id', message='所属项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='visibility', message='可见性：private/project/public不能为空')
    def get_visibility(self):
        return self.visibility

    @NotBlank(field_name='status', message='状态：draft/published/deprecated不能为空')
    def get_status(self):
        return self.status

    @NotBlank(field_name='version', message='内部版本号不能为空')
    def get_version(self):
        return self.version

    @NotBlank(field_name='source_type', message='来源类型：manual/json/openapi/database/code不能为空')
    def get_source_type(self):
        return self.source_type


    def validate_fields(self):
        self.get_project_id()
        self.get_visibility()
        self.get_status()
        self.get_version()
        self.get_source_type()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'model_id': 'modelId',
                'case_id': 'caseId',
                'group_id': 'groupId',
                'name': 'name',
                'display_name': 'displayName',
                'title': 'title',
                'schema_draft': 'schemaDraft',
                'root_node_id': 'rootNodeId',
                'model_category': 'modelCategory',
                'model_role': 'modelRole',
                'parent_model_id': 'parentModelId',
                'source_model_name': 'sourceModelName',
                'code_class_name': 'codeClassName',
                'code_file_name': 'codeFileName',
                'source_table_name': 'sourceTableName',
                'revision': 'revision',
                'source_id': 'sourceId',
                'create_by': 'createBy',
                'create_time': 'createTime',
                'update_by': 'updateBy',
                'update_time': 'updateTime',
                'remark': 'remark',
                'description': 'description',
                'sort_no': 'sortNo',
                'del_flag': 'delFlag',
            },
        )




class Schema_modelsQueryModel(Schema_modelsModel):
    """
    JSON Schema 数据模型主不分页查询模型
    """
    pass


@as_query
class Schema_modelsPageQueryModel(Schema_modelsQueryModel):
    """
    JSON Schema 数据模型主分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSchema_modelsModel(BaseModel):
    """
    删除JSON Schema 数据模型主模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    model_ids: str = Field(description='需要删除的模型ID')


class CreateSchemaModelWithRootModel(BaseModel):
    """
    创建JSON Schema 数据模型及根节点请求模型
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    model: Schema_modelsModel = Field(description='模型主信息')
    root_node: Schema_nodesModel = Field(description='根节点信息')


class SchemaModelPreviewRequestModel(BaseModel):
    """
    JSON Schema 数据模型预览请求
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    model: Optional[Schema_modelsModel] = Field(default=None, description='模型主信息')
    nodes: List[Schema_nodesModel] = Field(default_factory=list, description='当前模型节点，允许包含未保存修改')


class SchemaModelPreviewResponseModel(BaseModel):
    """
    JSON Schema 数据模型预览响应
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    example: Any = Field(default=None, description='根据节点与Mock规则生成的示例JSON')
    json_schema: Any = Field(default=None, alias='schema', description='根据节点生成的JSON Schema')
    warnings: List[str] = Field(default_factory=list, description='生成过程中的非阻塞提示')
