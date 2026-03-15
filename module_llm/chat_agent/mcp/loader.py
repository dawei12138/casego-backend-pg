# -*- coding: utf-8 -*-
"""
MCP 工具加载器

职责：
  1. 使用 langchain-mcp-adapters 的 MultiServerMCPClient 连接所有启用的 MCP 服务器
  2. 将 MCP 工具转换为标准 LangChain Tool，直接返回给 get_tools() 使用
  3. 提供带超时保护的异步加载，任何单台服务器失败不影响其余服务器
  4. 模块级缓存：应用生命周期内只加载一次，避免每次对话都重启 Playwright 进程

调用方（tools.py）示例：
    from module_llm.chat_agent.mcp.loader import load_mcp_tools, mcp_tools_context
    mcp_tools = await load_mcp_tools()               # 无状态服务器 / 简单场景
    async with mcp_tools_context() as tools: ...     # 需要保持浏览器状态的场景
"""
import asyncio
from contextlib import asynccontextmanager, AsyncExitStack

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools as _lc_load_mcp_tools

from module_llm.chat_agent.mcp.config import get_enabled_servers
from utils.log_util import logger

# 单台 MCP 服务器工具加载的超时秒数
# Playwright 首次启动需要下载浏览器，可能较慢，给 60 秒
_LOAD_TIMEOUT_SECONDS = 60

# 工具描述最大长度，超出截断，避免触发 API 敏感词检测或撑大 payload
_MAX_DESC_LENGTH = 200

# 模块级缓存：应用生命周期内只初始化一次，后续所有对话直接复用
# 设为 None 表示尚未加载；设为 [] 表示加载过但无可用工具
_cached_tools: list | None = None
_cache_lock = asyncio.Lock()


def _truncate_tool_descriptions(tools: list) -> list:
    """
    将每个工具的 description 截断至 _MAX_DESC_LENGTH 字符。

    超长的工具描述会：
      1. 显著增大发给 LLM 的 payload，导致超时
      2. 触发某些国内 API 中转服务的敏感词过滤（500 错误）

    注意：直接修改 tool.description 属性（LangChain BaseTool 支持）。
    """
    for t in tools:
        if t.description and len(t.description) > _MAX_DESC_LENGTH:
            t.description = t.description[:_MAX_DESC_LENGTH] + "..."
    return tools


def _enable_tool_error_handling(tools: list) -> list:
    """
    为所有工具启用错误处理，让工具在出错时返回错误信息而不是抛出异常。

    设置 handle_tool_error=True 后，工具执行失败时会：
      1. 捕获异常
      2. 将错误信息格式化为字符串
      3. 作为工具的返回值传递给 Agent
      4. Agent 可以看到错误信息并决定如何处理（重试、换方法等）

    这避免了工具调用失败导致整个对话流终止的致命缺陷。
    """
    for tool in tools:
        tool.handle_tool_error = True
    return tools


async def _do_load() -> list:
    """实际执行 MCP 工具加载的内部函数（不含缓存逻辑）。"""
    servers = get_enabled_servers()
    if not servers:
        logger.debug("没有启用的 MCP 服务器，跳过 MCP 工具加载")
        return []

    logger.info(f"开始加载 MCP 工具，服务器列表: {list(servers.keys())}")

    try:
        client = MultiServerMCPClient(connections=servers)
        tools = await asyncio.wait_for(
            client.get_tools(),
            timeout=_LOAD_TIMEOUT_SECONDS,
        )
        tools = _truncate_tool_descriptions(tools)
        tools = _enable_tool_error_handling(tools)
        logger.info(
            f"MCP 工具加载完成，共 {len(tools)} 个工具: "
            f"{[t.name for t in tools]}"
        )
        return tools

    except asyncio.TimeoutError:
        logger.warning(
            f"MCP 工具加载超时（>{_LOAD_TIMEOUT_SECONDS}s），跳过 MCP 工具"
        )
    except Exception as eg:
        # ExceptionGroup（TaskGroup 内部并发异常）逐个打印，方便定位根因
        try:
            for exc in eg.exceptions:
                logger.warning(f"MCP 工具加载失败，跳过 MCP 工具: {type(exc).__name__}: {exc}")
        except AttributeError:
            logger.warning(f"MCP 工具加载失败，跳过 MCP 工具: {type(eg).__name__}: {eg}")

    return []


async def load_mcp_tools() -> list:
    """
    连接所有启用的 MCP 服务器并返回全部工具列表（带模块级缓存）。

    首次调用时真正执行连接和加载（带双重检查锁防并发竞态），
    后续调用直接返回缓存结果，不再重启 Playwright 等子进程。

    - 单台服务器超时或异常时记录警告，不阻断其他服务器
    - 若所有服务器均不可用，返回空列表（系统仍可正常运行，只是少了 MCP 工具）

    Returns:
        list: LangChain BaseTool 列表，可直接传入 model.bind_tools()
    """
    global _cached_tools

    # 快速路径：已有缓存，直接返回（无锁开销）
    if _cached_tools is not None:
        return _cached_tools

    # 慢速路径：双重检查加锁，防止并发时重复加载
    async with _cache_lock:
        if _cached_tools is None:
            _cached_tools = await _do_load()

    return _cached_tools


async def reload_mcp_tools() -> list:
    """
    强制重新加载 MCP 工具（清除缓存后重新连接）。

    应用场景：运行时动态修改了 MCP_SERVERS 配置后调用。
    正常情况下无需调用，重启应用即可刷新。
    """
    global _cached_tools
    async with _cache_lock:
        _cached_tools = None
        _cached_tools = await _do_load()
    return _cached_tools


@asynccontextmanager
async def mcp_tools_context():
    """
    在 async with 块内为每个 MCP 服务器建立持久 session，退出时才关闭。

    适用于需要跨多次工具调用保持浏览器/进程状态的场景（如 Playwright）。

    使用 client.session(server_name) + AsyncExitStack 同时持有所有 server 的
    session，再调用 load_mcp_tools(session) —— 工具闭包中 session is not None，
    工具执行时直接走 await session.call_tool(...)，不再每次重建进程。

    用法（在 chat_controller.py 中）：
        async with mcp_tools_context() as mcp_tools:
            graph = await create_graph(model, mcp_tools=mcp_tools, ...)
            async for chunk in graph.astream(...):
                yield chunk
        # with 块退出后所有 session 才关闭（浏览器随之关闭）

    若没有启用的 MCP 服务器，yield 空列表，不影响正常流程。
    """
    servers = get_enabled_servers()
    if not servers:
        yield []
        return

    client = MultiServerMCPClient(connections=servers)
    all_tools: list = []

    async with AsyncExitStack() as stack:
        for name in servers:
            try:
                session = await stack.enter_async_context(client.session(name))
                try:
                    tools = await asyncio.wait_for(
                        _lc_load_mcp_tools(session, server_name=name),
                        timeout=_LOAD_TIMEOUT_SECONDS,
                    )
                    tools = _truncate_tool_descriptions(tools)
                    tools = _enable_tool_error_handling(tools)
                    all_tools.extend(tools)
                    logger.info(
                        f"MCP server '{name}' session 已建立，"
                        f"{len(tools)} 个工具: {[t.name for t in tools]}"
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"MCP server '{name}' 加载超时（>{_LOAD_TIMEOUT_SECONDS}s），跳过")
                except Exception as e:
                    logger.warning(f"MCP server '{name}' 工具加载失败，跳过: {type(e).__name__}: {e}")
            except Exception as e:
                logger.warning(f"MCP server '{name}' session 建立失败，跳过: {type(e).__name__}: {e}")

        logger.info(f"所有 MCP session 已就绪，共 {len(all_tools)} 个工具")
        yield all_tools
        # AsyncExitStack.__aexit__ 时按逆序关闭所有 session
