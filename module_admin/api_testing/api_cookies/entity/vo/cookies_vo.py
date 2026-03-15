from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional

from config.enums import DataTypeEnum
from module_admin.annotation.pydantic_annotation import as_query


class CookiesModel(BaseModel):
    """
    接口请求Cookie表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    cookie_id: Optional[int] = Field(default=None, description='ID')
    case_id: Optional[int] = Field(default=None, description='关联的测试用例ID')
    key: Optional[str] = Field(default=None, description='Cookie键名')
    value: Optional[str] = Field(default=None, description='Cookie值')
    domain: Optional[str] = Field(default=None, description='作用域')
    path: Optional[str] = Field(default=None, description='路径')
    is_run: Optional[int] = Field(default=None, description='是否启用该Cookie')
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

    @NotBlank(field_name='key', message='Cookie键名不能为空')
    def get_key(self):
        return self.key

    def validate_fields(self):
        self.get_case_id()
        self.get_key()


class CookiesQueryModel(CookiesModel):
    """
    接口请求Cookie不分页查询模型
    """
    pass


@as_query
class CookiesPageQueryModel(CookiesQueryModel):
    """
    接口请求Cookie分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteCookiesModel(BaseModel):
    """
    删除接口请求Cookie模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    cookie_ids: str = Field(description='需要删除的ID')
