from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmSession(Base):
    __tablename__ = 'llm_session'

    session_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(36), nullable=False)
    default_agent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    default_provider_id: Mapped[str] = mapped_column(String(36), nullable=False)
    default_model_code: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='active')
    last_error_summary: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    is_archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    memory_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    tool_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
