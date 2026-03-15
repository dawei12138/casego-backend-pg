import asyncio
import socket
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional, Callable, Awaitable

from redis import asyncio as aioredis
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import (
    AuthenticationError,
    TimeoutError,
    ConnectionError,
    RedisError
)

from config.env import RedisConfig
from config.database import AsyncSessionLocal
from module_admin.system.service.config_service import ConfigService
from module_admin.system.service.dict_service import DictDataService
from utils.log_util import logger


# ==============================
# Redis 代理类：自动重试所有 Redis 操作
# ==============================
class RedisProxy:
    """
    Redis 代理类：拦截所有 Redis 方法调用，自动应用重试逻辑

    使用此代理包装 Redis 实例后，所有 Redis 操作都会自动处理连接失效和重试
    无需修改任何业务代码即可实现自动重连
    """

    def __init__(self, redis_instance: aioredis.Redis):
        self._redis = redis_instance

    def __getattr__(self, name):
        """
        拦截所有属性访问，对方法调用进行包装
        """
        attr = getattr(self._redis, name)

        # 如果是可调用方法，包装重试逻辑
        if callable(attr):
            async def wrapper(*args, **kwargs):
                async def operation():
                    try:

                        await self._redis.ping()
                    except Exception:
                        logger.warning("Redis 连接失效，触发自动重连...")
                        # 断开旧连接，强制重新建立
                        await self._redis.connection_pool.disconnect()

                    # 执行实际操作
                    return await attr(*args, **kwargs)

                # 应用重试逻辑（来自 RedisUtil.redis_retry）
                return await redis_retry(operation)

            return wrapper

        # 非方法属性直接返回
        return attr

    # 支持直接访问底层 Redis 实例（用于特殊场景）
    @property
    def raw_redis(self):
        return self._redis

    # 支持直接访问连接池（用于特殊场景）
    @property
    def connection_pool(self):
        return self._redis.connection_pool

    # 直接代理 close 方法（关闭时不需要重试）
    async def close(self):
        return await self._redis.close()


# ==============================
# 核心：统一的重试逻辑
# ==============================
async def redis_retry(operation: Callable[[], Awaitable], retries=2, delay=0.1):
    """
    对所有 Redis 操作进行自动重试，确保连接断开后自动恢复
    """
    for attempt in range(retries):
        try:
            return await operation()

        except (ConnectionError, TimeoutError, OSError) as e:
            if attempt == retries - 1:
                raise
            logger.warning(f"Redis 操作失败（自动重试中）: {e}, retry={attempt + 1}")
            await asyncio.sleep(delay * (attempt + 1))


class RedisUtil:

    # ============================================
    # 创建 Redis 连接池（自动重连的关键）
    # ============================================
    @classmethod
    async def create_redis_pool(cls) -> aioredis.Redis:
        """
        创建具备自动重连能力的 Redis 对象（基于 ConnectionPool）
        """

        logger.info("开始连接 Redis...")

        # TCP KeepAlive
        socket_keepalive_options = {}
        if hasattr(socket, "TCP_KEEPIDLE"):
            socket_keepalive_options[socket.TCP_KEEPIDLE] = 60
            socket_keepalive_options[socket.TCP_KEEPINTVL] = 10
            socket_keepalive_options[socket.TCP_KEEPCNT] = 3

        pool: ConnectionPool = ConnectionPool(
            host=RedisConfig.redis_host,
            port=RedisConfig.redis_port,
            username=RedisConfig.redis_username,
            password=RedisConfig.redis_password,
            db=RedisConfig.redis_database,
            encoding="utf-8",
            decode_responses=True,

            # 自动重连核心能力
            max_connections=100,
            retry_on_timeout=True,
            retry_on_error=[ConnectionError, TimeoutError, OSError],  # 扩展重试错误类型

            # 超时配置（优化：延长超时时间，避免频繁超时）
            socket_timeout=60,  # 从 30 增加到 60 秒
            socket_connect_timeout=15,  # 从 10 增加到 15 秒

            # 健康检查（优化：更频繁检查，及时发现失效连接）
            health_check_interval=15,  # 从 30 减少到 15 秒

            # Keepalive（保持 TCP 连接活跃）
            socket_keepalive=True,
            socket_keepalive_options=socket_keepalive_options,
        )

        redis = aioredis.Redis(connection_pool=pool)

        # 启动时预热 + 自动修复
        await redis_retry(redis.ping)

        # logger.info("Redis 连接成功（自动重连已启用）")

        return redis

    # ============================================
    # 关闭连接池
    # ============================================
    @classmethod
    async def close_redis_pool(cls, app):
        try:
            if hasattr(app.state, "redis") and app.state.redis:
                # 如果是 RedisProxy，获取底层 Redis 实例
                redis = app.state.redis
                if isinstance(redis, RedisProxy):
                    redis = redis.raw_redis

                await redis.close()
                logger.info("关闭 Redis 连接成功")
        except Exception as e:
            logger.error(f"关闭 Redis 连接失败: {e}")

    # ============================================
    # 获取一次性连接（用于特殊操作）
    # ============================================
    @classmethod
    @asynccontextmanager
    async def get_redis_connection(cls) -> AsyncGenerator[aioredis.Redis, None]:

        redis = aioredis.Redis(
            host=RedisConfig.redis_host,
            port=RedisConfig.redis_port,
            username=RedisConfig.redis_username,
            password=RedisConfig.redis_password,
            db=RedisConfig.redis_database,
            encoding='utf-8',
            decode_responses=True,
            socket_timeout=5,           # 从 30 秒减少到 5 秒
            socket_connect_timeout=3,   # 从 10 秒减少到 3 秒
            retry_on_timeout=True
        )

        await redis_retry(redis.ping)

        try:
            yield redis
        finally:
            await redis.close()

    # ============================================
    # 自动保证连接正确的 Redis 操作封装
    # ============================================
    @classmethod
    async def safe_execute(cls, redis: aioredis.Redis, func: Callable, *args, **kwargs):
        """
        自动检测连接是否有效 + 自动修复 + 自动重试
        """
        async def op():
            try:
                # 检查连接是否活着
                await redis.ping()
            except Exception:
                logger.warning("Redis 连接失效，尝试 auto-reconnect...")
                await redis.connection_pool.disconnect()

            return await func(*args, **kwargs)

        return await redis_retry(op)

    # ============================================
    # 应用封装操作
    # ============================================
    @classmethod
    async def create_cache_key_value(cls, app, key, value,
                                     expire_time=None, namespace="Temp", nx=False, xx=False):

        redis = app.state.redis
        name_key = f"{namespace}:{key}" if namespace else key

        await cls.safe_execute(
            redis,
            redis.set,
            name_key,
            value,
            ex=expire_time,
            nx=nx,
            xx=xx
        )

    # ============================================
    # 缓存字典与配置
    # ============================================
    @classmethod
    async def init_sys_dict(cls, redis):
        async with AsyncSessionLocal() as session:
            await DictDataService.init_cache_sys_dict_services(session, redis)

    @classmethod
    async def init_sys_config(cls, redis):
        async with AsyncSessionLocal() as session:
            await ConfigService.init_cache_sys_config_services(session, redis)

    # ============================================
    # 清理残留的调度器锁
    # ============================================
    @classmethod
    async def clear_scheduler_locks(cls, redis) -> int:
        """
        清理 Redis 中残留的调度器任务锁

        在应用启动时调用，防止因异常退出导致锁未释放而影响任务执行

        Returns:
            int: 清理的锁数量
        """
        lock_pattern = "scheduler:job_lock:*"
        deleted_count = 0

        try:
            # 使用 SCAN 迭代查找所有匹配的锁键
            cursor = 0
            keys_to_delete = []

            while True:
                cursor, keys = await redis.scan(cursor, match=lock_pattern, count=100)
                keys_to_delete.extend(keys)

                if cursor == 0:
                    break

            # 批量删除找到的锁
            if keys_to_delete:
                deleted_count = await redis.delete(*keys_to_delete)
                logger.info(f"清理残留调度器锁完成，共删除 {deleted_count} 个锁: {keys_to_delete}")
            else:
                logger.info("未发现残留的调度器锁")

        except Exception as e:
            logger.error(f"清理调度器锁失败: {e}")

        return deleted_count
