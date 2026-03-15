#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin 
@File    ：executor_models.py
@Author  ：david
@Date    ：2025-08-28 17:45
@Description: Test executor database models based on JSON configuration
"""
from sqlalchemy import Column, Integer, String, Enum, Text, JSON, Index, DateTime, Boolean, BigInteger
import enum
from datetime import datetime
from typing import Dict, Any, List, Optional, Union

from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


# ========== 枚举类型 ==========


class ExecutorStatusEnum(str, enum.Enum):
    """执行器状态枚举"""
    DRAFT = "draft"  # 草稿
    ACTIVE = "active"  # 激活
    INACTIVE = "inactive"  # 停用
    ARCHIVED = "archived"  # 归档


class ExecutionModeEnum(str, enum.Enum):
    """执行模式枚举"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"  # 并行执行


# ========== 表定义 ==========

# class Executor(Base):
#     """测试执行器主表"""
#     __tablename__ = "api_workflow"
#     __table_args__ = (
#         Index('ix_workflow_name', 'name'),
#         {
#             'comment': '测试执行器主表'
#         }
#     )
#
#     workflow_id = Column(String(50), primary_key=True, comment="执行器ID")
#     name = Column(String(200), comment="执行器名称")
#     # status = Column(Enum(ExecutorStatusEnum), nullable=False, default=ExecutorStatusEnum.DRAFT, comment="执行器状态")
#     # 执行配置
#     execution_config = Column(JSONB, comment="执行配置")
#     # 关联字段
#     parent_submodule_id = Column(BigInteger, nullable=True, comment='父级模块ID')



class ExecutorSchema(Base):
    """执行器schema配置表"""
    __tablename__ = "api_workflow_schemas"
    __table_args__ = (
        {
            'comment': '执行器schema配置表'
        }
    )

    schemas_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
    schema_version = Column(String(20), nullable=False, comment="Schema版本")
    # Schema配置信息
    node_types = Column(JSONB, nullable=False, comment="节点类型定义")
    condition_operators = Column(JSONB, nullable=False, comment="条件操作符列表")
    error_handling_options = Column(JSONB, nullable=False, comment="错误处理选项")
    # 扩展配置
    custom_config = Column(JSONB, comment="自定义配置")


# class ExecutorExecution(Base):
#     """执行器执行记录表"""
#     __tablename__ = "api_workflow_executions"
#     __table_args__ = {
#         'comment': '执行器执行记录表'
#     }
#
#     workflow_execution_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='id')
#     workflow_id = Column(String(50), nullable=False, comment="执行器ID")
#     workflow_name = Column(String(200), comment="执行名称")
#
#     # 执行状态
#     status = Column(String(20), nullable=False, default="pending", comment="执行状态")
#
#     # 执行时间
#     start_time = Column(DateTime, comment="开始时间")
#     end_time = Column(DateTime, comment="结束时间")
#     duration = Column(Integer, comment="执行时长(秒)")
#
#     # 执行数据
#     input_data = Column(JSONB, comment="输入数据")
#     output_data = Column(JSONB, comment="输出数据")
#     context_data = Column(JSONB, comment="上下文数据")
#
#     # 执行结果统计
#     total_nodes = Column(Integer, default=0, comment="总节点数")
#     success_nodes = Column(Integer, default=0, comment="成功节点数")
#     failed_nodes = Column(Integer, default=0, comment="失败节点数")
#     skipped_nodes = Column(Integer, default=0, comment="跳过节点数")
#
#     # 错误信息
#     error_message = Column(Text, comment="错误信息")
#     error_details = Column(JSONB, comment="错误详情")
