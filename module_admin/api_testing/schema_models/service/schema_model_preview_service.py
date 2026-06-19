import ast
import random
import re
import string
from copy import deepcopy
from datetime import datetime
from typing import Any

from faker import Faker

from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import (
    SchemaModelPreviewResponseModel,
    Schema_modelsModel,
)
from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel


class SchemaModelPreviewService:
    """
    JSON Schema 数据模型预览生成服务。

    该服务只负责把模型节点转换为 schema/example，不访问数据库，方便后续 Mock 服务复用。
    """

    _faker = Faker(locale='zh_CN')
    _schema_keywords = {
        '$schema',
        'type',
        'title',
        'description',
        'properties',
        'required',
        'items',
        'format',
        'default',
        'example',
        'examples',
        'enum',
        'const',
        'deprecated',
        'readOnly',
        'writeOnly',
    }
    _constraint_keywords = {
        'minLength',
        'maxLength',
        'pattern',
        'minimum',
        'maximum',
        'exclusiveMinimum',
        'exclusiveMaximum',
        'multipleOf',
        'minItems',
        'maxItems',
        'uniqueItems',
        'minProperties',
        'maxProperties',
        'additionalProperties',
    }

    @classmethod
    def build_preview(
        cls,
        model: Schema_modelsModel | None,
        nodes: list[Schema_nodesModel] | None,
        ref_node_map: dict[str, list[Schema_nodesModel]] | None = None,
    ) -> SchemaModelPreviewResponseModel:
        normalized_nodes = cls._normalize_nodes(nodes or [])
        root = cls._find_root(normalized_nodes)
        warnings: list[str] = []

        if root is None:
            return SchemaModelPreviewResponseModel(example=None, json_schema={}, warnings=['模型缺少根节点'])

        child_map = cls._build_child_map(normalized_nodes)
        context = {
            'warnings': warnings,
            'ref_node_map': ref_node_map or {},
            'visited_models': {root.model_id} if root.model_id else set(),
        }
        schema = cls._build_node_schema(root, child_map)
        if model and model.schema_draft:
            schema.setdefault('$schema', cls._schema_draft_url(model.schema_draft))
        example = cls._build_node_example(root, child_map, context)

        return SchemaModelPreviewResponseModel(example=example, json_schema=schema, warnings=warnings)

    @classmethod
    def _normalize_nodes(cls, nodes: list[Schema_nodesModel]) -> list[Schema_nodesModel]:
        return sorted((Schema_nodesModel.model_validate(node) for node in nodes), key=cls._sort_key)

    @classmethod
    def _find_root(cls, nodes: list[Schema_nodesModel]) -> Schema_nodesModel | None:
        return next((node for node in nodes if node.node_kind == 'root'), None) or next(
            (node for node in nodes if not node.parent_id),
            None,
        )

    @classmethod
    def _build_child_map(cls, nodes: list[Schema_nodesModel]) -> dict[str, list[Schema_nodesModel]]:
        child_map: dict[str, list[Schema_nodesModel]] = {}
        for node in nodes:
            if not node.parent_id:
                continue
            child_map.setdefault(node.parent_id, []).append(node)
        for parent_id, children in child_map.items():
            child_map[parent_id] = sorted(children, key=cls._sort_key)
        return child_map

    @classmethod
    def _build_node_schema(cls, node: Schema_nodesModel, child_map: dict[str, list[Schema_nodesModel]]) -> dict[str, Any]:
        node_type = cls._node_type(node)
        schema: dict[str, Any] = {}

        if isinstance(node.raw_schema, dict):
            schema.update(cls._pick_raw_extras(node.raw_schema))
        if isinstance(node.raw_schema_extras, dict):
            schema.update(node.raw_schema_extras)

        schema['type'] = cls._schema_type(node)
        cls._assign_if_present(schema, 'title', node.title)
        cls._assign_if_present(schema, 'description', node.description)
        cls._assign_if_present(schema, 'format', node.format)
        cls._assign_if_present(schema, 'default', node.default_value)
        cls._assign_if_present(schema, 'example', node.example_value)
        cls._assign_if_present(schema, 'examples', node.examples)

        if node.deprecated:
            schema['deprecated'] = True
        if node.access_mode == 'readOnly':
            schema['readOnly'] = True
        if node.access_mode == 'writeOnly':
            schema['writeOnly'] = True
        if node.enum_enabled and cls._has_value(node.enum_values):
            schema['enum'] = node.enum_values
        if node.const_enabled and cls._has_value(node.const_value):
            schema['const'] = node.const_value
        if node.ref_config and isinstance(node.ref_config, dict) and node.ref_config.get('modelId'):
            schema['x-ref-model-id'] = node.ref_config.get('modelId')
        if node.mock_enabled:
            schema['x-mock-enabled'] = True
        cls._assign_if_present(schema, 'x-mock-type', node.mock_type)
        cls._assign_if_present(schema, 'x-mock-rule', node.mock_rule)
        cls._assign_if_present(schema, 'x-mock-value', node.mock_value)

        if isinstance(node.constraints, dict):
            schema.update({key: value for key, value in node.constraints.items() if value not in (None, '')})

        if node_type == 'object':
            properties: dict[str, Any] = {}
            required: list[str] = []
            for child in child_map.get(node.node_id, []):
                if child.node_kind != 'property' or not child.field_name:
                    continue
                properties[child.field_name] = cls._build_node_schema(child, child_map)
                if child.required:
                    required.append(child.field_name)
            if properties:
                schema['properties'] = properties
            if required:
                schema['required'] = required

        if node_type == 'array':
            items_node = next((child for child in child_map.get(node.node_id, []) if child.node_kind == 'items'), None)
            schema['items'] = cls._build_node_schema(items_node, child_map) if items_node else {'type': 'string'}

        return cls._compact(schema)

    @classmethod
    def _build_node_example(
        cls,
        node: Schema_nodesModel,
        child_map: dict[str, list[Schema_nodesModel]],
        context: dict[str, Any],
    ) -> Any:
        node_type = cls._node_type(node)
        if node_type == 'object':
            referenced = cls._build_referenced_example(node, context)
            if referenced is not _Missing:
                return referenced
            children = [
                child for child in child_map.get(node.node_id, []) if child.node_kind == 'property' and child.field_name
            ]
            if children:
                return {child.field_name: cls._build_node_example(child, child_map, context) for child in children}
            preferred = cls._preferred_typed_example(node, context, dict)
            if preferred is not _Missing:
                return deepcopy(preferred)
            return {}

        if node_type == 'array':
            items_node = next((child for child in child_map.get(node.node_id, []) if child.node_kind == 'items'), None)
            if items_node:
                return [cls._build_node_example(items_node, child_map, context)]
            preferred = cls._preferred_typed_example(node, context, list)
            if preferred is not _Missing:
                return deepcopy(preferred)
            return []

        preferred = cls._preferred_scalar_example(node, context)
        if preferred is not _Missing:
            return deepcopy(preferred)

        return cls._generate_by_type(node)

    @classmethod
    def _preferred_typed_example(cls, node: Schema_nodesModel, context: dict[str, Any], expected_type: type) -> Any:
        candidates: list[Any] = []
        if node.mock_enabled and cls._has_value(node.mock_value):
            candidates.append(node.mock_value)
        if node.mock_enabled and node.mock_rule:
            value = cls._call_faker_rule(node.mock_rule)
            if value is not None:
                candidates.append(value)
            else:
                context['warnings'].append(f'Mock规则暂不支持，已使用类型默认值：{node.mock_rule}')
        if isinstance(node.examples, list) and node.examples:
            candidates.append(node.examples[0])
        if cls._has_value(node.example_value):
            candidates.append(node.example_value)
        if cls._has_value(node.default_value):
            candidates.append(node.default_value)
        if node.const_enabled and cls._has_value(node.const_value):
            candidates.append(node.const_value)
        if node.enum_enabled and isinstance(node.enum_values, list) and node.enum_values:
            candidates.append(node.enum_values[0])

        for candidate in candidates:
            if isinstance(candidate, expected_type):
                return candidate
        return _Missing

    @classmethod
    def _build_referenced_example(cls, node: Schema_nodesModel, context: dict[str, Any]) -> Any:
        if not isinstance(node.ref_config, dict):
            return _Missing
        ref_model_id = node.ref_config.get('modelId')
        if not ref_model_id:
            return _Missing
        if ref_model_id in context['visited_models']:
            context['warnings'].append(f'引用模型存在循环，已跳过：{ref_model_id}')
            return {}

        ref_nodes = context['ref_node_map'].get(ref_model_id)
        if not ref_nodes:
            context['warnings'].append(f'引用模型未加载，已按空对象预览：{ref_model_id}')
            return {}

        ref_normalized = cls._normalize_nodes(ref_nodes)
        ref_root = cls._find_root(ref_normalized)
        if not ref_root:
            context['warnings'].append(f'引用模型缺少根节点：{ref_model_id}')
            return {}

        context['visited_models'].add(ref_model_id)
        try:
            return cls._build_node_example(ref_root, cls._build_child_map(ref_normalized), context)
        finally:
            context['visited_models'].discard(ref_model_id)

    @classmethod
    def _preferred_scalar_example(cls, node: Schema_nodesModel, context: dict[str, Any]) -> Any:
        if node.mock_enabled and cls._has_value(node.mock_value):
            return node.mock_value
        if node.mock_enabled and node.mock_rule:
            value = cls._call_faker_rule(node.mock_rule)
            if value is not None:
                return value
            context['warnings'].append(f'Mock规则暂不支持，已使用类型默认值：{node.mock_rule}')
        if isinstance(node.examples, list) and node.examples:
            return node.examples[0]
        if cls._has_value(node.example_value):
            return node.example_value
        if cls._has_value(node.default_value):
            return node.default_value
        if node.const_enabled and cls._has_value(node.const_value):
            return node.const_value
        if node.enum_enabled and isinstance(node.enum_values, list) and node.enum_values:
            return node.enum_values[0]
        return _Missing

    @classmethod
    def _call_faker_rule(cls, rule: str, args: list[Any] | None = None) -> Any:
        normalized_rule, parsed_args = cls._parse_rule_call(rule)
        args = args if args is not None else parsed_args

        rule_map = {
            '$string': lambda: cls._faker.word(),
            'string': lambda: cls._faker.word(),
            'uuid': lambda: cls._faker.uuid4(),
            'nanoid': lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=21)),
            'alpha': lambda: ''.join(random.choices(string.ascii_letters, k=8)),
            'numeric': lambda: ''.join(random.choices(string.digits, k=8)),
            'alphanumeric': lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            'symbol': lambda: random.choice(['@', '#', '$', '%', '&', '*']),
            'number.int': lambda: random.randint(0, 5000),
            'integer': lambda: random.randint(0, 5000),
            'number.float': lambda: round(random.uniform(0, 1000), 2),
            'float': lambda: round(random.uniform(0, 1000), 2),
            'boolean': lambda: cls._faker.boolean(),
            'datetime': lambda: cls._faker.date_time().isoformat(),
            'date': lambda: cls._faker.date(),
            'fromCharacters': lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
        }
        if normalized_rule in rule_map:
            return rule_map[normalized_rule]()

        callable_value = cls._find_callable(normalized_rule)
        if callable_value is not None:
            return callable_value(*args)
        return None

    @classmethod
    def _find_callable(cls, name: str):
        from utils.api_tools.regular_faker_data import Context

        context = Context()
        if hasattr(context, name) and callable(getattr(context, name)):
            return getattr(context, name)

        try:
            from module_admin.api_testing.api_faker_func.faker_config_controller import reload_custom_faker
            from utils.api_tools import custom_faker

            reload_custom_faker()
            if hasattr(custom_faker, name) and callable(getattr(custom_faker, name)):
                return getattr(custom_faker, name)
        except Exception:
            return None
        return None

    @classmethod
    def _parse_rule_call(cls, rule: str) -> tuple[str, list[Any]]:
        value = str(rule or '').strip()
        if value.startswith('{{') and value.endswith('}}'):
            value = value[2:-2].strip()
        match = re.fullmatch(r'([\w\u4e00-\u9fff.]+)\((.*)\)', value)
        if not match:
            return value, []
        name, raw_args = match.groups()
        if not raw_args.strip():
            return name, []
        try:
            parsed = ast.literal_eval(f'({raw_args},)')
            return name, list(parsed)
        except Exception:
            return name, [item.strip() for item in raw_args.split(',') if item.strip()]

    @classmethod
    def _generate_by_type(cls, node: Schema_nodesModel) -> Any:
        node_type = cls._node_type(node)
        field_name = (node.field_name or node.title or '').lower()
        if node_type == 'string':
            return cls._generate_string(node, field_name)
        if node_type == 'integer':
            return random.randint(0, 5000)
        if node_type == 'number':
            return round(random.uniform(0, 1000), 2)
        if node_type == 'boolean':
            return cls._faker.boolean()
        if node_type == 'null':
            return None
        return None

    @classmethod
    def _generate_string(cls, node: Schema_nodesModel, field_name: str) -> str:
        if node.format == 'email' or 'email' in field_name:
            return cls._faker.email()
        if node.format == 'uuid' or field_name.endswith('id'):
            return cls._faker.uuid4()
        if node.format == 'uri' or field_name.endswith('url'):
            return cls._faker.url()
        if node.format == 'date':
            return cls._faker.date()
        if node.format == 'date-time':
            return cls._faker.date_time().isoformat()
        if 'phone' in field_name or 'mobile' in field_name:
            return cls._faker.phone_number()
        if 'name' in field_name:
            return cls._faker.name()
        if 'address' in field_name:
            return cls._faker.address()
        if 'company' in field_name:
            return cls._faker.company()
        if 'time' in field_name:
            return datetime.now().isoformat(timespec='seconds')
        return cls._faker.word()

    @classmethod
    def _node_type(cls, node: Schema_nodesModel) -> str:
        if isinstance(node.type_list, list) and node.type_list:
            return next((item for item in node.type_list if item != 'null'), node.type_list[0])
        return node.type or 'string'

    @classmethod
    def _schema_type(cls, node: Schema_nodesModel) -> str | list[str]:
        if isinstance(node.type_list, list) and node.type_list:
            return node.type_list
        node_type = cls._node_type(node)
        return [node_type, 'null'] if node.nullable and node_type != 'null' else node_type

    @staticmethod
    def _schema_draft_url(schema_draft: str) -> str:
        draft = schema_draft if schema_draft.startswith('http') else str(schema_draft).lower()
        if draft in {'draft-07', 'draft7'}:
            return 'http://json-schema.org/draft-07/schema#'
        return schema_draft

    @classmethod
    def _pick_raw_extras(cls, schema: dict[str, Any]) -> dict[str, Any]:
        return {
            key: value
            for key, value in schema.items()
            if key not in cls._schema_keywords and key not in cls._constraint_keywords
        }

    @staticmethod
    def _assign_if_present(target: dict[str, Any], key: str, value: Any):
        if value not in (None, ''):
            target[key] = value

    @staticmethod
    def _compact(value: dict[str, Any]) -> dict[str, Any]:
        return {key: item for key, item in value.items() if item not in (None, '')}

    @staticmethod
    def _has_value(value: Any) -> bool:
        return value is not None and value != ''

    @staticmethod
    def _sort_key(node: Schema_nodesModel):
        return (node.level or 0, node.sort_no or 0, node.node_id or '')


class _MissingValue:
    pass


_Missing = _MissingValue()
