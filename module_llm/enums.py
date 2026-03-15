# -*- coding: utf-8 -*-
"""
LLM模块枚举类型定义
"""
from enum import IntEnum, Enum


class ModelProviderEnum(str, Enum):
    """模型提供商枚举"""
    OPENAI = "openai"               # OpenAI官方
    AZURE_OPENAI = "azure_openai"   # Azure OpenAI
    ANTHROPIC = "anthropic"         # Claude/Anthropic
    GOOGLE = "google"               # Google Gemini
    DEEPSEEK = "deepseek"           # DeepSeek
    QWEN = "qwen"                   # 通义千问
    ZHIPU = "zhipu"                 # 智谱AI
    MOONSHOT = "moonshot"           # 月之暗面Kimi
    BAICHUAN = "baichuan"           # 百川智能
    MINIMAX = "minimax"             # MiniMax
    SPARK = "spark"                 # 讯飞星火
    WENXIN = "wenxin"               # 百度文心
    HUNYUAN = "hunyuan"             # 腾讯混元
    OLLAMA = "ollama"               # Ollama本地模型
    CUSTOM = "custom"               # 自定义模型(OpenAI兼容)


class ModelStatusEnum(IntEnum):
    """模型状态枚举"""
    DISABLED = 0    # 禁用
    ENABLED = 1     # 启用


class ModelTypeEnum(str, Enum):
    """模型类型枚举"""
    CHAT = "chat"           # 对话模型
    COMPLETION = "completion"   # 补全模型
    EMBEDDING = "embedding"     # 嵌入模型
    IMAGE = "image"             # 图像模型
    AUDIO = "audio"             # 音频模型


class MessageRoleEnum(str, Enum):
    """消息角色枚举"""
    USER = "user"           # 用户消息
    ASSISTANT = "assistant" # AI助手消息
    SYSTEM = "system"       # 系统消息


class MessagePartTypeEnum(str, Enum):
    """消息部分类型枚举"""
    TEXT = "text"                       # 文本内容
    REASONING = "reasoning"             # 推理/思考过程
    TOOL_INVOCATION = "tool-invocation" # 工具调用
    FILE = "file"                       # 文件附件
    SOURCE_URL = "source-url"           # 来源URL
    STEP_START = "step-start"           # 步骤开始标记


class ToolCallStateEnum(str, Enum):
    """工具调用状态枚举"""
    INPUT_AVAILABLE = "input-available"     # 输入可用
    OUTPUT_AVAILABLE = "output-available"   # 输出可用
    OUTPUT_PARTIAL = "output-partial"       # 部分输出
    ERROR = "error"                         # 错误


class ToolChoiceEnum(str, Enum):
    """工具选择模式枚举"""
    AUTO = "auto"       # 自动选择
    NONE = "none"       # 不使用工具
    MANUAL = "manual"   # 手动选择
