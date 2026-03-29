from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmMemoryItem(Base):
    __tablename__ = 'llm_memory_item'

    memory_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False)
    session_id: Mapped[str] = mapped_column(String(36), nullable=False)
    run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False, default='run')
    source_run_id: Mapped[str] = mapped_column(String(36), nullable=False, default='')
    write_reason: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    last_recalled_at: Mapped[str] = mapped_column(String(50), nullable=False, default='')
    delete_reason: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
