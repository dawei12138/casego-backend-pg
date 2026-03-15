import uuid
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, Dict, Any, List

from module_admin.annotation.pydantic_annotation import as_query


# ================== Enum 定义（强烈推荐） ==================

class ToolChoice(str, Enum):
    """
    工具调用策略
    """
    auto = "auto"  # 模型自动决定
    manual = "manual"  # 人工确认
    none = "none"  # 禁用工具


# ================== 子结构模型 ==================

class ChatModelConfig(BaseModel):
    """
    模型配置
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    provider: str = Field(description='模型提供商')
    model: str = Field(description='模型名称')


class MentionConfig(BaseModel):
    """
    Agent / Workflow 注入配置
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    type: str = Field(description='类型(agent/workflow)')
    name: Optional[str] = Field(default=None, description='名称')
    description: Optional[str] = Field(default=None, description='描述')

    agent_id: Optional[str] = Field(default=None, description='Agent ID')
    workflow_id: Optional[str] = Field(default=None, description='Workflow ID')


class SessionConfigModel(BaseModel):
    """
    会话级配置（核心模型）
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    chat_model: Optional[ChatModelConfig] = Field(default=None, description='模型配置')

    tool_choice: Optional[ToolChoice] = Field(
        default=ToolChoice.auto,
        description='工具调用策略'
    )

    allowed_app_default_toolkit: Optional[List[str]] = Field(
        default_factory=list,
        description='允许的默认工具集'
    )

    allowed_mcp_servers: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description='允许的 MCP Server'
    )

    is_thinking: Optional[bool] = Field(
        default=False,
        description='允许的 MCP Server'
    )

    mentions: Optional[List[MentionConfig]] = Field(
        default_factory=list,
        description='Agent / Workflow 注入配置'
    )


# ================== 主线程模型 ==================

class ThreadModel(BaseModel):
    """
    LLM聊天线程 VO
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    thread_id: Optional[uuid.UUID] = Field(default=None, description='线程唯一标识符')
    title: Optional[str] = Field(default=None, description='线程标题')
    user_id: Optional[int] = Field(default=None, description='所属用户ID')

    session_config: Optional[SessionConfigModel] = Field(
        default=None,
        description='会话配置'
    )

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')

    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')

    remark: Optional[str] = Field(default=None, description='备注')
    del_flag: Optional[str] = Field(default=None, description='删除标志')


# ================== 查询模型 ==================

class ThreadQueryModel(ThreadModel):
    """
    不分页查询模型
    """
    pass


@as_query
class ThreadPageQueryModel(ThreadQueryModel):
    """
    分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


# ================== 删除模型 ==================

class DeleteThreadModel(BaseModel):
    """
    删除线程模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    # thread_ids: List[uuid.UUID] = Field(description='需要删除的线程ID列表')
    thread_ids: str = Field(description='需要删除的线程ID列表')
