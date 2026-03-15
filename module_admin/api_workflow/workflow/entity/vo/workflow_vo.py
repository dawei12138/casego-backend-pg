from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, List

from pydantic_validation_decorator import NotBlank

from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import WorknodesModel, WorknodesModelWithChildren, \
    ErrorHandlingStrategy


class RetryPolicyModel(BaseModel):
    """重试策略模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    max_retries: int = Field(default=3, description='最大重试次数')
    retry_delay: int = Field(default=5, description='重试延迟(秒)')
    retry_on: List[str] = Field(default_factory=lambda: ["ConnectionError", "TimeoutError"],
                                description='重试触发条件')


class ReportConfigModel(BaseModel):
    """报告配置模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    format: List[str] = Field(default_factory=lambda: ["html", "json"], description='报告格式')
    include_logs: bool = Field(default=True, description='是否包含日志')
    include_screenshots: bool = Field(default=False, description='是否包含截图')
    on_error: Optional[ErrorHandlingStrategy] = Field(
        default=ErrorHandlingStrategy.IGNORE,
        description='错误处理方式: ignore(忽略), next_iteration(跳到下一轮循环), break_loop(结束循环), stop_running(结束运行), retry(重试)'
    )


class ExecutionConfigModel(BaseModel):
    """环境，参数化，多线程相关配置"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)
    parameterization_data: Optional[list[dict]] = Field(default=[], description='参数化数据')
    parameterization_id: Optional[int] = Field(default=None, description='参数化id')
    env_id: Optional[int] = Field(default=None, description='环境id')
    loop_count: Optional[int] = Field(default=1, description='循环次数')
    threading_count: Optional[int] = Field(default=1, description='线程数')
    # mode: str = Field(default="sequential", description='执行模式')
    # timeout: int = Field(default=5000, description='超时时间()')
    # retry_policy: RetryPolicyModel = Field(default_factory=RetryPolicyModel, description='重试策略')
    # report_config: ReportConfigModel = Field(default_factory=ReportConfigModel, description='报告配置')


class WorkflowModel(BaseModel):
    """
    测试执行器主表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    workflow_id: Optional[int] = Field(default=None, description='执行器ID')
    name: Optional[str] = Field(default=None, description='执行器名称')
    execution_config: Optional[ExecutionConfigModel | dict] = Field(default=ExecutionConfigModel(),
                                                                    description='输入数据')
    parent_submodule_id: Optional[int] = Field(default=None, description='父级模块ID')
    project_id: Optional[int] = Field(default=None, description='父级模块ID')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')


class WorkflowQueryModel(WorkflowModel):
    """
    测试执行器主不分页查询模型
    """
    pass


@as_query
class WorkflowPageQueryModel(WorkflowQueryModel):
    """
    测试执行器主分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteWorkflowModel(BaseModel):
    """
    删除测试执行器主模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    workflow_ids: str = Field(description='需要删除的执行器ID')


class ExecWorkflowModel(WorkflowQueryModel):
    """
    删除测试执行器主模型
    """
    workflow_id: int = Field(description='执行器ID')
    parameterization_id: Optional[int] = None,
    env_id: Optional[int] = None,
    loop_count: int = 1,

    @NotBlank(field_name='workflow_id', message='Cookie键名不能为空')
    def get_workflow_id(self):
        return self.workflow_id

    def validate_fields(self):
        self.get_workflow_id()


class WorkflowTreeModel(WorkflowModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    worknodes: Optional[WorknodesModelWithChildren | list] = Field(default=None, description='输入数据')
    # children: Optional[List["WorkflowTreeModel"]] = Field(
    #     default_factory=list,
    #     description='子节点列表（嵌套结构）'
    # )


if __name__ == "__main__":
    class UserIgnoreExtra(BaseModel):
        id: int
        name: str = Field(default=None)


    # 现在会忽略多余字段
    data = {"id": 1}
    user = UserIgnoreExtra.model_validate(data)
    print(user)  # id=1 name='John' - age和email被忽略
    print(user.model_dump_json())
    print(user.model_dump())
    pass
