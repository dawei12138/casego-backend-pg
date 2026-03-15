import asyncio
from datetime import datetime
from sqlalchemy import text, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.exc import SQLAlchemyError
from config.database import AsyncSessionLocal
from config.env import DataBaseConfig
from config.get_redis import RedisUtil
from utils.log_util import logger
from fastapi import FastAPI


class DatabaseTestUtil:
    """数据库和Redis连接测试工具"""

    @classmethod
    def _get_db_label(cls) -> str:
        """获取当前数据库类型标签"""
        return 'PostgreSQL' if DataBaseConfig.db_type == 'postgresql' else 'MySQL'

    @classmethod
    def _get_create_temp_table_sql(cls) -> str:
        """根据数据库类型返回创建临时表的SQL"""
        if DataBaseConfig.db_type == 'postgresql':
            return """
                CREATE TEMPORARY TABLE test_connection_temp (
                    id SERIAL PRIMARY KEY,
                    test_name VARCHAR(100) NOT NULL,
                    test_value VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        else:
            return """
                CREATE TEMPORARY TABLE test_connection_temp (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_name VARCHAR(100) NOT NULL,
                    test_value VARCHAR(200),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """

    @classmethod
    async def test_db_connection(cls):
        """测试数据库连接和基本操作"""
        db_label = cls._get_db_label()
        test_results = {
            'connection': False,
            'query': False,
            'insert': False,
            'delete': False,
            'error': None
        }

        try:
            async with AsyncSessionLocal() as session:
                # 1. 测试连接
                result = await session.execute(text("SELECT 1 as test"))
                if result.fetchone():
                    test_results['connection'] = True

                # 2. 测试查询 - 查询数据库版本和当前时间
                version_result = await session.execute(text("SELECT VERSION() as db_version, NOW() as db_time"))
                version_data = version_result.fetchone()
                if version_data:
                    test_results['query'] = True

                # 3. 创建临时测试表
                create_table_sql = cls._get_create_temp_table_sql()
                await session.execute(text(create_table_sql))

                # 4. 测试插入
                test_data = {
                    'test_name': 'connection_test',
                    'test_value': f'test_value_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                }

                insert_sql = """
                INSERT INTO test_connection_temp (test_name, test_value)
                VALUES (:test_name, :test_value)
                """
                insert_result = await session.execute(text(insert_sql), test_data)
                if insert_result.rowcount > 0:
                    test_results['insert'] = True

                # 5. 查询插入的数据
                select_sql = "SELECT * FROM test_connection_temp WHERE test_name = :test_name"
                select_result = await session.execute(text(select_sql), {'test_name': test_data['test_name']})
                inserted_data = select_result.fetchone()

                # 6. 测试删除
                delete_sql = "DELETE FROM test_connection_temp WHERE test_name = :test_name"
                delete_result = await session.execute(text(delete_sql), {'test_name': test_data['test_name']})
                if delete_result.rowcount > 0:
                    test_results['delete'] = True

                # 提交事务
                await session.commit()

        except SQLAlchemyError as e:
            test_results['error'] = str(e)
            logger.error(f"✗ {db_label}测试失败: {e}")
        except Exception as e:
            test_results['error'] = str(e)
            logger.error(f"✗ {db_label}测试出现异常: {e}")

        return test_results

    @classmethod
    async def test_redis_connection(cls, app: FastAPI):
        """测试Redis连接和基本操作"""
        test_results = {
            'connection': False,
            'set': False,
            'get': False,
            'delete': False,
            'error': None
        }

        try:
            if not hasattr(app.state, 'redis') or app.state.redis is None:
                raise Exception("Redis连接未初始化")

            redis = app.state.redis
            # logger.info("开始测试Redis连接...")

            # 1. 测试连接
            pong = await redis.ping()
            if pong:
                test_results['connection'] = True
                # logger.info("✓ Redis连接测试成功")

            # 2. 测试设置键值对
            timestamp = datetime.now().strftime('%H%M%S')
            test_key_suffix = f"connection_{timestamp}"
            test_value = f"test_value_{datetime.now().timestamp()}"

            await RedisUtil.create_cache_key_value(
                app,
                test_key_suffix,
                test_value,
                expire_time=300,  # 5分钟过期
                namespace="test"
            )
            test_results['set'] = True
            # # logger.info("✓ Redis设置键值对测试成功")

            # 3. 测试获取键值对
            full_key = f"test:{test_key_suffix}"
            stored_value = await redis.get(full_key)
            if stored_value == test_value:
                test_results['get'] = True
                # # logger.info(f"✓ Redis获取键值对测试成功: {stored_value}")

            # 4. 测试删除键
            delete_result = await redis.delete(full_key)
            if delete_result >= 0:  # 删除成功返回删除的键数量
                test_results['delete'] = True
                # # logger.info("✓ Redis删除键测试成功")

            # 5. 测试Redis信息
            info = await redis.info()
            # logger.info(f"✓ Redis服务器信息获取成功 - 版本: {info.get('redis_version', 'unknown')}")

        except Exception as e:
            test_results['error'] = str(e)
            logger.error(f"✗ Redis测试失败: {e}")

        return test_results

    @classmethod
    async def run_full_connection_test(cls, app: FastAPI):
        """运行完整的连接测试"""
        db_label = cls._get_db_label()

        # 测试数据库
        db_results = await cls.test_db_connection()

        # 测试Redis
        redis_results = await cls.test_redis_connection(app)

        # 汇总结果
        for test_name, result in db_results.items():
            if test_name == 'error':
                continue
            status = "✓" if result else "✗"

        if db_results['error']:
            logger.error(f"  {db_label}错误: {db_results['error']}")

        for test_name, result in redis_results.items():
            if test_name == 'error':
                continue
            status = "✓" if result else "✗"

        if redis_results['error']:
            logger.error(f"  Redis错误: {redis_results['error']}")

        # 总体评估
        db_success = all(db_results[k] for k in ['connection', 'query', 'insert', 'delete'])
        redis_success = all(redis_results[k] for k in ['connection', 'set', 'get', 'delete'])

        if db_success and redis_success:
            logger.info(f"🎉 所有测试通过！{db_label}和Redis连接正常")

        return {
            'db': db_results,
            'redis': redis_results,
            'overall_success': db_success and redis_success
        }


# 在主应用中添加测试路由（可选）
def add_test_routes(app: FastAPI):
    """为FastAPI应用添加测试路由"""

    @app.get("/api/test/database", tags=["测试模块"])
    async def test_database_connection():
        """测试数据库连接"""
        db_results = await DatabaseTestUtil.test_db_connection()
        return {"status": "success", "data": db_results}

    @app.get("/api/test/redis", tags=["测试模块"])
    async def test_redis_connection():
        """测试Redis连接"""
        redis_results = await DatabaseTestUtil.test_redis_connection(app)
        return {"status": "success", "data": redis_results}

    @app.get("/api/test/all", tags=["测试模块"])
    async def test_all_connections():
        """测试所有连接"""
        results = await DatabaseTestUtil.run_full_connection_test(app)
        return {"status": "success", "data": results}


# 使用示例
async def run_startup_test(app: FastAPI):
    """在应用启动时运行测试"""
    try:
        await DatabaseTestUtil.run_full_connection_test(app)
    except Exception as e:
        logger.error(f"启动测试失败: {e}")


# 如果需要在命令行中单独测试
if __name__ == "__main__":
    async def standalone_test():
        """独立运行测试"""
        from fastapi import FastAPI

        # 创建临时FastAPI实例用于测试
        test_app = FastAPI()

        # 初始化Redis连接
        test_app.state.redis = await RedisUtil.create_redis_pool()

        try:
            # 运行测试
            await DatabaseTestUtil.run_full_connection_test(test_app)
        finally:
            # 清理资源
            await RedisUtil.close_redis_pool(test_app)


    asyncio.run(standalone_test())