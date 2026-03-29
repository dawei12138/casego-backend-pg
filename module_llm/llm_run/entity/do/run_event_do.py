from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmRunEvent(Base):
    __tablename__ = 'llm_run_event'

    event_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    seq_no: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    event_payload: Mapped[str] = mapped_column(String(1000), nullable=False, default='{}')
