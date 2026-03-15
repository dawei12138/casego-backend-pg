from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Public_steps_stepsModel(BaseModel):
    """
    公共步骤-步骤关联表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    public_steps_id: Optional[int] = Field(default=None, description='公共步骤ID')
    steps_id: Optional[int] = Field(default=None, description='步骤ID')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')






class Public_steps_stepsQueryModel(Public_steps_stepsModel):
    """
    公共步骤-步骤关联不分页查询模型
    """
    pass


@as_query
class Public_steps_stepsPageQueryModel(Public_steps_stepsQueryModel):
    """
    公共步骤-步骤关联分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeletePublic_steps_stepsModel(BaseModel):
    """
    删除公共步骤-步骤关联模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    public_steps_ids: str = Field(description='需要删除的公共步骤ID')
