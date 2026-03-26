#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：ruoyi-fastapi-backend
@File    ：base.py
@Author  ：david
@Date    ：2025-07-02 14:04
"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import DateTime, Integer, Column, String, Float, func, text, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIMESTAMP


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    create_by = Column(String(64), nullable=True, default='')

    create_time = Column(
        TIMESTAMP(precision=0),
        nullable=True,
        server_default=func.now(),
        comment="创建时间"
    )
    update_by = Column(String(64), nullable=True, default='')

    update_time = Column(
        TIMESTAMP(precision=0),
        nullable=True,
        server_default=func.now(),
        comment="更新时间"
    )

    remark = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    sort_no = Column(Float, nullable=True, default=1)
    del_flag = Column(String(1), nullable=True, default="0")
