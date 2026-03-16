# -*- coding: utf-8 -*-
"""
MCP服务器配置表
存储MCP服务器的连接配置信息，支持 stdio / streamable_http / sse / websocket 四种传输类型
"""

from sqlalchemy import Column, BigInteger, String, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from config.base import Base
import uuid


class LlmMcpConfig(Base):
    """
    MCP服务器配置表 - 将原本静态的 MCP_SERVERS 字典持久化到数据库
    每行代表一个MCP服务器的完整连接配置
    """

    __tablename__ = 'llm_mcp_config'
    __table_args__ = (
        Index('idx_mcp_config_server_name', 'server_name'),
        {'comment': 'MCP服务器配置表'}
    )

    # ================== 主键 ==================

    config_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment='配置唯一标识符(UUID)'
    )

    # ================== 服务器基础信息 ==================

    server_name = Column(
        String(128),
        nullable=False,
        comment='服务器逻辑名称，作为工具名前缀（如 playwright、fetch）'
    )

    enabled = Column(
        Boolean,
        nullable=True,
        default=True,
        comment='是否启用此服务器'
    )

    transport = Column(
        String(32),
        nullable=True,
        comment='传输类型: stdio / streamable_http / sse / websocket'
    )

    # ================== stdio 专用字段 ==================

    command = Column(
        String(256),
        nullable=True,
        comment='stdio模式: 可执行文件路径（如 npx、python、uvx）'
    )

    args = Column(
        JSONB,
        nullable=True,
        comment='stdio模式: 命令行参数列表，如 ["@playwright/mcp@latest", "--headless"]'
    )

    env = Column(
        JSONB,
        nullable=True,
        comment='stdio模式: 子进程环境变量字典'
    )

    cwd = Column(
        String(512),
        nullable=True,
        comment='stdio模式: 子进程工作目录'
    )

    # ================== HTTP 类传输字段 ==================

    url = Column(
        String(1024),
        nullable=True,
        comment='streamable_http/sse/websocket模式: 远程服务器URL'
    )

    headers = Column(
        JSONB,
        nullable=True,
        comment='streamable_http/sse模式: 附加HTTP请求头（如认证token）'
    )

    timeout = Column(
        BigInteger,
        nullable=True,
        comment='请求超时时间（秒）'
    )

    sse_read_timeout = Column(
        BigInteger,
        nullable=True,
        comment='SSE流读取超时时间（秒）'
    )

    # ================== 扩展配置 ==================

    session_kwargs = Column(
        JSONB,
        nullable=True,
        comment='传递给MCP ClientSession的额外参数'
    )





