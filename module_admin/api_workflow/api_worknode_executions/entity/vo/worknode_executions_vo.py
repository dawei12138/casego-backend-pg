from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Worknode_executionsModel(BaseModel):
    """
    节点执行记录表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    node_execution_id: Optional[int] = Field(default=None, description='节点执行记录ID')
    workflow_execution_id: Optional[int] = Field(default=None, description='执行器执行记录ID')
    node_id: Optional[int] = Field(default=None, description='节点ID')
    status: Optional[str] = Field(default=None, description='执行状态')
    start_time: Optional[datetime] = Field(default=None, description='开始时间')
    end_time: Optional[datetime] = Field(default=None, description='结束时间')
    duration: Optional[int] = Field(default=None, description='执行时长(毫秒)')
    input_data: Optional[dict] = Field(default=None, description='输入数据')
    output_data: Optional[dict] = Field(default=None, description='输出数据')
    context_snapshot: Optional[dict] = Field(default=None, description='执行时上下文快照')
    loop_index: Optional[int] = Field(default=None, description='循环索引')
    loop_item: Optional[dict] = Field(default=None, description='循环项数据')
    condition_result: Optional[int] = Field(default=None, description='条件判断结果')
    error_message: Optional[str] = Field(default=None, description='错误信息')
    error_details: Optional[dict] = Field(default=None, description='错误详情')
    retry_count: Optional[int] = Field(default=None, description='重试次数')
    created_at: Optional[datetime] = Field(default=None, description='创建时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='created_at', message='创建时间不能为空')
    def get_created_at(self):
        return self.created_at


    def validate_fields(self):
        self.get_created_at()




class Worknode_executionsQueryModel(Worknode_executionsModel):
    """
    节点执行记录不分页查询模型
    """
    pass


@as_query
class Worknode_executionsPageQueryModel(Worknode_executionsQueryModel):
    """
    节点执行记录分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteWorknode_executionsModel(BaseModel):
    """
    删除节点执行记录模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    node_execution_ids: str = Field(description='需要删除的节点执行记录ID')
