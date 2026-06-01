from datetime import date, datetime, time, timedelta
from decimal import Decimal
from module_admin.module_demo.entity.enums.module_demo_enum import DemoStatusEnum
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank
from typing import Any, Optional
from module_admin.annotation.pydantic_annotation import as_query


def is_empty_generated_value(value):
    return value == '' or (isinstance(value, (list, dict)) and len(value) == 0)


def normalize_empty_generated_values(values, field_alias_map):
    if not isinstance(values, dict):
        return values
    data = values.copy()
    for field_name, alias_name in field_alias_map.items():
        for key in {field_name, alias_name}:
            if key in data and is_empty_generated_value(data.get(key)):
                data[key] = None
    return data




class Module_demoModel(BaseModel):
    """
    Demo全类型测试表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True, populate_by_name=True)

    id: Optional[int] = Field(default=None, description='主键ID-bigint')
    string_value: Optional[str] = Field(default=None, description='字符串-varchar')
    fixed_char_value: Optional[str] = Field(default=None, description='定长字符-char')
    unicode_value: Optional[str] = Field(default=None, description='Unicode字符串-unicode')
    text_value: Optional[str] = Field(default=None, description='长文本-text')
    unicode_text_value: Optional[str] = Field(default=None, description='Unicode长文本-unicode text')
    small_integer_value: Optional[int] = Field(default=None, description='短整数-smallint')
    integer_value: Optional[int] = Field(default=None, description='整数-integer')
    big_integer_value: Optional[int] = Field(default=None, description='长整数-bigint')
    numeric_value: Optional[Decimal] = Field(default=None, description='高精度小数-numeric')
    decimal_value: Optional[Decimal] = Field(default=None, description='高精度小数-decimal')
    money_value: Optional[Decimal] = Field(default=None, description='金额-money')
    float_value: Optional[float] = Field(default=None, description='浮点数-float')
    real_value: Optional[float] = Field(default=None, description='单精度浮点-real')
    double_value: Optional[float] = Field(default=None, description='双精度浮点-double precision')
    boolean_value: Optional[bool] = Field(default=None, description='布尔-boolean')
    date_value: Optional[date] = Field(default=None, description='日期-date')
    time_value: Optional[time] = Field(default=None, description='时间-time without time zone')
    time_tz_value: Optional[time] = Field(default=None, description='带时区时间-time with time zone')
    datetime_value: Optional[datetime] = Field(default=None, description='日期时间-timestamp without time zone')
    datetime_tz_value: Optional[datetime] = Field(default=None, description='带时区日期时间-timestamp with time zone')
    interval_value: Optional[timedelta] = Field(default=None, description='时间间隔-interval')
    json_value: Optional[Any] = Field(default=None, description='JSON-json')
    jsonb_object_value: Optional[Any] = Field(default=None, description='JSON对象-jsonb/object')
    jsonb_array_value: Optional[Any] = Field(default=None, description='JSON数组-jsonb/array')
    jsonpath_value: Optional[str] = Field(default=None, description='JSON路径-jsonpath')
    binary_value: Optional[bytes] = Field(default=None, description='二进制-bytea')
    enum_value: Optional[DemoStatusEnum] = Field(default=None, description='枚举-enum')
    uuid_value: Optional[str] = Field(default=None, description='UUID-uuid')
    string_array_value: Optional[list] = Field(default=None, description='字符串数组-array/varchar')
    integer_array_value: Optional[list] = Field(default=None, description='整数数组-array/integer')
    jsonb_array_items_value: Optional[list] = Field(default=None, description='JSONB数组-array/jsonb')
    inet_value: Optional[str] = Field(default=None, description='IP地址-inet')
    cidr_value: Optional[str] = Field(default=None, description='网络地址-cidr')
    macaddr_value: Optional[str] = Field(default=None, description='MAC地址-macaddr')
    macaddr8_value: Optional[str] = Field(default=None, description='EUI-64 MAC地址-macaddr8')
    bit_value: Optional[str] = Field(default=None, description='固定长度位-bit')
    bit_varying_value: Optional[str] = Field(default=None, description='可变长度位-bit varying')
    tsvector_value: Optional[str] = Field(default=None, description='全文检索向量-tsvector')
    tsquery_value: Optional[str] = Field(default=None, description='全文检索查询-tsquery')
    int4_range_value: Optional[list] = Field(default=None, description='整数范围-int4range')
    int8_range_value: Optional[list] = Field(default=None, description='长整数范围-int8range')
    numeric_range_value: Optional[list] = Field(default=None, description='小数范围-numrange')
    date_range_value: Optional[list] = Field(default=None, description='日期范围-daterange')
    timestamp_range_value: Optional[list] = Field(default=None, description='时间戳范围-tsrange')
    timestamp_tz_range_value: Optional[list] = Field(default=None, description='带时区时间戳范围-tstzrange')
    int4_multirange_value: Optional[list] = Field(default=None, description='整数多范围-int4multirange')
    int8_multirange_value: Optional[list] = Field(default=None, description='长整数多范围-int8multirange')
    numeric_multirange_value: Optional[list] = Field(default=None, description='小数多范围-nummultirange')
    date_multirange_value: Optional[list] = Field(default=None, description='日期多范围-datemultirange')
    timestamp_multirange_value: Optional[list] = Field(default=None, description='时间戳多范围-tsmultirange')
    timestamp_tz_multirange_value: Optional[list] = Field(default=None, description='带时区时间戳多范围-tstzmultirange')
    oid_value: Optional[int] = Field(default=None, description='对象ID-oid')
    regclass_value: Optional[str] = Field(default=None, description='关系对象-regclass')
    regconfig_value: Optional[str] = Field(default=None, description='文本搜索配置-regconfig')
    create_by: Optional[str] = Field(default=None, description='')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='')
    description: Optional[str] = Field(default=None, description='')
    sort_no: Optional[float] = Field(default=None, description='')
    del_flag: Optional[str] = Field(default=None, description='')

    @NotBlank(field_name='string_value', message='字符串-varchar不能为空')
    def get_string_value(self):
        return self.string_value


    def validate_fields(self):
        self.get_string_value()

    @model_validator(mode='before')
    @classmethod
    def normalize_empty_values(cls, values):
        return normalize_empty_generated_values(
            values,
            {
                'id': 'id',
                'fixed_char_value': 'fixedCharValue',
                'unicode_value': 'unicodeValue',
                'text_value': 'textValue',
                'unicode_text_value': 'unicodeTextValue',
                'small_integer_value': 'smallIntegerValue',
                'integer_value': 'integerValue',
                'big_integer_value': 'bigIntegerValue',
                'numeric_value': 'numericValue',
                'decimal_value': 'decimalValue',
                'money_value': 'moneyValue',
                'float_value': 'floatValue',
                'real_value': 'realValue',
                'double_value': 'doubleValue',
                'boolean_value': 'booleanValue',
                'date_value': 'dateValue',
                'time_value': 'timeValue',
                'time_tz_value': 'timeTzValue',
                'datetime_value': 'datetimeValue',
                'datetime_tz_value': 'datetimeTzValue',
                'interval_value': 'intervalValue',
                'jsonpath_value': 'jsonpathValue',
                'binary_value': 'binaryValue',
                'enum_value': 'enumValue',
                'uuid_value': 'uuidValue',
                'inet_value': 'inetValue',
                'cidr_value': 'cidrValue',
                'macaddr_value': 'macaddrValue',
                'macaddr8_value': 'macaddr8Value',
                'bit_value': 'bitValue',
                'bit_varying_value': 'bitVaryingValue',
                'tsvector_value': 'tsvectorValue',
                'tsquery_value': 'tsqueryValue',
                'int4_range_value': 'int4RangeValue',
                'int8_range_value': 'int8RangeValue',
                'numeric_range_value': 'numericRangeValue',
                'date_range_value': 'dateRangeValue',
                'timestamp_range_value': 'timestampRangeValue',
                'timestamp_tz_range_value': 'timestampTzRangeValue',
                'int4_multirange_value': 'int4MultirangeValue',
                'int8_multirange_value': 'int8MultirangeValue',
                'numeric_multirange_value': 'numericMultirangeValue',
                'date_multirange_value': 'dateMultirangeValue',
                'timestamp_multirange_value': 'timestampMultirangeValue',
                'timestamp_tz_multirange_value': 'timestampTzMultirangeValue',
                'oid_value': 'oidValue',
                'regclass_value': 'regclassValue',
                'regconfig_value': 'regconfigValue',
                'create_by': 'createBy',
                'create_time': 'createTime',
                'update_by': 'updateBy',
                'update_time': 'updateTime',
                'remark': 'remark',
                'description': 'description',
                'sort_no': 'sortNo',
                'del_flag': 'delFlag',
            },
        )




class Module_demoQueryModel(Module_demoModel):
    """
    Demo全类型测试不分页查询模型
    """
    pass


@as_query
class Module_demoPageQueryModel(Module_demoQueryModel):
    """
    Demo全类型测试分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteModule_demoModel(BaseModel):
    """
    删除Demo全类型测试模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID-bigint')
