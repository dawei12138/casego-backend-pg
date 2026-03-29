from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmToolInvokeLog(Base):
    __tablename__ = 'llm_tool_invoke_log'

    log_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    tool_id: Mapped[str] = mapped_column(String(36), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='success')
    retry_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
