#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File    ：db_operation_executor.py
@Author  ：david
@Date    ：2025-12-17
@Desc    ：数据库操作执行器
"""
import re
import time
import json
from typing import Dict, Any

from jsonpath import jsonpath

from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataQueryModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from module_admin.api_testing.api_databases.service.api_databases_service import Api_databasesService
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import Task_config
from utils.api_tools.executors.db_mysql_control import MysqlDB
from utils.api_tools.executors.models import ExecutorResult
from utils.api_tools.regular_control import advanced_template_parser
from utils.api_workflow_tools.executors.base_executor import BaseTaskExecutor
from utils.log_util import logger


class DBOperationExecutor(BaseTaskExecutor):
    """
    数据库操作执行器

    支持执行 SQL 查询和增删改操作，支持变量替换和结果提取。
    """

    async def execute(self, task_config: Task_config) -> ExecutorResult:
        """
        执行数据库操作

        Args:
            task_config: 任务配置，包含:
                - db_operation_id: 数据库连接ID
                - db_operation_script: SQL脚本

        Returns:
            执行结果
        """
        start_time = time.time()
        exec_log = {"extract_variables": []}

        try:
            # 获取数据库操作脚本
            script = task_config.db_operation_script
            if not script:
                return ExecutorResult(
                    success=False,
                    error="数据库脚本为空"
                )

            # 获取数据库连接ID
            db_conn_config_id = task_config.db_operation_id
            if not db_conn_config_id:
                return ExecutorResult(
                    success=False,
                    error="数据库连接ID为空"
                )

            exec_log["db_connection_id"] = db_conn_config_id
            exec_log["original_script"] = script

            logger.info(f"开始执行数据库操作，连接ID: {db_conn_config_id}")

            # 获取数据库连接配置
            db_conn_config = await Api_databasesService.api_databases_detail_services(
                query_db=self.executor_ctx.mysql_obj,
                id=int(db_conn_config_id)
            )

            if not db_conn_config:
                return ExecutorResult(
                    success=False,
                    error=f"未找到数据库连接配置，ID: {db_conn_config_id}"
                )

            # 变量替换
            query_obj = Cache_dataQueryModel(
                user_id=self.executor_ctx.user_id,
                environment_id=self.executor_ctx.env_id
            )
            replace_script = await advanced_template_parser(
                script,
                self.executor_ctx.redis_obj,
                query_obj,
                variables_dict=self.executor_ctx.parameterization
            )

            exec_log["replaced_script"] = replace_script
            logger.info(f"SQL脚本变量替换完成: {replace_script}")

            # 执行数据库操作
            sql_res = None
            if db_conn_config.db_type == "1":  # MySQL
                mysql_conn = MysqlDB(db_conn_config)
                sql_type = self._get_sql_execution_type(replace_script)
                exec_log["sql_type"] = sql_type

                logger.info(f"执行 SQL，类型: {sql_type}")
                sql_res = getattr(mysql_conn, sql_type)(replace_script)
                exec_log["sql_result"] = sql_res
            else:
                return ExecutorResult(
                    success=False,
                    error=f"暂不支持该数据库类型: {db_conn_config.db_type}"
                )

            # 提取变量（如果配置了的话）
            # 注意：这里需要从节点配置中获取变量提取配置
            extract_config = getattr(self.config, 'extract_variables', None) or \
                            getattr(task_config, 'extract_variables', None)

            if sql_res and extract_config:
                for variables in extract_config:
                    jsonpath_expr = variables.get('jsonpath')
                    variable_name = variables.get('variable_name')

                    if jsonpath_expr and variable_name:
                        value = jsonpath(sql_res, jsonpath_expr)
                        cache_value = str(value[0]) if value and len(value) > 0 else ""

                        # 存入缓存
                        from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel
                        query = Cache_dataPageQueryModel(
                            cache_key=variable_name,
                            environment_id=self.executor_ctx.env_id,
                            user_id=self.executor_ctx.user_id,
                            cache_value=cache_value
                        )
                        await Cache_dataService.add_cache_data_services(
                            self.executor_ctx.redis_obj,
                            query
                        )
                        exec_log["extract_variables"].append({variable_name: cache_value})

                        # 同时更新上下文变量
                        self.executor_ctx.variables[variable_name] = cache_value

            execution_time = time.time() - start_time

            logger.info(f"数据库操作执行完成，耗时: {execution_time:.3f}s")

            return ExecutorResult(
                success=True,
                message="数据库操作执行成功",
                data=sql_res,
                log=exec_log,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"数据库操作执行异常: {str(e)}")
            return ExecutorResult(
                success=False,
                error=f"数据库操作失败: {str(e)}",
                log=exec_log,
                execution_time=execution_time
            )

    @classmethod
    def _get_sql_execution_type(cls, sql: str) -> str:
        """
        识别SQL语句类型，返回应该使用的执行函数类型

        Args:
            sql: SQL语句

        Returns:
            'query'(查询), 'execute'(增删改), 'unknown'(未识别)
        """
        if not sql or not sql.strip():
            return 'unknown'

        # 去除首尾空白并转换为大写
        sql_upper = sql.strip().upper()

        # 增删改语句 - 使用 execute 函数
        if re.match(r'^\s*(INSERT\s+INTO|UPDATE\s+|DELETE\s+FROM)', sql_upper):
            return 'execute'

        # 其他默认使用 query 函数（包括 SELECT、WITH 等）
        return 'query'

    def validate(self, task_config: Task_config) -> bool:
        """
        验证数据库操作配置

        Args:
            task_config: 任务配置

        Returns:
            验证是否通过
        """
        if not task_config.db_operation_script:
            logger.warning("数据库脚本为空")
            return False

        if not task_config.db_operation_id:
            logger.warning("数据库连接ID为空")
            return False

        return True
