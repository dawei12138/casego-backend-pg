from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_query
from module_app.enums import AgentStatusEnum


class AgentsModel(BaseModel):
    """
    Agent代理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='主键ID')
    name: Optional[str] = Field(default=None, description='Agent名称')
    host: Optional[str] = Field(default=None, description='Agent的IP地址')
    port: Optional[int] = Field(default=None, description='Agent的端口')
    secret_key: Optional[str] = Field(default=None, description='Agent的密钥')
    status: Optional[AgentStatusEnum] = Field(default=None, description='Agent状态')
    system_type: Optional[str] = Field(default=None, description='Agent系统类型: windows/linux/macos')
    version: Optional[str] = Field(default=None, description='Agent端代码版本')
    lock_version: Optional[int] = Field(default=None, description='乐观锁版本号')
    high_temp: Optional[int] = Field(default=None, description='高温预警阈值(摄氏度)')
    high_temp_time: Optional[int] = Field(default=None, description='高温持续时间阈值(分钟)')
    has_hub: Optional[int] = Field(default=None, description='是否使用Sonic Hub: 0否 1是')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    description: Optional[str] = Field(default=None, description='描述')
    sort_no: Optional[float] = Field(default=None, description='排序值')
    del_flag: Optional[str] = Field(default=None, description='删除标志 0正常 1删除 2代表删除')






class AgentsQueryModel(AgentsModel):
    """
    Agent代理不分页查询模型
    """
    pass


@as_query
class AgentsPageQueryModel(AgentsQueryModel):
    """
    Agent代理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteAgentsModel(BaseModel):
    """
    删除Agent代理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID')
