from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmRun(Base):
    __tablename__ = 'llm_run'

    run_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    agent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(36), nullable=False)
    model_code: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='created')
    input_summary: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    output_summary: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    failure_stage: Mapped[str] = mapped_column(String(50), nullable=False, default='')
    failure_category: Mapped[str] = mapped_column(String(50), nullable=False, default='')
    used_memory: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    used_tool: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    cost_summary: Mapped[str] = mapped_column(String(255), nullable=False, default='')
