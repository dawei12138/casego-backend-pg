# # utils/api_tools/executors/__init__.py
# """
# API测试执行器模块
#
# 这个模块提供了一个灵活的执行器框架，用于处理接口测试中的前置脚本、后置脚本等各种执行任务。
#
# 主要组件:
# - ExecutorContext: 执行上下文，包含公共参数
# - SetupConfig/TeardownConfig: 前置/后置脚本配置模型
# - ExecutorStrategy: 执行器策略基类
# - ExecutorFactory: 执行器工厂，用于创建执行器实例
# - ExecutorManager: 执行器管理器，统一调度执行
# """
# from .db_executor import DbConnectionExecutor
# from .extract_variable_executor import ExtractVariableExecutor
# from .js_exector import JsScriptExecutor
# from .models import (
#     ExecutorType,
#     ExecutorContext,
#     SetupConfig,
#     TeardownConfig,
#     ExecutorResult,
# )
# from .py_exector import PythonScriptExecutor
# from .strategies import (
#     # ExecutorStrategy,
#
#     # ExtractVariableExecutor,
#     WaitTimeExecutor,
# )
#
# # ExtractVariableExecutor
#
# from .factory import ExecutorFactory
# from .manager import ExecutorManager
#
# # 版本信息
# __version__ = "1.0.0"
# __author__ = "API Test Team"
#
# # 导出的公共接口
# __all__ = [
#     # 模型类
#     "ExecutorType",
#     "ExecutorContext",
#     "SetupConfig",
#     "TeardownConfig",
#     "ExecutorResult",
#
#     # 策略类
#     # "ExecutorStrategy",
#     "PythonScriptExecutor",
#     "DbConnectionExecutor",
#     "JsScriptExecutor",
#     "ExtractVariableExecutor",
#     "WaitTimeExecutor",
#
#     # 工厂和管理器
#     "ExecutorFactory",
#     "ExecutorManager",
# ]