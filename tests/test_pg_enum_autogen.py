import enum

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from utils.pg_enum_autogen import (
    EnumColumn,
    EnumDefinition,
    build_pg_enum_sync_sql,
    collect_add_column_enum_type_names,
    collect_metadata_enum_definitions,
    discover_generated_enum_modules,
)


class DemoStatusEnum(str, enum.Enum):
    DRAFT = 'draft'
    ACTIVE = 'active'
    TEST = 'test'


class GenericStatusEnum(str, enum.Enum):
    ENABLED = 'enabled'
    DISABLED = 'disabled'


GeneratedDemoStatusEnum = enum.Enum(
    'DemoStatusEnum',
    {
        'DRAFT': 'draft',
        'ACTIVE': 'active',
        'DISABLED': 'disabled',
        'TEST': 'test',
    },
    type=str,
)


StaleDemoStatusEnum = enum.Enum(
    'DemoStatusEnum',
    {
        'DRAFT': 'draft',
        'ACTIVE': 'active',
        'DISABLED': 'disabled',
    },
    type=str,
)


def test_collect_metadata_enums_marks_only_create_type_false_for_explicit_create():
    metadata = sa.MetaData()
    sa.Table(
        'module_demo_all_types',
        metadata,
        sa.Column(
            'enum_value',
            postgresql.ENUM(DemoStatusEnum, name='demo_status_enum', create_type=False),
        ),
        sa.Column(
            'generic_value',
            sa.Enum(GenericStatusEnum, name='GenericStatusEnum'),
        ),
    )

    enum_definitions = collect_metadata_enum_definitions(metadata)

    assert enum_definitions['demo_status_enum'].labels == ('DRAFT', 'ACTIVE', 'TEST')
    assert enum_definitions['demo_status_enum'].requires_explicit_create is True
    assert enum_definitions['GenericStatusEnum'].labels == ('ENABLED', 'DISABLED')
    assert enum_definitions['GenericStatusEnum'].requires_explicit_create is False


def test_collect_metadata_enums_prefers_scanned_enum_file_values_when_do_model_is_stale():
    metadata = sa.MetaData()
    sa.Table(
        'module_demo_all_types',
        metadata,
        sa.Column('enum_value', sa.Enum(StaleDemoStatusEnum, name='demo_status_enum')),
    )

    enum_definitions = collect_metadata_enum_definitions(
        metadata,
        {'DemoStatusEnum': GeneratedDemoStatusEnum},
    )

    assert enum_definitions['demo_status_enum'].labels == ('DRAFT', 'ACTIVE', 'DISABLED', 'TEST')


def test_build_pg_enum_sync_sql_adds_values_from_scanned_enum_file_when_do_model_is_stale():
    metadata = sa.MetaData()
    sa.Table(
        'module_demo_all_types',
        metadata,
        sa.Column('enum_value', sa.Enum(StaleDemoStatusEnum, name='demo_status_enum')),
    )
    enum_definitions = collect_metadata_enum_definitions(
        metadata,
        {'DemoStatusEnum': GeneratedDemoStatusEnum},
    )

    upgrade_sql, downgrade_sql = build_pg_enum_sync_sql(
        enum_definitions,
        {'demo_status_enum': ('DRAFT', 'ACTIVE', 'DISABLED')},
        {'demo_status_enum': [EnumColumn(None, 'module_demo_all_types', 'enum_value')]},
    )

    assert upgrade_sql == ['ALTER TYPE "demo_status_enum" ADD VALUE IF NOT EXISTS \'TEST\'']
    assert downgrade_sql == [
        'ALTER TYPE "demo_status_enum" RENAME TO "demo_status_enum_old"',
        'CREATE TYPE "demo_status_enum" AS ENUM (\'DRAFT\', \'ACTIVE\', \'DISABLED\')',
        (
            'ALTER TABLE "module_demo_all_types" ALTER COLUMN "enum_value" '
            'TYPE "demo_status_enum" USING "enum_value"::text::"demo_status_enum"'
        ),
        'DROP TYPE "demo_status_enum_old"',
    ]


def test_build_pg_enum_sync_sql_creates_only_generated_enum_types_without_init_conflict():
    metadata = sa.MetaData()
    sa.Table(
        'module_demo_all_types',
        metadata,
        sa.Column(
            'enum_value',
            postgresql.ENUM(DemoStatusEnum, name='demo_status_enum', create_type=False),
        ),
        sa.Column(
            'generic_value',
            sa.Enum(GenericStatusEnum, name='GenericStatusEnum'),
        ),
    )
    enum_definitions = collect_metadata_enum_definitions(metadata)

    upgrade_sql, downgrade_sql = build_pg_enum_sync_sql(enum_definitions, {}, {})

    assert 'CREATE TYPE "demo_status_enum" AS ENUM (\'DRAFT\', \'ACTIVE\', \'TEST\')' in upgrade_sql
    assert 'CREATE TYPE "GenericStatusEnum"' not in upgrade_sql
    assert 'DROP TYPE IF EXISTS "demo_status_enum"' in downgrade_sql
    assert 'DROP TYPE IF EXISTS "GenericStatusEnum"' not in downgrade_sql


def test_build_pg_enum_sync_sql_creates_enum_type_for_added_column():
    enum_definitions = {
        'module_uuid_demo_type_enum': EnumDefinition(
            name='module_uuid_demo_type_enum',
            labels=('normal', 'important', 'urgent'),
            requires_explicit_create=False,
        ),
    }

    upgrade_sql, downgrade_sql = build_pg_enum_sync_sql(
        enum_definitions,
        {},
        {},
        {'module_uuid_demo_type_enum'},
    )

    assert upgrade_sql == [
        'CREATE TYPE "module_uuid_demo_type_enum" AS ENUM (\'normal\', \'important\', \'urgent\')'
    ]
    assert downgrade_sql == ['DROP TYPE IF EXISTS "module_uuid_demo_type_enum"']


def test_collect_add_column_enum_type_names_ignores_create_table_enums():
    metadata = sa.MetaData()
    add_column = type(
        'AddColumnOp',
        (),
        {
            'column': sa.Column(
                'type',
                sa.Enum('normal', 'important', 'urgent', name='module_uuid_demo_type_enum'),
            )
        },
    )()
    create_table = type(
        'CreateTableOp',
        (),
        {
            'columns': [
                sa.Column(
                    'type',
                    sa.Enum('normal', 'important', 'urgent', name='create_table_enum'),
                )
            ]
        },
    )()
    upgrade_ops = type('UpgradeOps', (), {'ops': [create_table, add_column]})()
    directive = type('MigrationScript', (), {'upgrade_ops': upgrade_ops})()

    assert collect_add_column_enum_type_names([directive]) == {'module_uuid_demo_type_enum'}


def test_build_pg_enum_sync_sql_adds_missing_values_without_recreating_type():
    metadata = sa.MetaData()
    sa.Table(
        'module_demo_all_types',
        metadata,
        sa.Column(
            'enum_value',
            postgresql.ENUM(DemoStatusEnum, name='demo_status_enum', create_type=False),
        ),
    )
    enum_definitions = collect_metadata_enum_definitions(metadata)

    upgrade_sql, downgrade_sql = build_pg_enum_sync_sql(
        enum_definitions,
        {'demo_status_enum': ('DRAFT', 'ACTIVE')},
        {'demo_status_enum': [EnumColumn(None, 'module_demo_all_types', 'enum_value')]},
    )

    assert upgrade_sql == ['ALTER TYPE "demo_status_enum" ADD VALUE IF NOT EXISTS \'TEST\'']
    assert downgrade_sql == [
        'ALTER TYPE "demo_status_enum" RENAME TO "demo_status_enum_old"',
        'CREATE TYPE "demo_status_enum" AS ENUM (\'DRAFT\', \'ACTIVE\')',
        (
            'ALTER TABLE "module_demo_all_types" ALTER COLUMN "enum_value" '
            'TYPE "demo_status_enum" USING "enum_value"::text::"demo_status_enum"'
        ),
        'DROP TYPE "demo_status_enum_old"',
    ]


def test_build_pg_enum_sync_sql_recreates_type_when_values_are_removed():
    metadata = sa.MetaData()
    sa.Table(
        'module_demo_all_types',
        metadata,
        sa.Column(
            'enum_value',
            postgresql.ENUM(DemoStatusEnum, name='demo_status_enum', create_type=False),
        ),
    )
    enum_definitions = collect_metadata_enum_definitions(metadata)

    upgrade_sql, downgrade_sql = build_pg_enum_sync_sql(
        enum_definitions,
        {'demo_status_enum': ('DRAFT', 'ACTIVE', 'DISABLED')},
        {'demo_status_enum': [EnumColumn(None, 'module_demo_all_types', 'enum_value')]},
    )

    assert upgrade_sql == [
        'ALTER TYPE "demo_status_enum" RENAME TO "demo_status_enum_old"',
        'CREATE TYPE "demo_status_enum" AS ENUM (\'DRAFT\', \'ACTIVE\', \'TEST\')',
        (
            'ALTER TABLE "module_demo_all_types" ALTER COLUMN "enum_value" '
            'TYPE "demo_status_enum" USING "enum_value"::text::"demo_status_enum"'
        ),
        'DROP TYPE "demo_status_enum_old"',
    ]
    assert downgrade_sql == [
        'ALTER TYPE "demo_status_enum" RENAME TO "demo_status_enum_old"',
        'CREATE TYPE "demo_status_enum" AS ENUM (\'DRAFT\', \'ACTIVE\', \'DISABLED\')',
        (
            'ALTER TABLE "module_demo_all_types" ALTER COLUMN "enum_value" '
            'TYPE "demo_status_enum" USING "enum_value"::text::"demo_status_enum"'
        ),
        'DROP TYPE "demo_status_enum_old"',
    ]


def test_discover_generated_enum_modules_uses_existing_scan_dirs(tmp_path):
    enum_file = tmp_path / 'module_admin' / 'module_demo' / 'entity' / 'enums' / 'module_demo_enum.py'
    enum_file.parent.mkdir(parents=True)
    enum_file.write_text('import enum\n\nclass DemoStatusEnum(str, enum.Enum):\n    DRAFT = "draft"\n')
    ignored_file = tmp_path / 'module_admin' / 'module_demo' / 'entity' / 'vo' / 'module_demo_vo.py'
    ignored_file.parent.mkdir(parents=True, exist_ok=True)
    ignored_file.write_text('')

    assert discover_generated_enum_modules(tmp_path, ['module_admin']) == [
        'module_admin.module_demo.entity.enums.module_demo_enum'
    ]
