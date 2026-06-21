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


def test_model_copy_clones_model_and_nodes(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_models.dao.schema_models_dao import Schema_modelsDao
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import (
        SchemaModelCopyRequestModel,
        Schema_modelsModel,
    )
    from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService
    from module_admin.api_testing.schema_nodes.dao.schema_nodes_dao import Schema_nodesDao
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel, Schema_nodesPageQueryModel

    session = FakeSession()
    captured = {'models': [], 'nodes': []}

    async def fake_detail(cls, query_db, model_id):
        return Schema_modelsModel(
            modelId=model_id,
            projectId=1,
            groupId='group_old',
            name='Order',
            displayName='订单',
            title='Order',
            visibility='project',
            status='draft',
            version=2,
            sourceType='manual',
            rootNodeId='root_old',
        )

    async def fake_nodes(cls, query_db, query_object: Schema_nodesPageQueryModel, is_page=False):
        return [
            Schema_nodesModel(
                nodeId='root_old',
                modelId=query_object.model_id,
                nodeKind='root',
                type='object',
                nullable=False,
                required=False,
                deprecated=False,
                accessMode='readWrite',
                enumEnabled=False,
                constEnabled=False,
                mockEnabled=False,
                level=0,
                sortNo=0,
            ),
            Schema_nodesModel(
                nodeId='field_old',
                modelId=query_object.model_id,
                parentId='root_old',
                rootId='root_old',
                nodeKind='property',
                fieldName='id',
                type='string',
                nullable=False,
                required=True,
                deprecated=False,
                accessMode='readWrite',
                enumEnabled=False,
                constEnabled=False,
                mockEnabled=False,
                level=1,
                sortNo=1,
            ),
        ]

    async def fake_add_model(cls, query_db, model):
        captured['models'].append(model)

    async def fake_add_node(cls, query_db, node):
        captured['nodes'].append(node)

    monkeypatch.setattr(Schema_modelsService, 'schema_models_detail_services', classmethod(fake_detail))
    monkeypatch.setattr(Schema_nodesDao, 'get_schema_nodes_list', classmethod(fake_nodes))
    monkeypatch.setattr(Schema_modelsDao, 'add_schema_models_dao', classmethod(fake_add_model))
    monkeypatch.setattr(Schema_nodesDao, 'add_schema_nodes_dao', classmethod(fake_add_node))

    result = run_async(
        Schema_modelsService.copy_schema_model_services(
            session,
            SchemaModelCopyRequestModel(
                modelId='schema_order',
                targetGroupId='group_new',
                name='OrderCopy',
                displayName='订单副本',
            ),
        )
    )

    assert session.committed is True
    assert result.result['modelId'] != 'schema_order'
    assert captured['models'][0].group_id == 'group_new'
    assert captured['models'][0].name == 'OrderCopy'
    assert len(captured['nodes']) == 2
    assert captured['nodes'][0].node_id != 'root_old'
    assert captured['nodes'][1].parent_id == captured['nodes'][0].node_id


def test_model_move_updates_group_without_touching_nodes(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_models.dao.schema_models_dao import Schema_modelsDao
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import (
        SchemaModelMoveRequestModel,
        Schema_modelsModel,
    )
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
        Schema_modelsService.move_schema_model_services(
            session,
            SchemaModelMoveRequestModel(modelId='schema_order', targetGroupId='group_target'),
        )
    )

    assert session.committed is True
    assert captured['payload']['model_id'] == 'schema_order'
    assert captured['payload']['group_id'] == 'group_target'
    assert captured['payload']['version'] == 3
    assert result.result['groupId'] == 'group_target'


def test_model_delete_soft_deletes_visual_nodes(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_models.dao.schema_models_dao import Schema_modelsDao
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import DeleteSchema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService
    from module_admin.api_testing.schema_nodes.dao.schema_nodes_dao import Schema_nodesDao

    session = FakeSession()
    captured = {'models': [], 'node_models': []}

    async def fake_delete_model(cls, query_db, model):
        captured['models'].append(model.model_id)

    async def fake_delete_nodes_by_model(cls, query_db, model_id):
        captured['node_models'].append(model_id)

    monkeypatch.setattr(Schema_modelsDao, 'delete_schema_models_dao', classmethod(fake_delete_model))
    monkeypatch.setattr(Schema_nodesDao, 'delete_schema_nodes_by_model_id_dao', classmethod(fake_delete_nodes_by_model))

    result = run_async(
        Schema_modelsService.delete_schema_models_services(
            session,
            DeleteSchema_modelsModel(modelIds='schema_order,schema_user'),
        )
    )

    assert session.committed is True
    assert result.message == '删除成功'
    assert captured['models'] == ['schema_order', 'schema_user']
    assert captured['node_models'] == ['schema_order', 'schema_user']


def test_copy_to_branch_requires_target_branch(monkeypatch):
    use_dev_env(monkeypatch)
    from exceptions.exception import ServiceException
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import SchemaModelCopyRequestModel
    from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService

    session = FakeSession()

    with pytest.raises(ServiceException) as exc_info:
        run_async(
            Schema_modelsService.copy_schema_model_services(
                session,
                SchemaModelCopyRequestModel(modelId='schema_order'),
                require_target_branch=True,
            )
        )

    assert exc_info.value.message == '目标分支不能为空'
    assert session.committed is False


def test_property_node_requires_field_name_before_persist(monkeypatch):
    use_dev_env(monkeypatch)
    from exceptions.exception import ServiceException
    from module_admin.api_testing.schema_nodes.dao.schema_nodes_dao import Schema_nodesDao
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel
    from module_admin.api_testing.schema_nodes.service.schema_nodes_service import Schema_nodesService

    session = FakeSession()
    captured = {'added': False}

    async def fake_add(cls, query_db, node):
        captured['added'] = True

    monkeypatch.setattr(Schema_nodesDao, 'add_schema_nodes_dao', classmethod(fake_add))

    with pytest.raises(ServiceException) as exc_info:
        run_async(
            Schema_nodesService.add_schema_nodes_services(
                session,
                Schema_nodesModel(
                    nodeId='unnamed',
                    modelId='schema_order',
                    parentId='root',
                    rootId='root',
                    nodeKind='property',
                    fieldName='',
                    type='string',
                    nullable=False,
                    required=False,
                    deprecated=False,
                    accessMode='readWrite',
                    enumEnabled=False,
                    constEnabled=False,
                    mockEnabled=False,
                    level=1,
                    sortNo=1,
                ),
            )
        )

    assert exc_info.value.message == '字段名不能为空'
    assert captured['added'] is False
    assert session.committed is False


def test_schema_model_group_service_crud_contract(monkeypatch):
    use_dev_env(monkeypatch)
    from module_admin.api_testing.schema_model_groups.dao.schema_model_groups_dao import Schema_model_groupsDao
    from module_admin.api_testing.schema_model_groups.entity.vo.schema_model_groups_vo import Schema_model_groupsModel
    from module_admin.api_testing.schema_model_groups.service.schema_model_groups_service import Schema_model_groupsService

    session = FakeSession()
    captured = {}

    async def fake_add(cls, query_db, group):
        captured['add'] = group

    async def fake_detail(cls, query_db, group_id):
        return Schema_model_groupsModel(
            groupId=group_id,
            projectId=1,
            branchId='main',
            parentId=None,
            name='默认目录',
            sortNo=1,
            delFlag='0',
        )

    async def fake_edit(cls, query_db, payload):
        captured['edit'] = payload

    monkeypatch.setattr(Schema_model_groupsDao, 'add_schema_model_groups_dao', classmethod(fake_add))
    monkeypatch.setattr(Schema_model_groupsDao, 'get_schema_model_groups_detail_by_id', classmethod(fake_detail))
    monkeypatch.setattr(Schema_model_groupsDao, 'edit_schema_model_groups_dao', classmethod(fake_edit))

    group = Schema_model_groupsModel(groupId='group_default', projectId=1, branchId='main', name='默认目录', sortNo=1)
    add_result = run_async(Schema_model_groupsService.add_schema_model_groups_services(session, group))
    edit_result = run_async(
        Schema_model_groupsService.edit_schema_model_groups_services(
            session,
            Schema_model_groupsModel(groupId='group_default', projectId=1, branchId='main', name='接口响应', sortNo=2),
        )
    )

    assert add_result.result['groupId'] == 'group_default'
    assert edit_result.result['name'] == '接口响应'
    assert captured['add'].name == '默认目录'
    assert captured['edit']['group_id'] == 'group_default'


def test_generate_schema_model_from_json_and_reports_unsupported_sources(monkeypatch):
    use_dev_env(monkeypatch)
    from exceptions.exception import ServiceException
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import SchemaModelGenerateRequestModel
    from module_admin.api_testing.schema_models.service.schema_models_service import Schema_modelsService

    result = Schema_modelsService.generate_schema_model_services(
        SchemaModelGenerateRequestModel(
            sourceType='JSON',
            content={
                'id': 1,
                'name': 'Alice',
                'roles': ['admin', 'user'],
                'profile': {'enabled': True},
            },
        )
    )

    assert result.json_schema['type'] == 'object'
    assert result.json_schema['x-apifox-orders'] == ['id', 'name', 'roles', 'profile']
    assert result.json_schema['properties']['id']['type'] == 'integer'
    assert result.json_schema['properties']['roles']['items']['type'] == 'string'
    assert [node.field_name for node in result.nodes if node.node_kind == 'property' and node.parent_id == 'root'] == [
        'id',
        'name',
        'roles',
        'profile',
    ]

    with pytest.raises(ServiceException) as exc_info:
        Schema_modelsService.generate_schema_model_services(
            SchemaModelGenerateRequestModel(sourceType='DATABASE', content='CREATE TABLE user_info(id bigint)')
        )

    assert exc_info.value.message == '从数据库导入开发中'
