# -*- coding: utf-8 -*-
"""
LLM聊天线程表
存储用户与AI的对话会话信息（仅持久化线程级数据）
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from config.base import Base
import uuid


class LlmChatThread(Base):
    """
    聊天线程表 - 代表用户与AI的一次完整对话会话
    """

    __tablename__ = 'llm_chat_thread'
    __table_args__ = (
        Index('idx_thread_user_id', 'user_id'),
        {'comment': 'LLM聊天线程表'}
    )

    # ================== 主键 ==================

    thread_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment='线程唯一标识符(UUID)'
    )

    # ================== 基础信息 ==================

    title = Column(
        Text,
        nullable=True,
        default='',
        comment='线程标题，首次对话后自动生成'
    )

    user_id = Column(
        BigInteger,
        nullable=True,
        comment='所属用户ID'
    )

    # ================== 会话配置（核心字段） ==================

    session_config = Column(
        JSONB,
        nullable=True,
        comment='会话配置(JSONB)，存储模型/工具/运行参数等'
    )
