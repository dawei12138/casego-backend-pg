import asyncio
import importlib
import os
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 将项目根目录添加到 sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 导入 SQLAlchemy Base
from config.base import Base
from utils.pg_enum_autogen import (
    append_pg_enum_sync_operations,
    collect_python_enum_classes,
    discover_generated_enum_modules,
)


SCAN_DIRS = ['module_admin', 'module_task', 'module_generator', 'module_app', 'module_llm']
FIXED_ENUM_MODULES = ['config.enums']


def import_all_enum_modules():
    """
    动态扫描并导入所有需要参与PostgreSQL enum迁移比对的枚举文件。
    """
    module_paths = list(FIXED_ENUM_MODULES)
    module_paths.extend(discover_generated_enum_modules(PROJECT_ROOT, SCAN_DIRS))

    imported_modules = []
    for module_path in module_paths:
        try:
            print(f"[IMPORTING ENUM] {module_path}")
            imported_modules.append(importlib.import_module(module_path))
            print(f"[OK ENUM] {module_path}")
        except Exception as e:
            print(f"[FAILED ENUM] {module_path}: {e}")
    return imported_modules


def import_all_do_models():
    """
    动态扫描并导入所有 DO 模型文件
    """
    for scan_dir in SCAN_DIRS:
        scan_path = PROJECT_ROOT / scan_dir
        if not scan_path.exists():
            continue

        print(f"[SCAN DIR] {scan_dir}")

        for do_file in scan_path.rglob('*_do.py'):
            relative_path = do_file.relative_to(PROJECT_ROOT)
            module_path = str(relative_path.with_suffix('')).replace(os.sep, '.')

            try:
                print(f"[IMPORTING] {module_path}")
                importlib.import_module(module_path)
                print(f"[OK] {module_path}")
            except Exception as e:
                print(f"[FAILED] {module_path}: {e}")


# 动态导入所有枚举与 DO 模型
IMPORTED_ENUM_MODULES = import_all_enum_modules()
ENUM_CLASS_OVERRIDES = collect_python_enum_classes(IMPORTED_ENUM_MODULES)
import_all_do_models()
print("模型扫描完成")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 设置 target_metadata 为 Base.metadata
target_metadata = Base.metadata

# 需要排除的表（这些表由外部库管理，没有对应的 DO 模型）
EXCLUDE_TABLES = {
    'checkpoint_blobs',
    'checkpoint_writes',
    'checkpoints',
    'checkpoint_migrations',
}


def include_object(object, name, type_, reflected, compare_to):
    """
    过滤函数：决定哪些对象应该被 Alembic 迁移管理
    返回 False 表示排除该对象
    """
    if type_ == "table" and name in EXCLUDE_TABLES:
        return False
    return True


def process_revision_directives(migration_context, revision, directives):
    """
    在 Alembic autogenerate 阶段补充PostgreSQL enum value的新增/删除迁移SQL。
    """
    cmd_opts = getattr(config, 'cmd_opts', None)
    append_pg_enum_sync_operations(
        connection=migration_context.connection,
        metadata=target_metadata,
        directives=directives,
        is_autogenerate=bool(getattr(cmd_opts, 'autogenerate', False)),
        enum_class_overrides=ENUM_CLASS_OVERRIDES,
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_object=include_object,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine.

    In this scenario we need to create an async Engine
    and associate a connection with the context.

    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
