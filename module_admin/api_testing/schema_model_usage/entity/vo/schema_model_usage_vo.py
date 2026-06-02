from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
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




class Schema_model_usageModel(BaseModel):
    """
    JSON Schema 模型使用关系表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    usage_id: Optional[str] = Field(default=None, description='使用关系ID')
    model_id: Optional[str] = Field(default=None, description='模型ID')
    usage_type: Optional[str] = Field(default=None, description='使用类型')
    usage_target_id: Optional[str] = Field(default=None, description='使用目标ID')
    usage_target_name: Optional[str] = Field(default=None, description='使用目标名称')
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

    @NotBlank(field_name='usage_type', message='使用类型不能为空')
    def get_usage_type(self):
        return self.usage_type

    @NotBlank(field_name='usage_target_id', message='使用目标ID不能为空')
    def get_usage_target_id(self):
        return self.usage_target_id


    def validate_fields(self):
        self.get_model_id()
        self.get_usage_type()
        self.get_usage_target_id()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'usage_id': 'usageId',
                'usage_target_name': 'usageTargetName',
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




class Schema_model_usageQueryModel(Schema_model_usageModel):
    """
    JSON Schema 模型使用关系不分页查询模型
    """
    pass


@as_query
class Schema_model_usagePageQueryModel(Schema_model_usageQueryModel):
    """
    JSON Schema 模型使用关系分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSchema_model_usageModel(BaseModel):
    """
    删除JSON Schema 模型使用关系模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    usage_ids: str = Field(description='需要删除的使用关系ID')
