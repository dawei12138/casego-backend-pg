import sys
from sqlalchemy import Column, MetaData, Table, insert
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.dialects.postgresql.asyncpg import PGDialect_asyncpg

_original_argv = sys.argv[:]
sys.argv = [sys.argv[0]]
from module_generator.entity.vo.gen_vo import GenTableColumnModel, GenTableModel
from utils.gen_util import GenUtils
from utils.template_util import TemplateInitializer, TemplateUtils
sys.argv = _original_argv


def test_postgresql_internal_aliases_initialize_generator_column_types():
    table = GenTableModel(tableId=1, tableName='module_demo_all_types', createBy='tester', updateBy='tester')
    cases = [
        ('string_array_value', '_varchar', 'list'),
        ('integer_array_value', '_int4', 'list'),
        ('jsonb_array_items_value', '_jsonb', 'list'),
        ('enum_value', 'USER-DEFINED', 'str'),
        ('macaddr8_value', 'macaddr8', 'str'),
        ('int4_range_value', 'int4range', 'list'),
        ('timestamp_tz_multirange_value', 'tstzmultirange', 'list'),
        ('regconfig_value', 'regconfig', 'str'),
        ('jsonpath_value', 'jsonpath', 'str'),
        ('fixed_char_value', 'char(1)', 'str'),
    ]

    for column_name, column_type, python_type in cases:
        column = GenTableColumnModel(
            columnName=column_name,
            columnType=column_type,
            columnComment=column_name,
            isPk='0',
        )

        GenUtils.init_column_field(column, table)

        assert column.python_type == python_type
        assert column.html_type is not None


def test_postgresql_types_initialize_specific_frontend_component_types():
    table = GenTableModel(tableId=1, tableName='module_demo_all_types', createBy='tester', updateBy='tester')
    cases = [
        ('numeric_value', 'numeric(18,6)', 'number'),
        ('money_value', 'money', 'number'),
        ('boolean_value', 'boolean', 'switch'),
        ('date_value', 'date', 'date'),
        ('time_value', 'time', 'time'),
        ('time_tz_value', 'time with time zone', 'timeTz'),
        ('datetime_value', 'timestamp', 'datetime'),
        ('datetime_tz_value', 'timestamptz', 'datetimeTz'),
        ('interval_value', 'interval', 'duration'),
        ('json_value', 'json', 'json'),
        ('jsonb_array_value', 'jsonb', 'json'),
        ('binary_value', 'bytea', 'binary'),
        ('string_array_value', '_varchar', 'array'),
        ('int4_range_value', 'int4range', 'range'),
        ('timestamp_tz_multirange_value', 'tstzmultirange', 'range'),
    ]

    for column_name, column_type, html_type in cases:
        column = GenTableColumnModel(
            columnName=column_name,
            columnType=column_type,
            columnComment=column_name,
            isPk='0',
        )

        GenUtils.init_column_field(column, table)

        assert column.html_type == html_type


def test_postgresql_dialect_types_generate_valid_do_imports_and_type_expressions():
    table = GenTableModel(
        tableName='module_demo_all_types',
        columns=[
            GenTableColumnModel(columnName='string_array_value', columnType='_varchar', pythonField='stringArrayValue'),
            GenTableColumnModel(columnName='jsonb_array_items_value', columnType='_jsonb', pythonField='jsonbArrayItemsValue'),
            GenTableColumnModel(columnName='inet_value', columnType='inet', pythonField='inetValue'),
            GenTableColumnModel(columnName='jsonpath_value', columnType='jsonpath', pythonField='jsonpathValue'),
            GenTableColumnModel(columnName='oid_value', columnType='oid', pythonField='oidValue'),
            GenTableColumnModel(columnName='regclass_value', columnType='regclass', pythonField='regclassValue'),
            GenTableColumnModel(columnName='regconfig_value', columnType='regconfig', pythonField='regconfigValue'),
        ],
    )

    imports = TemplateUtils.get_do_import_list(table)

    assert TemplateUtils.get_sqlalchemy_type('_varchar') == 'ARRAY(String)'
    assert TemplateUtils.get_sqlalchemy_type('_jsonb') == 'ARRAY(JSONB)'
    assert TemplateUtils.get_sqlalchemy_type('inet') == 'INET'
    assert TemplateUtils.get_sqlalchemy_type('oid') == 'OID'
    assert TemplateUtils.get_sqlalchemy_type('regclass') == 'REGCLASS'
    assert TemplateUtils.get_sqlalchemy_type('regconfig') == 'REGCONFIG'
    assert TemplateUtils.get_sqlalchemy_type('char(1)') == 'CHAR(1)'
    assert 'from sqlalchemy import Column, String' in imports
    assert 'from sqlalchemy.dialects.postgresql import ARRAY, INET, JSONB, JSONPATH, OID, REGCLASS, REGCONFIG' in imports


def test_postgresql_enum_type_generates_enum_cast_for_asyncpg():
    table = GenTableModel(
        tableName='module_demo_all_types',
        tableComment='Demo全类型测试表',
        className='ModuleDemoAllTypes',
        packageName='module_admin.module_demo',
        moduleName='module_demo',
        businessName='module_demo',
        functionName='Demo全类型测试',
        functionAuthor='tester',
        tplCategory='crud',
        tplWebType='element-plus',
        options='{}',
        columns=[
            GenTableColumnModel(
                columnName='enum_value',
                columnType='USER-DEFINED(demo_status_enum|DRAFT|ACTIVE|DISABLED)',
                pythonField='enumValue',
                pythonType='str',
                columnComment='枚举-enum',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    imports = TemplateUtils.get_do_import_list(table)
    vo_imports = TemplateUtils.get_vo_import_list(table)
    sqlalchemy_type = TemplateUtils.get_sqlalchemy_type('USER-DEFINED(demo_status_enum|DRAFT|ACTIVE|DISABLED)')
    context = TemplateUtils.prepare_context(table)
    env = TemplateInitializer.init_jinja2()
    template_list = TemplateUtils.get_template_list(table.tpl_category, table.tpl_web_type, table)
    do_source = env.get_template('python/do.py.jinja2').render(**context)
    vo_source = env.get_template('python/vo.py.jinja2').render(**context)
    enum_source = env.get_template('python/enum.py.jinja2').render(**context)
    js_enum_source = env.get_template('js/enums.js.jinja2').render(**context)
    vue_source = env.get_template('vue/v3/index.vue.jinja2').render(**context)

    class DemoStatusEnum(str, __import__('enum').Enum):
        DRAFT = 'draft'
        ACTIVE = 'active'
        DISABLED = 'disabled'

    metadata = MetaData()
    enum_table = Table(
        'module_demo_all_types',
        metadata,
        Column('enum_value', eval(sqlalchemy_type, {'ENUM': ENUM, 'DemoStatusEnum': DemoStatusEnum})),
    )
    compiled = insert(enum_table).values(enum_value='active').compile(dialect=PGDialect_asyncpg())
    bind_processor = enum_table.c.enum_value.type.bind_processor(PGDialect_asyncpg())

    assert sqlalchemy_type == "ENUM(DemoStatusEnum, name='demo_status_enum', create_type=False)"
    assert 'python/enum.py.jinja2' in template_list
    assert 'js/enums.js.jinja2' in template_list
    assert (
        TemplateUtils.get_file_name('python/enum.py.jinja2', table)
        == 'backend/module_admin/module_demo/entity/enums/module_demo_enum.py'
    )
    assert (
        TemplateUtils.get_file_name('js/enums.js.jinja2', table)
        == 'frontend/api/module_demo/module_demo_enum.js'
    )
    assert 'import enum' not in imports
    assert 'from sqlalchemy.dialects.postgresql import ENUM' in imports
    assert 'from module_admin.module_demo.entity.enums.module_demo_enum import DemoStatusEnum' in imports
    assert 'from module_admin.module_demo.entity.enums.module_demo_enum import DemoStatusEnum' in vo_imports
    assert 'class DemoStatusEnum(str, enum.Enum):' not in do_source
    assert 'class DemoStatusEnum(str, enum.Enum):' not in vo_source
    assert 'class DemoStatusEnum(str, enum.Enum):' in enum_source
    assert "    DRAFT = 'draft'" in enum_source
    assert "    ACTIVE = 'active'" in enum_source
    assert "    DISABLED = 'disabled'" in enum_source
    assert 'export const demoStatusEnumOptions = [' in js_enum_source
    assert "{ label: 'active', value: 'active' }" in js_enum_source
    assert 'import { demoStatusEnumOptions } from "@/api/module_demo/module_demo_enum";' in vue_source
    assert 'v-for="option in demoStatusEnumOptions"' in vue_source
    assert ':options="demoStatusEnumOptions"' in vue_source
    assert '<dict-tag :options="demoStatusEnumOptions" :value="scope.row.enumValue"/>' in vue_source
    assert '请选择字典生成' not in vue_source
    assert 'enum_value = Column(ENUM(DemoStatusEnum' in do_source
    assert 'enum_value: Optional[DemoStatusEnum]' in vo_source
    assert '$1::demo_status_enum' in str(compiled)
    assert bind_processor('active') == 'ACTIVE'
    compile(do_source, '<generated-do>', 'exec')
    compile(vo_source, '<generated-vo>', 'exec')
    compile(enum_source, '<generated-enum>', 'exec')


def test_vue_template_renders_type_specific_components_and_payload_transforms():
    table = GenTableModel(
        tableName='module_demo_all_types',
        tableComment='Demo全类型测试表',
        className='ModuleDemoAllTypes',
        packageName='module_admin.module_demo',
        moduleName='module_demo',
        businessName='moduleDemo',
        functionName='Demo全类型测试',
        functionAuthor='tester',
        tplCategory='crud',
        tplWebType='element-plus',
        options='{}',
        columns=[
            GenTableColumnModel(
                columnName='id',
                columnType='bigint',
                pythonField='id',
                pythonType='int',
                htmlType='input',
                columnComment='主键ID-bigint',
                isPk='1',
            ),
            GenTableColumnModel(
                columnName='numeric_value',
                columnType='numeric(18,6)',
                pythonField='numericValue',
                pythonType='Decimal',
                htmlType='',
                columnComment='高精度小数-numeric',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
            GenTableColumnModel(
                columnName='boolean_value',
                columnType='boolean',
                pythonField='booleanValue',
                pythonType='bool',
                htmlType='',
                columnComment='布尔-boolean',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
            GenTableColumnModel(
                columnName='time_value',
                columnType='time',
                pythonField='timeValue',
                pythonType='time',
                htmlType='',
                columnComment='时间-time without time zone',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
            GenTableColumnModel(
                columnName='json_value',
                columnType='json',
                pythonField='jsonValue',
                pythonType='dict',
                htmlType='',
                columnComment='JSON-json',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
            GenTableColumnModel(
                columnName='string_array_value',
                columnType='_varchar',
                pythonField='stringArrayValue',
                pythonType='list',
                htmlType='',
                columnComment='字符串数组-array/varchar',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
            GenTableColumnModel(
                columnName='binary_value',
                columnType='bytea',
                pythonField='binaryValue',
                pythonType='bytes',
                htmlType='',
                columnComment='二进制-bytea',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    source = TemplateInitializer.init_jinja2().get_template('vue/v3/index.vue.jinja2').render(**context)

    assert '<el-input-number' in source
    assert 'v-model="form.numericValue"' in source
    assert '<el-switch v-model="form.booleanValue"' in source
    assert '<el-time-picker' in source
    assert '<el-input v-model="form.jsonValue" type="textarea"' in source
    assert '<el-input v-model="form.stringArrayValue" type="textarea"' in source
    assert '<el-input v-model="form.binaryValue" type="textarea"' in source
    assert 'formatTableValue(scope.row.jsonValue)' in source
    assert "const jsonFields = ['jsonValue', 'stringArrayValue']" in source
    assert "const binaryFields = ['binaryValue']" in source
    assert 'normalizeGeneratedPayload' in source


def test_vo_template_derives_missing_python_types_from_column_types():
    table = GenTableModel(
        tableName='module_demo_all_types',
        tableComment='Demo全类型测试表',
        className='ModuleDemoAllTypes',
        packageName='module_admin.module_demo',
        moduleName='module_demo',
        businessName='module_demo',
        functionName='Demo全类型测试',
        functionAuthor='tester',
        tplCategory='crud',
        tplWebType='element-plus',
        options='{}',
        columns=[
            GenTableColumnModel(
                columnName='id',
                columnType='bigint',
                pythonField='id',
                pythonType='int',
                columnComment='主键ID-bigint',
                isPk='1',
            ),
            GenTableColumnModel(
                columnName='fixed_char_value',
                columnType='char(1)',
                pythonField='fixedCharValue',
                pythonType='',
                columnComment='定长字符-char',
            ),
            GenTableColumnModel(
                columnName='interval_value',
                columnType='interval',
                pythonField='intervalValue',
                pythonType='',
                columnComment='时间间隔-interval',
            ),
            GenTableColumnModel(
                columnName='string_array_value',
                columnType='_varchar',
                pythonField='stringArrayValue',
                pythonType='',
                columnComment='字符串数组-array/varchar',
            ),
            GenTableColumnModel(
                columnName='jsonpath_value',
                columnType='jsonpath',
                pythonField='jsonpathValue',
                pythonType='',
                columnComment='JSON路径-jsonpath',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    source = TemplateInitializer.init_jinja2().get_template('python/vo.py.jinja2').render(**context)

    assert 'Optional[]' not in source
    assert 'from datetime import timedelta' in source
    compile(source, '<generated-vo>', 'exec')
