import asyncio
import json
import uuid
import functools
from apscheduler.events import EVENT_ALL
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from asyncio import iscoroutinefunction
from datetime import datetime, timedelta
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Union, Optional, Callable, Any
from config.database import AsyncSessionLocal, quote_plus
from config.env import DataBaseConfig, RedisConfig
from module_admin.system.dao.job_dao import JobDao
from module_admin.system.entity.vo.job_vo import JobLogModel, JobModel
from module_admin.system.service.job_log_service import JobLogService
from utils.log_util import logger
import module_task  # noqa: F401

# 当前 Worker 的唯一标识
WORKER_ID = str(uuid.uuid4())[:8]

# Redis Pub/Sub 频道名称（用于跨 Worker 同步任务状态）
SCHEDULER_CHANNEL = "scheduler:job_sync"


# 重写Cron定时
class MyCronTrigger(CronTrigger):
    @classmethod
    def from_crontab(cls, expr: str, timezone=None):
        values = expr.split()
        if len(values) != 6 and len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 6 or 7'.format(len(values)))

        second = values[0]
        minute = values[1]
        hour = values[2]
        if '?' in values[3]:
            day = None
        elif 'L' in values[5]:
            day = f"last {values[5].replace('L', '')}"
        elif 'W' in values[3]:
            day = cls.__find_recent_workday(int(values[3].split('W')[0]))
        else:
            day = values[3].replace('L', 'last')
        month = values[4]
        if '?' in values[5] or 'L' in values[5]:
            week = None
        elif '#' in values[5]:
            week = int(values[5].split('#')[1])
        else:
            week = values[5]
        if '#' in values[5]:
            day_of_week = int(values[5].split('#')[0]) - 1
        else:
            day_of_week = None
        year = values[6] if len(values) == 7 else None
        return cls(
            second=second,
            minute=minute,
            hour=hour,
            day=day,
            month=month,
            week=week,
            day_of_week=day_of_week,
            year=year,
            timezone=timezone,
        )

    @classmethod
    def __find_recent_workday(cls, day: int):
        now = datetime.now()
        date = datetime(now.year, now.month, day)
        if date.weekday() < 5:
            return date.day
        else:
            diff = 1
            while True:
                previous_day = date - timedelta(days=diff)
                if previous_day.weekday() < 5:
                    return previous_day.day
                else:
                    diff += 1


SQLALCHEMY_DATABASE_URL = (
    f'mysql+pymysql://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
    f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
)
if DataBaseConfig.db_type == 'postgresql':
    SQLALCHEMY_DATABASE_URL = (
        f'postgresql+psycopg2://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
        f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
    )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=DataBaseConfig.db_echo,
    max_overflow=DataBaseConfig.db_max_overflow,
    pool_size=DataBaseConfig.db_pool_size,
    pool_recycle=DataBaseConfig.db_pool_recycle,
    # pool_timeout=DataBaseConfig.db_pool_timeout,
    # postgresql不支持超时
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Redis JobStore 配置（用于多 Worker 共享）
redis_jobstore_config = dict(
    host=RedisConfig.redis_host,
    port=RedisConfig.redis_port,
    username=RedisConfig.redis_username,
    password=RedisConfig.redis_password,
    db=RedisConfig.redis_database,
)

job_stores = {
    # 使用 MemoryJobStore，每个 Worker 独立调度
    # 并发控制由 DistributedJobLock 通过 Redis 锁实现
    'default': MemoryJobStore(),
    'sqlalchemy': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL, engine=engine),
    'redis': RedisJobStore(**redis_jobstore_config),
}
executors = {'default': AsyncIOExecutor(), 'processpool': ProcessPoolExecutor(5)}
job_defaults = {'coalesce': True, 'max_instances': 1, 'misfire_grace_time': 60}
scheduler = AsyncIOScheduler()
scheduler.configure(jobstores=job_stores, executors=executors, job_defaults=job_defaults)


class DistributedJobLock:
    """
    分布式任务锁 - 用于控制多 Worker 下的任务执行

    - 禁止并发(concurrent='1'): 使用分布式锁，只有获取锁的 Worker 执行
    - 允许并发(concurrent='0'): 多个 Worker 可以同时执行
    """

    # Redis key 前缀
    CONCURRENT_CONFIG_PREFIX = "scheduler:job_concurrent:"
    STATUS_CONFIG_PREFIX = "scheduler:job_status:"
    LOCK_PREFIX = "scheduler:job_lock:"

    @classmethod
    async def set_job_concurrent(cls, job_id: str, concurrent: str, redis=None):
        """记录任务的并发配置到 Redis"""
        key = f"{cls.CONCURRENT_CONFIG_PREFIX}{job_id}"
        if redis:
            await redis.set(key, concurrent)
            logger.debug(f"[Worker-{WORKER_ID}] 设置任务并发配置: job_id={job_id}, concurrent={concurrent}")
        else:
            from config.get_redis import RedisUtil
            async with RedisUtil.get_redis_connection() as redis:
                await redis.set(key, concurrent)
                logger.debug(f"[Worker-{WORKER_ID}] 设置任务并发配置: job_id={job_id}, concurrent={concurrent}")

    @classmethod
    async def get_job_concurrent(cls, job_id: str, redis=None) -> str:
        """从 Redis 获取任务的并发配置，默认禁止并发"""
        key = f"{cls.CONCURRENT_CONFIG_PREFIX}{job_id}"
        if redis:
            value = await redis.get(key)
            if value:
                return value.decode() if isinstance(value, bytes) else value
            return '1'
        else:
            from config.get_redis import RedisUtil
            async with RedisUtil.get_redis_connection() as redis:
                value = await redis.get(key)
                if value:
                    return value.decode() if isinstance(value, bytes) else value
                return '1'  # 默认禁止并发

    @classmethod
    async def remove_job_concurrent(cls, job_id: str, redis=None):
        """从 Redis 移除任务的并发配置"""
        key = f"{cls.CONCURRENT_CONFIG_PREFIX}{job_id}"
        if redis:
            await redis.delete(key)
        else:
            from config.get_redis import RedisUtil
            async with RedisUtil.get_redis_connection() as redis:
                await redis.delete(key)

    @classmethod
    async def set_job_status(cls, job_id: str, status: str, redis=None):
        """记录任务的启用/暂停状态到 Redis"""
        key = f"{cls.STATUS_CONFIG_PREFIX}{job_id}"
        if redis:
            await redis.set(key, status)
            logger.debug(f"[Worker-{WORKER_ID}] 设置任务状态: job_id={job_id}, status={status}")
        else:
            from config.get_redis import RedisUtil
            async with RedisUtil.get_redis_connection() as redis:
                await redis.set(key, status)
                logger.debug(f"[Worker-{WORKER_ID}] 设置任务状态: job_id={job_id}, status={status}")

    @classmethod
    async def get_job_status(cls, job_id: str, redis=None) -> str:
        """从 Redis 获取任务的启用/暂停状态，默认暂停"""
        key = f"{cls.STATUS_CONFIG_PREFIX}{job_id}"
        if redis:
            value = await redis.get(key)
            if value:
                return value.decode() if isinstance(value, bytes) else value
            return '1'
        else:
            from config.get_redis import RedisUtil
            async with RedisUtil.get_redis_connection() as redis:
                value = await redis.get(key)
                if value:
                    return value.decode() if isinstance(value, bytes) else value
                return '1'  # 默认暂停

    @classmethod
    async def remove_job_status(cls, job_id: str, redis=None):
        """从 Redis 移除任务的状态配置"""
        key = f"{cls.STATUS_CONFIG_PREFIX}{job_id}"
        if redis:
            await redis.delete(key)
        else:
            from config.get_redis import RedisUtil
            async with RedisUtil.get_redis_connection() as redis:
                await redis.delete(key)

    @classmethod
    async def try_acquire_lock(cls, job_id: str, lock_timeout: int = 60) -> tuple[bool, str]:
        """
        尝试获取分布式锁

        Args:
            job_id: 任务ID
            lock_timeout: 锁超时时间（秒）

        Returns:
            (是否获取成功, 锁值)
        """
        from config.get_redis import RedisUtil

        lock_key = f"{cls.LOCK_PREFIX}{job_id}"
        lock_value = f"{WORKER_ID}:{datetime.now().isoformat()}"

        async with RedisUtil.get_redis_connection() as redis:
            # 使用 SETNX 实现分布式锁
            lock_acquired = await redis.set(
                lock_key,
                lock_value,
                nx=True,
                ex=lock_timeout
            )

            if lock_acquired:
                logger.debug(f"[Worker-{WORKER_ID}] 获取任务锁成功: job_id={job_id}")
                return True, lock_value

            # 检查锁是否异常（无过期时间）
            ttl = await redis.ttl(lock_key)
            if ttl == -1:
                logger.warning(f"[Worker-{WORKER_ID}] 发现异常锁(无TTL)，尝试清理: {lock_key}")
                await redis.delete(lock_key)
                lock_acquired = await redis.set(lock_key, lock_value, nx=True, ex=lock_timeout)
                if lock_acquired:
                    return True, lock_value

            current_holder = await redis.get(lock_key)
            logger.debug(f"[Worker-{WORKER_ID}] 任务锁已被占用: job_id={job_id}, holder={current_holder}, TTL={ttl}s")
            return False, ""

    @classmethod
    async def release_lock(cls, job_id: str, lock_value: str):
        """
        释放分布式锁（只释放自己持有的锁）

        Args:
            job_id: 任务ID
            lock_value: 锁值（用于验证持有者）
        """
        from config.get_redis import RedisUtil

        lock_key = f"{cls.LOCK_PREFIX}{job_id}"

        async with RedisUtil.get_redis_connection() as redis:
            current_value = await redis.get(lock_key)
            if current_value:
                current_str = current_value.decode() if isinstance(current_value, bytes) else current_value
                if current_str == lock_value:
                    await redis.delete(lock_key)
                    logger.debug(f"[Worker-{WORKER_ID}] 释放任务锁: job_id={job_id}")
                else:
                    logger.debug(f"[Worker-{WORKER_ID}] 锁已被其他进程持有或已过期，跳过释放: job_id={job_id}")


def create_distributed_job_wrapper(job_id: str, job_func: Callable, concurrent: str, execution_timeout: int = 280) -> Callable:
    """
    创建带分布式锁控制的任务包装器

    Args:
        job_id: 任务ID
        job_func: 原始任务函数
        concurrent: 并发配置 ('0'=允许并发, '1'=禁止并发)
        execution_timeout: 任务执行超时时间（秒），默认280秒（小于锁超时300秒）
        注意: concurrent 参数在创建时传入，但执行时会从 Redis 重新获取最新配置

    Returns:
        包装后的任务函数
    """
    is_async = iscoroutinefunction(job_func)

    if is_async:
        @functools.wraps(job_func)
        async def async_wrapper(*args, **kwargs):
            # 每次执行时从 Redis 获取最新的配置（添加超时保护，防止阻塞事件循环）
            try:
                current_status = await asyncio.wait_for(
                    DistributedJobLock.get_job_status(job_id),
                    timeout=5  # Redis 查询超时 5 秒
                )
            except asyncio.TimeoutError:
                logger.warning(f"[Worker-{WORKER_ID}] 获取任务状态超时，使用默认值继续: job_id={job_id}")
                current_status = '1'  # 默认暂停
            except Exception as e:
                logger.warning(f"[Worker-{WORKER_ID}] 获取任务状态失败: job_id={job_id}, error={e}")
                current_status = '1'  # 出错时默认暂停

            # 检查任务是否处于暂停状态
            if current_status != '0':
                logger.info(f"[Worker-{WORKER_ID}] 任务已暂停，跳过执行: job_id={job_id}, status={current_status}")
                return None

            try:
                current_concurrent = await asyncio.wait_for(
                    DistributedJobLock.get_job_concurrent(job_id),
                    timeout=5  # Redis 查询超时 5 秒
                )
            except asyncio.TimeoutError:
                logger.warning(f"[Worker-{WORKER_ID}] 获取并发配置超时，使用默认值: job_id={job_id}")
                current_concurrent = '1'  # 默认禁止并发
            except Exception as e:
                logger.warning(f"[Worker-{WORKER_ID}] 获取并发配置失败: job_id={job_id}, error={e}")
                current_concurrent = '1'

            if current_concurrent == '0':
                # 允许并发：直接执行（也加超时保护）
                logger.debug(f"[Worker-{WORKER_ID}] 执行并发任务: job_id={job_id}")
                try:
                    return await asyncio.wait_for(
                        job_func(*args, **kwargs),
                        timeout=execution_timeout
                    )
                except asyncio.TimeoutError:
                    logger.error(f"[Worker-{WORKER_ID}] 并发任务执行超时: job_id={job_id}, timeout={execution_timeout}s")
                    return None
            else:
                # 禁止并发：需要获取锁
                try:
                    acquired, lock_value = await asyncio.wait_for(
                        DistributedJobLock.try_acquire_lock(job_id),
                        timeout=5
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"[Worker-{WORKER_ID}] 获取分布式锁超时，跳过执行: job_id={job_id}")
                    return None

                if not acquired:
                    logger.info(f"[Worker-{WORKER_ID}] 任务已被其他 Worker 执行，跳过: job_id={job_id}")
                    return None

                try:
                    logger.info(f"[Worker-{WORKER_ID}] 开始执行单例任务: job_id={job_id}")
                    logger.debug(f"[Worker-{WORKER_ID}] 准备调用任务函数...")
                    result = await asyncio.wait_for(
                        job_func(*args, **kwargs),
                        timeout=execution_timeout
                    )
                    logger.debug(f"[Worker-{WORKER_ID}] 任务函数执行完成: job_id={job_id}")
                    return result
                except asyncio.TimeoutError:
                    logger.error(f"[Worker-{WORKER_ID}] 单例任务执行超时: job_id={job_id}, timeout={execution_timeout}s")
                    return None
                except Exception as e:
                    logger.error(f"[Worker-{WORKER_ID}] 任务执行异常: job_id={job_id}, error={e}")
                    raise
                finally:
                    # 释放锁（添加超时保护，防止阻塞）
                    try:
                        await asyncio.wait_for(
                            DistributedJobLock.release_lock(job_id, lock_value),
                            timeout=5
                        )
                    except asyncio.TimeoutError:
                        logger.error(f"[Worker-{WORKER_ID}] 释放锁超时: job_id={job_id}，锁将在 TTL 后自动过期")
                    except Exception as e:
                        logger.error(f"[Worker-{WORKER_ID}] 释放锁失败: job_id={job_id}, error={e}")
        return async_wrapper
    else:
        @functools.wraps(job_func)
        def sync_wrapper(*args, **kwargs):
            import asyncio

            # 获取或创建事件循环
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # 从 Redis 获取最新的配置
            current_status = loop.run_until_complete(
                DistributedJobLock.get_job_status(job_id)
            )

            # 检查任务是否处于暂停状态
            if current_status != '0':
                logger.info(f"[Worker-{WORKER_ID}] 任务已暂停，跳过执行: job_id={job_id}, status={current_status}")
                return None

            current_concurrent = loop.run_until_complete(
                DistributedJobLock.get_job_concurrent(job_id)
            )

            if current_concurrent == '0':
                # 允许并发：直接执行
                logger.debug(f"[Worker-{WORKER_ID}] 执行并发任务: job_id={job_id}")
                return job_func(*args, **kwargs)
            else:
                # 禁止并发：需要获取锁
                acquired, lock_value = loop.run_until_complete(
                    DistributedJobLock.try_acquire_lock(job_id)
                )
                if not acquired:
                    logger.info(f"[Worker-{WORKER_ID}] 任务已被其他 Worker 执行，跳过: job_id={job_id}")
                    return None

                try:
                    logger.info(f"[Worker-{WORKER_ID}] 开始执行单例任务: job_id={job_id}")
                    return job_func(*args, **kwargs)
                finally:
                    loop.run_until_complete(
                        DistributedJobLock.release_lock(job_id, lock_value)
                    )
        return sync_wrapper


class SchedulerUtil:
    """
    定时任务相关方法
    """

    # 存储订阅任务引用，用于关闭时取消
    _subscriber_task: Optional[asyncio.Task] = None

    @classmethod
    async def init_system_scheduler(cls):
        """
        应用启动时初始化定时任务

        多 Worker 模式下的处理逻辑:
        1. 使用 Redis JobStore 确保任务共享
        2. 使用 replace_existing=True 避免重复添加
        3. 根据 concurrent 配置决定是否需要分布式锁
        4. 启动 Redis Pub/Sub 订阅，监听跨 Worker 的任务同步消息
        """
        logger.info(f'[Worker-{WORKER_ID}] 开始启动定时任务...')
        scheduler.start()

        async with AsyncSessionLocal() as session:
            job_list = await JobDao.get_job_list_for_scheduler(session)
            for item in job_list:
                # 记录任务的并发配置和状态到 Redis
                await DistributedJobLock.set_job_concurrent(str(item.job_id), item.concurrent)
                await DistributedJobLock.set_job_status(str(item.job_id), item.status)
                # 添加任务（replace_existing=True 确保幂等）
                cls._add_scheduler_job_sync(item)

        scheduler.add_listener(cls.scheduler_event_listener, EVENT_ALL)

        # 启动 Redis Pub/Sub 订阅，监听任务同步消息
        cls._subscriber_task = asyncio.create_task(cls._start_job_sync_subscriber())

        logger.info(f'[Worker-{WORKER_ID}] 系统初始定时任务加载成功，共 {len(job_list) if "job_list" in dir() else 0} 个任务')

    @classmethod
    async def close_system_scheduler(cls):
        """
        应用关闭时关闭定时任务

        :return:
        """
        # 取消 Pub/Sub 订阅任务
        if cls._subscriber_task and not cls._subscriber_task.done():
            cls._subscriber_task.cancel()
            try:
                await cls._subscriber_task
            except asyncio.CancelledError:
                pass
            logger.info(f'[Worker-{WORKER_ID}] 已取消任务同步订阅')

        scheduler.shutdown()
        logger.info(f'[Worker-{WORKER_ID}] 关闭定时任务成功')

    @classmethod
    def get_scheduler_job(cls, job_id: Union[str, int]):
        """
        根据任务id获取任务对象

        :param job_id: 任务id
        :return: 任务对象
        """
        query_job = scheduler.get_job(job_id=str(job_id))

        return query_job

    @classmethod
    async def add_scheduler_job(cls, job_info: JobModel):
        """
        根据输入的任务对象信息添加任务（异步版本，广播到所有 Worker）

        多 Worker 模式:
        - 使用 replace_existing=True 确保幂等
        - 根据 concurrent 配置包装任务函数
        - 统一使用 'default' (Memory) jobstore
        - 通过 Redis Pub/Sub 广播到其他 Worker

        :param job_info: 任务对象信息
        :return:
        """
        from config.get_redis import RedisUtil

        job_id = str(job_info.job_id)

        # 复用一个 Redis 连接完成所有操作
        async with RedisUtil.get_redis_connection() as redis:
            # 记录并发配置和状态到 Redis
            await DistributedJobLock.set_job_concurrent(job_id, job_info.concurrent, redis=redis)
            await DistributedJobLock.set_job_status(job_id, job_info.status, redis=redis)

            # 调用同步方法添加任务
            cls._add_scheduler_job_sync(job_info)

            # 发布添加消息到 Redis，通知其他 Worker
            await cls._publish_job_sync_message({
                'action': 'add',
                'job_id': job_id,
                'source_worker': WORKER_ID
            }, redis=redis)

    @classmethod
    def _add_scheduler_job_sync(cls, job_info: JobModel):
        """
        添加任务到调度器（同步内部方法）

        :param job_info: 任务对象信息
        """
        job_id = str(job_info.job_id)
        job_func = eval(job_info.invoke_target)
        job_executor = job_info.job_executor

        # 异步函数强制使用 default 执行器
        if iscoroutinefunction(job_func):
            job_executor = 'default'

        # 包装任务函数（添加分布式锁控制）
        wrapped_func = create_distributed_job_wrapper(
            job_id=job_id,
            job_func=job_func,
            concurrent=job_info.concurrent
        )

        # 统一使用 'default' (Redis) jobstore 确保多 Worker 共享
        jobstore = 'default'

        scheduler.add_job(
            func=wrapped_func,
            trigger=MyCronTrigger.from_crontab(job_info.cron_expression),
            args=job_info.job_args.split(',') if job_info.job_args else None,
            kwargs=json.loads(job_info.job_kwargs) if job_info.job_kwargs else None,
            id=job_id,
            name=job_info.job_name,
            misfire_grace_time=1000000000000 if job_info.misfire_policy == '3' else None,
            coalesce=True if job_info.misfire_policy == '2' else False,
            max_instances=3 if job_info.concurrent == '0' else 1,
            jobstore=jobstore,
            executor=job_executor,
            replace_existing=True,  # 关键：避免重复添加
        )

    @classmethod
    async def execute_scheduler_job_once(cls, job_info: JobModel):
        """
        根据输入的任务对象执行一次任务

        :param job_info: 任务对象信息
        :return:
        """
        from config.get_redis import RedisUtil

        job_id = str(job_info.job_id)
        job_func = eval(job_info.invoke_target)
        job_executor = job_info.job_executor

        if iscoroutinefunction(job_func):
            job_executor = 'default'

        # 复用一个 Redis 连接完成所有操作
        async with RedisUtil.get_redis_connection() as redis:
            # 记录并发配置和状态到 Redis
            await DistributedJobLock.set_job_concurrent(job_id, job_info.concurrent, redis=redis)
            await DistributedJobLock.set_job_status(job_id, job_info.status, redis=redis)

        # 包装任务函数
        wrapped_func = create_distributed_job_wrapper(
            job_id=job_id,
            job_func=job_func,
            concurrent=job_info.concurrent
        )

        job_trigger = DateTrigger()
        if job_info.status == '0':
            job_trigger = OrTrigger(triggers=[DateTrigger(), MyCronTrigger.from_crontab(job_info.cron_expression)])

        scheduler.add_job(
            func=wrapped_func,
            trigger=job_trigger,
            args=job_info.job_args.split(',') if job_info.job_args else None,
            kwargs=json.loads(job_info.job_kwargs) if job_info.job_kwargs else None,
            id=job_id,
            name=job_info.job_name,
            misfire_grace_time=1000000000000 if job_info.misfire_policy == '3' else None,
            coalesce=True if job_info.misfire_policy == '2' else False,
            max_instances=3 if job_info.concurrent == '0' else 1,
            jobstore='default',
            executor=job_executor,
            replace_existing=True,
        )

    @classmethod
    async def remove_scheduler_job(cls, job_id: Union[str, int]):
        """
        根据任务id移除任务（广播到所有 Worker）

        :param job_id: 任务id
        :return:
        """
        from config.get_redis import RedisUtil

        job_id_str = str(job_id)

        # 先在本地移除
        cls._local_remove_scheduler_job(job_id_str)

        # 复用一个 Redis 连接完成所有操作
        async with RedisUtil.get_redis_connection() as redis:
            # 清理 Redis 中的并发配置和状态
            await DistributedJobLock.remove_job_concurrent(job_id_str, redis=redis)
            await DistributedJobLock.remove_job_status(job_id_str, redis=redis)

            # 发布移除消息到 Redis，通知其他 Worker
            await cls._publish_job_sync_message({
                'action': 'remove',
                'job_id': job_id_str,
                'source_worker': WORKER_ID
            }, redis=redis)

    @classmethod
    def _local_remove_scheduler_job(cls, job_id: str):
        """
        从本地调度器移除任务（不广播）

        :param job_id: 任务id
        """
        query_job = cls.get_scheduler_job(job_id=job_id)
        if query_job:
            scheduler.remove_job(job_id=job_id)
            logger.debug(f'[Worker-{WORKER_ID}] 本地移除任务: job_id={job_id}')

    @classmethod
    def scheduler_event_listener(cls, event):
        # 获取事件类型和任务ID
        event_type = event.__class__.__name__
        # 获取任务执行异常信息
        status = '0'
        exception_info = ''
        if event_type == 'JobExecutionEvent' and event.exception:
            exception_info = str(event.exception)
            status = '1'

        # 记录调度延迟信息（关键排查信息）
        if hasattr(event, 'scheduled_run_time') and event.scheduled_run_time:
            scheduled_time = event.scheduled_run_time
            actual_time = datetime.now(scheduled_time.tzinfo) if scheduled_time.tzinfo else datetime.now()
            delay_seconds = (actual_time - scheduled_time).total_seconds()
            if delay_seconds > 5:  # 延迟超过5秒才记录警告
                logger.warning(
                    f"[Scheduler] 任务延迟执行: job_id={getattr(event, 'job_id', 'N/A')}, "
                    f"计划时间={scheduled_time.strftime('%H:%M:%S')}, "
                    f"实际时间={actual_time.strftime('%H:%M:%S')}, "
                    f"延迟={delay_seconds:.1f}秒"
                )

        if hasattr(event, 'job_id'):
            job_id = event.job_id
            query_job = cls.get_scheduler_job(job_id=job_id)
            if query_job:
                query_job_info = query_job.__getstate__()
                # 获取任务名称
                job_name = query_job_info.get('name')
                # 获取任务组名
                job_group = query_job._jobstore_alias
                # 获取任务执行器
                job_executor = query_job_info.get('executor')
                # 获取调用目标字符串
                invoke_target = query_job_info.get('func')
                # 获取调用函数位置参数
                args = query_job_info.get('args')
                job_args = ','.join(args) if args else ''
                # 获取调用函数关键字参数
                kwargs = query_job_info.get('kwargs')
                job_kwargs = json.dumps(kwargs) if kwargs else '{}'
                # 获取任务触发器
                job_trigger = str(query_job_info.get('trigger'))
                # 构造日志消息（包含 Worker ID）
                job_message = (
                    f"事件类型: {event_type}, 任务ID: {job_id}, 任务名称: {job_name}, "
                    f"Worker: {WORKER_ID}, 执行于{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                )
                job_log = JobLogModel(
                    jobName=job_name,
                    jobGroup=job_group,
                    jobExecutor=job_executor,
                    invokeTarget=invoke_target,
                    jobArgs=job_args,
                    jobKwargs=job_kwargs,
                    jobTrigger=job_trigger,
                    jobMessage=job_message,
                    status=status,
                    exceptionInfo=exception_info,
                    createTime=datetime.now(),
                )
                session = SessionLocal()
                JobLogService.add_job_log_services(session, job_log)
                session.close()

    @classmethod
    async def _publish_job_sync_message(cls, message: dict, redis=None):
        """
        发布任务同步消息到 Redis Pub/Sub

        :param message: 消息内容，包含 action, job_id, source_worker 等字段
        :param redis: 可选的 Redis 连接，传入则复用，否则新建
        """
        try:
            if redis:
                await redis.publish(SCHEDULER_CHANNEL, json.dumps(message))
                logger.debug(f'[Worker-{WORKER_ID}] 发布任务同步消息: {message}')
            else:
                from config.get_redis import RedisUtil
                async with RedisUtil.get_redis_connection() as redis:
                    await redis.publish(SCHEDULER_CHANNEL, json.dumps(message))
                    logger.debug(f'[Worker-{WORKER_ID}] 发布任务同步消息: {message}')
        except Exception as e:
            logger.error(f'[Worker-{WORKER_ID}] 发布任务同步消息失败: {e}')

    @classmethod
    async def _start_job_sync_subscriber(cls):
        """
        启动 Redis Pub/Sub 订阅，监听任务同步消息

        消息格式:
        {
            "action": "remove" | "add",
            "job_id": "任务ID",
            "source_worker": "发送消息的 Worker ID"
        }
        """
        from redis import asyncio as aioredis
        from config.env import RedisConfig

        logger.info(f'[Worker-{WORKER_ID}] 启动任务同步订阅...')

        while True:
            try:
                # 创建独立的 Redis 连接用于订阅（订阅需要专用连接）
                redis = aioredis.Redis(
                    host=RedisConfig.redis_host,
                    port=RedisConfig.redis_port,
                    username=RedisConfig.redis_username,
                    password=RedisConfig.redis_password,
                    db=RedisConfig.redis_database,
                    encoding='utf-8',
                    decode_responses=True,
                )

                pubsub = redis.pubsub()
                await pubsub.subscribe(SCHEDULER_CHANNEL)
                logger.info(f'[Worker-{WORKER_ID}] 已订阅任务同步频道: {SCHEDULER_CHANNEL}')

                try:
                    async for message in pubsub.listen():
                        if message['type'] == 'message':
                            await cls._handle_job_sync_message(message['data'])
                except asyncio.CancelledError:
                    logger.info(f'[Worker-{WORKER_ID}] 任务同步订阅被取消')
                    raise
                finally:
                    await pubsub.unsubscribe(SCHEDULER_CHANNEL)
                    await redis.close()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f'[Worker-{WORKER_ID}] 任务同步订阅异常，5秒后重试: {e}')
                await asyncio.sleep(5)

    @classmethod
    async def _handle_job_sync_message(cls, data: str):
        """
        处理任务同步消息

        :param data: JSON 格式的消息数据
        """
        try:
            message = json.loads(data)
            action = message.get('action')
            job_id = message.get('job_id')
            source_worker = message.get('source_worker')

            # 忽略自己发送的消息
            if source_worker == WORKER_ID:
                return

            if action == 'remove':
                # 从本地调度器移除任务
                cls._local_remove_scheduler_job(job_id)
                logger.info(f'[Worker-{WORKER_ID}] 收到移除任务消息，已本地移除: job_id={job_id}, from={source_worker}')

            elif action == 'add':
                # 添加任务需要从数据库重新获取完整信息
                async with AsyncSessionLocal() as session:
                    from module_admin.system.service.job_service import JobService
                    job_info = await JobService.job_detail_services(session, int(job_id))
                    if job_info and job_info.job_id:
                        # 先移除可能存在的旧任务
                        cls._local_remove_scheduler_job(job_id)
                        # 设置并发配置和状态到 Redis
                        await DistributedJobLock.set_job_concurrent(job_id, job_info.concurrent)
                        await DistributedJobLock.set_job_status(job_id, job_info.status)
                        # 添加新任务
                        cls._add_scheduler_job_sync(job_info)
                        logger.info(f'[Worker-{WORKER_ID}] 收到添加任务消息，已本地添加: job_id={job_id}, from={source_worker}')

        except json.JSONDecodeError as e:
            logger.error(f'[Worker-{WORKER_ID}] 解析任务同步消息失败: {e}')
        except Exception as e:
            logger.error(f'[Worker-{WORKER_ID}] 处理任务同步消息异常: {e}')
