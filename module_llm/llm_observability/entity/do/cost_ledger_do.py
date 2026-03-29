from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmCostLedger(Base):
    __tablename__ = 'llm_cost_ledger'

    ledger_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(36), nullable=False)
    provider_id: Mapped[str] = mapped_column(String(36), nullable=False)
    model_code: Mapped[str] = mapped_column(String(100), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
