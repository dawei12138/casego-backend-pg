from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Optional

from config.enums import NotificationType
from module_admin.annotation.pydantic_annotation import as_query


class NotificationModel(BaseModel):
    """
    通知消息表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    notification_id: Optional[int] = Field(default=None, description='通知ID')
    user_id: Optional[int] = Field(default=None, description='接收用户ID')
    notification_type: Optional[NotificationType] = Field(default=None,
                                                          description='通知类型(system/task/workflow/alert)')
    title: Optional[str] = Field(default=None, description='通知标题')
    message: Optional[str] = Field(default=None, description='通知内容')
    is_read: Optional[int] = Field(default=None, description='是否已读')
    read_time: Optional[datetime] = Field(default=None, description='阅读时间')
    business_type: Optional[str] = Field(default=None, description='关联业务类型(workflow/test_case/report等)')
    business_id: Optional[int] = Field(default=None, description='关联业务ID')
    extra_data: Optional[dict] = Field(default=None, description='扩展数据')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')

    @NotBlank(field_name='user_id', message='接收用户ID不能为空')
    def get_user_id(self):
        return self.user_id

    def validate_fields(self):
        pass
        # self.get_user_id()


class NotificationQueryModel(NotificationModel):
    """
    通知消息不分页查询模型
    """
    pass


@as_query
class NotificationPageQueryModel(NotificationQueryModel):
    """
    通知消息分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteNotificationModel(BaseModel):
    """
    删除通知消息模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    notification_ids: str = Field(description='需要删除的通知ID')
