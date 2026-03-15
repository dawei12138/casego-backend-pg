#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File ：mcp_instance.py.py
@Author ：david
@Date ：2025-09-16 15:52
"""
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import StaticTokenVerifier
from module_fastmcp.middleware.logging_middleware import LoggingMiddleware
from utils.log_util import logger

# 创建认证器
verifier = StaticTokenVerifier(
    tokens={
        "dev-david-StaticTokenVerifier-token": {
            "client_id": "alice@company.com",
            "scopes": ["read:data", "write:data", "admin:users"]
        },
        "dev-guest-token": {
            "client_id": "guest-user",
            "scopes": ["read:data"]
        }
    },
    required_scopes=["read:data"]
)

# 创建全局MCP实例
mcp = FastMCP(name="Development Server", auth=verifier)


# 添加日志中间件
logging_middleware = LoggingMiddleware(
    log_level="INFO",
    include_payloads=True,
    max_payload_length=2000,
    log_timing=True,
    log_strategy="specific"
)
mcp.add_middleware(logging_middleware)


def register_all_components():
    """注册所有MCP组件"""
    logger.info("🔄 开始注册MCP组件...")
    # 导入工具模块
    from module_fastmcp.tools import data_tools
    from module_fastmcp.tools import user_tools
    # 导入资源模块
    from module_fastmcp.resources import config_resources
    # 导入提示模块
    from module_fastmcp.prompts import template_prompts
    logger.info("✅ 所有组件模块已导入")


# 注册所有组件
register_all_components()

# 移除了创建HTTP应用的代码，这部分将在 mcp_server.py 中处理
