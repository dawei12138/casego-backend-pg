from module_fastmcp.mcp_instance import mcp
from module_fastmcp.middleware.logging_middleware import LoggingMiddleware
from utils.log_util import logger

# 添加日志中间件
logging_middleware = LoggingMiddleware(
    log_level="INFO",
    include_payloads=True,
    max_payload_length=2000,
    log_timing=True,
    log_strategy="specific"
)
mcp.add_middleware(logging_middleware)


# 导入所有工具、资源、提示模块（这会触发装饰器执行）
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

# 创建HTTP应用
mcp_app = mcp.http_app(path='/mcp')
