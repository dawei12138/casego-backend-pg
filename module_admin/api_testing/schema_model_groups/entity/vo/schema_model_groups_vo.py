from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank

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


class Schema_model_groupsModel(BaseModel):
    """
    JSON Schema 数据模型目录表对应pydantic模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    group_id: Optional[str] = Field(default=None, description='目录ID')
    project_id: Optional[int] = Field(default=None, description='所属项目ID')
    branch_id: Optional[str] = Field(default=None, description='所属分支ID')
    parent_id: Optional[str] = Field(default=None, description='父目录ID')
    name: Optional[str] = Field(default=None, description='目录名称')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    description: Optional[str] = Field(default=None, description='')
    sort_no: Optional[float] = Field(default=None, description='排序号')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='project_id', message='所属项目ID不能为空')
    def get_project_id(self):
        return self.project_id

    @NotBlank(field_name='name', message='目录名称不能为空')
    def get_name(self):
        return self.name

    def validate_fields(self):
        self.get_project_id()
        self.get_name()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'group_id': 'groupId',
                'branch_id': 'branchId',
                'parent_id': 'parentId',
                'name': 'name',
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


class Schema_model_groupsQueryModel(Schema_model_groupsModel):
    """
    JSON Schema 数据模型目录不分页查询模型
    """

    pass


@as_query
class Schema_model_groupsPageQueryModel(Schema_model_groupsQueryModel):
    """
    JSON Schema 数据模型目录分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSchema_model_groupsModel(BaseModel):
    """
    删除JSON Schema 数据模型目录模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    group_ids: str = Field(description='需要删除的目录ID')
