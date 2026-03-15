#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：js_exector.py.py
@Author  ：david
@Date    ：2025-08-13 21:47 
"""
import asyncio
import json

from utils.api_tools.executors.js_script_control import PostmanJSExecutor
from utils.api_tools.executors.strategies import ExecutorStrategy
import time
from typing import Union
from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult


class JsScriptExecutor(ExecutorStrategy):
    """JavaScript脚本执行器"""

    async def execute(self, context: ExecutorContext, config: Union[SetupConfig, TeardownConfig]) -> ExecutorResult:
        start_time = time.time()
        data = {}
        try:
            script = getattr(config, 'script', '')
            if not script:
                return ExecutorResult(success=False, error="JS脚本内容为空")
            func = PostmanJSExecutor.execute
            result4 = await asyncio.to_thread(
                func, script)
            res = json.dumps(result4, indent=2, ensure_ascii=False)
            data.update({"script": script, "result": result4})
            execution_time = time.time() - start_time
            return ExecutorResult(
                success=True,
                message='js脚本执行成功',
                # data=res,
                log=res,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutorResult(
                success=False,
                error=f"JS脚本执行失败: {str(e)}",
                execution_time=execution_time
            )
