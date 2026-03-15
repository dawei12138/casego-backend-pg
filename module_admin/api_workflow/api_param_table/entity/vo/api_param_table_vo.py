from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, List
from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemModel


class Api_param_tableModel(BaseModel):
    """
    参数化数据主表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    parameterization_id: Optional[int] = Field(default=None, description='主键ID')
    workflow_id: Optional[int] = Field(default=None, description='所属执行器ID')
    name: Optional[str] = Field(default=None, description='参数表名称')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')


class Api_param_tableQueryModel(Api_param_tableModel):
    """
    参数化数据主不分页查询模型
    """
    pass


class Api_param_table_itemModel(Api_param_tableModel):
    """
    参数化数据主不分页查询模型
    """
    items: Optional[List[Api_param_itemModel]] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
    total: Optional[int] = Field(default=None, description='每页记录数')


@as_query
class Api_param_tablePageQueryModel(Api_param_tableQueryModel):
    """
    参数化数据主分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteApi_param_tableModel(BaseModel):
    """
    删除参数化数据主模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    parameterization_ids: str = Field(description='需要删除的主键ID')
