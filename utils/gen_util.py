import re
from datetime import datetime
from typing import List
from config.constant import GenConstant
from config.env import GenConfig
from module_generator.entity.vo.gen_vo import GenTableColumnModel, GenTableModel
from utils.string_util import StringUtil


class GenUtils:
    """代码生成器工具类"""

    @classmethod
    def init_table(cls, gen_table: GenTableModel, oper_name: str) -> None:
        """
        初始化表信息

        param gen_table: 业务表对象
        param oper_name: 操作人
        :return:
        """
        gen_table.class_name = cls.convert_class_name(gen_table.table_name)
        gen_table.package_name = GenConfig.package_name
        gen_table.module_name = cls.get_module_name(GenConfig.package_name)
        gen_table.business_name = cls.get_business_name(gen_table.table_name)
        gen_table.function_name = cls.replace_text(gen_table.table_comment)
        gen_table.function_author = GenConfig.author
        gen_table.create_by = oper_name
        gen_table.create_time = datetime.now()
        gen_table.update_by = oper_name
        gen_table.update_time = datetime.now()

    @classmethod
    def init_column_field(cls, column: GenTableColumnModel, table: GenTableModel) -> None:
        """
        初始化列属性字段

        param column: 业务表字段对象
        param table: 业务表对象
        :return:
        """
        data_type = cls.get_db_type(column.column_type)
        column_name = column.column_name
        column.table_id = table.table_id
        column.create_by = table.create_by
        # 设置Python字段名
        column.python_field = cls.to_camel_case(column_name)
        # 设置默认类型
        column.python_type = StringUtil.get_mapping_value_by_key_ignore_case(
            GenConstant.DB_TO_PYTHON_TYPE_MAPPING, data_type
        )
        column.query_type = GenConstant.QUERY_EQ

        column.html_type = cls.get_column_html_type(data_type, column.python_type, column.column_type)

        # 插入字段（默认所有字段都需要插入）
        column.is_insert = GenConstant.REQUIRE

        # 编辑字段
        if not cls.arrays_contains(GenConstant.COLUMNNAME_NOT_EDIT, column_name) and not column.pk:
            column.is_edit = GenConstant.REQUIRE
        # 列表字段
        if not cls.arrays_contains(GenConstant.COLUMNNAME_NOT_LIST, column_name) and not column.pk:
            column.is_list = GenConstant.REQUIRE
        # 查询字段
        if not cls.arrays_contains(GenConstant.COLUMNNAME_NOT_QUERY, column_name) and not column.pk:
            column.is_query = GenConstant.REQUIRE

        # 查询字段类型
        if column_name.lower().endswith('name'):
            column.query_type = GenConstant.QUERY_LIKE
        # 状态字段设置单选框
        if column_name.lower().endswith('status'):
            column.html_type = GenConstant.HTML_RADIO
        # 类型&性别字段设置下拉框
        elif column_name.lower().endswith('type') or column_name.lower().endswith('sex'):
            column.html_type = GenConstant.HTML_SELECT
        # 图片字段设置图片上传控件
        elif column_name.lower().endswith('image'):
            column.html_type = GenConstant.HTML_IMAGE_UPLOAD
        # 文件字段设置文件上传控件
        elif column_name.lower().endswith('file'):
            column.html_type = GenConstant.HTML_FILE_UPLOAD
        # 内容字段设置富文本控件
        elif column_name.lower().endswith('content'):
            column.html_type = GenConstant.HTML_EDITOR
        
        column.create_by = table.create_by
        column.create_time = datetime.now()
        column.update_by = table.update_by
        column.update_time = datetime.now()

    @classmethod
    def arrays_contains(cls, arr: List[str], target_value: str) -> bool:
        """
        校验数组是否包含指定值

        param arr: 数组
        param target_value: 需要校验的值
        :return: 校验结果
        """
        return target_value in arr

    @classmethod
    def get_column_html_type(cls, data_type: str, python_type: str, column_type: str) -> str:
        """
        根据数据库类型和Python类型选择前端生成组件类型。

        param data_type: 标准化后的数据库类型
        param python_type: Python类型
        param column_type: 原始字段类型
        :return: 前端显示类型
        """
        data_type = (data_type or '').lower()
        python_type = python_type or ''
        range_types = [
            'range',
            'int4range',
            'int8range',
            'numrange',
            'daterange',
            'tsrange',
            'tstzrange',
            'int4multirange',
            'int8multirange',
            'nummultirange',
            'datemultirange',
            'tsmultirange',
            'tstzmultirange',
        ]
        number_types = [
            'tinyint',
            'smallint',
            'int2',
            'mediumint',
            'int',
            'int4',
            'number',
            'integer',
            'bigint',
            'int8',
            'real',
            'float',
            'float4',
            'float8',
            'double',
            'double precision',
            'decimal',
            'numeric',
            'money',
            'oid',
        ]

        if data_type == 'date':
            return GenConstant.HTML_DATE
        if data_type in ['time', 'time without time zone']:
            return GenConstant.HTML_TIME
        if data_type in ['timetz', 'time with time zone']:
            return GenConstant.HTML_TIME_TZ
        if data_type in ['timestamp', 'timestamp without time zone']:
            return GenConstant.HTML_DATETIME
        if data_type in ['timestamptz', 'timestamp with time zone']:
            return GenConstant.HTML_DATETIME_TZ
        if data_type == 'interval':
            return GenConstant.HTML_DURATION
        if data_type in ['boolean', 'bool'] or python_type == 'bool':
            return GenConstant.HTML_SWITCH
        if data_type in ['json', 'jsonb', 'composite'] or python_type == 'dict':
            return GenConstant.HTML_JSON
        if data_type.startswith('_') or data_type in ['array', 'int2vector', 'oidvector']:
            return GenConstant.HTML_ARRAY
        if data_type in range_types:
            return GenConstant.HTML_RANGE
        if data_type == 'bytea' or python_type == 'bytes':
            return GenConstant.HTML_BINARY
        if data_type in GenConstant.COLUMNTYPE_TEXT:
            return GenConstant.HTML_TEXTAREA
        if data_type in GenConstant.COLUMNTYPE_STR:
            column_length = cls.get_column_length(column_type)
            return GenConstant.HTML_TEXTAREA if column_length >= 500 else GenConstant.HTML_INPUT
        if data_type in ['bit', 'bit varying']:
            return GenConstant.HTML_INPUT
        if data_type in number_types or python_type in ['Decimal', 'float', 'int']:
            return GenConstant.HTML_NUMBER
        if python_type == 'list':
            return GenConstant.HTML_ARRAY
        return GenConstant.HTML_INPUT

    @classmethod
    def get_module_name(cls, package_name: str) -> str:
        """
        获取模块名

        param package_name: 包名
        :return: 模块名
        """
        return package_name.split('.')[-1]

    @classmethod
    def get_business_name(cls, table_name: str) -> str:
        """
        获取业务名

        param table_name: 业务表名
        :return: 业务名
        """
        return table_name.split('_')[-1]

    @classmethod
    def convert_class_name(cls, table_name: str) -> str:
        """
        表名转换成Python类名

        param table_name: 业务表名
        :return: Python类名
        """
        auto_remove_pre = GenConfig.auto_remove_pre
        table_prefix = GenConfig.table_prefix
        if auto_remove_pre and table_prefix:
            search_list = table_prefix.split(',')
            table_name = cls.replace_first(table_name, search_list)
        return StringUtil.convert_to_camel_case(table_name)

    @classmethod
    def replace_first(cls, replacement: str, search_list: List[str]) -> str:
        """
        批量替换前缀

        param replacement: 需要被替换的字符串
        param search_list: 可替换的字符串列表
        :return: 替换后的字符串
        """
        for search_string in search_list:
            if replacement.startswith(search_string):
                return replacement.replace(search_string, '', 1)
        return replacement

    @classmethod
    def replace_text(cls, text: str) -> str:
        """
        关键字替换

        param text: 需要被替换的字符串
        :return: 替换后的字符串
        """
        return re.sub(r'(?:表|若依)', '', text)

    @classmethod
    def get_db_type(cls, column_type: str) -> str:
        """
        获取数据库类型字段

        param column_type: 字段类型
        :return: 数据库类型
        """
        if '(' in column_type:
            return column_type.split('(')[0]
        return column_type

    @classmethod
    def get_column_length(cls, column_type: str) -> int:
        """
        获取字段长度

        param column_type: 字段类型
        :return: 字段长度
        """
        if '(' in column_type:
            length = column_type.split('(')[1].split(')')[0].split(',')[0].strip()
            return int(length) if length.isdigit() else 0
        return 0

    @classmethod
    def split_column_type(cls, column_type: str) -> List[str]:
        """
        拆分列类型

        param column_type: 字段类型
        :return: 拆分结果
        """
        if '(' in column_type and ')' in column_type:
            return column_type.split('(')[1].split(')')[0].split(',')
        return []

    @classmethod
    def to_camel_case(cls, text: str) -> str:
        """
        将字符串转换为驼峰命名

        param text: 需要转换的字符串
        :return: 驼峰命名
        """
        parts = text.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])
