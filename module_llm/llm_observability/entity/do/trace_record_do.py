from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmTraceRecord(Base):
    __tablename__ = 'llm_trace_record'

    trace_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    agent_id: Mapped[str] = mapped_column(String(36), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='completed')
