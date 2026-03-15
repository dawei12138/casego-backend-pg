from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query




class Workflow_executionsModel(BaseModel):
    """
    执行器执行记录表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    workflow_execution_id: Optional[int] = Field(default=None, description='执行记录ID')
    workflow_id: Optional[int] = Field(default=None, description='执行器ID')
    workflow_name: Optional[str] = Field(default=None, description='执行名称')
    status: Optional[str] = Field(default=None, description='执行状态')
    start_time: Optional[datetime] = Field(default=None, description='开始时间')
    end_time: Optional[datetime] = Field(default=None, description='结束时间')
    duration: Optional[int] = Field(default=None, description='执行时长(秒)')
    input_data: Optional[dict] = Field(default=None, description='输入数据')
    output_data: Optional[dict] = Field(default=None, description='输出数据')
    context_data: Optional[dict] = Field(default=None, description='上下文数据')
    total_nodes: Optional[int] = Field(default=None, description='总节点数')
    success_nodes: Optional[int] = Field(default=None, description='成功节点数')
    failed_nodes: Optional[int] = Field(default=None, description='失败节点数')
    skipped_nodes: Optional[int] = Field(default=None, description='跳过节点数')
    error_message: Optional[str] = Field(default=None, description='错误信息')
    error_details: Optional[dict] = Field(default=None, description='错误详情')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')






class Workflow_executionsQueryModel(Workflow_executionsModel):
    """
    执行器执行记录不分页查询模型
    """
    pass


@as_query
class Workflow_executionsPageQueryModel(Workflow_executionsQueryModel):
    """
    执行器执行记录分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteWorkflow_executionsModel(BaseModel):
    """
    删除执行器执行记录模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    workflow_execution_ids: str = Field(description='需要删除的执行记录ID')
