import sys
import uuid
from sqlalchemy import Column, DateTime, MetaData, Table, Time, insert
from sqlalchemy.dialects.postgresql import BIT, ENUM
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
        ('bit_value', 'bit', 'str'),
        ('bit_varying_value', 'bit varying', 'str'),
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


def test_postgresql_insert_bind_casts_match_timezone_and_bit_types():
    cases = [
        ('time_tz_value', 'time with time zone', 'Time(timezone=True)', '$1::TIME WITH TIME ZONE'),
        ('timetz_value', 'timetz', 'Time(timezone=True)', '$1::TIME WITH TIME ZONE'),
        (
            'datetime_tz_value',
            'timestamp with time zone',
            'DateTime(timezone=True)',
            '$1::TIMESTAMP WITH TIME ZONE',
        ),
        ('timestamptz_value', 'timestamptz', 'DateTime(timezone=True)', '$1::TIMESTAMP WITH TIME ZONE'),
        ('bit_varying_value', 'bit varying', 'BIT(varying=True)', '$1::BIT VARYING'),
        ('bit_varying_value', 'bit varying(16)', 'BIT(16, varying=True)', '$1::BIT VARYING(16)'),
    ]

    for column_name, column_type, expected_type, expected_cast in cases:
        sqlalchemy_type = TemplateUtils.get_sqlalchemy_type(column_type)
        table = Table(
            'module_demo_all_types',
            MetaData(),
            Column(column_name, eval(sqlalchemy_type, {'Time': Time, 'DateTime': DateTime, 'BIT': BIT})),
        )
        compiled = insert(table).values({column_name: None}).compile(dialect=PGDialect_asyncpg())

        assert sqlalchemy_type == expected_type
        assert expected_cast in str(compiled)

    assert TemplateUtils.get_sqlalchemy_type('_timetz') == 'ARRAY(Time(timezone=True))'
    assert TemplateUtils.get_sqlalchemy_type('_timestamptz') == 'ARRAY(DateTime(timezone=True))'


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
            GenTableColumnModel(
                columnName='jsonpath_value',
                columnType='jsonpath',
                pythonField='jsonpathValue',
                pythonType='str',
                htmlType='',
                columnComment='JSON路径-jsonpath',
                isInsert='1',
                isEdit='1',
                isList='1',
                isQuery='1',
            ),
            GenTableColumnModel(
                columnName='bit_value',
                columnType='bit',
                pythonField='bitValue',
                pythonType='str',
                htmlType='',
                columnComment='固定长度位-bit',
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
    assert "const emptyStringNullFields = ['jsonValue', 'stringArrayValue', 'binaryValue', 'jsonpathValue', 'bitValue']" in source
    assert 'normalizeGeneratedPayload' in source
    assert 'emptyStringNullFields.forEach(field => {' in source


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


def test_vo_template_allows_json_fields_to_receive_objects_and_arrays():
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
                columnName='json_value',
                columnType='json',
                pythonField='jsonValue',
                pythonType='dict',
                columnComment='JSON-json',
            ),
            GenTableColumnModel(
                columnName='jsonb_object_value',
                columnType='jsonb',
                pythonField='jsonbObjectValue',
                pythonType='dict',
                columnComment='JSON对象-jsonb/object',
            ),
            GenTableColumnModel(
                columnName='jsonb_array_value',
                columnType='jsonb',
                pythonField='jsonbArrayValue',
                pythonType='dict',
                columnComment='JSON数组-jsonb/array',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    source = TemplateInitializer.init_jinja2().get_template('python/vo.py.jinja2').render(**context)
    namespace = {}

    exec(source, namespace)
    model = namespace['Module_demoModel'].model_validate(
        {
            'jsonValue': [],
            'jsonbObjectValue': {'enabled': True},
            'jsonbArrayValue': [{'id': 1}],
        }
    )

    assert 'json_value: Optional[Any]' in source
    assert model.json_value == []
    assert model.jsonb_object_value == {'enabled': True}
    assert model.jsonb_array_value == [{'id': 1}]


def test_do_template_uses_string_default_for_del_flag():
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
                columnName='del_flag',
                columnType='varchar(1)',
                pythonField='delFlag',
                pythonType='str',
                columnComment='删除标志',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    source = TemplateInitializer.init_jinja2().get_template('python/do.py.jinja2').render(**context)

    assert "del_flag = Column(String(1), nullable=True, default='0', comment='删除标志')" in source
    assert "default=0" not in source
    compile(source, '<generated-do>', 'exec')


def test_uuid_primary_key_generates_python_default_and_string_route_types():
    table = GenTableModel(
        tableName='module_uuid_demo_test',
        tableComment='UUID主键业务示例表',
        className='ModuleUuidDemoTest',
        packageName='module_admin.module_demo.module_uuid_demo',
        moduleName='uuid_demo',
        businessName='module_uuid_demo',
        functionName='UUID主键业务示例',
        functionAuthor='tester',
        tplCategory='crud',
        tplWebType='element-plus',
        options='{}',
        columns=[
            GenTableColumnModel(
                columnName='id',
                columnType='uuid',
                pythonField='id',
                pythonType='str',
                columnComment='主键ID-uuid',
                isPk='1',
            ),
            GenTableColumnModel(
                columnName='title',
                columnType='varchar(100)',
                pythonField='title',
                pythonType='str',
                columnComment='业务标题',
                isInsert='1',
                isRequired='1',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    env = TemplateInitializer.init_jinja2()
    do_source = env.get_template('python/do.py.jinja2').render(**context)
    controller_source = env.get_template('python/controller.py.jinja2').render(**context)
    dao_source = env.get_template('python/dao.py.jinja2').render(**context)
    service_source = env.get_template('python/service.py.jinja2').render(**context)

    assert 'import uuid' in do_source
    assert "id = Column(Uuid, primary_key=True, nullable=False, default=uuid.uuid4, comment='主键ID-uuid')" in do_source
    assert 'async def query_detail_uuid_demo_module_uuid_demo(request: Request, id: str,' in controller_source
    assert 'async def get_module_uuid_demo_detail_by_id(cls, db: AsyncSession, id: str):' in dao_source
    assert 'async def module_uuid_demo_detail_services(cls, query_db: AsyncSession, id: str):' in service_source
    assert 'int(id)' not in service_source
    compile(do_source, '<generated-do>', 'exec')
    compile(controller_source, '<generated-controller>', 'exec')
    compile(dao_source, '<generated-dao>', 'exec')
    compile(service_source, '<generated-service>', 'exec')


def test_uuid_columns_generate_uuid_vo_type_and_accept_database_uuid_values():
    table = GenTableModel(
        tableName='module_uuid_demo_test',
        tableComment='UUID主键业务示例表',
        className='ModuleUuidDemoTest',
        packageName='module_admin.module_demo.module_uuid_demo',
        moduleName='uuid_demo',
        businessName='module_uuid_demo',
        functionName='UUID主键业务示例',
        functionAuthor='tester',
        tplCategory='crud',
        tplWebType='element-plus',
        options='{}',
        columns=[
            GenTableColumnModel(
                columnName='id',
                columnType='uuid',
                pythonField='id',
                pythonType='str',
                columnComment='主键ID-uuid',
                isPk='1',
            ),
            GenTableColumnModel(
                columnName='title',
                columnType='varchar(100)',
                pythonField='title',
                pythonType='str',
                columnComment='业务标题',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    source = TemplateInitializer.init_jinja2().get_template('python/vo.py.jinja2').render(**context)
    namespace = {}
    database_id = uuid.uuid4()

    exec(source, namespace)
    model = namespace['Module_uuid_demoModel'].model_validate({'id': database_id, 'title': '编辑详情'})

    assert 'from uuid import UUID' in source
    assert 'id: Optional[UUID]' in source
    assert model.id == database_id
    assert model.model_dump(mode='json', by_alias=True)['id'] == str(database_id)
    compile(source, '<generated-vo>', 'exec')


def test_dao_add_template_omits_none_values_on_insert():
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
                columnName='string_value',
                columnType='varchar(100)',
                pythonField='stringValue',
                pythonType='str',
                columnComment='字符串-varchar',
                isInsert='1',
            ),
            GenTableColumnModel(
                columnName='time_tz_value',
                columnType='time with time zone',
                pythonField='timeTzValue',
                pythonType='time',
                columnComment='带时区时间-time with time zone',
                isInsert='1',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    source = TemplateInitializer.init_jinja2().get_template('python/dao.py.jinja2').render(**context)

    assert 'model_dump(exclude_none=True, exclude={' in source
    compile(source, '<generated-dao>', 'exec')


def test_generated_code_normalizes_empty_containers_for_scalar_fields_before_insert():
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
                columnName='string_value',
                columnType='varchar(100)',
                pythonField='stringValue',
                pythonType='str',
                columnComment='字符串-varchar',
                isInsert='1',
                isRequired='1',
            ),
            GenTableColumnModel(
                columnName='jsonpath_value',
                columnType='jsonpath',
                pythonField='jsonpathValue',
                pythonType='str',
                htmlType='',
                columnComment='JSON路径-jsonpath',
                isInsert='1',
            ),
            GenTableColumnModel(
                columnName='bit_value',
                columnType='bit',
                pythonField='bitValue',
                pythonType='str',
                htmlType='',
                columnComment='固定长度位-bit',
                isInsert='1',
            ),
            GenTableColumnModel(
                columnName='string_array_value',
                columnType='_varchar',
                pythonField='stringArrayValue',
                pythonType='list',
                htmlType='',
                columnComment='字符串数组-array/varchar',
                isInsert='1',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    env = TemplateInitializer.init_jinja2()
    vo_source = env.get_template('python/vo.py.jinja2').render(**context)
    dao_source = env.get_template('python/dao.py.jinja2').render(**context)
    vue_source = env.get_template('vue/v3/index.vue.jinja2').render(**context)

    namespace = {}
    exec(vo_source, namespace)
    model = namespace['Module_demoModel'].model_validate(
        {
            'stringValue': 'demo',
            'jsonpathValue': [],
            'bitValue': {},
            'stringArrayValue': [],
        }
    )

    assert model.jsonpath_value is None
    assert model.bit_value is None
    assert model.string_array_value == []
    assert '@model_validator(mode=\'before\')' in vo_source
    assert "'jsonpath_value': 'jsonpathValue'" in vo_source
    assert "'bit_value': 'bitValue'" in vo_source
    assert "'string_array_value': 'stringArrayValue'" not in vo_source
    assert 'normalize_empty_values(' in dao_source
    assert "'jsonpath_value'" in dao_source
    assert "'bit_value'" in dao_source
    assert "'string_array_value'" not in dao_source
    assert 'isEmptyGeneratedValue(payload[field])' in vue_source


def test_service_template_revalidates_payload_to_apply_generated_empty_value_normalization():
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
                columnName='string_value',
                columnType='varchar(100)',
                pythonField='stringValue',
                pythonType='str',
                columnComment='字符串-varchar',
                isInsert='1',
                isRequired='1',
            ),
            GenTableColumnModel(
                columnName='jsonpath_value',
                columnType='jsonpath',
                pythonField='jsonpathValue',
                pythonType='str',
                columnComment='JSON路径-jsonpath',
                isInsert='1',
                isEdit='1',
            ),
        ],
    )
    table.pk_column = table.columns[0]

    context = TemplateUtils.prepare_context(table)
    service_source = TemplateInitializer.init_jinja2().get_template('python/service.py.jinja2').render(**context)

    assert 'page_object = Module_demoModel.model_validate(page_object.model_dump())' in service_source
    compile(service_source, '<generated-service>', 'exec')
