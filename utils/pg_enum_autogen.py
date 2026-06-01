import enum
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

import sqlalchemy as sa
from sqlalchemy import Enum as SAEnum


@dataclass(frozen=True)
class EnumDefinition:
    name: str
    labels: Tuple[str, ...]
    requires_explicit_create: bool = False


@dataclass(frozen=True)
class EnumColumn:
    schema: Optional[str]
    table_name: str
    column_name: str


def discover_generated_enum_modules(project_root: Path, scan_dirs: Sequence[str]) -> List[str]:
    """
    Discover code-generator enum modules using the same top-level scan dirs as model discovery.
    """
    modules = []
    project_root = Path(project_root)
    for scan_dir in scan_dirs:
        scan_path = project_root / scan_dir
        if not scan_path.exists():
            continue
        for enum_file in scan_path.rglob('*enum.py'):
            if '__pycache__' in enum_file.parts:
                continue
            relative_path = enum_file.relative_to(project_root)
            modules.append('.'.join(relative_path.with_suffix('').parts))
    return sorted(modules)


def import_enum_modules(
    project_root: Path,
    scan_dirs: Sequence[str],
    fixed_modules: Sequence[str] = ('config.enums',),
) -> Dict[str, object]:
    project_root = Path(project_root)
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    imported_modules = {}
    module_names = list(fixed_modules) + discover_generated_enum_modules(project_root, scan_dirs)
    for module_name in module_names:
        imported_modules[module_name] = importlib.import_module(module_name)
    return imported_modules


def collect_python_enum_classes(enum_modules: Iterable[object]) -> Dict[str, enum.EnumMeta]:
    enum_classes: Dict[str, enum.EnumMeta] = {}
    for enum_module in enum_modules:
        for value in vars(enum_module).values():
            if isinstance(value, enum.EnumMeta) and value.__module__ == enum_module.__name__:
                enum_classes[value.__name__] = value
    return enum_classes


def collect_metadata_enum_definitions(
    metadata: sa.MetaData,
    enum_class_overrides: Optional[Mapping[str, enum.EnumMeta]] = None,
) -> Dict[str, EnumDefinition]:
    enum_definitions: Dict[str, EnumDefinition] = {}
    enum_class_overrides = enum_class_overrides or {}

    for table in metadata.tables.values():
        for column in table.columns:
            for enum_type in _iter_enum_types(column.type):
                if not enum_type.name:
                    continue
                labels = _resolve_enum_labels(enum_type, enum_class_overrides)
                requires_explicit_create = getattr(enum_type, 'create_type', None) is False
                current_definition = enum_definitions.get(enum_type.name)
                if current_definition is None:
                    enum_definitions[enum_type.name] = EnumDefinition(
                        name=enum_type.name,
                        labels=labels,
                        requires_explicit_create=requires_explicit_create,
                    )
                    continue

                if current_definition.labels != labels:
                    raise ValueError(
                        f'Conflicting labels for PostgreSQL enum {enum_type.name}: '
                        f'{current_definition.labels} != {labels}'
                    )
                if requires_explicit_create and not current_definition.requires_explicit_create:
                    enum_definitions[enum_type.name] = EnumDefinition(
                        name=enum_type.name,
                        labels=current_definition.labels,
                        requires_explicit_create=True,
                    )

    return enum_definitions


def collect_add_column_enum_type_names(directives: Sequence[object]) -> Set[str]:
    enum_type_names: Set[str] = set()
    for directive in directives:
        upgrade_ops = getattr(directive, 'upgrade_ops', None)
        for operation in _iter_operations(getattr(upgrade_ops, 'ops', ())):
            column = getattr(operation, 'column', None)
            if not isinstance(column, sa.Column):
                continue
            for enum_type in _iter_enum_types(column.type):
                if enum_type.name and getattr(enum_type, 'native_enum', True):
                    enum_type_names.add(enum_type.name)
    return enum_type_names


def fetch_database_enum_definitions(connection: sa.Connection) -> Dict[str, Tuple[str, ...]]:
    result = connection.execute(
        sa.text(
            """
            SELECT t.typname AS enum_name, array_agg(e.enumlabel ORDER BY e.enumsortorder) AS enum_labels
            FROM pg_type t
            JOIN pg_enum e ON e.enumtypid = t.oid
            JOIN pg_namespace n ON n.oid = t.typnamespace
            WHERE n.nspname = current_schema()
            GROUP BY t.typname
            """
        )
    )
    return {row.enum_name: tuple(row.enum_labels or []) for row in result}


def fetch_database_enum_columns(connection: sa.Connection) -> Dict[str, List[EnumColumn]]:
    result = connection.execute(
        sa.text(
            """
            SELECT
                t.typname AS enum_name,
                n.nspname AS schema_name,
                c.relname AS table_name,
                a.attname AS column_name
            FROM pg_type t
            JOIN pg_attribute a ON a.atttypid = t.oid
            JOIN pg_class c ON c.oid = a.attrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
            WHERE t.typtype = 'e'
              AND n.nspname = current_schema()
              AND a.attnum > 0
              AND NOT a.attisdropped
              AND c.relkind IN ('r', 'p')
            ORDER BY t.typname, n.nspname, c.relname, a.attname
            """
        )
    )
    enum_columns: Dict[str, List[EnumColumn]] = {}
    for row in result:
        enum_columns.setdefault(row.enum_name, []).append(
            EnumColumn(row.schema_name, row.table_name, row.column_name)
        )
    return enum_columns


def build_pg_enum_sync_sql(
    target_enums: Mapping[str, EnumDefinition],
    database_enums: Mapping[str, Sequence[str]],
    enum_columns: Mapping[str, Sequence[EnumColumn]],
    add_column_enum_type_names: Optional[Set[str]] = None,
) -> Tuple[List[str], List[str]]:
    upgrade_sql: List[str] = []
    downgrade_sql: List[str] = []
    add_column_enum_type_names = add_column_enum_type_names or set()

    for enum_name in sorted(target_enums):
        target_enum = target_enums[enum_name]
        target_labels = tuple(target_enum.labels)
        database_labels = tuple(database_enums.get(enum_name, ()))

        if enum_name not in database_enums:
            if target_enum.requires_explicit_create or enum_name in add_column_enum_type_names:
                upgrade_sql.append(_create_enum_type_sql(enum_name, target_labels))
                downgrade_sql.append(f'DROP TYPE IF EXISTS {_quote_identifier(enum_name)}')
            continue

        if database_labels == target_labels:
            continue

        removed_labels = [label for label in database_labels if label not in target_labels]
        order_changed = not _labels_keep_existing_order(database_labels, target_labels)
        columns = enum_columns.get(enum_name, ())
        if removed_labels or order_changed:
            upgrade_sql.extend(_recreate_enum_type_sql(enum_name, target_labels, columns))
            downgrade_sql.extend(_recreate_enum_type_sql(enum_name, database_labels, columns))
            continue

        upgrade_sql.extend(_add_missing_enum_value_sql(enum_name, database_labels, target_labels))
        downgrade_sql.extend(_recreate_enum_type_sql(enum_name, database_labels, columns))

    return upgrade_sql, downgrade_sql


def append_pg_enum_sync_operations(
    *,
    connection: sa.Connection,
    metadata: sa.MetaData,
    directives: Sequence[object],
    is_autogenerate: bool,
    enum_class_overrides: Optional[Mapping[str, enum.EnumMeta]] = None,
) -> None:
    if not is_autogenerate or not directives:
        return

    target_enums = collect_metadata_enum_definitions(metadata, enum_class_overrides)
    if not target_enums:
        return

    database_enums = fetch_database_enum_definitions(connection)
    enum_columns = fetch_database_enum_columns(connection)
    add_column_enum_type_names = collect_add_column_enum_type_names(directives)
    upgrade_sql, downgrade_sql = build_pg_enum_sync_sql(
        target_enums,
        database_enums,
        enum_columns,
        add_column_enum_type_names,
    )
    if not upgrade_sql and not downgrade_sql:
        return

    from alembic.operations import ops

    migration_script = directives[0]
    migration_script.upgrade_ops.ops[0:0] = [ops.ExecuteSQLOp(sql) for sql in upgrade_sql]
    migration_script.downgrade_ops.ops.extend(ops.ExecuteSQLOp(sql) for sql in downgrade_sql)


def _iter_operations(operations: Iterable[object]) -> Iterable[object]:
    for operation in operations:
        yield operation
        nested_operations = getattr(operation, 'ops', None)
        if nested_operations:
            yield from _iter_operations(nested_operations)


def _iter_enum_types(column_type: sa.types.TypeEngine) -> Iterable[SAEnum]:
    if isinstance(column_type, SAEnum):
        yield column_type
        return

    item_type = getattr(column_type, 'item_type', None)
    if item_type is not None:
        yield from _iter_enum_types(item_type)


def _resolve_enum_labels(
    enum_type: SAEnum,
    enum_class_overrides: Mapping[str, enum.EnumMeta],
) -> Tuple[str, ...]:
    labels = tuple(str(label) for label in enum_type.enums)
    enum_class = getattr(enum_type, 'enum_class', None)
    if enum_class is None:
        return labels

    override_class = enum_class_overrides.get(enum_class.__name__)
    if override_class is None or override_class is enum_class:
        return labels

    if _enum_type_uses_member_values(enum_type):
        return tuple(str(member.value) for member in override_class)
    return tuple(member.name for member in override_class)


def _enum_type_uses_member_values(enum_type: SAEnum) -> bool:
    enum_class = getattr(enum_type, 'enum_class', None)
    if enum_class is None:
        return False

    labels = tuple(str(label) for label in enum_type.enums)
    member_names = tuple(member.name for member in enum_class)
    member_values = tuple(str(member.value) for member in enum_class)
    if labels == member_values:
        return True
    if labels == member_names:
        return False

    name_match_count = sum(label in member_names for label in labels)
    value_match_count = sum(label in member_values for label in labels)
    return value_match_count > name_match_count


def _labels_keep_existing_order(database_labels: Sequence[str], target_labels: Sequence[str]) -> bool:
    target_positions = {label: index for index, label in enumerate(target_labels)}
    existing_positions = [target_positions[label] for label in database_labels if label in target_positions]
    return existing_positions == sorted(existing_positions)


def _add_missing_enum_value_sql(
    enum_name: str,
    database_labels: Sequence[str],
    target_labels: Sequence[str],
) -> List[str]:
    sql = []
    current_labels = list(database_labels)
    for target_index, label in enumerate(target_labels):
        if label in current_labels:
            continue

        before_label = next(
            (candidate for candidate in target_labels[target_index + 1:] if candidate in current_labels),
            None,
        )
        statement = f'ALTER TYPE {_quote_identifier(enum_name)} ADD VALUE IF NOT EXISTS {_quote_literal(label)}'
        if before_label is not None:
            statement += f' BEFORE {_quote_literal(before_label)}'
            current_labels.insert(current_labels.index(before_label), label)
        else:
            current_labels.append(label)
        sql.append(statement)
    return sql


def _recreate_enum_type_sql(
    enum_name: str,
    labels: Sequence[str],
    columns: Sequence[EnumColumn],
) -> List[str]:
    quoted_enum_name = _quote_identifier(enum_name)
    old_enum_name = f'{enum_name}_old'
    quoted_old_enum_name = _quote_identifier(old_enum_name)
    sql = [
        f'ALTER TYPE {quoted_enum_name} RENAME TO {quoted_old_enum_name}',
        _create_enum_type_sql(enum_name, labels),
    ]
    for column in columns:
        sql.append(
            f'ALTER TABLE {_quote_table_name(column)} ALTER COLUMN {_quote_identifier(column.column_name)} '
            f'TYPE {quoted_enum_name} USING {_quote_identifier(column.column_name)}::text::{quoted_enum_name}'
        )
    sql.append(f'DROP TYPE {quoted_old_enum_name}')
    return sql


def _create_enum_type_sql(enum_name: str, labels: Sequence[str]) -> str:
    return f'CREATE TYPE {_quote_identifier(enum_name)} AS ENUM ({_format_labels(labels)})'


def _format_labels(labels: Sequence[str]) -> str:
    return ', '.join(_quote_literal(label) for label in labels)


def _quote_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _quote_identifier(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _quote_table_name(column: EnumColumn) -> str:
    table_name = _quote_identifier(column.table_name)
    if not column.schema:
        return table_name
    return f'{_quote_identifier(column.schema)}.{table_name}'
