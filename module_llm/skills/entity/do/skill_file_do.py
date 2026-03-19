# -*- coding: utf-8 -*-
"""
AI技能文件表
存储技能目录下的所有文件内容，支持从数据库同步到文件系统
"""

from sqlalchemy import Column, String, Boolean, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from config.base import Base
import uuid


class LlmSkillFile(Base):
    """
    AI技能文件表 - 存储技能目录中的每个文件
    每行代表技能目录中的一个文件（如 SKILL.md、references/tracing.md）
    """

    __tablename__ = 'llm_skill_file'
    __table_args__ = (
        Index('idx_skill_file_skill_id', 'skill_id'),
        Index('idx_skill_file_path', 'skill_id', 'file_path', unique=True),
        {'comment': 'AI技能文件表'}
    )

    # ================== 主键 ==================

    file_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment='文件唯一标识符(UUID)'
    )

    # ================== 关联信息 ==================

    skill_id = Column(
        UUID(as_uuid=True),
        nullable=False,
        comment='所属技能ID（关联llm_skill.skill_id）'
    )

    # ================== 文件信息 ==================

    file_path = Column(
        String(512),
        nullable=False,
        comment='文件在技能目录内的相对路径（如 SKILL.md、references/tracing.md）'
    )

    content = Column(
        Text,
        nullable=True,
        comment='文件文本内容'
    )

    is_binary = Column(
        Boolean,
        nullable=True,
        default=False,
        comment='是否为二进制文件'
    )
