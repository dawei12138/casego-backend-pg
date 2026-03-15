#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：models.py
@Author  ：david
@Date    ：2025-09-02 22:53 
"""
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel

from config.enums import Request_method
from utils.api_tools.executors.models import ExecutorContext
from module_admin.api_workflow.workflow.entity.vo.workflow_vo import ExecutionConfigModel, WorkflowTreeModel


class ExtendedAssertionMethod(str, Enum):
    """扩展的断言比较方法"""
    # 基础比较
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="

    # 包含操作
    CONTAINS = "contain"
    NOT_CONTAINS = "not_contain"

    # 空值判断
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    EXIST = "exist"
    NOT_EXIST = "not_exist"

    # 正则匹配
    REGULAR_TYPE = "REGULAR_TYPE"

    # 集合操作
    BELONG_TO_SET = "belong_to_set"
    NOT_BELONG_TO_SET = "not_belong_to_set"


class TriggerType(str, Enum):
    MANUAL = "manual"  # 手动触发
    CRON = "cron"  # 定时任务
    API = "api"  # API 调用触发
    SYSTEM = "system"  # 系统自动触发


class StreamEventType(str, Enum):
    """流事件类型"""
    HEARTBEAT = "heartbeat"
    WORKFLOW_START = "workflow_start"
    WORKFLOW_END = "workflow_end"
    NODE_START = "node_start"
    NODE_END = "node_end"
    NODE_ERROR = "node_error"
    LOOP_START = "loop_start"
    LOOP_ITERATION = "loop_iteration"
    LOOP_END = "loop_end"
    PROGRESS = "progress"
    LOG = "log"
    ERROR = "error"
    CONFIG_INFO = "config_info"
    CASE_RESULT = "case_result"


class StreamEvent(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    """流事件模型"""
    event_type: StreamEventType = Field(default=StreamEventType.LOG, )
    timestamp: datetime = Field(default_factory=datetime.now)
    data: Optional[Dict[str, Any]] = None
    message: Optional[str] = None
    node_id: Optional[int] = None
    log_id: Optional[int] = None
    is_success: Optional[bool] = True
    progress: Optional[float] = None
    workflow_id: Optional[int] = None
    case_id: Optional[int] = None
    response_status_code: Optional[int] = None
    response_time: Optional[float] = None
    # execution_time: Optional[float] = None
    path: Optional[str] = Field(default=None, description='请求路径')
    name: Optional[str] = Field(default=None, description='请求名称')
    method: Optional[Request_method] = Field(default=None, description='请求方法 (GET, POST等)')
    assertion_success: Optional[bool] = Field(default=True, description='断言成功是否')


class Cache_dataQueryModel(BaseModel):
    """缓存数据查询模型"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    user_id: Optional[int] = None
    environment_id: Optional[int] = None


class StreamingExecutionContext(BaseModel):
    """流式执行上下文"""
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    # 接口执行的基础上下文
    executor_context: ExecutorContext

    # 执行配置
    execution_config: Optional[ExecutionConfigModel] = Field(default=None)

    # 流程控制
    loop_stack: List[Dict[str, Any]] = Field(default_factory=list)
    should_stop: bool = Field(default=False)
    should_break: bool = Field(default=False)
    should_continue: bool = Field(default=False)

    # 流式输出相关
    workflow_id: Optional[int] = Field(default=None)
    total_nodes: int = Field(default=0)
    completed_nodes: int = Field(default=0)
    failed_nodes: int = Field(default=0)
    skipped_nodes: int = Field(default=0)
    start_time: datetime = Field(default_factory=datetime.now)
    last_heartbeat: datetime = Field(default_factory=datetime.now)

    def set_variable(self, key: str, value: Any):
        """设置变量到执行器上下文"""
        self.executor_context.variables[key] = value

    def get_variable(self, key: str, default: Any = None) -> Any:
        """从执行器上下文获取变量"""
        return self.executor_context.variables.get(key, default)

    def set_parameterization(self, key: str, value: Any):
        """设置参数化变量"""
        self.executor_context.parameterization[key] = value

    def get_parameterization(self, key: str, default: Any = None) -> Any:
        """获取参数化变量"""
        return self.executor_context.parameterization.get(key, default)

    def get_progress(self) -> float:
        """获取执行进度百分比"""
        if self.total_nodes == 0:
            return 0.0
        return (self.completed_nodes / self.total_nodes) * 100

    def increment_completed(self):
        """增加已完成节点数"""
        self.completed_nodes += 1

    def increment_failed(self):
        """增加失败节点数"""
        self.failed_nodes += 1

    def increment_skipped(self):
        """增加跳过节点数"""
        self.skipped_nodes += 1

    def should_send_heartbeat(self, interval: int = 30) -> bool:
        """判断是否应该发送心跳（默认30秒间隔）"""
        return (datetime.now() - self.last_heartbeat).seconds >= interval

    def update_heartbeat(self):
        """更新心跳时间"""
        self.last_heartbeat = datetime.now()

    def get_runtime_stats(self) -> Dict[str, Any]:
        """获取运行时统计信息（返回 camelCase 键）"""
        runtime = (datetime.now() - self.start_time).total_seconds()
        return {
            "totalNodes": self.total_nodes,
            "completedNodes": self.completed_nodes,
            "failedNodes": self.failed_nodes,
            "skippedNodes": self.skipped_nodes,
            "progressPercentage": self.get_progress(),
            "runtimeSeconds": runtime,
            "nodesPerSecond": self.completed_nodes / runtime if runtime > 0 else 0
        }
