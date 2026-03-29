from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmProviderModel(Base):
    __tablename__ = 'llm_provider_model'

    model_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    provider_id: Mapped[str] = mapped_column(String(36), nullable=False)
    model_code: Mapped[str] = mapped_column(String(100), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    capabilities: Mapped[str] = mapped_column(String(255), nullable=False, default='chat')
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
