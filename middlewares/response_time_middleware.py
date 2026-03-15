#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：response_time_middleware.py
@Author  ：david
@Date    ：2025-08-06 14:07 
"""
import time
from fastapi import FastAPI, Request
from starlette.responses import Response
from utils.log_util import logger


def add_response_time_middleware(app: FastAPI):
    """
    添加接口响应时间日志中间件
    """

    @app.middleware("http")
    async def log_response_time(request: Request, call_next):
        if request.headers.get("accept") == "text/event-stream":
            return await call_next(request)

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = (time.time() - start_time) * 1000  # 单位：毫秒

        method = request.method
        url = request.url.path
        status_code = response.status_code

        logger.info(f"{method} {url} - {status_code} - {process_time:.2f}ms")
        return response
