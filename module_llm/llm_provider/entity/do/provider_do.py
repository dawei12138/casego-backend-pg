from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmProvider(Base):
    __tablename__ = 'llm_provider'

    provider_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    provider_type: Mapped[str] = mapped_column(String(50), nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    api_key_masked: Mapped[str] = mapped_column(String(255), nullable=False, default='')
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
