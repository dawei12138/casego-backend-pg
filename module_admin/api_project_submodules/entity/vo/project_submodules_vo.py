from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional

from config.enums import Module_type
from module_admin.annotation.pydantic_annotation import as_query


class Project_submodulesModel(BaseModel):
    """
    项目模块表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='ID')
    name: Optional[str] = Field(default=None, description='模块名称')
    # type: # Module_type = Field(default=None, description='模块类型 (1: 接口模块, 2: 套件模块, 3: UI模块)')
    type: Optional[str] = Field(default=None, description='模块类型 (1: 接口模块, 2: 套件模块, 3: UI模块)')
    parent_id: Optional[int] = Field(default=None, description='父id')
    ancestors: Optional[str] = Field(default=None, description='祖级列表')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    project_id: Optional[int] = Field(default=None, description='所属项目id')


class Project_submodulesQueryModel(Project_submodulesModel):
    """
    项目模块不分页查询模型
    """
    pass


@as_query
class Project_submodulesPageQueryModel(Project_submodulesQueryModel):
    """
    项目模块分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProject_submodulesModel(BaseModel):
    """
    删除项目模块模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的ID')


class AddProject_submodulesModel(Project_submodulesModel):
    """
    删除项目模块模型
    """
    project_id: Optional[int] = Field(default=None, description='ID')
