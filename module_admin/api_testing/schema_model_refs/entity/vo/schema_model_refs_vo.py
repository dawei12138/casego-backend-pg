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




class Schema_model_refsModel(BaseModel):
    """
    JSON Schema 模型引用关系表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    ref_id: Optional[str] = Field(default=None, description='引用ID')
    model_id: Optional[str] = Field(default=None, description='模型ID')
    ref_model_id: Optional[str] = Field(default=None, description='被引用模型ID')
    ref_path: Optional[str] = Field(default=None, description='引用路径')
    ref_version: Optional[str] = Field(default=None, description='引用版本')
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

    @NotBlank(field_name='ref_model_id', message='被引用模型ID不能为空')
    def get_ref_model_id(self):
        return self.ref_model_id


    def validate_fields(self):
        self.get_model_id()
        self.get_ref_model_id()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'ref_id': 'refId',
                'ref_path': 'refPath',
                'ref_version': 'refVersion',
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




class Schema_model_refsQueryModel(Schema_model_refsModel):
    """
    JSON Schema 模型引用关系不分页查询模型
    """
    pass


@as_query
class Schema_model_refsPageQueryModel(Schema_model_refsQueryModel):
    """
    JSON Schema 模型引用关系分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSchema_model_refsModel(BaseModel):
    """
    删除JSON Schema 模型引用关系模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ref_ids: str = Field(description='需要删除的引用ID')
