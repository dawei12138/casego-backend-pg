from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional

from config.enums import Request_method
from module_admin.annotation.pydantic_annotation import as_query
from utils.api_workflow_tools.models import StreamEventType


class Execution_logModel(BaseModel):
    """
    接口测试执行日志表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    log_id: Optional[int] = Field(default=None, description='执行日志ID')
    case_id: Optional[int] = Field(default=None, description='测试用例ID')
    execution_time: Optional[datetime] = Field(default=None, description='执行时间')
    is_success: Optional[int] = Field(default=None, description='是否执行成功')
    execution_data: Optional[dict] = Field(default=None, description='完整执行数据')
    response_status_code: Optional[int] = Field(default=None, description='响应状态码')
    response_time: Optional[float] = Field(default=None, description='响应时间(秒)')
    assertion_success: Optional[int] = Field(default=None, description='断言是否成功')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')
    method: Optional[Request_method] = Field(default=None, description='请求方法 (GET, POST等)')
    path: Optional[str] = Field(default=None, description='请求路径')
    name: Optional[str] = Field(default=None, description='测试用例名称')
    workflow_id: Optional[int] = Field(default=None, description='执行器ID')
    report_id: Optional[int] = Field(default=None, description='执行器ID')
    event_type: Optional[StreamEventType] = Field(default=None, )

    @NotBlank(field_name='case_id', message='测试用例ID不能为空')
    def get_case_id(self):
        return self.case_id

    def validate_fields(self):
        self.get_case_id()


class Execution_logQueryModel(Execution_logModel):
    """
    接口测试执行日志不分页查询模型
    """
    pass


@as_query
class Execution_logPageQueryModel(Execution_logQueryModel):
    """
    接口测试执行日志分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteExecution_logModel(BaseModel):
    """
    删除接口测试执行日志模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    log_ids: str = Field(description='需要删除的执行日志ID')
