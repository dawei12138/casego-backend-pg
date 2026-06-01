import json
import keyword
import os
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Set
from config.constant import GenConstant
from config.env import DataBaseConfig
from exceptions.exception import ServiceWarning
from module_generator.entity.vo.gen_vo import GenTableModel, GenTableColumnModel
from utils.common_util import CamelCaseUtil, SnakeCaseUtil
from utils.gen_util import GenUtils
from utils.string_util import StringUtil


class TemplateInitializer:
    """
    模板引擎初始化类
    """

    @classmethod
    def init_jinja2(cls):
        """
        初始化 Jinja2 模板引擎

        :return: Jinja2 环境对象
        """
        try:
            template_dir = os.path.join(os.getcwd(), 'module_generator', 'templates')
            env = Environment(
                loader=FileSystemLoader(template_dir),
                keep_trailing_newline=True,
                trim_blocks=True,
                lstrip_blocks=True,
            )
            env.filters.update(
                {
                    'camel_to_snake': SnakeCaseUtil.camel_to_snake,
                    'snake_to_camel': CamelCaseUtil.snake_to_camel,
                    'get_sqlalchemy_type': TemplateUtils.get_sqlalchemy_type,
                    'get_vo_python_type': TemplateUtils.get_vo_python_type,
                    'is_enum_column': TemplateUtils.is_enum_column,
                    'get_enum_options_name': TemplateUtils.get_enum_options_name,
                    'py_repr': repr,
                }
            )
            return env
        except Exception as e:
            raise RuntimeError(f'初始化Jinja2模板引擎失败: {e}')


class TemplateUtils:
    """
    模板工具类
    """

    # 项目路径
    FRONTEND_PROJECT_PATH = 'frontend'
    BACKEND_PROJECT_PATH = 'backend'
    DEFAULT_PARENT_MENU_ID = '3'
    POSTGRESQL_SQLALCHEMY_TYPES = {
        'ARRAY',
        'BIT',
        'CIDR',
        'DATERANGE',
        'DATEMULTIRANGE',
        'ENUM',
        'INET',
        'INT4MULTIRANGE',
        'INT4RANGE',
        'INT8MULTIRANGE',
        'INT8RANGE',
        'JSONB',
        'JSONPATH',
        'MACADDR',
        'MACADDR8',
        'MONEY',
        'NUMMULTIRANGE',
        'NUMRANGE',
        'OID',
        'REGCLASS',
        'REGCONFIG',
        'TSQUERY',
        'TSVECTOR',
        'TSMULTIRANGE',
        'TSRANGE',
        'TSTZMULTIRANGE',
        'TSTZRANGE',
    }

    @classmethod
    def prepare_context(cls, gen_table: GenTableModel):
        """
        准备模板变量

        :param gen_table: 生成表的配置信息
        :return: 模板上下文字典
        """
        if not gen_table.options:
            raise ServiceWarning(message='请先完善生成配置信息')
        cls.normalize_render_columns(gen_table)
        class_name = gen_table.class_name
        module_name = gen_table.module_name
        business_name = gen_table.business_name
        package_name = gen_table.package_name
        tpl_category = gen_table.tpl_category
        function_name = gen_table.function_name

        context = {
            'tplCategory': tpl_category,
            'tableName': gen_table.table_name,
            'functionName': function_name if StringUtil.is_not_empty(function_name) else '【请填写功能名称】',
            'ClassName': class_name,
            'className': class_name.lower(),
            'moduleName': module_name,
            'BusinessName': business_name.capitalize(),
            'businessName': business_name,
            'basePackage': cls.get_package_prefix(package_name),
            'packageName': package_name,
            'author': gen_table.function_author,
            'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'pkColumn': gen_table.pk_column,
            'doImportList': cls.get_do_import_list(gen_table),
            'voImportList': cls.get_vo_import_list(gen_table),
            'permissionPrefix': cls.get_permission_prefix(module_name, business_name),
            'columns': gen_table.columns,
            'table': gen_table,
            'dicts': cls.get_dicts(gen_table),
            'enumFields': cls.get_enum_fields(gen_table),
            'enumImportNames': cls.get_enum_import_names(gen_table),
            'frontendJsonFields': cls.get_frontend_field_names(
                gen_table, [GenConstant.HTML_JSON, GenConstant.HTML_ARRAY, GenConstant.HTML_RANGE]
            ),
            'frontendBinaryFields': cls.get_frontend_field_names(gen_table, [GenConstant.HTML_BINARY]),
            'dbType': DataBaseConfig.db_type,
            'column_not_add_show': GenConstant.COLUMNNAME_NOT_ADD_SHOW,
            'column_not_edit_show': GenConstant.COLUMNNAME_NOT_EDIT_SHOW,
        }

        # 设置菜单、树形结构、子表的上下文
        cls.set_menu_context(context, gen_table)
        if tpl_category == GenConstant.TPL_TREE:
            cls.set_tree_context(context, gen_table)
        if tpl_category == GenConstant.TPL_SUB:
            cls.set_sub_context(context, gen_table)

        return context

    @classmethod
    def normalize_render_columns(cls, gen_table: GenTableModel):
        """
        补齐生成模板所需的字段元数据，兼容修复前已导入的字段配置。

        :param gen_table: 生成表的配置信息
        :return:
        """
        for column in gen_table.columns or []:
            cls.normalize_render_column(column)
        if gen_table.sub_table is not None:
            for column in gen_table.sub_table.columns or []:
                cls.normalize_render_column(column)

    @classmethod
    def normalize_render_column(cls, column: GenTableColumnModel):
        """
        根据column_type补齐python_type和html_type，避免旧配置渲染出Optional[]。

        :param column: 字段配置
        :return:
        """
        data_type = cls.get_db_type(column.column_type)
        if not column.python_type:
            column.python_type = StringUtil.get_mapping_value_by_key_ignore_case(
                GenConstant.DB_TO_PYTHON_TYPE_MAPPING, data_type
            )
        if cls.is_enum_column(column):
            column.html_type = GenConstant.HTML_SELECT
            return
        html_type = GenUtils.get_column_html_type(data_type, column.python_type, column.column_type)
        if not column.html_type or column.html_type in [
            GenConstant.HTML_INPUT,
            GenConstant.HTML_TEXTAREA,
            GenConstant.HTML_DATETIME,
        ]:
            column.html_type = html_type

    @classmethod
    def get_frontend_field_names(cls, gen_table: GenTableModel, html_types: List[str]) -> List[str]:
        """
        获取前端需要特殊序列化的字段名。

        :param gen_table: 生成表的配置信息
        :param html_types: 前端显示类型列表
        :return: 字段名列表
        """
        return [
            column.python_field
            for column in gen_table.columns or []
            if column.python_field and column.html_type in html_types
        ]

    @classmethod
    def set_menu_context(cls, context: Dict, gen_table: GenTableModel):
        """
        设置菜单上下文

        :param context: 模板上下文字典
        :param gen_table: 生成表的配置信息
        :return: 新的模板上下文字典
        """
        options = gen_table.options
        params_obj = json.loads(options)
        context['parentMenuId'] = cls.get_parent_menu_id(params_obj)

    @classmethod
    def set_tree_context(cls, context: Dict, gen_table: GenTableModel):
        """
        设置树形结构上下文

        :param context: 模板上下文字典
        :param gen_table: 生成表的配置信息
        :return: 新的模板上下文字典
        """
        options = gen_table.options
        params_obj = json.loads(options)
        context['treeCode'] = cls.get_tree_code(params_obj)
        context['treeParentCode'] = cls.get_tree_parent_code(params_obj)
        context['treeName'] = cls.get_tree_name(params_obj)
        context['expandColumn'] = cls.get_expand_column(gen_table)

    @classmethod
    def set_sub_context(cls, context: Dict, gen_table: GenTableModel):
        """
        设置子表上下文

        :param context: 模板上下文字典
        :param gen_table: 生成表的配置信息
        :return: 新的模板上下文字典
        """
        sub_table = gen_table.sub_table
        sub_table_name = gen_table.sub_table_name
        sub_table_fk_name = gen_table.sub_table_fk_name
        sub_class_name = sub_table.class_name
        sub_table_fk_class_name = StringUtil.convert_to_camel_case(sub_table_fk_name)
        context['subTable'] = sub_table
        context['subTableName'] = sub_table_name
        context['subTableFkName'] = sub_table_fk_name
        context['subTableFkClassName'] = sub_table_fk_class_name
        context['subTableFkclassName'] = sub_table_fk_class_name.lower()
        context['subClassName'] = sub_class_name
        context['subclassName'] = sub_class_name.lower()

    @classmethod
    def get_template_list(cls, tpl_category: str, tpl_web_type: str, gen_table: GenTableModel = None):
        """
        获取模板列表

        :param tpl_category: 生成模板类型
        :param tpl_web_type: 前端类型
        :return: 模板列表
        """
        use_web_type = 'vue'
        if tpl_web_type == 'element-plus':
            use_web_type = 'vue/v3'
        templates = [
            'python/controller.py.jinja2',
            'python/dao.py.jinja2',
            'python/do.py.jinja2',
            'python/service.py.jinja2',
            'python/vo.py.jinja2',
            'sql/sql.jinja2',
            'js/api.js.jinja2',
        ]
        if gen_table is not None and cls.get_enum_fields(gen_table):
            templates.append('python/enum.py.jinja2')
            templates.append('js/enums.js.jinja2')
        if tpl_category == GenConstant.TPL_CRUD:
            templates.append(f'{use_web_type}/index.vue.jinja2')
        elif tpl_category == GenConstant.TPL_TREE:
            templates.append(f'{use_web_type}/index-tree.vue.jinja2')
        elif tpl_category == GenConstant.TPL_SUB:
            templates.append(f'{use_web_type}/index.vue.jinja2')
            # templates.append('python/sub-domain.python.jinja2')
        return templates

    @classmethod
    def get_file_name(cls, template: List[str], gen_table: GenTableModel):
        """
        根据模板生成文件名

        :param template: 模板列表
        :param gen_table: 生成表的配置信息
        :return: 模板生成文件名
        """
        package_name = gen_table.package_name
        module_name = gen_table.module_name
        business_name = gen_table.business_name

        vue_path = cls.FRONTEND_PROJECT_PATH
        python_path = f'{cls.BACKEND_PROJECT_PATH}/{package_name.replace(".", "/")}'

        if 'controller.py.jinja2' in template:
            return f'{python_path}/controller/{business_name}_controller.py'
        elif 'dao.py.jinja2' in template:
            return f'{python_path}/dao/{business_name}_dao.py'
        elif 'do.py.jinja2' in template:
            return f'{python_path}/entity/do/{business_name}_do.py'
        elif 'enum.py.jinja2' in template:
            return f'{python_path}/entity/enums/{business_name}_enum.py'
        elif 'service.py.jinja2' in template:
            return f'{python_path}/service/{business_name}_service.py'
        elif 'vo.py.jinja2' in template:
            return f'{python_path}/entity/vo/{business_name}_vo.py'
        elif 'sql.jinja2' in template:
            return f'{cls.BACKEND_PROJECT_PATH}/sql/{business_name}_menu.sql'
        elif 'api.js.jinja2' in template:
            return f'{vue_path}/api/{module_name}/{business_name}.js'
        elif 'enums.js.jinja2' in template:
            return f'{vue_path}/api/{module_name}/{business_name}_enum.js'
        elif 'index.vue.jinja2' in template or 'index-tree.vue.jinja2' in template:
            return f'{vue_path}/views/{module_name}/{business_name}/index.vue'
        return ''

    @classmethod
    def get_package_prefix(cls, package_name: str):
        """
        获取包前缀

        :param package_name: 包名
        :return: 包前缀
        """
        return package_name[: package_name.rfind('.')]

    @classmethod
    def get_vo_import_list(cls, gen_table: GenTableModel):
        """
        获取vo模板导入包列表

        :param gen_table: 生成表的配置信息
        :return: 导入包列表
        """
        columns = gen_table.columns or []
        import_list = set()
        enum_import_names = cls.get_enum_import_names(gen_table)
        if enum_import_names:
            import_list.add(
                f'from {gen_table.package_name}.entity.enums.{gen_table.business_name}_enum import '
                f'{", ".join(enum_import_names)}'
            )
        for column in columns:
            if column.python_type in GenConstant.TYPE_DATE:
                import_list.add(f'from datetime import {column.python_type}')
            elif column.python_type == GenConstant.TYPE_DECIMAL:
                import_list.add('from decimal import Decimal')
        if gen_table.sub:
            sub_columns = gen_table.sub_table.columns or []
            for sub_column in sub_columns:
                if sub_column.python_type in GenConstant.TYPE_DATE:
                    import_list.add(f'from datetime import {sub_column.python_type}')
                elif sub_column.python_type == GenConstant.TYPE_DECIMAL:
                    import_list.add('from decimal import Decimal')
        return cls.merge_same_imports(list(import_list), 'from datetime import')

    @classmethod
    def get_do_import_list(cls, gen_table: GenTableModel):
        """
        获取do模板导入包列表

        :param gen_table: 生成表的配置信息
        :return: 导入包列表
        """
        columns = gen_table.columns or []
        import_list = set()
        enum_import_names = cls.get_enum_import_names(gen_table)
        if enum_import_names:
            import_list.add(
                f'from {gen_table.package_name}.entity.enums.{gen_table.business_name}_enum import '
                f'{", ".join(enum_import_names)}'
            )
        import_list.add('from sqlalchemy import Column')
        for column in columns:
            if cls.get_db_type(column.column_type) in GenConstant.COLUMNTYPE_GEOMETRY:
                import_list.add('from geoalchemy2 import Geometry')
            cls.add_do_type_imports(import_list, cls.get_sqlalchemy_type(column.column_type))
        if gen_table.sub:
            import_list.add('from sqlalchemy import ForeignKey')
            sub_columns = gen_table.sub_table.columns or []
            for sub_column in sub_columns:
                cls.add_do_type_imports(import_list, cls.get_sqlalchemy_type(sub_column.column_type))
        imports = cls.merge_same_imports(list(import_list), 'from sqlalchemy import')
        return cls.merge_same_imports(imports, 'from sqlalchemy.dialects.postgresql import')

    @classmethod
    def add_do_type_imports(cls, import_list: Set[str], sqlalchemy_type: str):
        """
        根据SQLAlchemy类型表达式补充DO模型导入。

        :param import_list: 导入语句集合
        :param sqlalchemy_type: SQLAlchemy类型表达式，如String(100)、ARRAY(JSONB)
        :return:
        """
        if not sqlalchemy_type:
            return
        for type_name in re.findall(r'\b[A-Z][A-Za-z0-9_]*\b', sqlalchemy_type):
            if type_name in ['True', 'False', 'None']:
                continue
            if type_name.endswith('Enum') and type_name != 'Enum':
                continue
            if type_name in cls.POSTGRESQL_SQLALCHEMY_TYPES:
                import_list.add(f'from sqlalchemy.dialects.postgresql import {type_name}')
            else:
                import_list.add(f'from sqlalchemy import {type_name}')

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
    def parse_postgresql_enum_type(cls, column_type: str) -> Dict:
        """
        解析PostgreSQL enum类型描述。

        格式:
        - USER-DEFINED(demo_status_enum)
        - USER-DEFINED(demo_status_enum|DRAFT|ACTIVE|DISABLED)
        """
        if not column_type or cls.get_db_type(column_type).upper() != 'USER-DEFINED' or '(' not in column_type:
            return {}
        payload = column_type.split('(', 1)[1].rsplit(')', 1)[0]
        if not payload:
            return {}
        enum_parts = payload.split('|')
        enum_type_name = enum_parts[0].strip()
        enum_labels = [enum_label for enum_label in enum_parts[1:] if enum_label != '']
        if not enum_type_name:
            return {}

        return {
            'enum_type_name': enum_type_name,
            'enum_labels': enum_labels,
            'enum_class_name': cls.get_enum_class_name(enum_type_name),
            'use_db_labels': cls.should_use_db_enum_labels(enum_labels),
        }

    @classmethod
    def get_enum_fields(cls, gen_table: GenTableModel) -> List[Dict]:
        """
        获取生成DO/VO模型时需要声明的Python枚举类。
        """
        enum_fields = []
        enum_field_keys = set()
        columns = list(gen_table.columns or [])
        if gen_table.sub_table is not None:
            columns.extend(gen_table.sub_table.columns or [])

        for column in columns:
            enum_info = cls.parse_postgresql_enum_type(column.column_type)
            enum_labels = enum_info.get('enum_labels') or []
            if not enum_info or not enum_labels:
                continue
            enum_key = (enum_info['enum_type_name'], tuple(enum_labels))
            if enum_key in enum_field_keys:
                continue
            enum_field_keys.add(enum_key)
            enum_fields.append(
                {
                    'enum_type_name': enum_info['enum_type_name'],
                    'enum_class_name': enum_info['enum_class_name'],
                    'enum_options_name': cls.get_enum_options_name(column),
                    'use_db_labels': enum_info['use_db_labels'],
                    'enum_values': cls.get_enum_values(enum_labels),
                }
            )

        return enum_fields

    @classmethod
    def get_enum_import_names(cls, gen_table: GenTableModel) -> List[str]:
        """
        获取DO/VO需要导入的枚举类名。
        """
        return sorted({enum_field.get('enum_class_name') for enum_field in cls.get_enum_fields(gen_table)})

    @classmethod
    def get_enum_values(cls, enum_labels: List[str]) -> List[Dict]:
        """
        生成Python枚举成员名和值。
        """
        enum_values = []
        used_member_names = set()
        use_db_labels = cls.should_use_db_enum_labels(enum_labels)
        for enum_label in enum_labels:
            member_name = cls.get_enum_member_name(enum_label)
            original_member_name = member_name
            index = 2
            while member_name in used_member_names:
                member_name = f'{original_member_name}_{index}'
                index += 1
            used_member_names.add(member_name)
            enum_values.append(
                {
                    'name': member_name,
                    'value': enum_label if use_db_labels else enum_label.lower(),
                    'db_label': enum_label,
                }
            )
        return enum_values

    @classmethod
    def should_use_db_enum_labels(cls, enum_labels: List[str]) -> bool:
        """
        判断Python枚举值是否应直接使用数据库label。

        PostgreSQL enum常见建模会使用DRAFT/ACTIVE这类大写label。此时Python枚举值转为draft/active，
        SQLAlchemy仍会按枚举成员名写入数据库，接口JSON Schema也更贴近日常API值。
        """
        return not enum_labels or not all(re.match(r'^[A-Z][A-Z0-9_]*$', enum_label) for enum_label in enum_labels)

    @classmethod
    def get_enum_class_name(cls, enum_type_name: str) -> str:
        """
        根据数据库enum类型名生成Python枚举类名。
        """
        class_parts = [part for part in re.split(r'[^0-9A-Za-z]+', enum_type_name) if part]
        enum_class_name = ''.join(part[:1].upper() + part[1:].lower() for part in class_parts)
        if not enum_class_name:
            return 'GeneratedEnum'
        if enum_class_name[0].isdigit():
            enum_class_name = f'Enum{enum_class_name}'
        return enum_class_name

    @classmethod
    def get_enum_member_name(cls, enum_label: str) -> str:
        """
        根据数据库enum label生成合法的Python枚举成员名。
        """
        member_name = re.sub(r'\W+', '_', enum_label).strip('_').upper()
        if not member_name:
            member_name = 'VALUE'
        if member_name[0].isdigit() or keyword.iskeyword(member_name.lower()):
            member_name = f'VALUE_{member_name}'
        return member_name

    @classmethod
    def get_vo_python_type(cls, column: GenTableColumnModel) -> str:
        """
        获取VO字段Python类型。
        """
        enum_info = cls.parse_postgresql_enum_type(column.column_type)
        if enum_info and enum_info.get('enum_labels'):
            return enum_info['enum_class_name']
        return column.python_type

    @classmethod
    def is_enum_column(cls, column: GenTableColumnModel) -> bool:
        """
        判断字段是否为带labels的PostgreSQL枚举字段。
        """
        enum_info = cls.parse_postgresql_enum_type(column.column_type)
        return bool(enum_info and enum_info.get('enum_labels'))

    @classmethod
    def get_enum_options_name(cls, column: GenTableColumnModel) -> str:
        """
        获取前端枚举options常量名。
        """
        enum_info = cls.parse_postgresql_enum_type(column.column_type)
        if not enum_info:
            return ''
        enum_class_name = enum_info['enum_class_name']
        return enum_class_name[:1].lower() + enum_class_name[1:] + 'Options'

    @classmethod
    def get_column_length(cls, column_type: str) -> int:
        """
        获取字段长度。

        :param column_type: 字段类型
        :return: 字段长度
        """
        if '(' in column_type:
            length = column_type.split('(')[1].split(')')[0].split(',')[0].strip()
            return int(length) if length.isdigit() else 0
        return 0

    @classmethod
    def merge_same_imports(cls, imports: List[str], import_start: str) -> List[str]:
        """
        合并相同的导入语句

        :param imports: 导入语句列表
        :param import_start: 导入语句的起始字符串
        :return: 合并后的导入语句列表
        """
        merged_imports = []
        _imports = []
        for import_stmt in imports:
            if import_stmt.startswith(import_start):
                imported_items = import_stmt.split('import')[1].strip()
                _imports.extend(imported_items.split(', '))
            else:
                merged_imports.append(import_stmt)

        if _imports:
            merged_datetime_import = f'{import_start} {", ".join(sorted(set(_imports)))}'
            merged_imports.append(merged_datetime_import)

        return sorted(merged_imports)

    @classmethod
    def get_dicts(cls, gen_table: GenTableModel):
        """
        获取字典列表

        :param gen_table: 生成表的配置信息
        :return: 字典列表
        """
        columns = gen_table.columns or []
        dicts = set()
        cls.add_dicts(dicts, columns)
        if gen_table.sub_table is not None:
            cls.add_dicts(dicts, gen_table.sub_table.columns)
        return ', '.join(dicts)

    @classmethod
    def add_dicts(cls, dicts: Set[str], columns: List[GenTableColumnModel]):
        """
        添加字典列表

        :param dicts: 字典列表
        :param columns: 字段列表
        :return: 新的字典列表
        """
        for column in columns:
            if (
                not column.super_column
                and StringUtil.is_not_empty(column.dict_type)
                and StringUtil.equals_any_ignore_case(
                    column.html_type, [GenConstant.HTML_SELECT, GenConstant.HTML_RADIO, GenConstant.HTML_CHECKBOX]
                )
            ):
                dicts.add(f"'{column.dict_type}'")

    @classmethod
    def get_permission_prefix(cls, module_name: str, business_name: str):
        """
        获取权限前缀

        :param module_name: 模块名
        :param business_name: 业务名
        :return: 权限前缀
        """
        return f'{module_name}:{business_name}'

    @classmethod
    def get_parent_menu_id(cls, params_obj: Dict):
        """
        获取上级菜单ID

        :param params_obj: 菜单参数字典
        :return: 上级菜单ID
        """
        if params_obj and params_obj.get(GenConstant.PARENT_MENU_ID):
            return params_obj.get(GenConstant.PARENT_MENU_ID)
        return cls.DEFAULT_PARENT_MENU_ID

    @classmethod
    def get_tree_code(cls, params_obj: Dict):
        """
        获取树编码

        :param params_obj: 菜单参数字典
        :return: 树编码
        """
        if GenConstant.TREE_CODE in params_obj:
            return cls.to_camel_case(params_obj.get(GenConstant.TREE_CODE))
        return ''

    @classmethod
    def get_tree_parent_code(cls, params_obj: Dict):
        """
        获取树父编码

        :param params_obj: 菜单参数字典
        :return: 树父编码
        """
        if GenConstant.TREE_PARENT_CODE in params_obj:
            return cls.to_camel_case(params_obj.get(GenConstant.TREE_PARENT_CODE))
        return ''

    @classmethod
    def get_tree_name(cls, params_obj: Dict):
        """
        获取树名称

        :param params_obj: 菜单参数字典
        :return: 树名称
        """
        if GenConstant.TREE_NAME in params_obj:
            return cls.to_camel_case(params_obj.get(GenConstant.TREE_NAME))
        return ''

    @classmethod
    def get_expand_column(cls, gen_table: GenTableModel):
        """
        获取展开列

        :param gen_table: 生成表的配置信息
        :return: 展开列
        """
        options = gen_table.options
        params_obj = json.loads(options)
        tree_name = params_obj.get(GenConstant.TREE_NAME)
        num = 0
        for column in gen_table.columns or []:
            if column.list:
                num += 1
                if column.column_name == tree_name:
                    break
        return num

    @classmethod
    def to_camel_case(cls, text: str) -> str:
        """
        将字符串转换为驼峰命名

        :param text: 待转换的字符串
        :return: 转换后的驼峰命名字符串
        """
        parts = text.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    @classmethod
    def get_sqlalchemy_type(cls, column_type: str):
        """
        获取SQLAlchemy类型

        :param column_type: 列类型
        :return: SQLAlchemy类型
        """
        if '(' in column_type:
            column_type_list = column_type.split('(')
            data_type = column_type_list[0]
            if data_type.upper() == 'USER-DEFINED':
                enum_info = cls.parse_postgresql_enum_type(column_type)
                enum_type_name = enum_info.get('enum_type_name')
                enum_labels = enum_info.get('enum_labels') or []
                enum_class_name = enum_info.get('enum_class_name')
                if enum_labels and enum_class_name:
                    if enum_info.get('use_db_labels'):
                        return (
                            f"ENUM({enum_class_name}, values_callable=lambda x: [e.value for e in x], "
                            f"name='{enum_type_name}', create_type=False)"
                        )
                    return f"ENUM({enum_class_name}, name='{enum_type_name}', create_type=False)"
                return f"ENUM(name='{enum_type_name}', create_type=False)"
            mapped_type = StringUtil.get_mapping_value_by_key_ignore_case(
                GenConstant.DB_TO_SQLALCHEMY_TYPE_MAPPING, data_type
            )
            if data_type in GenConstant.COLUMNTYPE_STR:
                sqlalchemy_type = (
                    mapped_type
                    + '('
                    + column_type_list[1]
                )
            elif mapped_type in ['Numeric', 'DECIMAL']:
                sqlalchemy_type = mapped_type + '(' + column_type_list[1]
            else:
                sqlalchemy_type = mapped_type
        else:
            sqlalchemy_type = StringUtil.get_mapping_value_by_key_ignore_case(
                GenConstant.DB_TO_SQLALCHEMY_TYPE_MAPPING, column_type
            )

        return sqlalchemy_type
