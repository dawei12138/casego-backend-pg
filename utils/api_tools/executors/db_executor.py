#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：DbConnectionExecutor.py
@Author  ：david
@Date    ：2025-08-12 11:15 
"""
import re
from jsonpath import jsonpath
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataQueryModel, \
    Cache_dataPageQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from module_admin.api_testing.api_databases.service.api_databases_service import Api_databasesService
from utils.api_tools.executors.strategies import ExecutorStrategy
import time
from abc import ABC, abstractmethod
from typing import Union

from utils.api_tools.executors.db_mysql_control import MysqlDB
from utils.api_tools.executors.models import ExecutorContext, SetupConfig, TeardownConfig, ExecutorResult
from utils.api_tools.regular_control import advanced_template_parser


class DbConnectionExecutor(ExecutorStrategy):
    """数据库连接执行器"""

    async def execute(self, context: ExecutorContext, config: Union[SetupConfig, TeardownConfig]) -> ExecutorResult:
        start_time = time.time()
        exec_log = {"extract_variables": []}
        try:
            script = getattr(config, 'script', '') or getattr(config, 'db_operation', '')
            if not script:
                return ExecutorResult(success=False, error="数据库脚本为空")

            # 选择数据库连接
            db_conn_config_id = getattr(config, 'db_connection_id', '') or getattr(config, 'database_id', '')
            if not db_conn_config_id:
                # 这里可以根据db_connection_id选择不同的连接
                return ExecutorResult(success=False, error="数据库连接ID为空")

            db_conn_config = await Api_databasesService.api_databases_detail_services(query_db=context.mysql_obj,
                                                                                      id=int(db_conn_config_id))
            # 数据库语句替换，需要考虑redis缓存替换和全局变量替换两种方式，全局变量替换优先级更高

            query_obj = Cache_dataQueryModel(user_id=context.user_id, environment_id=context.env_id)
            replace_script = await advanced_template_parser(script, context.redis_obj, query_obj,
                                                            variables_dict=context.parameterization)
            exec_log.update({"script": replace_script})
            # 执行数据库操作，查询和增删改分开，考虑多行sql执行如何进行，这里需要根据数据库类型做判断使用不同类型的数据库连接
            sql_res = None
            if db_conn_config.db_type == "1":
                pass
                mysql_conn = MysqlDB(db_conn_config)
                sql_type = DbConnectionExecutor.get_sql_execution_type(replace_script)
                sql_res = getattr(mysql_conn, f'{sql_type}', '')(replace_script)
                exec_log.update({"sql_res": sql_res})
            else:
                raise Exception("暂时不支持REDIS计划")
            # 执行后的结果存到redis缓存中，jsonpath提取

            if sql_res and config.extract_variables:
                for variables in config.extract_variables:
                    value = jsonpath(sql_res, variables.get('jsonpath'))
                    cache_value = str(value) if value else " "
                    query = Cache_dataPageQueryModel(cache_key=variables.get('variable_name'),
                                                     environment_id=context.env_id, user_id=context.user_id,
                                                     cache_value=cache_value)
                    await Cache_dataService.add_cache_data_services(context.redis_obj, query)
                    exec_log["extract_variables"].append({variables.get('variable_name'): cache_value})

            execution_time = time.time() - start_time
            return ExecutorResult(
                success=True,
                message="数据库操作执行成功",
                log=exec_log,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return ExecutorResult(
                success=False,
                error=f"数据库操作失败: {str(e)},日志{exec_log}",
                log=f"数据库操作失败: {str(e)},日志{exec_log}",
                message=f"数据库操作失败: {str(e)},日志{exec_log}",
                execution_time=execution_time
            )

    @classmethod
    def get_sql_execution_type(cls, sql):
        """
        识别SQL语句类型，返回应该使用的执行函数类型

        参数:
            sql (str): SQL语句

        返回:
            str: 'query'(查询-使用query函数), 'execute'(增删改-使用execute函数), 'unknown'(未识别-不操作)
        """
        if not sql or not sql.strip():
            return 'unknown'

        # 去除首尾空白并转换为大写
        sql = sql.strip().upper()

        # 查询语句 - 使用query函数
        # if re.match(r'^\s*(SELECT|WITH)', sql):
        #     return 'query'

        # 增删改语句 - 使用execute函数
        if re.match(r'^\s*(INSERT\s+INTO|UPDATE\s+|DELETE\s+FROM)', sql):
            return 'execute'

        # 未识别的语句类型 - 不操作
        else:
            return 'query'
