from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from config.base import Base


class LlmMcpServer(Base):
    __tablename__ = 'llm_mcp_server'

    server_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    transport: Mapped[str] = mapped_column(String(20), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    health_status: Mapped[str] = mapped_column(String(20), nullable=False, default='healthy')
