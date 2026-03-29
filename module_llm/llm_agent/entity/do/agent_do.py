from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmAgent(Base):
    __tablename__ = 'llm_agent'

    agent_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    agent_code: Mapped[str] = mapped_column(String(50), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    scenario: Mapped[str] = mapped_column(String(255), nullable=False, default='general')
    default_model_code: Mapped[str] = mapped_column(String(100), nullable=False, default='')
    allow_tools: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    allow_memory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    allow_skills: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    max_steps: Mapped[int] = mapped_column(Integer, nullable=False, default=8)
    max_tool_calls: Mapped[int] = mapped_column(Integer, nullable=False, default=4)
    timeout_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    is_user_visible: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_recommended: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
