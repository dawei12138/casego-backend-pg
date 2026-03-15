import aiohttp
from aiohttp import TraceConfig, AsyncResolver, TCPConnector, CookieJar
from typing import AsyncGenerator
import time
from utils.log_util import logger
import ssl


async def get_trace_config():
    trace_config = TraceConfig()

    @trace_config.on_request_start.append
    async def on_request_start(session, trace_config_ctx, params):
        trace_config_ctx.start = time.time()
        # logger.warning("请求开始")

    @trace_config.on_connection_create_start.append
    async def on_conn_create_start(session, trace_config_ctx, params):
        trace_config_ctx.conn_start = time.time()
        # logger.warning("开始建立连接")

    @trace_config.on_dns_resolvehost_start.append
    async def on_dns_start(session, trace_config_ctx, params):
        trace_config_ctx.dns_start = time.time()
        # logger.warning(f"开始DNS解析 {params.host}")

    @trace_config.on_dns_resolvehost_end.append
    async def on_dns_end(session, trace_config_ctx, params):
        # logger.warning(f"DNS解析耗时 {time.time() - trace_config_ctx.dns_start:.3f}s")
        pass

    @trace_config.on_connection_create_end.append
    async def on_conn_create_end(session, trace_config_ctx, params):
        pass
        # logger.warning(f"连接建立耗时 {time.time() - trace_config_ctx.conn_start:.3f}s")

    @trace_config.on_request_end.append
    async def on_request_end(session, trace_config_ctx, params):
        logger.warning(f"整个请求耗时 {time.time() - trace_config_ctx.start:.3f}s")

    return trace_config


# 创建 aiohttp 客户端依赖
async def get_http_client() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """创建并返回 aiohttp 客户端会话"""

    # 创建SSL上下文，不验证证书
    ssl_context = ssl.create_default_context()
    # ssl_context = ssl._create_unverified_context()
    ssl_context.set_ciphers('DEFAULT')
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    # 禁用不安全的协议，强制使用TLSv1.2及以上
    # ssl_context.options |= ssl.OP_NO_SSLv2
    # ssl_context.options |= ssl.OP_NO_SSLv3
    # ssl_context.options |= ssl.OP_NO_TLSv1
    # ssl_context.options |= ssl.OP_NO_TLSv1_1

    # 设置超时
    timeout = aiohttp.ClientTimeout(total=60, connect=30)

    # 指定自定义 DNS（这里用 Google DNS）
    # resolver = AsyncResolver(nameservers=["8.8.8.8", "8.8.4.4"])
    # resolver = AsyncResolver(nameservers=["223.5.5.5", "223.6.6.6"])  # 阿里云DNS
    # resolver = AsyncResolver(nameservers=["114.114.114.114"])  # 114DNS

    # 创建 CookieJar - 用于自动管理 cookie
    # unsafe=True 允许接收来自 IP 地址的 cookie（默认只接受域名的 cookie）
    # quote_cookie=False 禁用 cookie 值的 URL 编码
    cookie_jar = CookieJar(unsafe=True, quote_cookie=False)

    # 创建连接器
    # connector = TCPConnector(ssl=ssl_context, resolver=resolver)
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    trace_config = await get_trace_config()
    async with aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            trace_configs=[trace_config],
            cookie_jar=cookie_jar  # 添加 cookie_jar 自动管理 cookie
    ) as session:
        logger.info("获取http_client")
        yield session
