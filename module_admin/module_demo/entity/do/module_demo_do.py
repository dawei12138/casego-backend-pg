from module_admin.module_demo.entity.enums.module_demo_enum import DemoStatusEnum
from sqlalchemy import BigInteger, Boolean, CHAR, Column, Date, DateTime, Float, Integer, Interval, JSON, LargeBinary, Numeric, SmallInteger, String, Text, Time, Uuid
from sqlalchemy.dialects.postgresql import ARRAY, BIT, CIDR, DATEMULTIRANGE, DATERANGE, ENUM, INET, INT4MULTIRANGE, INT4RANGE, INT8MULTIRANGE, INT8RANGE, JSONB, JSONPATH, MACADDR, MACADDR8, MONEY, NUMMULTIRANGE, NUMRANGE, OID, REGCLASS, REGCONFIG, TSMULTIRANGE, TSQUERY, TSRANGE, TSTZMULTIRANGE, TSTZRANGE, TSVECTOR
from config.base import Base


class ModuleDemoAllTypes(Base):
    """
    Demo全类型测试表
    """

    __tablename__ = 'module_demo_all_types'
    __table_args__ = {'comment': 'Demo全类型测试表'}

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False, comment='主键ID-bigint')
    string_value = Column(String(100), nullable=False, comment='字符串-varchar')
    fixed_char_value = Column(CHAR(1), nullable=True, comment='定长字符-char')
    unicode_value = Column(String(100), nullable=True, comment='Unicode字符串-unicode')
    text_value = Column(Text, nullable=True, comment='长文本-text')
    unicode_text_value = Column(Text, nullable=True, comment='Unicode长文本-unicode text')
    small_integer_value = Column(SmallInteger, nullable=True, comment='短整数-smallint')
    integer_value = Column(Integer, nullable=True, comment='整数-integer')
    big_integer_value = Column(BigInteger, nullable=True, comment='长整数-bigint')
    numeric_value = Column(Numeric(18,6), nullable=True, comment='高精度小数-numeric')
    decimal_value = Column(Numeric(18,6), nullable=True, comment='高精度小数-decimal')
    money_value = Column(MONEY, nullable=True, comment='金额-money')
    float_value = Column(Float, nullable=True, comment='浮点数-float')
    real_value = Column(Float, nullable=True, comment='单精度浮点-real')
    double_value = Column(Float, nullable=True, comment='双精度浮点-double precision')
    boolean_value = Column(Boolean, nullable=True, comment='布尔-boolean')
    date_value = Column(Date, nullable=True, comment='日期-date')
    time_value = Column(Time, nullable=True, comment='时间-time without time zone')
    time_tz_value = Column(Time(timezone=True), nullable=True, comment='带时区时间-time with time zone')
    datetime_value = Column(DateTime, nullable=True, comment='日期时间-timestamp without time zone')
    datetime_tz_value = Column(DateTime(timezone=True), nullable=True, comment='带时区日期时间-timestamp with time zone')
    interval_value = Column(Interval, nullable=True, comment='时间间隔-interval')
    json_value = Column(JSON, nullable=True, comment='JSON-json')
    jsonb_object_value = Column(JSONB, nullable=True, comment='JSON对象-jsonb/object')
    jsonb_array_value = Column(JSONB, nullable=True, comment='JSON数组-jsonb/array')
    jsonpath_value = Column(JSONPATH, nullable=True, comment='JSON路径-jsonpath')
    binary_value = Column(LargeBinary, nullable=True, comment='二进制-bytea')
    enum_value = Column(ENUM(DemoStatusEnum, name='demo_status_enum', create_type=False), nullable=True, comment='枚举-enum')
    uuid_value = Column(Uuid, nullable=True, comment='UUID-uuid')
    string_array_value = Column(ARRAY(String), nullable=True, comment='字符串数组-array/varchar')
    integer_array_value = Column(ARRAY(Integer), nullable=True, comment='整数数组-array/integer')
    jsonb_array_items_value = Column(ARRAY(JSONB), nullable=True, comment='JSONB数组-array/jsonb')
    inet_value = Column(INET, nullable=True, comment='IP地址-inet')
    cidr_value = Column(CIDR, nullable=True, comment='网络地址-cidr')
    macaddr_value = Column(MACADDR, nullable=True, comment='MAC地址-macaddr')
    macaddr8_value = Column(MACADDR8, nullable=True, comment='EUI-64 MAC地址-macaddr8')
    bit_value = Column(BIT, nullable=True, comment='固定长度位-bit')
    bit_varying_value = Column(BIT(varying=True), nullable=True, comment='可变长度位-bit varying')
    tsvector_value = Column(TSVECTOR, nullable=True, comment='全文检索向量-tsvector')
    tsquery_value = Column(TSQUERY, nullable=True, comment='全文检索查询-tsquery')
    int4_range_value = Column(INT4RANGE, nullable=True, comment='整数范围-int4range')
    int8_range_value = Column(INT8RANGE, nullable=True, comment='长整数范围-int8range')
    numeric_range_value = Column(NUMRANGE, nullable=True, comment='小数范围-numrange')
    date_range_value = Column(DATERANGE, nullable=True, comment='日期范围-daterange')
    timestamp_range_value = Column(TSRANGE, nullable=True, comment='时间戳范围-tsrange')
    timestamp_tz_range_value = Column(TSTZRANGE, nullable=True, comment='带时区时间戳范围-tstzrange')
    int4_multirange_value = Column(INT4MULTIRANGE, nullable=True, comment='整数多范围-int4multirange')
    int8_multirange_value = Column(INT8MULTIRANGE, nullable=True, comment='长整数多范围-int8multirange')
    numeric_multirange_value = Column(NUMMULTIRANGE, nullable=True, comment='小数多范围-nummultirange')
    date_multirange_value = Column(DATEMULTIRANGE, nullable=True, comment='日期多范围-datemultirange')
    timestamp_multirange_value = Column(TSMULTIRANGE, nullable=True, comment='时间戳多范围-tsmultirange')
    timestamp_tz_multirange_value = Column(TSTZMULTIRANGE, nullable=True, comment='带时区时间戳多范围-tstzmultirange')
    oid_value = Column(OID, nullable=True, comment='对象ID-oid')
    regclass_value = Column(REGCLASS, nullable=True, comment='关系对象-regclass')
    regconfig_value = Column(REGCONFIG, nullable=True, comment='文本搜索配置-regconfig')
    create_by = Column(String(64), nullable=True, comment='')
    create_time = Column(DateTime, nullable=True, comment='创建时间')
    update_by = Column(String(64), nullable=True, comment='')
    update_time = Column(DateTime, nullable=True, comment='更新时间')
    remark = Column(String(500), nullable=True, comment='')
    description = Column(Text, nullable=True, comment='')
    sort_no = Column(Float, nullable=True, comment='')
    del_flag = Column(String(1), nullable=True, default='0', comment='')




