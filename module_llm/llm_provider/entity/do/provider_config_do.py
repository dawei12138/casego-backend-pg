# -*- coding: utf-8 -*-
"""
LLM提供商配置表
存储各AI模型提供商的基础配置信息，如API Key、Base URL等
"""
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Text, Integer, Boolean, Index, JSON
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class LlmProvider(Base):
    """
    AI提供商配置表 - 存储各AI模型提供商的基础配置

    支持的提供商类型参考 module_llm.enums.ModelProviderEnum
    """

    __tablename__ = 'llm_provider'
    __table_args__ = (
        Index('idx_provider_key', 'provider_key'),
        Index('idx_provider_status', 'status'),
        {'comment': 'LLM提供商配置表'}
    )

    # 主键
    provider_id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        comment='提供商配置ID'
    )

    # 提供商标识: openai/anthropic/google/xai/groq/ollama/openrouter等
    provider_key = Column(
        String(50),
        nullable=True,
        unique=True,
        comment='提供商标识(如openai/anthropic/google等)'
    )

    # 提供商名称: 显示名称
    provider_name = Column(
        String(100),
        nullable=True,
        comment='提供商显示名称(如OpenAI/Anthropic/Google等)'
    )

    # API密钥
    api_key = Column(
        String(500),
        nullable=True,
        comment='API密钥(建议加密存储)'
    )

    # API密钥对(部分提供商需要，如百度文心)
    api_secret = Column(
        String(500),
        nullable=True,
        comment='API密钥对(部分提供商需要)'
    )

    # API基础URL: 自定义或代理时使用
    base_url = Column(
        String(500),
        nullable=True,
        comment='API基础URL(自定义或代理时使用)'
    )

    # API版本(Azure等需要)
    api_version = Column(
        String(50),
        nullable=True,
        comment='API版本(Azure等需要)'
    )

    # 请求超时时间(秒)
    timeout = Column(
        Integer,
        nullable=True,
        default=60,
        comment='请求超时时间(秒)'
    )

    # 最大重试次数
    max_retries = Column(
        Integer,
        nullable=True,
        default=3,
        comment='最大重试次数'
    )

    # 额外请求头(JSON格式)
    extra_headers = Column(
        JSON, nullable=True, default={},
        comment='额外请求头(JSON格式)'
    )

    # 额外请求参数(JSON格式)，用于兼容接口透传请求体参数
    extra_params = Column(
        JSONB, nullable=True, default=dict,
        comment='额外请求参数(JSON格式)'
    )

    # 接口协议类型: openai/claude/gemini/deepseek/openrouter/openai_compatible
    api_protocol = Column(
        String(32),
        nullable=True,
        default='openai_compatible',
        comment='接口协议类型(openai/claude/gemini/deepseek/openrouter/openai_compatible)'
    )

    # 可选模型型号列表
    models = Column(
        JSONB,
        nullable=True,
        default=list,
        comment='模型型号列表(JSON数组)'
    )

    # 默认模型型号
    default_model = Column(
        String(120),
        nullable=True,
        comment='默认模型型号'
    )

    # 支持的思考程度: low/medium/high/xhigh/max
    thinking_levels = Column(
        JSONB,
        nullable=True,
        default=list,
        comment='支持的思考程度(JSON数组)'
    )

    # 图标URL
    icon_url = Column(
        String(500),
        nullable=True,
        comment='提供商图标URL'
    )

    # 状态: 0-禁用 1-启用
    status = Column(
        String(1),
        default='1',
        comment='状态（0禁用 1启用）'
    )

