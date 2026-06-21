import re
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_preview_generator_builds_faker_example_and_schema(monkeypatch):
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel

    monkeypatch.setattr(
        SchemaModelPreviewService,
        '_call_faker_rule',
        staticmethod(lambda rule, args=None: {'get_email': 'tester@example.com', 'uuid': 'fixed-uuid'}.get(rule)),
    )

    root = Schema_nodesModel(
        nodeId='root',
        modelId='schema_order',
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
    )
    nodes = [
        root,
        Schema_nodesModel(
            nodeId='order_id',
            modelId='schema_order',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='orderId',
            type='string',
            nullable=False,
            required=True,
            deprecated=False,
            accessMode='readWrite',
            format='uuid',
            mockEnabled=True,
            mockRule='uuid',
            enumEnabled=False,
            constEnabled=False,
            level=1,
            sortNo=1,
        ),
        Schema_nodesModel(
            nodeId='email',
            modelId='schema_order',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='email',
            type='string',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            format='email',
            mockEnabled=True,
            mockRule='get_email',
            enumEnabled=False,
            constEnabled=False,
            level=1,
            sortNo=2,
        ),
        Schema_nodesModel(
            nodeId='amount',
            modelId='schema_order',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='amount',
            type='number',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            mockEnabled=True,
            mockRule='number.float',
            enumEnabled=False,
            constEnabled=False,
            level=1,
            sortNo=3,
        ),
        Schema_nodesModel(
            nodeId='items',
            modelId='schema_order',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='items',
            type='array',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            mockEnabled=False,
            enumEnabled=False,
            constEnabled=False,
            level=1,
            sortNo=4,
        ),
        Schema_nodesModel(
            nodeId='items_value',
            modelId='schema_order',
            parentId='items',
            rootId='root',
            nodeKind='items',
            type='integer',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            mockEnabled=True,
            mockRule='number.int',
            enumEnabled=False,
            constEnabled=False,
            level=2,
            sortNo=1,
        ),
    ]

    result = SchemaModelPreviewService.build_preview(
        Schema_modelsModel(modelId='schema_order', title='Order', schemaDraft='draft-07'),
        nodes,
    )

    assert result.example['orderId'] == 'fixed-uuid'
    assert result.example['email'] == 'tester@example.com'
    assert isinstance(result.example['amount'], float)
    assert isinstance(result.example['items'][0], int)
    assert result.json_schema['properties']['orderId']['format'] == 'uuid'
    assert result.json_schema['required'] == ['orderId']


def test_preview_generator_prefers_fixed_values_and_resolves_referenced_models():
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel

    current_nodes = [
        Schema_nodesModel(
            nodeId='root',
            modelId='schema_profile',
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
            nodeId='user_ref',
            modelId='schema_profile',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='user',
            type='object',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            refConfig={'modelId': 'schema_user'},
            enumEnabled=False,
            constEnabled=False,
            mockEnabled=False,
            level=1,
            sortNo=1,
        ),
    ]
    referenced_nodes = [
        Schema_nodesModel(
            nodeId='user_root',
            modelId='schema_user',
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
            nodeId='user_name',
            modelId='schema_user',
            parentId='user_root',
            rootId='user_root',
            nodeKind='property',
            fieldName='name',
            type='string',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            mockValue='张三',
            enumEnabled=False,
            constEnabled=False,
            mockEnabled=True,
            level=1,
            sortNo=1,
        ),
        Schema_nodesModel(
            nodeId='user_status',
            modelId='schema_user',
            parentId='user_root',
            rootId='user_root',
            nodeKind='property',
            fieldName='status',
            type='string',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            enumEnabled=True,
            enumValues=['enabled', 'disabled'],
            constEnabled=False,
            mockEnabled=False,
            level=1,
            sortNo=2,
        ),
    ]

    result = SchemaModelPreviewService.build_preview(
        Schema_modelsModel(modelId='schema_profile', title='Profile', schemaDraft='draft-07'),
        current_nodes,
        ref_node_map={'schema_user': referenced_nodes},
    )

    assert result.example['user'] == {'name': '张三', 'status': 'enabled'}
    assert result.json_schema['properties']['user']['x-ref-model-id'] == 'schema_user'
    assert not result.warnings


def test_preview_generator_uses_type_and_format_defaults_without_empty_placeholders():
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel

    nodes = [
        Schema_nodesModel(
            nodeId='root',
            modelId='schema_user',
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
            nodeId='email',
            modelId='schema_user',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='email',
            type='string',
            format='email',
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
        Schema_nodesModel(
            nodeId='created_at',
            modelId='schema_user',
            parentId='root',
            rootId='root',
            nodeKind='property',
            fieldName='createdAt',
            type='string',
            format='date-time',
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            enumEnabled=False,
            constEnabled=False,
            mockEnabled=False,
            level=1,
            sortNo=2,
        ),
    ]

    result = SchemaModelPreviewService.build_preview(Schema_modelsModel(modelId='schema_user'), nodes)

    assert re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', result.example['email'])
    assert result.example['createdAt']
    assert result.example['createdAt'] != ''


def test_preview_generator_keeps_object_and_array_children_when_container_has_mock_rule(monkeypatch):
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel

    monkeypatch.setattr(
        SchemaModelPreviewService,
        '_call_faker_rule',
        staticmethod(lambda rule, args=None: 'container-scalar'),
    )

    def node(node_id, parent_id, node_kind, field_name, node_type, *, mock_rule=None, example=None, level=1, sort_no=1):
        return Schema_nodesModel(
            nodeId=node_id,
            modelId='schema_order_result',
            parentId=parent_id,
            rootId='root',
            nodeKind=node_kind,
            fieldName=field_name,
            type=node_type,
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            exampleValue=example,
            enumEnabled=False,
            constEnabled=False,
            mockEnabled=bool(mock_rule),
            mockRule=mock_rule,
            level=level,
            sortNo=sort_no,
        )

    nodes = [
        node('root', None, 'root', None, 'object', level=0, sort_no=0),
        node('amount', 'root', 'property', 'amount', 'object', mock_rule='$string', example='由子', level=1, sort_no=1),
        node('amount_text', 'amount', 'property', 'amountText', 'string', example='金额说明', level=2, sort_no=1),
        node('amount_value', 'amount', 'property', 'value', 'number', example=12.35, level=2, sort_no=2),
        node('lines', 'root', 'property', 'lines', 'array', mock_rule='$string', example='错误数组占位', level=1, sort_no=2),
        node('line_item', 'lines', 'items', None, 'object', mock_rule='$string', example='错误对象占位', level=2, sort_no=1),
        node('line_name', 'line_item', 'property', 'name', 'string', example='商品A', level=3, sort_no=1),
        node('line_count', 'line_item', 'property', 'count', 'integer', example=2, level=3, sort_no=2),
    ]

    result = SchemaModelPreviewService.build_preview(
        Schema_modelsModel(modelId='schema_order_result', title='OrderResult', schemaDraft='draft-07'),
        nodes,
    )

    assert result.example['amount'] == {'amountText': '金额说明', 'value': 12.35}
    assert result.example['lines'] == [{'name': '商品A', 'count': 2}]
    assert set(result.json_schema['properties']['amount']['properties'].keys()) == {'amountText', 'value'}
    assert set(result.json_schema['properties']['lines']['items']['properties'].keys()) == {'name', 'count'}


def test_preview_generator_outputs_apifox_orders_any_and_composition():
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel

    def node(node_id, parent_id, node_kind, field_name, node_type, *, sort_no=1, type_list=None):
        return Schema_nodesModel(
            nodeId=node_id,
            modelId='schema_probe',
            parentId=parent_id,
            rootId='root',
            nodeKind=node_kind,
            fieldName=field_name,
            type=node_type,
            typeList=type_list,
            nullable=False,
            required=False,
            deprecated=False,
            accessMode='readWrite',
            enumEnabled=False,
            constEnabled=False,
            mockEnabled=False,
            level=0 if node_id == 'root' else 1,
            sortNo=sort_no,
        )

    nodes = [
        node('root', None, 'root', None, 'object', sort_no=0),
        node('second', 'root', 'property', 'second', 'string', sort_no=2),
        node(
            'any_value',
            'root',
            'property',
            'anyValue',
            'any',
            sort_no=3,
            type_list=['string', 'integer', 'boolean', 'array', 'object', 'number', 'null'],
        ),
        node('mixed', 'root', 'property', 'mixed', 'oneOf', sort_no=4),
        node('mixed_0', 'mixed', 'composition', '0', 'string', sort_no=0),
        node('mixed_1', 'mixed', 'composition', '1', 'integer', sort_no=1),
        node('first', 'root', 'property', 'first', 'integer', sort_no=1),
    ]

    result = SchemaModelPreviewService.build_preview(Schema_modelsModel(modelId='schema_probe'), nodes)
    schema = result.json_schema

    assert schema['x-apifox-orders'] == ['first', 'second', 'anyValue', 'mixed']
    assert schema['properties']['anyValue']['type'] == [
        'string',
        'integer',
        'boolean',
        'array',
        'object',
        'number',
        'null',
    ]
    assert schema['properties']['mixed']['oneOf'] == [{'type': 'string'}, {'type': 'integer'}]
