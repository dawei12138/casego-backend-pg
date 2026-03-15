#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fast_api_admin
@File    ：db_redis_control.py
@Author  ：david
@Date    ：2025-12-10

"""
from utils.log_util import logger
from dataclasses import dataclass
import redis
from typing import Optional


class RedisDB:
    """ Redis 封装,接收config对象，建立连接，执行操作"""

    def __init__(self, config):
        try:
            self.conn = redis.Redis(
                host=config.host,
                port=config.port,
                password=config.password if config.password else None,
                decode_responses=True
            )
        except Exception as error:
            logger.error(f"Redis连接失败，失败原因{error}")

    def __del__(self):
        try:
            if self.conn:
                self.conn.close()
        except Exception as error:
            logger.error(f"Redis关闭连接失败，失败原因{error}")

    @staticmethod
    def test_connection(host: str, port: int, password: Optional[str] = None) -> dict:
        """
        测试Redis连接
        :param host: Redis主机
        :param port: Redis端口
        :param password: 密码（可选）
        :return: 包含连接状态和消息的字典
        """
        conn = None
        try:
            conn = redis.Redis(
                host=host,
                port=port,
                password=password if password else None,
                decode_responses=True,
                socket_connect_timeout=10
            )
            # 执行PING命令验证连接
            response = conn.ping()
            if response:
                return {"success": True, "message": "Redis连接成功"}
            else:
                return {"success": False, "message": "Redis连接失败：PING返回异常"}
        except redis.exceptions.AuthenticationError as e:
            logger.error(f"Redis认证失败: {str(e)}")
            return {"success": False, "message": f"认证失败: {str(e)}"}
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Redis连接失败: {str(e)}")
            return {"success": False, "message": f"连接失败: {str(e)}"}
        except redis.exceptions.TimeoutError as e:
            logger.error(f"Redis连接超时: {str(e)}")
            return {"success": False, "message": f"连接超时: {str(e)}"}
        except Exception as e:
            logger.error(f"Redis连接测试异常: {str(e)}")
            return {"success": False, "message": f"连接异常: {str(e)}"}
        finally:
            if conn:
                conn.close()

    def get(self, key: str):
        """
        获取key的值
        :param key: 键名
        :return: 值
        """
        try:
            return self.conn.get(key)
        except Exception as error:
            logger.error(f"Redis获取数据失败，失败原因{error}")
            return None

    def set(self, key: str, value: str, ex: Optional[int] = None):
        """
        设置key的值
        :param key: 键名
        :param value: 值
        :param ex: 过期时间（秒）
        :return: 是否成功
        """
        try:
            return self.conn.set(key, value, ex=ex)
        except Exception as error:
            logger.error(f"Redis设置数据失败，失败原因{error}")
            return False

    def delete(self, key: str):
        """
        删除key
        :param key: 键名
        :return: 删除的key数量
        """
        try:
            return self.conn.delete(key)
        except Exception as error:
            logger.error(f"Redis删除数据失败，失败原因{error}")
            return 0

    def exists(self, key: str) -> bool:
        """
        检查key是否存在
        :param key: 键名
        :return: 是否存在
        """
        try:
            return self.conn.exists(key) > 0
        except Exception as error:
            logger.error(f"Redis检查key失败，失败原因{error}")
            return False


if __name__ == '__main__':
    @dataclass
    class Config:
        host = "127.0.0.1"
        port = 6379
        password = ""

    r = RedisDB(Config)
    result = RedisDB.test_connection("127.0.0.1", 6379, "")
    print(result)
