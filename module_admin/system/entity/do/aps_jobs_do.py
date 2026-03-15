#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：ruoyi-fastapi-backend 
@File    ：aps_jobs.py
@Author  ：david
@Date    ：2025-07-02 17:46 
'''
from sqlalchemy import Column, String, Float, LargeBinary, Index

from config.base import Base
from sqlalchemy.dialects.postgresql import JSONB


class ApschedulerJobs(Base):
    """
    APScheduler 任务存储表
    对应 MySQL 表结构:
    CREATE TABLE `apscheduler_jobs` (
      `id` varchar(191) NOT NULL,
      `next_run_time` double DEFAULT NULL,
      `job_state` blob NOT NULL,
      PRIMARY KEY (`id`),
      KEY `ix_apscheduler_jobs_next_run_time` (`next_run_time`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
    """
    __tablename__ = 'apscheduler_jobs'
    __table_args__ = (
        # 创建 next_run_time 的索引
        Index('ix_apscheduler_jobs_next_run_time', 'next_run_time'),
        # 表级参数
        {'mysql_engine': 'InnoDB',
         'mysql_charset': 'utf8mb4',
         'mysql_collate': 'utf8mb4_0900_ai_ci'}
    )

    id = Column(String(191), primary_key=True, nullable=False, comment='任务ID')
    next_run_time = Column(Float, nullable=True, comment='下次运行时间')
    job_state = Column(LargeBinary, nullable=False, comment='任务状态数据')
