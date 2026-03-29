from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmTool(Base):
    __tablename__ = 'llm_tool'

    tool_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_id: Mapped[str] = mapped_column(String(36), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False, default='low')
