import asyncio
import sys
from pathlib import Path

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


class FakeSession:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True


def run_async(coro):
    return asyncio.run(coro)


def use_dev_env(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0], '--env', 'dev'])


def test_active_schema_tables_match_migration_contract():
    from module_admin.api_testing.schema_models.entity.do.schema_models_do import SchemaModel
    from module_admin.api_testing.schema_nodes.entity.do.schema_nodes_do import SchemaNode

    for table in (SchemaModel.__table__, SchemaNode.__table__):
        for column_name in ('create_by', 'create_time', 'update_by', 'update_time', 'remark', 'description', 'del_flag'):
            assert column_name in table.c, f'{table.name} should map migration column {column_name}'
        assert table.c.del_flag.default is not None
        assert table.c.del_flag.default.arg == '0'


def test_model_update_uses_optimistic_version_and_returns_next_version(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_models.dao.schema_models_dao import Schema_modelsDao
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService

    session = FakeSession()
    captured = {}

    async def fake_detail(cls, query_db, model_id):
        return Schema_modelsModel(
            modelId=model_id,
            projectId=1,
            name='Order',
            title='Order',
            visibility='project',
            status='draft',
            version=2,
            sourceType='manual',
        )

    async def fake_edit(cls, query_db, payload):
        captured['payload'] = payload

    monkeypatch.setattr(Schema_modelsService, 'schema_models_detail_services', classmethod(fake_detail))
    monkeypatch.setattr(Schema_modelsDao, 'edit_schema_models_dao', classmethod(fake_edit))

    result = run_async(
        Schema_modelsService.edit_schema_models_services(
            session,
            Schema_modelsModel(
                modelId='schema_order',
                projectId=1,
                name='Order',
                title='Order',
                visibility='project',
                status='draft',
                version=2,
                sourceType='manual',
            ),
        )
    )

    assert session.committed is True
    assert captured['payload']['version'] == 3
    assert result.result['modelId'] == 'schema_order'
    assert result.result['version'] == 3


def test_model_update_rejects_stale_version(monkeypatch):
    use_dev_env(monkeypatch)
    from exceptions.exception import ServiceException
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService

    session = FakeSession()

    async def fake_detail(cls, query_db, model_id):
        return Schema_modelsModel(
            modelId=model_id,
            projectId=1,
            name='Order',
            title='Order',
            visibility='project',
            status='draft',
            version=3,
            sourceType='manual',
        )

    monkeypatch.setattr(Schema_modelsService, 'schema_models_detail_services', classmethod(fake_detail))

    with pytest.raises(ServiceException) as exc_info:
        run_async(
            Schema_modelsService.edit_schema_models_services(
                session,
                Schema_modelsModel(
                    modelId='schema_order',
                    projectId=1,
                    name='Order',
                    title='Order',
                    visibility='project',
                    status='draft',
                    version=2,
                    sourceType='manual',
                ),
            )
        )

    assert exc_info.value.message == '模型已被更新，请刷新后重试'
    assert session.committed is False


def test_model_keyword_filter_searches_name_display_name_and_title(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_models.dao.schema_models_dao import build_model_keyword_filter
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsPageQueryModel

    empty_filter = build_model_keyword_filter(Schema_modelsPageQueryModel())
    keyword_filter = build_model_keyword_filter(Schema_modelsPageQueryModel(name='UserProfile'))
    compiled = str(keyword_filter)

    assert empty_filter is True
    assert 'schema_models.name LIKE' in compiled
    assert 'schema_models.display_name LIKE' in compiled
    assert 'schema_models.title LIKE' in compiled


def test_add_and_edit_services_return_saved_data(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_nodes.dao.schema_nodes_dao import Schema_nodesDao
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel
    from module_admin.api_testing.schema_nodes.service.schema_nodes_service import Schema_nodesService

    session = FakeSession()

    async def fake_add(cls, query_db, node):
        return node

    async def fake_detail(cls, query_db, node_id):
        return Schema_nodesModel(
            nodeId=node_id,
            modelId='schema_order',
            nodeKind='property',
            fieldName='id',
            type='integer',
            nullable=False,
            required=True,
            deprecated=False,
            accessMode='readWrite',
            enumEnabled=False,
            constEnabled=False,
            mockEnabled=False,
            level=1,
            sortNo=1,
        )

    async def fake_edit(cls, query_db, payload):
        return None

    monkeypatch.setattr(Schema_nodesDao, 'add_schema_nodes_dao', classmethod(fake_add))
    monkeypatch.setattr(Schema_nodesDao, 'edit_schema_nodes_dao', classmethod(fake_edit))
    monkeypatch.setattr(Schema_nodesService, 'schema_nodes_detail_services', classmethod(fake_detail))

    node = Schema_nodesModel(
        nodeId='node_order_id',
        modelId='schema_order',
        nodeKind='property',
        fieldName='id',
        type='integer',
        nullable=False,
        required=True,
        deprecated=False,
        accessMode='readWrite',
        enumEnabled=False,
        constEnabled=False,
        mockEnabled=False,
        level=1,
        sortNo=1,
    )

    add_result = run_async(Schema_nodesService.add_schema_nodes_services(session, node))
    edit_result = run_async(Schema_nodesService.edit_schema_nodes_services(session, node))

    assert add_result.result['nodeId'] == 'node_order_id'
    assert edit_result.result['nodeId'] == 'node_order_id'
