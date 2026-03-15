# -*- coding: utf-8 -*-
"""
MCP 服务器连接配置

每个 key 是服务器名称，value 是对应的连接配置字典。
配置格式由 langchain-mcp-adapters 的 MultiServerMCPClient 决定。

─────────────────────────────────────────────
transport 类型对照：

  "stdio"          - 本地子进程，通过标准 I/O 与 MCP 服务器通信
  "streamable_http"- 远程 HTTP，使用 Streamable HTTP 协议（MCP 官方推荐）
  "sse"            - 远程 HTTP，使用旧版 SSE 协议（部分旧服务器使用）
  "websocket"      - 远程 WebSocket 协议

─────────────────────────────────────────────
stdio 参数说明：

  command  (str)           - 要执行的可执行文件（如 "npx"、"python"、"uvx"）
  args     (list[str])     - 传递给可执行文件的命令行参数列表
  env      (dict|None)     - 子进程的环境变量，None 表示继承当前进程环境
  cwd      (str|None)      - 子进程的工作目录，None 表示继承当前目录
  encoding (str)           - 标准 I/O 编码，默认 "utf-8"
  session_kwargs (dict)    - 传递给 MCP ClientSession 的额外参数

─────────────────────────────────────────────
streamable_http 参数说明：

  url                (str)        - 远程 MCP 服务器的完整 URL（必填）
  headers            (dict|None)  - 附加到每次请求的 HTTP 请求头（认证 token 等）
  timeout            (timedelta)  - 单次请求超时，默认 5 秒
  sse_read_timeout   (timedelta)  - SSE 流读取超时，默认 5 分钟
  terminate_on_close (bool)       - 关闭时是否发送 terminate 信号，默认 True
  session_kwargs     (dict)       - 传递给 MCP ClientSession 的额外参数

─────────────────────────────────────────────
MCP_SERVERS 中每个条目的顶层字段：

  enabled  (bool)  - 是否启用此服务器，False 时 get_mcp_tools() 跳过它
  其余字段全部透传给 MultiServerMCPClient 的 connections 参数
"""

import os

# ──────────────────────────────────────────────────────────────────
# MCP 服务器配置字典
# key   = 服务器逻辑名称（在 tool_name_prefix=True 时会成为工具名前缀）
# value = 连接配置，"enabled" 是本框架自定义字段，其余字段透传给 MCP 适配器
# ──────────────────────────────────────────────────────────────────
MCP_SERVERS: dict = {

    # ──────────────────────────────────────────
    # 示例 1：本地 Playwright MCP（stdio transport）
    #
    # 前提：已安装 Node.js 22+，运行以下命令安装：
    #   npm install -g @playwright/mcp
    # 或者直接用 npx（无需全局安装，会自动下载）：
    #   npx @playwright/mcp@latest
    #
    # 工具清单（部分）：
    #   browser_navigate      - 导航到指定 URL
    #   browser_snapshot      - 截取页面无障碍树快照（用于 AI 理解页面结构）
    #   browser_click         - 点击页面元素
    #   browser_type          - 在输入框中输入文本
    #   browser_screenshot    - 截图并返回 base64
    #   browser_close         - 关闭浏览器
    # ──────────────────────────────────────────
    "playwright": {
        "enabled": True,           # 已启用错误处理，工具失败不会导致对话终止
        "transport": "stdio",      # 使用本地子进程通信
        "command": "npx",          # 通过 npx 启动，无需全局安装
        "args": [
            "@playwright/mcp@latest",   # Playwright MCP 包名
            # "--headless",               # 无头模式（无 GUI），服务器环境必须
            # "--port", "8931",         # 可选：也可以让它监听 HTTP 端口（http transport）
        ],
        "env": {
            # 继承系统 PATH，确保 npx 能找到 Node.js
            "PATH": os.environ.get("PATH", ""),
        },
    },

    # ──────────────────────────────────────────
    # 示例 2：远程公共 Fetch MCP（streamable_http transport）
    #
    # 这是 Anthropic 官方维护的 fetch MCP 服务，可以抓取网页内容。
    # 使用 streamable_http（MCP 2025-03-26 规范推荐的传输协议）。
    #
    # 注意：此为公开演示服务，生产环境建议自行部署。
    #
    # 工具清单：
    #   fetch  - 获取指定 URL 的网页/文档内容，返回 Markdown 格式
    # ──────────────────────────────────────────
    "fetch": {
        "enabled": False,
        "transport": "streamable_http",   # 远程 HTTP 流式传输
        "url": "https://remote.mcp.run/anthropic/fetch",  # 远程服务 URL
        "headers": {
            # 此公共服务无需认证；若是私有服务则在此添加：
            # "Authorization": "Bearer YOUR_TOKEN",
        },
        # timeout 默认 5 秒；若网络慢可以适当增大
        # "timeout": timedelta(seconds=30),
    },

}


def get_enabled_servers() -> dict:
    """
    返回所有 enabled=True 的服务器配置，
    并剔除 "enabled" 字段本身（不传给 MCP 适配器）。
    """
    result = {}
    for name, cfg in MCP_SERVERS.items():
        if cfg.get("enabled", True):
            conn_cfg = {k: v for k, v in cfg.items() if k != "enabled"}
            result[name] = conn_cfg
    return result
