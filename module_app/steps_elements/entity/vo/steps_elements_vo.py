from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Steps_elementsModel(BaseModel):
    """
    步骤-元素关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    steps_id: Optional[int] = Field(default=None, description='步骤ID')
    elements_id: Optional[int] = Field(default=None, description='元素ID')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')






class Steps_elementsQueryModel(Steps_elementsModel):
    """
    步骤-元素关联不分页查询模型
    """
    pass


@as_query
class Steps_elementsPageQueryModel(Steps_elementsQueryModel):
    """
    步骤-元素关联分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSteps_elementsModel(BaseModel):
    """
    删除步骤-元素关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    steps_ids: str = Field(description='需要删除的步骤ID')
