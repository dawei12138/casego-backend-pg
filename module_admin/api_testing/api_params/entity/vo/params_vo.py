from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional

from config.enums import DataTypeEnum
from module_admin.annotation.pydantic_annotation import as_query


class ParamsModel(BaseModel):
    """
    接口请求参数表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    param_id: Optional[int] = Field(default=None, description='ID')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    key: Optional[str] = Field(default=None, description='参数键名')
    value: Optional[str] = Field(default=None, description='参数值')
    is_run: Optional[int] = Field(default=None, description='是否启用该参数')
    is_required: Optional[int] = Field(default=None, description='是否必填')
    description: Optional[str] = Field(default=None, description='描述')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    data_type: Optional[DataTypeEnum] = Field(default=DataTypeEnum.STRING, description='数据类型枚举')

    @field_validator('data_type')
    @classmethod
    def validate_data_type(cls, v):
        if v == DataTypeEnum.FILE:
            raise ValueError('FILE类型不被允许，请选择其他数据类型')
        return v

    @NotBlank(field_name='case_id', message='关联的测试用例ID不能为空')
    def get_case_id(self):
        return self.case_id

    @NotBlank(field_name='key', message='参数键名不能为空')
    def get_key(self):
        return self.key

    def validate_fields(self):
        self.get_case_id()
        self.get_key()


class ParamsQueryModel(ParamsModel):
    """
    接口请求参数不分页查询模型
    """
    pass


@as_query
class ParamsPageQueryModel(ParamsQueryModel):
    """
    接口请求参数分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteParamsModel(BaseModel):
    """
    删除接口请求参数模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    param_ids: str = Field(description='需要删除的ID')
