#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：factory.py
@Author  ：david
@Date    ：2025-08-11 23:39 
"""

from utils.api_tools.executors.db_executor import DbConnectionExecutor
from utils.api_tools.executors.extract_variable_executor import ExtractVariableExecutor
from utils.api_tools.executors.js_exector import JsScriptExecutor
from utils.api_tools.executors.models import ExecutorType
from utils.api_tools.executors.py_exector import PythonScriptExecutor
from utils.api_tools.executors.strategies import ExecutorStrategy, WaitTimeExecutor


class ExecutorFactory:
    """执行器工厂，根据不同的操作类型创建对应的执行器实例"""

    _executors = {
        ExecutorType.PYTHON_SCRIPT: PythonScriptExecutor,
        ExecutorType.DB_CONNECTION: DbConnectionExecutor,
        ExecutorType.JS_SCRIPT: JsScriptExecutor,
        ExecutorType.EXTRACT_VARIABLE: ExtractVariableExecutor,
        ExecutorType.WAIT_TIME: WaitTimeExecutor,
    }

    @classmethod
    def create_executor(cls, executor_type: ExecutorType) -> ExecutorStrategy:
        """创建执行器实例"""
        executor_class = cls._executors.get(executor_type)
        if not executor_class:
            raise ValueError(f"不支持的执行器类型: {executor_type}")
        return executor_class()

    @classmethod
    def register_executor(cls, executor_type: ExecutorType, executor_class: type):
        """注册新的执行器类型"""
        if not issubclass(executor_class, ExecutorStrategy):
            raise TypeError("执行器类必须继承自ExecutorStrategy")
        cls._executors[executor_type] = executor_class

    @classmethod
    def get_supported_types(cls) -> list:
        """获取支持的执行器类型列表"""
        return list(cls._executors.keys())

    @classmethod
    def is_supported(cls, executor_type: ExecutorType) -> bool:
        """检查是否支持指定的执行器类型"""
        return executor_type in cls._executors
