from datetime import date, datetime
from decimal import Decimal
from module_admin.module_demo.module_uuid_demo.entity.enums.module_uuid_demo_enum import ModuleUuidDemoTypeEnum
from uuid import UUID
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




class Module_uuid_demoModel(BaseModel):
    """
    UUID主键业务示例表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[UUID] = Field(default=None, description='主键ID-uuid')
    title: Optional[str] = Field(default=None, description='业务标题')
    business_code: Optional[str] = Field(default=None, description='业务编号')
    customer_name: Optional[str] = Field(default=None, description='客户名称')
    status: Optional[str] = Field(default=None, description='业务状态')
    priority: Optional[int] = Field(default=None, description='优先级')
    amount: Optional[Decimal] = Field(default=None, description='业务金额')
    enabled: Optional[bool] = Field(default=None, description='是否启用')
    occurred_date: Optional[date] = Field(default=None, description='发生日期')
    closed_time: Optional[datetime] = Field(default=None, description='关闭时间')
    extra_info: Optional[Any] = Field(default=None, description='扩展信息')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[int] = Field(default=None, description='排序号')
    del_flag: Optional[str] = Field(default=None, description='删除标志')
    type: Optional[ModuleUuidDemoTypeEnum] = Field(default=None, description='业务类型')

    @NotBlank(field_name='title', message='业务标题不能为空')
    def get_title(self):
        return self.title

    @NotBlank(field_name='type', message='业务类型不能为空')
    def get_type(self):
        return self.type

    def validate_fields(self):
        self.get_title()
        self.get_type()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'id': 'id',
                'business_code': 'businessCode',
                'customer_name': 'customerName',
                'status': 'status',
                'priority': 'priority',
                'amount': 'amount',
                'enabled': 'enabled',
                'occurred_date': 'occurredDate',
                'closed_time': 'closedTime',
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




class Module_uuid_demoQueryModel(Module_uuid_demoModel):
    """
    UUID主键业务示例不分页查询模型
    """
    pass


@as_query
class Module_uuid_demoPageQueryModel(Module_uuid_demoQueryModel):
    """
    UUID主键业务示例分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteModule_uuid_demoModel(BaseModel):
    """
    删除UUID主键业务示例模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID-uuid')
