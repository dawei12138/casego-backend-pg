#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fast_api_admin
@File ：regular_faker_data.py
@Author ：david
@Date ：2025-08-08 9:25
"""
import datetime
import random
from datetime import date, timedelta, datetime
from typing import Union
from fastapi import Request
from jsonpath import jsonpath
from faker import Faker
from config.get_db import get_db


class Context:
    """ 正则替换 """

    def __init__(self):
        self.faker = Faker(locale='zh_CN')

    # ======================== 数字相关 ========================
    @classmethod
    def random_int(cls, min_val: int = 0, max_val: int = 5000) -> int:
        """ 生成指定范围的随机整数 """
        return random.randint(min_val, max_val)

    @classmethod
    def random_float(cls, min_val: float = 0.0, max_val: float = 1000.0, digits: int = 2) -> float:
        """ 生成指定范围的随机浮点数 """
        return round(random.uniform(min_val, max_val), digits)

    def random_price(self) -> str:
        """ 生成随机价格 """
        return f"{self.faker.pydecimal(left_digits=4, right_digits=2, positive=True)}"

    def random_discount(self) -> str:
        """ 生成随机折扣(0.1-0.9) """
        return f"{round(random.uniform(0.1, 0.9), 1)}"

    # ======================== 个人信息相关 ========================
    def get_phone(self) -> str:
        """ 随机生成手机号码 """
        phone = self.faker.phone_number()
        return phone

    def get_id_number(self) -> str:
        """ 随机生成身份证号码 """
        id_number = self.faker.ssn()
        return id_number

    def get_female_name(self) -> str:
        """ 女生姓名 """
        female_name = self.faker.name_female()
        return female_name

    def get_male_name(self) -> str:
        """ 男生姓名 """
        male_name = self.faker.name_male()
        return male_name

    def get_name(self) -> str:
        """ 随机姓名 """
        return self.faker.name()

    def get_first_name(self) -> str:
        """ 名字 """
        return self.faker.first_name()

    def get_last_name(self) -> str:
        """ 姓氏 """
        return self.faker.last_name()

    def get_age(self) -> int:
        """ 随机年龄(18-80) """
        return random.randint(18, 80)

    def get_birthday(self) -> str:
        """ 随机生日 """
        return self.faker.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')

    # ======================== 联系方式相关 ========================
    def get_email(self) -> str:
        """ 生成邮箱 """
        email = self.faker.email()
        return email

    def get_safe_email(self) -> str:
        """ 生成安全邮箱(example.com域名) """
        return self.faker.safe_email()

    def get_company_email(self) -> str:
        """ 生成公司邮箱 """
        return self.faker.company_email()

    def get_free_email(self) -> str:
        """ 生成免费邮箱 """
        return self.faker.free_email()

    # ======================== 地址相关 ========================
    def get_province(self) -> str:
        """ 省份 """
        return self.faker.province()

    def get_city(self) -> str:
        """ 城市 """
        return self.faker.city()

    def get_district(self) -> str:
        """ 区县 """
        return self.faker.district()

    def get_address(self) -> str:
        """ 完整地址 """
        return self.faker.address()

    def get_street_address(self) -> str:
        """ 街道地址 """
        return self.faker.street_address()

    def get_postcode(self) -> str:
        """ 邮政编码 """
        return self.faker.postcode()

    def get_country(self) -> str:
        """ 国家 """
        return self.faker.country()

    # ======================== 公司相关 ========================
    def get_company(self) -> str:
        """ 公司名称 """
        return self.faker.company()

    def get_company_suffix(self) -> str:
        """ 公司后缀(有限公司等) """
        return self.faker.company_suffix()

    def get_job(self) -> str:
        """ 职位 """
        return self.faker.job()

    def get_department(self) -> str:
        """ 部门(自定义) """
        departments = ['技术部', '市场部', '销售部', '人事部', '财务部', '运营部', '产品部', '设计部', '客服部', '行政部']
        return random.choice(departments)

    # ======================== 网络相关 ========================
    def get_username(self) -> str:
        """ 用户名 """
        return self.faker.user_name()

    def get_password(self) -> str:
        """ 密码 """
        return self.faker.password()

    def get_url(self) -> str:
        """ 网址 """
        return self.faker.url()

    def get_domain_name(self) -> str:
        """ 域名 """
        return self.faker.domain_name()

    def get_ipv4(self) -> str:
        """ IPv4地址 """
        return self.faker.ipv4()

    def get_ipv6(self) -> str:
        """ IPv6地址 """
        return self.faker.ipv6()

    def get_mac_address(self) -> str:
        """ MAC地址 """
        return self.faker.mac_address()

    def get_user_agent(self) -> str:
        """ 用户代理 """
        return self.faker.user_agent()

    # ======================== 银行相关 ========================
    def get_credit_card_number(self) -> str:
        """ 信用卡号 """
        return self.faker.credit_card_number()

    def get_credit_card_provider(self) -> str:
        """ 信用卡提供商 """
        return self.faker.credit_card_provider()

    def get_credit_card_security_code(self) -> str:
        """ 信用卡安全码 """
        return self.faker.credit_card_security_code()

    def get_bank_card_number(self) -> str:
        """ 银行卡号(中国) """
        # 生成19位银行卡号
        return ''.join([str(random.randint(0, 9)) for _ in range(19)])

    # ======================== 文本相关 ========================
    def get_word(self) -> str:
        """ 随机单词 """
        return self.faker.word()

    def get_words(self, nb: int = 3) -> str:
        """ 随机多个单词 """
        return ' '.join(self.faker.words(nb=nb))

    def get_sentence(self) -> str:
        """ 随机句子 """
        return self.faker.sentence()

    def get_text(self, max_nb_chars: int = 200) -> str:
        """ 随机文本 """
        return self.faker.text(max_nb_chars=max_nb_chars)

    def get_paragraph(self) -> str:
        """ 随机段落 """
        return self.faker.paragraph()

    # ======================== 颜色相关 ========================
    def get_color_name(self) -> str:
        """ 颜色名称 """
        return self.faker.color_name()

    def get_hex_color(self) -> str:
        """ 十六进制颜色 """
        return self.faker.hex_color()

    def get_rgb_color(self) -> str:
        """ RGB颜色 """
        return self.faker.rgb_color()

    # ======================== 文件相关 ========================
    def get_file_name(self) -> str:
        """ 文件名 """
        return self.faker.file_name()

    def get_file_extension(self) -> str:
        """ 文件扩展名 """
        return self.faker.file_extension()

    def get_image_url(self) -> str:
        """ 图片URL """
        return self.faker.image_url()

    # ======================== UUID相关 ========================
    def get_uuid4(self) -> str:
        """ UUID4 """
        return self.faker.uuid4()

    def get_uuid1(self) -> str:
        """ UUID1 """
        return str(self.faker.uuid4())  # faker没有uuid1，用uuid4代替

    # ======================== 车辆相关 ========================
    def get_license_plate(self) -> str:
        """ 车牌号 """
        return self.faker.license_plate()

    # ======================== 时间相关 ========================
    @classmethod
    def self_operated_id(cls):
        """ 自营店铺 ID """
        operated_id = 212
        return operated_id

    @classmethod
    def get_time(cls) -> str:
        """ 计算当前时间 """
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return now_time

    @classmethod
    def today_date(cls):
        """ 获取今日0点整时间 """
        today = date.today().strftime("%Y-%m-%d") + " 00:00:00"
        return str(today)

    @classmethod
    def time_after_week(cls):
        """ 获取一周后12点整的时间 """
        time_after_week = (date.today() + timedelta(days=+6)).strftime("%Y-%m-%d") + " 00:00:00"
        return time_after_week

    def get_future_date(self, days: int = 30) -> str:
        """ 获取未来日期 """
        future_date = self.faker.future_date(end_date=f'+{days}d')
        return future_date.strftime('%Y-%m-%d')

    def get_past_date(self, days: int = 30) -> str:
        """ 获取过去日期 """
        past_date = self.faker.past_date(start_date=f'-{days}d')
        return past_date.strftime('%Y-%m-%d')

    def get_random_date(self) -> str:
        """ 获取随机日期(过去5年到未来1年) """
        return self.faker.date_between(start_date='-5y', end_date='+1y').strftime('%Y-%m-%d')

    def get_timestamp(self) -> int:
        """ 获取时间戳 """
        return int(self.faker.date_time().timestamp())

    # ======================== 状态相关 ========================
    def get_boolean(self) -> bool:
        """ 随机布尔值 """
        return self.faker.boolean()

    def get_status(self) -> str:
        """ 随机状态 """
        statuses = ['启用', '禁用', '待审核', '已审核', '已删除', '正常']
        return random.choice(statuses)

    def get_order_status(self) -> str:
        """ 订单状态 """
        statuses = ['待支付', '已支付', '已发货', '已收货', '已完成', '已取消', '退款中', '已退款']
        return random.choice(statuses)

    # ======================== 业务相关 ========================
    def get_product_name(self) -> str:
        """ 商品名称 """
        products = ['苹果', '香蕉', '橘子', '葡萄', '西瓜', '草莓', '蓝莓', '樱桃', '桃子', '梨子',
                   '手机', '电脑', '平板', '耳机', '音响', '键盘', '鼠标', '显示器', '摄像头', '充电器']
        return random.choice(products)

    def get_category(self) -> str:
        """ 商品分类 """
        categories = ['数码电子', '服装鞋帽', '家居用品', '美妆护肤', '食品饮料', '图书音像', '运动户外', '母婴用品']
        return random.choice(categories)

    def get_brand(self) -> str:
        """ 品牌名称 """
        brands = ['苹果', '华为', '小米', '三星', 'vivo', 'oppo', '联想', '戴尔', '惠普', '索尼']
        return random.choice(brands)

    def 随机职位(self):
        """ 生成随机职位"""
        return self.faker.job()

    @classmethod
    def get_test_data(cls, name):
        """ 获取测试数据 """
        return f"{name}牛牪犇逼"

    # ======================== 测试专用方法 ========================
    def get_test_account(self) -> dict:
        """ 生成测试账号信息 """
        return {
            'username': self.get_username(),
            'password': self.get_password(),
            'email': self.get_email(),
            'phone': self.get_phone(),
            'name': self.get_name()
        }

    def 随机测试用户(self) -> dict:
        """ 生成测试用户完整信息 """
        return {
            'name': self.get_name(),
            'age': self.get_age(),
            'phone': self.get_phone(),
            'email': self.get_email(),
            'address': self.get_address(),
            'company': self.get_company(),
            'job': self.get_job(),
            'id_number': self.get_id_number(),
            'birthday': self.get_birthday()
        }

    def 随机测试订单(self) -> dict:
        """ 生成测试订单信息 """
        return {
            'order_id': self.get_uuid4(),
            'product_name': self.get_product_name(),
            'price': self.random_price(),
            'quantity': self.random_int(1, 10),
            'status': self.get_order_status(),
            'create_time': self.get_time(),
            'user_name': self.get_name(),
            'user_phone': self.get_phone()
        }