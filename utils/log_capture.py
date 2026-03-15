"""
日志捕获工具 - 用于捕获指定作用域内的日志

使用方式:
1. 上下文管理器: with capture_logs() as capture: ...
2. 装饰器: @with_log_capture

运行示例:
    python -m utils.log_capture
"""

import asyncio
import re
import contextvars
from contextlib import contextmanager, asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import List, Optional, Callable, Any, Dict

from middlewares.trace_middleware import TraceCtx
from utils.log_util import logger

# 与 log_util.py 保持一致的日志格式（无颜色）
LOG_FORMAT = (
    '{time:YYYY-MM-DD HH:mm:ss.SSS} | '
    '{extra[trace_id]} | '
    '{level: <8} | '
    '{name}:{function}:{line} - '
    '{message}'
)


@dataclass
class LogRecord:
    """日志记录"""
    level: str
    message: str
    time: str
    function: str
    line: int
    file: str


@dataclass
class LogCapture:
    """日志捕获器"""
    logs: List[LogRecord] = field(default_factory=list)
    raw_logs: List[str] = field(default_factory=list)  # 原始格式化日志
    _handler_id: Optional[int] = field(default=None, repr=False)

    def _sink(self, message):
        """自定义 sink，收集日志"""
        record = message.record
        self.logs.append(LogRecord(
            level=record["level"].name,
            message=record["message"],
            time=record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            function=record["function"],
            line=record["line"],
            file=record["file"].name if record["file"] else ""
        ))
        # 捕获原始格式化日志（去除颜色代码和末尾换行）
        raw_text = str(message).rstrip('\n')
        # 移除 ANSI 颜色代码
        raw_text = re.sub(r'\x1b\[[0-9;]*m', '', raw_text)
        self.raw_logs.append(raw_text)

    def _filter(self, record: Dict) -> bool:
        """添加 trace_id 到日志记录"""
        record['extra']['trace_id'] = TraceCtx.get_id()
        return True

    def start(self):
        """开始捕获"""
        self._handler_id = logger.add(
            self._sink,
            format=LOG_FORMAT,
            filter=self._filter,
            level="DEBUG"
        )
        return self

    def stop(self) -> List[LogRecord]:
        """停止捕获并返回日志"""
        if self._handler_id is not None:
            try:
                logger.remove(self._handler_id)
            except ValueError:
                pass  # handler 已被移除
            self._handler_id = None
        return self.logs

    def get_logs_as_text(self, include_time: bool = True) -> str:
        """以文本形式返回日志"""
        if include_time:
            return "\n".join(
                f"[{log.time}] [{log.level:8}] {log.function}:{log.line} - {log.message}"
                for log in self.logs
            )
        return "\n".join(
            f"[{log.level:8}] {log.function}:{log.line} - {log.message}"
            for log in self.logs
        )

    def get_logs_as_list(self) -> List[dict]:
        """以字典列表形式返回日志"""
        return [
            {
                "level": log.level,
                "message": log.message,
                "time": log.time,
                "function": log.function,
                "line": log.line,
                "file": log.file
            }
            for log in self.logs
        ]

    def get_raw_logs(self) -> str:
        """获取原始格式的日志文本（终端显示格式）"""
        return "\n".join(self.raw_logs)

    def clear(self):
        """清空已捕获的日志"""
        self.logs.clear()
        self.raw_logs.clear()


@contextmanager
def capture_logs():
    """
    同步上下文管理器 - 捕获作用域内的日志

    示例:
        with capture_logs() as capture:
            logger.info("这条日志会被捕获")
        print(capture.get_logs_as_text())
    """
    capture = LogCapture()
    capture.start()
    try:
        yield capture
    finally:
        capture.stop()


@asynccontextmanager
async def async_capture_logs():
    """
    异步上下文管理器 - 捕获作用域内的日志

    示例:
        async with async_capture_logs() as capture:
            logger.info("这条日志会被捕获")
        print(capture.get_logs_as_text())
    """
    capture = LogCapture()
    capture.start()
    try:
        yield capture
    finally:
        capture.stop()


def with_log_capture(func: Callable) -> Callable:
    """
    装饰器 - 自动捕获函数执行期间的日志

    被装饰的函数会额外返回一个包含日志的元组: (原返回值, 捕获的日志文本)

    示例:
        @with_log_capture
        def my_func():
            logger.info("执行中")
            return "result"

        result, logs = my_func()
    """
    if asyncio.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            capture = LogCapture()
            capture.start()
            try:
                result = await func(*args, **kwargs)
                return result, capture.get_logs_as_text()
            finally:
                capture.stop()
        return async_wrapper
    else:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            capture = LogCapture()
            capture.start()
            try:
                result = func(*args, **kwargs)
                return result, capture.get_logs_as_text()
            finally:
                capture.stop()
        return sync_wrapper


def with_log_capture_to_attr(attr_name: str = "captured_logs"):
    """
    装饰器 - 将捕获的日志注入到返回对象的属性中

    示例:
        @with_log_capture_to_attr("logs")
        def my_func():
            logger.info("执行中")
            return SomeObject()

        result = my_func()
        print(result.logs)  # 捕获的日志
    """
    def decorator(func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                capture = LogCapture()
                capture.start()
                try:
                    result = await func(*args, **kwargs)
                    if hasattr(result, '__dict__'):
                        setattr(result, attr_name, capture.get_logs_as_text())
                    return result
                finally:
                    capture.stop()
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                capture = LogCapture()
                capture.start()
                try:
                    result = func(*args, **kwargs)
                    if hasattr(result, '__dict__'):
                        setattr(result, attr_name, capture.get_logs_as_text())
                    return result
                finally:
                    capture.stop()
            return sync_wrapper
    return decorator


# ==================== 调试示例 ====================
if __name__ == "__main__":
    import time

    print("=" * 60)
    print("日志捕获工具调试示例")
    print("=" * 60)

    # 示例1: 上下文管理器方式
    print("\n【示例1】上下文管理器方式")
    print("-" * 40)

    with capture_logs() as capture:
        logger.debug("这是 DEBUG 日志")
        logger.info("这是 INFO 日志")
        logger.warning("这是 WARNING 日志")
        logger.error("这是 ERROR 日志")

    print("捕获到的日志:")
    print(capture.get_logs_as_text())
    print(f"\n共捕获 {len(capture.logs)} 条日志")

    # 示例2: 装饰器方式
    print("\n【示例2】装饰器方式 @with_log_capture")
    print("-" * 40)

    @with_log_capture
    def process_data(data: str):
        logger.info(f"开始处理数据: {data}")
        time.sleep(0.1)  # 模拟处理
        logger.info("数据处理完成")
        logger.warning("这是一个警告")
        return f"处理结果: {data.upper()}"

    result, logs = process_data("hello world")
    print(f"函数返回值: {result}")
    print(f"捕获的日志:\n{logs}")

    # 示例3: 异步函数
    print("\n【示例3】异步函数")
    print("-" * 40)

    @with_log_capture
    async def async_task(task_id: int):
        logger.info(f"异步任务 {task_id} 开始")
        await asyncio.sleep(0.1)
        logger.info(f"异步任务 {task_id} 完成")
        return f"Task-{task_id} Done"

    async def run_async_demo():
        result, logs = await async_task(1)
        print(f"异步函数返回值: {result}")
        print(f"捕获的日志:\n{logs}")

    asyncio.run(run_async_demo())

    # 示例4: 嵌套捕获
    print("\n【示例4】嵌套捕获 (各自独立)")
    print("-" * 40)

    with capture_logs() as outer:
        logger.info("外层日志 1")

        with capture_logs() as inner:
            logger.info("内层日志")

        logger.info("外层日志 2")

    print(f"外层捕获 {len(outer.logs)} 条: {[l.message for l in outer.logs]}")
    print(f"内层捕获 {len(inner.logs)} 条: {[l.message for l in inner.logs]}")

    # 示例5: 获取结构化数据
    print("\n【示例5】获取结构化日志数据")
    print("-" * 40)

    with capture_logs() as capture:
        logger.info("测试消息")
        logger.error("错误消息")

    for log_dict in capture.get_logs_as_list():
        print(f"  {log_dict}")

    print("\n" + "=" * 60)
    print("调试完成!")
    print("=" * 60)
