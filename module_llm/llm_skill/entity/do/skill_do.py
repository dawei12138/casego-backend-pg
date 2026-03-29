# -*- coding: utf-8 -*-
"""
AI技能配置表
存储技能的基础信息和元数据，支持动态管理和文件系统同步
"""

from sqlalchemy import Column, String, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from config.base import Base
import uuid


class LlmSkill(Base):
    """
    AI技能配置表 - 管理deepagents框架使用的技能
    每行代表一个技能目录的元数据信息
    """

    __tablename__ = 'llm_skill'
    __table_args__ = (
        Index('idx_skill_name', 'skill_name', unique=True),
        {'comment': 'AI技能配置表'}
    )

    # ================== 主键 ==================

    skill_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment='技能唯一标识符(UUID)'
    )

    # ================== 基础信息 ==================

    skill_name = Column(
        String(128),
        nullable=False,
        unique=True,
        comment='技能目录名（英文标识符，如 playwright-cli、requirement-analysis）'
    )

    display_name = Column(
        String(256),
        nullable=True,
        comment='技能显示名称（人类可读）'
    )

    enabled = Column(
        Boolean,
        nullable=True,
        default=True,
        comment='是否启用（启用时同步到文件系统）'
    )

    # ================== 来源信息 ==================

    source_type = Column(
        String(32),
        nullable=True,
        default='manual',
        comment='来源类型: manual(手动创建) / upload(上传) / url(URL导入)'
    )

    source_url = Column(
        String(1024),
        nullable=True,
        comment='URL导入时的源地址'
    )

    # ================== SKILL.md 元数据 ==================

    allowed_tools = Column(
        String(512),
        nullable=True,
        comment='允许的工具列表（来自SKILL.md frontmatter的allowed-tools字段）'
    )

    license_info = Column(
        String(256),
        nullable=True,
        comment='许可证信息（来自SKILL.md frontmatter的license字段）'
    )
