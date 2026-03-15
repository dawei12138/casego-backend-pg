from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query
from module_app.enums import PlatformEnum, ConditionTypeEnum, BoolFlagEnum, StepErrorEnum


class StepsModel(BaseModel):
    """
    测试步骤表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='主键ID')
    case_id: Optional[int] = Field(default=None, description='所属测试用例ID')
    project_id: Optional[int] = Field(default=None, description='所属项目ID')
    parent_id: Optional[int] = Field(default=None, description='父级步骤ID(用于条件分支)')
    step_type: Optional[str] = Field(default=None, description='步骤类型: click/sendKeys/swipe/getText等')
    content: Optional[str] = Field(default=None, description='输入内容/操作参数')
    text: Optional[str] = Field(default=None, description='附加信息(JSON格式)')
    platform: Optional[PlatformEnum] = Field(default=None, description='平台类型')
    error: Optional[StepErrorEnum] = Field(default=None, description='异常处理方式')
    condition_type: Optional[ConditionTypeEnum] = Field(default=None, description='条件类型')
    disabled: Optional[BoolFlagEnum] = Field(default=None, description='是否禁用')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')






class StepsQueryModel(StepsModel):
    """
    测试步骤不分页查询模型
    """
    pass


@as_query
class StepsPageQueryModel(StepsQueryModel):
    """
    测试步骤分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteStepsModel(BaseModel):
    """
    删除测试步骤模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID')
