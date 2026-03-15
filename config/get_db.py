import time

from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from config.database import async_engine, AsyncSessionLocal

from utils.log_util import logger


async def get_db():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接

    :return:
    """

    async with AsyncSessionLocal() as current_db:
        yield current_db


# 修改get_db函数，使其更适合你的使用场景
async def get_db_session():
    """
    获取数据库会话的简化版本
    """
    session = AsyncSessionLocal()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


async def init_create_table():
    """
    应用启动时初始化数据库连接

    :return:
    """
    logger.info('初始化数据库连接...')
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info('数据库连接成功')
