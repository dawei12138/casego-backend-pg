#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project : fast_api_admin
@File : custom_faker.py
@Description : 用户自定义 faker 函数文件
               前端可直接编辑此文件内容，保存后自动热重载生效

使用说明:
    1. 在此文件中定义函数，函数名即为调用名
    2. 支持带参数的函数
    3. 函数必须返回字符串或可转为字符串的值

调用示例:
    {{faker_email()}}           -> 调用 faker_email 函数
    {{random_score(60, 100)}}   -> 调用 random_score 函数，传入参数 60 和 100
    {{custom_name()}}           -> 调用 custom_name 函数
"""
import random
import string
from datetime import datetime, date, timedelta
from faker import Faker

# 初始化 Faker 实例，使用中文语言环境
faker = Faker('zh_CN')


# ======================== 示例函数 ========================

def test_num():
    return 111123123


def faker_email():
    """生成随机邮箱"""
    return faker.email()


def faker_phone():
    """生成随机手机号"""
    return faker.phone_number()


def faker_name():
    """生成随机中文姓名"""
    return faker.name()


def faker_address():
    """生成随机地址"""
    return faker.address()


def faker_company():
    """生成随机公司名"""
    return faker.company()


def faker_id_card():
    """生成随机身份证号"""
    return faker.ssn()


def random_score(min_val: int = 0, max_val: int = 100) -> int:
    """生成随机分数"""
    return random.randint(int(min_val), int(max_val))


def random_string(length: int = 8) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=int(length)))


def current_timestamp() -> int:
    """获取当前时间戳"""
    return int(datetime.now().timestamp())


def current_date() -> str:
    """获取当前日期 YYYY-MM-DD"""
    return date.today().strftime('%Y-%m-%d')


def current_datetime() -> str:
    """获取当前时间 YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def 获取当前时间() -> str:
    """获取当前时间 YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# ======================== 在下方添加自定义函数 ========================

