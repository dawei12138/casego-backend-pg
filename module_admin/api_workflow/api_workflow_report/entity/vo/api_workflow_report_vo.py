from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional, List
from module_admin.annotation.pydantic_annotation import as_query
from module_admin.api_testing.api_test_execution_log.entity.vo.execution_log_vo import Execution_logModel
from utils.api_workflow_tools.models import TriggerType


class Api_workflow_reportModel(BaseModel):
    """
    自动化测试执行报告表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    report_id: Optional[int] = Field(default=None, description='报告ID')
    workflow_id: Optional[int] = Field(default=None, description='执行器ID')
    name: Optional[str] = Field(default=None, description='报告名称')
    start_time: Optional[datetime] = Field(default=None, description='开始时间')
    end_time: Optional[datetime] = Field(default=None, description='结束时间')
    total_cases: Optional[int] = Field(default=None, description='总用例数')
    success_cases: Optional[int] = Field(default=None, description='成功用例数')
    failed_cases: Optional[int] = Field(default=None, description='失败用例数')
    duration: Optional[float] = Field(default=None, description='总耗时(秒)')
    is_success: Optional[int] = Field(default=None, description='是否全部成功')
    report_data: Optional[dict] = Field(default=None, description='完整报告JSON数据')
    trigger_type: Optional[TriggerType] = Field(default=None, description='触发类型')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='workflow_id', message='执行器ID不能为空')
    def get_workflow_id(self):
        return self.workflow_id

    def validate_fields(self):
        self.get_workflow_id()


class Api_workflow_reportQueryModel(Api_workflow_reportModel):
    """
    自动化测试执行报告不分页查询模型
    """
    pass


@as_query
class Api_workflow_reportPageQueryModel(Api_workflow_reportQueryModel):
    """
    自动化测试执行报告分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteApi_workflow_reportModel(BaseModel):
    """
    删除自动化测试执行报告模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    report_ids: str = Field(description='需要删除的报告ID')


class Api_workflow_report_log_Model(Api_workflow_reportModel):
    """

    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)
    report_logs: Optional[List[Execution_logModel]] = Field(
        default_factory=list,
        description="全局请求头列表")