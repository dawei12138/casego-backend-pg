from sqlalchemy import Column, BigInteger, Float, DateTime, Enum, Text, Integer, String, Index
from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from enum import Enum as PyEnum

from module_admin.api_testing.api_script_library.entity.vo.script_library_vo import ScriptTypeEnum


class ApiScriptLibrary(Base):
    """公共脚本库"""
    __tablename__ = "api_script_library"
    __table_args__ = (
        Index('ix_script_library_type', 'script_type'),
        Index('ix_script_library_name', 'script_name'),
        {'comment': '公共脚本库'},
    )

    script_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='脚本ID')
    script_name = Column(String(100), nullable=True, comment='脚本名称')
    script_type = Column(
        Enum(ScriptTypeEnum, values_callable=lambda x: [e.value for e in x], name="ScriptTypeEnum"),
        nullable=True,
        # default=ScriptTypeEnum.PYTHON,
        comment='脚本类型(python/javascript)'
    )
    script_content = Column(Text, nullable=True, comment='脚本内容')
    status = Column(Integer, default=1, comment='状态(0停用 1正常)')
