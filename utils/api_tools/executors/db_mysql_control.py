#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@Project ：fast_api_admin
@File    ：mysql_control.py
@Author  ：david
@Date    ：2025-08-11 15:23

"""
from utils.log_util import logger
import ast
from dataclasses import dataclass

import datetime
import decimal
from warnings import filterwarnings
import pymysql
from typing import List, Union, Text, Dict

# 忽略 Mysql 告警信息
filterwarnings("ignore", category=pymysql.Warning)


class MysqlDB:
    """ mysql 封装,接收config对象 ，建立连接，执行语句"""

    def __init__(self, config):
        try:
            self.conn = pymysql.connect(
                host=config.host,
                user=config.username,
                password=config.password,
                port=config.port
            )

            # 使用 cursor 方法获取操作游标，得到一个可以执行sql语句，并且操作结果为字典返回的游标
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except AttributeError as error:
            logger.error(f"数据库连接失败，失败原因{error}", )

    @staticmethod
    def test_connection(host: str, port: int, username: str, password: str) -> dict:
        """
        测试数据库连接
        :param host: 数据库主机
        :param port: 数据库端口
        :param username: 用户名
        :param password: 密码
        :return: 包含连接状态和消息的字典
        """
        conn = None
        try:
            conn = pymysql.connect(
                host=host,
                user=username,
                password=password,
                port=port,
                connect_timeout=10
            )
            # 执行简单查询验证连接
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
            return {"success": True, "message": "数据库连接成功"}
        except pymysql.err.OperationalError as e:
            error_code, error_msg = e.args
            logger.error(f"数据库连接失败，错误码: {error_code}, 错误信息: {error_msg}")
            return {"success": False, "message": f"连接失败: {error_msg}"}
        except Exception as e:
            logger.error(f"数据库连接测试异常: {str(e)}")
            return {"success": False, "message": f"连接异常: {str(e)}"}
        finally:
            if conn:
                conn.close()

    @staticmethod
    def execute_script(host: str, port: int, username: str, password: str, script: str) -> dict:
        """
        执行SQL脚本
        :param host: 数据库主机
        :param port: 数据库端口
        :param username: 用户名
        :param password: 密码
        :param script: SQL脚本
        :return: 包含执行状态、消息和数据的字典
        """
        import time
        conn = None
        start_time = time.time()
        try:
            conn = pymysql.connect(
                host=host,
                user=username,
                password=password,
                port=port,
                connect_timeout=10,
                charset='utf8mb4'
            )
            with conn.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
                # 判断是否是查询语句
                script_upper = script.strip().upper()
                is_query = script_upper.startswith('SELECT') or script_upper.startswith('SHOW') or script_upper.startswith('DESC') or script_upper.startswith('EXPLAIN')

                cursor.execute(script)
                execute_time = int((time.time() - start_time) * 1000)  # 毫秒

                if is_query:
                    # 查询语句返回数据
                    data = cursor.fetchall()
                    # 处理特殊数据类型
                    rows = MysqlDB.sql_data_handler(list(data)) if data else []
                    # 获取列名
                    columns = [desc[0] for desc in cursor.description] if cursor.description else []
                    total = len(rows)
                    return {
                        "success": True,
                        "message": "执行成功",
                        "data": {
                            "columns": columns,
                            "rows": rows,
                            "affectedRows": total,
                            "executeTime": execute_time,
                            "total": total
                        }
                    }
                else:
                    # 非查询语句返回影响行数
                    conn.commit()
                    affected_rows = cursor.rowcount
                    return {
                        "success": True,
                        "message": "执行成功",
                        "data": {
                            "columns": [],
                            "rows": [],
                            "affectedRows": affected_rows,
                            "executeTime": execute_time,
                            "total": 0
                        }
                    }
        except pymysql.err.ProgrammingError as e:
            execute_time = int((time.time() - start_time) * 1000)
            error_code, error_msg = e.args
            logger.error(f"SQL语法错误，错误码: {error_code}, 错误信息: {error_msg}")
            return {"success": False, "message": f"SQL语法错误: {error_msg}", "data": None}
        except pymysql.err.OperationalError as e:
            execute_time = int((time.time() - start_time) * 1000)
            error_code, error_msg = e.args
            logger.error(f"数据库操作错误，错误码: {error_code}, 错误信息: {error_msg}")
            return {"success": False, "message": f"操作错误: {error_msg}", "data": None}
        except Exception as e:
            execute_time = int((time.time() - start_time) * 1000)
            logger.error(f"SQL执行异常: {str(e)}")
            return {"success": False, "message": f"执行异常: {str(e)}", "data": None}
        finally:
            if conn:
                conn.close()

    def __del__(self):
        try:
            # 关闭游标
            self.cur.close()
            # 关闭连接
            self.conn.close()
        except AttributeError as error:
            logger.error(f"数据库连接失败，失败原因{error}")

    def query(self, sql, state="all"):
        """
            查询
            :param sql:
            :param state:  all 是默认查询全部
            :return:
            """
        try:
            self.cur.execute(sql)

            if state == "all":
                # 查询全部
                data = self.cur.fetchall()
            else:
                # 查询单条
                data = self.cur.fetchone()
            return data
        except AttributeError as error_data:
            logger.error(f"数据库连接失败，失败原因{error_data}")

    def execute(self, sql: Text):
        """
            更新 、 删除、 新增
            :param sql:
            :return:
            """
        try:
            # 使用 execute 操作 sql
            rows = self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            return rows
        except AttributeError as error:
            logger.error(f"数据库连接失败，失败原因{error},sql:{sql}")
            # 如果事务异常，则回滚数据
            self.conn.rollback()
            # raise

    @classmethod
    def sql_data_handler(cls, query_data_list):
        """
        处理部分类型sql查询出来的数据格式
        @param query_data: 查询出来的sql数据
        @param data: 数据池
        @return:
        """
        # 将sql 返回的所有内容全部放入对象中
        data = []
        for query_data in query_data_list:
            for key, value in query_data.items():
                if isinstance(value, decimal.Decimal):
                    query_data[key] = float(value)
                elif isinstance(value, datetime.datetime):
                    query_data[key] = str(value)
                else:
                    query_data[key] = value
            data.append(query_data)
        return data


#
# class SetUpMySQL(MysqlDB):
#     """ 处理前置sql """
#
#     def setup_sql_data(self, sql: Union[List, None]) -> Dict:
#         """
#             处理前置请求sql
#             :param sql:
#             :return:
#             """
#         sql = ast.literal_eval(cache_regular(str(sql)))
#         try:
#             data = {}
#             if sql is not None:
#                 for i in sql:
#                     # 判断断言类型为查询类型的时候，
#                     if i[0:6].upper() == 'SELECT':
#                         sql_date = self.query(sql=i)[0]
#                         for key, value in sql_date.items():
#                             data[key] = value
#                     else:
#                         self.execute(sql=i)
#             return data
#         except IndexError as exc:
#             raise DataAcquisitionFailed("sql 数据查询失败，请检查setup_sql语句是否正确") from exc


if __name__ == '__main__':
    @dataclass
    class Config():
        host = "127.0.0.1"
        username = "root"
        password = "123456"
        port = 3306


    a = MysqlDB(Config)
    b = a.execute(sql="SELECT * FROM `ezdata`.`api_databases` ")
    print(b)
