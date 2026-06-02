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




class VersionsModel(BaseModel):
    """
    JSON Schema 模型版本表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    version_id: Optional[str] = Field(default=None, description='版本ID')
    model_id: Optional[str] = Field(default=None, description='模型ID')
    version: Optional[int] = Field(default=None, description='内部版本号')
    revision: Optional[str] = Field(default=None, description='语义版本号')
    schema_snapshot: Optional[Any] = Field(default=None, description='Schema快照')
    nodes_snapshot: Optional[Any] = Field(default=None, description='节点快照')
    change_log: Optional[str] = Field(default=None, description='变更说明')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    description: Optional[str] = Field(default=None, description='')
    sort_no: Optional[float] = Field(default=None, description='')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='model_id', message='模型ID不能为空')
    def get_model_id(self):
        return self.model_id

    @NotBlank(field_name='version', message='内部版本号不能为空')
    def get_version(self):
        return self.version

    @NotBlank(field_name='schema_snapshot', message='Schema快照不能为空')
    def get_schema_snapshot(self):
        return self.schema_snapshot


    def validate_fields(self):
        self.get_model_id()
        self.get_version()
        self.get_schema_snapshot()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'version_id': 'versionId',
                'revision': 'revision',
                'change_log': 'changeLog',
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




class VersionsQueryModel(VersionsModel):
    """
    JSON Schema 模型版本不分页查询模型
    """
    pass


@as_query
class VersionsPageQueryModel(VersionsQueryModel):
    """
    JSON Schema 模型版本分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteVersionsModel(BaseModel):
    """
    删除JSON Schema 模型版本模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    version_ids: str = Field(description='需要删除的版本ID')
