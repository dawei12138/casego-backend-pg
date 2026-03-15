from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query


class Api_param_itemModel(BaseModel):
    """
    参数化数据行表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    key_id: Optional[int] = Field(default=None, description='主键ID')
    parameterization_id: Optional[int] = Field(default=None, description='所属参数表ID')
    group_name: Optional[str] = Field(default=None, description='参数分组')
    key: Optional[str] = Field(default=None, description='参数键')
    value: Optional[str] = Field(default=None, description='参数值')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    item: Optional[dict] = Field(default={}, description='节点配置信息')

    @NotBlank(field_name='parameterization_id', message='所属参数表ID不能为空')
    def get_parameterization_id(self):
        return self.parameterization_id

    def validate_fields(self):
        self.get_parameterization_id()


class Api_param_itemQueryModel(Api_param_itemModel):
    """
    参数化数据行不分页查询模型
    """
    pass


@as_query
class Api_param_itemPageQueryModel(Api_param_itemQueryModel):
    """
    参数化数据行分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteApi_param_itemModel(BaseModel):
    """
    删除参数化数据行模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    key_ids: str = Field(description='需要删除的主键ID')
