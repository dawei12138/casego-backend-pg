# -*- coding: utf-8 -*-
"""
请求/响应模型
"""
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import Optional, List, Any
from datetime import datetime

# ── 附件配置常量 ──────────────────────────────────────────────────
CHAT_ATTACHMENT_MAX_SIZE = 10 * 1024 * 1024  # 10MB
CHAT_ATTACHMENT_MAX_COUNT = 5
CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS = {'.txt', '.json', '.csv', '.md', '.log', '.xml', '.yaml', '.yml'}
CHAT_ATTACHMENT_ALLOWED_EXTS = CHAT_ATTACHMENT_ALLOWED_IMAGE_EXTS | CHAT_ATTACHMENT_ALLOWED_TEXT_EXTS


class AttachmentMeta(BaseModel):
    """附件元数据 - 上传响应 / 消息请求 / 历史展示共用"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    filename: str = Field(description='原始文件名')
    stored_name: str = Field(description='工作区内相对路径，如 upload/20260313_abc_1234.png')
    file_type: str = Field(description='文件分类: image 或 text')
    mime_type: str = Field(description='MIME 类型，如 image/png')
    size: int = Field(description='文件大小(bytes)')


class ChatAttachmentUploadResponse(BaseModel):
    """附件上传响应"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    attachments: List[AttachmentMeta] = Field(description='上传成功的附件列表')
    failed: List[dict] = Field(default_factory=list, description='上传失败的文件及原因')


class ChatRequest(BaseModel):
    """对话请求"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    provider_key: str = Field(description='模型提供商标识(如openai/anthropic/deepseek等)')
    model: str = Field(description='模型名称(如gpt-4o, claude-sonnet-4-5-20250929)')
    thread_id: str = Field(description='会话线程ID，用于保持上下文')
    message: str = Field(description='用户消息内容')
    attachments: Optional[List[AttachmentMeta]] = Field(default=None, description='附件元数据列表(由上传接口返回)')
    system_prompt: Optional[str] = Field(default=None, description='系统提示词')
    enable_thinking: bool = Field(default=False, description='是否开启思考模式(扩展推理)')
    enable_web_search: bool = Field(default=False, description='是否开启联网搜索')
    mcp_config_ids: Optional[List[str]] = Field(default=None, description='MCP服务器配置ID列表，传入则动态加载对应MCP工具')


class ChatHistoryQuery(BaseModel):
    """聊天历史查询参数"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    thread_id: str = Field(description='会话线程ID')
    page: int = Field(default=1, ge=1, description='页码，从1开始')
    page_size: int = Field(default=20, ge=1, le=100, description='每页消息数量，最大100')


class AnswerRequest(BaseModel):
    """用户回答请求（恢复被 ask_user_question 中断的对话）"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    provider_key: str = Field(description='模型提供商标识(如openai/anthropic/deepseek等)')
    model: str = Field(description='模型名称(如gpt-4o, claude-sonnet-4-5-20250929)')
    thread_id: str = Field(description='会话线程ID')
    answers: dict = Field(description='用户回答，key为问题文本，value为选择的答案')
    enable_thinking: bool = Field(default=False, description='是否开启思考模式')
    enable_web_search: bool = Field(default=False, description='是否开启联网搜索')
    mcp_config_ids: Optional[List[str]] = Field(default=None, description='MCP服务器配置ID列表，传入则动态加载对应MCP工具')


class ToolCallModel(BaseModel):
    """工具调用模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    name: str = Field(description='工具名称')
    args: dict = Field(default_factory=dict, description='调用参数')
    call_id: Optional[str] = Field(default=None, description='调用ID')


class ChatMessageModel(BaseModel):
    """聊天消息模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[str] = Field(default=None, description='消息ID')
    type: str = Field(description='消息类型: human/ai/tool/system')
    content: Any = Field(description='消息内容')
    tool_calls: Optional[List[ToolCallModel]] = Field(default=None, description='工具调用列表(AI消息)')
    tool_call_id: Optional[str] = Field(default=None, description='工具调用ID(Tool消息)')
    tool_name: Optional[str] = Field(default=None, description='工具名称(Tool消息)')


class TurnEventModel(BaseModel):
    """统一事件模型 - SSE 流和历史记录共用"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    type: str = Field(description='事件类型: content/thinking/thinking_start/thinking_end/tool_call/tool_result')
    content: Optional[str] = Field(default=None, description='文本内容(content/thinking类型)')
    tool: Optional[str] = Field(default=None, description='工具名称(tool_call/tool_result类型)')
    args: Optional[dict] = Field(default=None, description='工具调用参数(tool_call/tool_result类型)')
    call_id: Optional[str] = Field(default=None, description='工具调用ID(tool_call/tool_result类型)')
    result: Optional[Any] = Field(default=None, description='工具执行结果(tool_result类型)')


class ConversationTurnModel(BaseModel):
    """一轮对话 = 用户消息 + AI 响应事件序列"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    request_id: str = Field(description='请求ID，SSE时为uuid4，历史中用HumanMessage.id')
    user_message: str = Field(description='用户输入内容')
    attachments: Optional[List[AttachmentMeta]] = Field(default=None, description='用户附件元数据')
    events: List[TurnEventModel] = Field(default_factory=list, description='AI响应事件列表')


class ChatHistoryResponse(BaseModel):
    """聊天历史响应 - 按轮次分组"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    thread_id: str = Field(description='会话线程ID')
    total: int = Field(description='轮次总数')
    page: int = Field(description='当前页码')
    page_size: int = Field(description='每页轮次数')
    pages: int = Field(description='总页数')
    has_more: bool = Field(description='是否有更多轮次')
    turns: List[ConversationTurnModel] = Field(description='对话轮次列表')
