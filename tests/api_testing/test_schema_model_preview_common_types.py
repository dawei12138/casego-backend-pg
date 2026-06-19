import sys
from pathlib import Path

from jsonschema import Draft7Validator, validate

BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


COMMON_TYPE_JSON_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',
    'type': 'object',
    'title': 'CommonTypePreview',
    'required': [
        'id',
        'username',
        'email',
        'age',
        'score',
        'enabled',
        'status',
        'role',
        'nothing',
        'homepage',
        'createdAt',
        'profile',
        'tags',
        'orders',
    ],
    'properties': {
        'id': {'type': 'string', 'format': 'uuid'},
        'username': {'type': 'string', 'example': 'casego-user'},
        'email': {'type': 'string', 'format': 'email'},
        'age': {'type': 'integer', 'minimum': 0},
        'score': {'type': 'number'},
        'enabled': {'type': 'boolean'},
        'status': {'type': 'string', 'enum': ['active', 'disabled']},
        'role': {'type': 'string', 'const': 'admin'},
        'optionalNote': {'type': ['string', 'null']},
        'nothing': {'type': 'null'},
        'homepage': {'type': 'string', 'format': 'uri'},
        'createdAt': {'type': 'string', 'format': 'date-time'},
        'profile': {
            'type': 'object',
            'required': ['name', 'address'],
            'properties': {
                'name': {'type': 'string'},
                'address': {'type': 'string'},
            },
        },
        'tags': {
            'type': 'array',
            'items': {'type': 'string'},
        },
        'orders': {
            'type': 'array',
            'items': {
                'type': 'object',
                'required': ['orderId', 'amount'],
                'properties': {
                    'orderId': {'type': 'string', 'format': 'uuid'},
                    'amount': {'type': 'number'},
                },
            },
        },
    },
}


def test_common_type_json_schema_acceptance_case_is_valid_and_complete():
    Draft7Validator.check_schema(COMMON_TYPE_JSON_SCHEMA)

    properties = COMMON_TYPE_JSON_SCHEMA['properties']
    assert properties['id']['format'] == 'uuid'
    assert properties['email']['format'] == 'email'
    assert properties['age']['type'] == 'integer'
    assert properties['score']['type'] == 'number'
    assert properties['enabled']['type'] == 'boolean'
    assert properties['profile']['type'] == 'object'
    assert properties['tags']['type'] == 'array'
    assert properties['nothing']['type'] == 'null'
    assert properties['optionalNote']['type'] == ['string', 'null']


def test_common_type_json_schema_preview_generates_valid_faker_values():
    from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import Schema_modelsModel
    from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService

    result = SchemaModelPreviewService.build_preview(
        Schema_modelsModel(modelId='schema_common', title='CommonTypePreview', schemaDraft='draft-07'),
        common_type_preview_nodes(),
    )

    validate(instance=result.example, schema=result.json_schema)

    example = result.example
    schema = result.json_schema
    assert schema['properties']['optionalNote']['type'] == ['string', 'null']
    assert isinstance(example['id'], str) and example['id']
    assert example['username'] == 'casego-user'
    assert '@' in example['email']
    assert isinstance(example['age'], int)
    assert isinstance(example['score'], float)
    assert isinstance(example['enabled'], bool)
    assert example['status'] == 'active'
    assert example['role'] == 'admin'
    assert example['nothing'] is None
    assert example['homepage'].startswith(('http://', 'https://'))
    assert isinstance(example['profile']['name'], str) and example['profile']['name']
    assert isinstance(example['profile']['address'], str) and example['profile']['address']
    assert isinstance(example['tags'], list) and isinstance(example['tags'][0], str)
    assert isinstance(example['orders'], list) and isinstance(example['orders'][0]['orderId'], str)
    assert isinstance(example['orders'][0]['amount'], float)
    assert not result.warnings


def common_type_preview_nodes():
    return [
        node('root', None, 'root', None, 'object', title='CommonTypePreview', level=0, sort_no=0),
        node('id', 'root', 'property', 'id', 'string', required=True, format='uuid', level=1, sort_no=1),
        node('username', 'root', 'property', 'username', 'string', required=True, example='casego-user', level=1, sort_no=2),
        node('email', 'root', 'property', 'email', 'string', required=True, format='email', level=1, sort_no=3),
        node('age', 'root', 'property', 'age', 'integer', required=True, constraints={'minimum': 0}, level=1, sort_no=4),
        node('score', 'root', 'property', 'score', 'number', required=True, level=1, sort_no=5),
        node('enabled', 'root', 'property', 'enabled', 'boolean', required=True, level=1, sort_no=6),
        node(
            'status',
            'root',
            'property',
            'status',
            'string',
            required=True,
            enum_values=['active', 'disabled'],
            level=1,
            sort_no=7,
        ),
        node('role', 'root', 'property', 'role', 'string', required=True, const_value='admin', level=1, sort_no=8),
        node(
            'optional_note',
            'root',
            'property',
            'optionalNote',
            'string',
            type_list=['string', 'null'],
            level=1,
            sort_no=9,
        ),
        node('nothing', 'root', 'property', 'nothing', 'null', required=True, level=1, sort_no=10),
        node('homepage', 'root', 'property', 'homepage', 'string', required=True, format='uri', level=1, sort_no=11),
        node('created_at', 'root', 'property', 'createdAt', 'string', required=True, format='date-time', level=1, sort_no=12),
        node('profile', 'root', 'property', 'profile', 'object', required=True, level=1, sort_no=13),
        node('profile_name', 'profile', 'property', 'name', 'string', required=True, level=2, sort_no=1),
        node('profile_address', 'profile', 'property', 'address', 'string', required=True, level=2, sort_no=2),
        node('tags', 'root', 'property', 'tags', 'array', required=True, level=1, sort_no=14),
        node('tags_item', 'tags', 'items', None, 'string', level=2, sort_no=1),
        node('orders', 'root', 'property', 'orders', 'array', required=True, level=1, sort_no=15),
        node('orders_item', 'orders', 'items', None, 'object', level=2, sort_no=1),
        node('orders_item_id', 'orders_item', 'property', 'orderId', 'string', required=True, format='uuid', level=3, sort_no=1),
        node('orders_item_amount', 'orders_item', 'property', 'amount', 'number', required=True, level=3, sort_no=2),
    ]


def node(
    node_id,
    parent_id,
    node_kind,
    field_name,
    node_type,
    *,
    title=None,
    required=False,
    format=None,
    example=None,
    enum_values=None,
    const_value=None,
    constraints=None,
    type_list=None,
    level=1,
    sort_no=1,
):
    from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel

    return Schema_nodesModel(
        nodeId=node_id,
        modelId='schema_common',
        parentId=parent_id,
        rootId='root',
        nodeKind=node_kind,
        fieldName=field_name,
        title=title,
        type=node_type,
        typeList=type_list,
        nullable=False,
        required=required,
        deprecated=False,
        accessMode='readWrite',
        format=format,
        exampleValue=example,
        enumEnabled=bool(enum_values),
        enumValues=enum_values,
        constEnabled=const_value is not None,
        constValue=const_value,
        mockEnabled=False,
        constraints=constraints or {},
        level=level,
        sortNo=sort_no,
    )
