#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
MCP 独立服务器
"""
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from module_fastmcp.mcp_instance import mcp
from config.env import AppConfig
from config.get_redis import RedisUtil
from utils.log_util import logger

# 先创建MCP应用
mcp_app = mcp.http_app(path='/mcp')


@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    # 启动Redis连接
    logger.info('MCP服务开始启动')
    app.state.redis = await RedisUtil.create_redis_pool()
    # await RedisUtil.init_sys_dict(app.state.redis)
    # await RedisUtil.init_sys_config(app.state.redis)
    logger.info('Redis连接已建立')

    # 启动MCP的lifespan
    async with mcp_app.lifespan(app):
        mcp_app.state.redis = app.state.redis
        logger.info('MCP服务启动成功')
        yield

    # 清理Redis连接
    await RedisUtil.close_redis_pool(app)
    logger.info('MCP服务已关闭')


# 创建最终的FastAPI应用，使用组合的lifespan
app = FastAPI(
    title="MCP Server",
    description="MCP独立服务器",
    version="1.0.0",
    lifespan=combined_lifespan,
)

# 挂载MCP应用
app.mount("/v1", mcp_app)

if __name__ == '__main__':
    print("启动MCP服务...")
    uvicorn.run(
        app='module_fastmcp.mcp_server:app',
        host=AppConfig.app_host,
        port=8001,
        reload=AppConfig.app_reload,
        workers=1
    )