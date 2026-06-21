from copy import deepcopy
from datetime import datetime
import json
import re
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.schema_nodes.dao.schema_nodes_dao import Schema_nodesDao
from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import Schema_nodesModel, Schema_nodesPageQueryModel
from module_admin.api_testing.schema_models.dao.schema_models_dao import Schema_modelsDao
from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import (
    CreateSchemaModelWithRootModel,
    DeleteSchema_modelsModel,
    SchemaModelCopyRequestModel,
    SchemaModelGenerateRequestModel,
    SchemaModelGenerateResponseModel,
    SchemaModelMoveRequestModel,
    SchemaModelPreviewRequestModel,
    SchemaModelPreviewResponseModel,
    Schema_modelsModel,
    Schema_modelsPageQueryModel,
)
from module_admin.api_testing.schema_models.service.schema_model_preview_service import SchemaModelPreviewService
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Schema_modelsService:
    """
    JSON Schema 数据模型主模块服务层
    """

    @classmethod
    async def get_schema_models_list_services(
        cls, query_db: AsyncSession, query_object: Schema_modelsPageQueryModel, is_page: bool = False
    ):
        """
        获取JSON Schema 数据模型主列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 数据模型主列表信息对象
        """
        schema_models_list_result = await Schema_modelsDao.get_schema_models_list(query_db, query_object, is_page)

        return schema_models_list_result


    @classmethod
    async def add_schema_models_services(cls, query_db: AsyncSession, page_object: Schema_modelsModel):
        """
        新增JSON Schema 数据模型主信息service

        :param query_db: orm对象
        :param page_object: 新增JSON Schema 数据模型主对象
        :return: 新增JSON Schema 数据模型主校验结果
        """
        page_object = Schema_modelsModel.model_validate(page_object.model_dump())
        try:
            await Schema_modelsDao.add_schema_models_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(
                is_success=True,
                message='新增成功',
                result=page_object.model_dump(by_alias=True),
            )
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def add_schema_model_with_root_services(
        cls, query_db: AsyncSession, create_object: CreateSchemaModelWithRootModel
    ):
        """
        事务创建JSON Schema 数据模型主信息及根节点

        :param query_db: orm对象
        :param create_object: 新增JSON Schema 数据模型及根节点对象
        :return: 新增JSON Schema 数据模型及根节点校验结果
        """
        model_object = Schema_modelsModel.model_validate(create_object.model.model_dump())
        root_node_object = create_object.root_node
        root_node_object.model_id = model_object.model_id
        root_node_object.root_id = root_node_object.root_id or root_node_object.node_id
        root_node_object.parent_id = None
        root_node_object.node_kind = root_node_object.node_kind or 'root'
        model_object.root_node_id = model_object.root_node_id or root_node_object.node_id

        model_object.validate_fields()
        root_node_object.validate_fields()

        try:
            await Schema_modelsDao.add_schema_models_dao(query_db, model_object)
            await Schema_nodesDao.add_schema_nodes_dao(query_db, root_node_object)
            await query_db.commit()
            result = model_object.model_dump(by_alias=True)
            result['rootNode'] = root_node_object.model_dump(by_alias=True)
            return CrudResponseModel(is_success=True, message='新增成功', result=result)
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_schema_models_services(cls, query_db: AsyncSession, page_object: Schema_modelsModel):
        """
        编辑JSON Schema 数据模型主信息service

        :param query_db: orm对象
        :param page_object: 编辑JSON Schema 数据模型主对象
        :return: 编辑JSON Schema 数据模型主校验结果
        """
        page_object = Schema_modelsModel.model_validate(page_object.model_dump())
        edit_schema_models = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        schema_models_info = await cls.schema_models_detail_services(query_db, page_object.model_id)
        if schema_models_info.model_id:
            current_version = int(schema_models_info.version or 0)
            submit_version = int(page_object.version or 0)
            if submit_version != current_version:
                raise ServiceException(message='模型已被更新，请刷新后重试')
            edit_schema_models['version'] = current_version + 1
            try:
                await Schema_modelsDao.edit_schema_models_dao(query_db, edit_schema_models)
                await query_db.commit()
                result = Schema_modelsModel.model_validate(edit_schema_models).model_dump(by_alias=True)
                return CrudResponseModel(is_success=True, message='更新成功', result=result)
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='JSON Schema 数据模型主不存在')

    @classmethod
    async def delete_schema_models_services(cls, query_db: AsyncSession, page_object: DeleteSchema_modelsModel):
        """
        删除JSON Schema 数据模型主信息service

        :param query_db: orm对象
        :param page_object: 删除JSON Schema 数据模型主对象
        :return: 删除JSON Schema 数据模型主校验结果
        """
        if page_object.model_ids:
            model_id_list = page_object.model_ids.split(',')
            try:
                for model_id in model_id_list:
                    model_id_obj = Schema_modelsModel.model_validate({'model_id': model_id}).model_id
                    await Schema_nodesDao.delete_schema_nodes_by_model_id_dao(query_db, model_id_obj)
                    await Schema_modelsDao.delete_schema_models_dao(query_db, Schema_modelsModel(modelId=model_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入模型ID为空')

    @classmethod
    async def schema_models_detail_services(cls, query_db: AsyncSession, model_id: str):
        """
        获取JSON Schema 数据模型主详细信息service

        :param query_db: orm对象
        :param model_id: 模型ID
        :return: 模型ID对应的信息
        """
        schema_models = await Schema_modelsDao.get_schema_models_detail_by_id(query_db, model_id=model_id)
        if schema_models:
            result = Schema_modelsModel(**CamelCaseUtil.transform_result(schema_models))
        else:
            result = Schema_modelsModel(**dict())

        return result

    @classmethod
    async def preview_schema_model_services(
        cls,
        query_db: AsyncSession,
        preview_object: SchemaModelPreviewRequestModel,
    ) -> SchemaModelPreviewResponseModel:
        """
        根据当前模型节点生成预览示例和JSON Schema。

        前端会传入当前未保存的节点；后端只补充引用模型节点，生成逻辑集中在 SchemaModelPreviewService 中，
        便于后续 Mock 服务复用同一套规则。
        """
        ref_node_map = await cls._load_referenced_nodes(query_db, preview_object.nodes)
        return SchemaModelPreviewService.build_preview(preview_object.model, preview_object.nodes, ref_node_map=ref_node_map)

    @classmethod
    async def copy_schema_model_services(
        cls,
        query_db: AsyncSession,
        copy_object: SchemaModelCopyRequestModel,
        operator: str | None = None,
        require_target_branch: bool = False,
    ):
        """
        复制数据模型及其可视化节点，可用于同目录复制或复制到其他分支。
        """
        if require_target_branch and not copy_object.target_branch_id:
            raise ServiceException(message='目标分支不能为空')

        source_model = await cls.schema_models_detail_services(query_db, copy_object.model_id)
        if not source_model.model_id:
            raise ServiceException(message='JSON Schema 数据模型主不存在')

        source_nodes = await Schema_nodesDao.get_schema_nodes_list(
            query_db,
            Schema_nodesPageQueryModel(modelId=copy_object.model_id, pageNum=1, pageSize=2000),
            is_page=False,
        )
        normalized_nodes = [Schema_nodesModel.model_validate(node) for node in source_nodes or []]
        node_id_map = {node.node_id: cls._new_schema_id('node') for node in normalized_nodes if node.node_id}
        source_root = next((node for node in normalized_nodes if node.node_kind == 'root'), None)
        new_root_node_id = node_id_map.get(source_model.root_node_id) or node_id_map.get(source_root.node_id if source_root else None)
        new_model_id = cls._new_schema_id('schema')
        now = datetime.now()

        new_model_payload = deepcopy(source_model.model_dump())
        new_model_payload.update(
            {
                'model_id': new_model_id,
                'group_id': copy_object.target_group_id if copy_object.target_group_id is not None else source_model.group_id,
                'branch_id': copy_object.target_branch_id if copy_object.target_branch_id is not None else source_model.branch_id,
                'name': copy_object.name or cls._copy_name(source_model.name or source_model.title or source_model.display_name),
                'display_name': copy_object.display_name or cls._copy_name(source_model.display_name or source_model.name),
                'title': copy_object.display_name or copy_object.name or cls._copy_name(source_model.title or source_model.name),
                'root_node_id': new_root_node_id,
                'parent_model_id': source_model.model_id,
                'source_model_name': source_model.name or source_model.title or source_model.display_name,
                'version': 1,
                'create_by': operator or source_model.create_by,
                'create_time': now,
                'update_by': operator or source_model.update_by,
                'update_time': now,
                'del_flag': '0',
            }
        )
        new_model = Schema_modelsModel.model_validate(new_model_payload)

        try:
            await Schema_modelsDao.add_schema_models_dao(query_db, new_model)
            cloned_nodes = []
            for source_node in normalized_nodes:
                cloned_node = cls._clone_schema_node(
                    source_node,
                    new_model_id=new_model_id,
                    node_id_map=node_id_map,
                    new_root_node_id=new_root_node_id,
                    operator=operator,
                    now=now,
                )
                cloned_nodes.append(cloned_node)
                await Schema_nodesDao.add_schema_nodes_dao(query_db, cloned_node)

            await query_db.commit()
            result = new_model.model_dump(by_alias=True)
            result['nodes'] = [node.model_dump(by_alias=True) for node in cloned_nodes]
            return CrudResponseModel(is_success=True, message='复制成功', result=result)
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    def generate_schema_model_services(
        cls,
        generate_object: SchemaModelGenerateRequestModel,
    ) -> SchemaModelGenerateResponseModel:
        """
        根据输入内容生成 JSON Schema 与可视化节点。

        第一版后端只承接不依赖外部服务的 JSON / JSON Schema 转换；数据库、XML、Mockjs 和 AI
        返回明确开发中错误，避免前端误判为成功。
        """
        source_type = str(generate_object.source_type or '').strip().upper().replace('-', '_')
        unsupported_messages = {
            'XML': '通过 XML 生成开发中',
            'DATABASE': '从数据库导入开发中',
            'DB': '从数据库导入开发中',
            'MOCKJS': '通过 Mock.js 生成开发中',
            'MOCK_JS': '通过 Mock.js 生成开发中',
            'AI': 'AI 生成暂未规划，开发中',
        }
        if source_type in unsupported_messages:
            raise ServiceException(message=unsupported_messages[source_type])

        content = cls._parse_generate_content(generate_object.content)
        if source_type == 'JSON':
            schema = cls._infer_schema_from_json(content)
        elif source_type in {'JSON_SCHEMA', 'JSONSCHEMA', 'SCHEMA'}:
            if not isinstance(content, dict):
                raise ServiceException(message='JSON Schema 内容必须是对象')
            schema = deepcopy(content)
        else:
            raise ServiceException(message='生成来源类型暂不支持')

        nodes = cls._build_nodes_from_schema(
            schema,
            model_id=generate_object.model_id or 'preview',
            root_title=generate_object.root_title or 'GeneratedModel',
        )
        return SchemaModelGenerateResponseModel(
            sourceType=source_type,
            supported=True,
            message='生成成功',
            schema=schema,
            nodes=nodes,
            warnings=[],
        )

    @classmethod
    def _parse_generate_content(cls, content: Any) -> Any:
        if content in (None, ''):
            raise ServiceException(message='生成内容不能为空')
        if isinstance(content, str):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                raise ServiceException(message='JSON 格式错误，请检查后重试')
        return deepcopy(content)

    @classmethod
    def _infer_schema_from_json(cls, value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            properties = {str(key): cls._infer_schema_from_json(item) for key, item in value.items()}
            schema: dict[str, Any] = {
                'type': 'object',
                'properties': properties,
                'x-apifox-orders': list(properties.keys()),
            }
            if properties:
                schema['required'] = list(properties.keys())
            return schema

        if isinstance(value, list):
            if not value:
                return {'type': 'array', 'items': {'type': 'string'}}
            item_schemas = [cls._infer_schema_from_json(item) for item in value]
            unique_schemas = cls._unique_schemas(item_schemas)
            if len(unique_schemas) == 1:
                return {'type': 'array', 'items': unique_schemas[0]}
            return {'type': 'array', 'items': {'oneOf': unique_schemas}}

        if isinstance(value, bool):
            return {'type': 'boolean'}
        if isinstance(value, int) and not isinstance(value, bool):
            return {'type': 'integer'}
        if isinstance(value, float):
            return {'type': 'number'}
        if value is None:
            return {'type': 'null'}
        return {'type': 'string'}

    @staticmethod
    def _unique_schemas(schemas: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        seen: set[str] = set()
        for schema in schemas:
            fingerprint = json.dumps(schema, ensure_ascii=False, sort_keys=True)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            result.append(schema)
        return result

    @classmethod
    def _build_nodes_from_schema(
        cls,
        schema: dict[str, Any],
        model_id: str,
        root_title: str,
    ) -> list[Schema_nodesModel]:
        nodes: list[Schema_nodesModel] = []
        root_schema = schema if isinstance(schema, dict) else {'type': 'string'}
        root_node = cls._schema_to_node(
            root_schema,
            model_id=model_id,
            node_id='root',
            parent_id=None,
            root_id='root',
            node_kind='root',
            field_name=None,
            title=root_schema.get('title') or root_title,
            required=False,
            level=0,
            sort_no=0,
        )
        nodes.append(root_node)
        cls._append_schema_children(nodes, root_schema, root_node, model_id=model_id, root_id='root')
        return nodes

    @classmethod
    def _append_schema_children(
        cls,
        nodes: list[Schema_nodesModel],
        schema: dict[str, Any],
        parent_node: Schema_nodesModel,
        model_id: str,
        root_id: str,
    ):
        node_type = cls._schema_primary_type(schema)
        composition_type = cls._schema_composition_type(schema)
        if composition_type:
            for index, item in enumerate(schema.get(composition_type) or []):
                child_id = f'{parent_node.node_id}_{index}'
                child = cls._schema_to_node(
                    item if isinstance(item, dict) else {'type': 'string'},
                    model_id=model_id,
                    node_id=child_id,
                    parent_id=parent_node.node_id,
                    root_id=root_id,
                    node_kind='composition',
                    field_name=str(index),
                    title=None,
                    required=False,
                    level=(parent_node.level or 0) + 1,
                    sort_no=index,
                )
                nodes.append(child)
                cls._append_schema_children(nodes, item if isinstance(item, dict) else {}, child, model_id, root_id)
            return

        if node_type == 'object':
            properties = schema.get('properties') if isinstance(schema.get('properties'), dict) else {}
            orders = schema.get('x-apifox-orders') if isinstance(schema.get('x-apifox-orders'), list) else list(properties.keys())
            ordered_keys = [key for key in orders if key in properties] + [key for key in properties.keys() if key not in orders]
            required_keys = set(schema.get('required') if isinstance(schema.get('required'), list) else [])
            for index, field_name in enumerate(ordered_keys):
                child_schema = properties[field_name] if isinstance(properties[field_name], dict) else {'type': 'string'}
                child_id = cls._node_id(parent_node.node_id, field_name)
                child = cls._schema_to_node(
                    child_schema,
                    model_id=model_id,
                    node_id=child_id,
                    parent_id=parent_node.node_id,
                    root_id=root_id,
                    node_kind='property',
                    field_name=field_name,
                    title=child_schema.get('title'),
                    required=field_name in required_keys,
                    level=(parent_node.level or 0) + 1,
                    sort_no=index + 1,
                )
                nodes.append(child)
                cls._append_schema_children(nodes, child_schema, child, model_id, root_id)
            return

        if node_type == 'array':
            items_schema = schema.get('items') if isinstance(schema.get('items'), dict) else {'type': 'string'}
            items_node = cls._schema_to_node(
                items_schema,
                model_id=model_id,
                node_id=f'{parent_node.node_id}_items',
                parent_id=parent_node.node_id,
                root_id=root_id,
                node_kind='items',
                field_name=None,
                title=items_schema.get('title'),
                required=False,
                level=(parent_node.level or 0) + 1,
                sort_no=1,
            )
            nodes.append(items_node)
            cls._append_schema_children(nodes, items_schema, items_node, model_id, root_id)

    @classmethod
    def _schema_to_node(
        cls,
        schema: dict[str, Any],
        model_id: str,
        node_id: str,
        parent_id: str | None,
        root_id: str,
        node_kind: str,
        field_name: str | None,
        title: str | None,
        required: bool,
        level: int,
        sort_no: float,
    ) -> Schema_nodesModel:
        schema = schema if isinstance(schema, dict) else {}
        node_type = cls._schema_composition_type(schema) or cls._schema_primary_type(schema)
        type_list = schema.get('type') if isinstance(schema.get('type'), list) else None
        raw_schema_extras = {
            key: deepcopy(value)
            for key, value in schema.items()
            if key not in SchemaModelPreviewService._schema_keywords
            and key not in SchemaModelPreviewService._constraint_keywords
        }
        constraints = {
            key: deepcopy(value)
            for key, value in schema.items()
            if key in SchemaModelPreviewService._constraint_keywords
        }
        return Schema_nodesModel(
            nodeId=node_id,
            modelId=model_id,
            parentId=parent_id,
            rootId=root_id,
            nodeKind=node_kind,
            fieldName=field_name,
            title=title,
            type=node_type,
            typeList=type_list,
            nullable=cls._schema_nullable(schema),
            required=required,
            deprecated=bool(schema.get('deprecated', False)),
            accessMode='readOnly' if schema.get('readOnly') else 'writeOnly' if schema.get('writeOnly') else 'readWrite',
            format=schema.get('format'),
            defaultValue=schema.get('default'),
            exampleValue=schema.get('example'),
            examples=schema.get('examples'),
            enumEnabled=isinstance(schema.get('enum'), list),
            enumValues=schema.get('enum'),
            constEnabled='const' in schema,
            constValue=schema.get('const'),
            mockEnabled=bool(schema.get('x-mock-enabled')),
            mockType=schema.get('x-mock-type'),
            mockRule=schema.get('x-mock-rule'),
            mockValue=schema.get('x-mock-value'),
            constraints=constraints,
            rawSchemaExtras=raw_schema_extras or None,
            level=level,
            sortNo=sort_no,
            expanded=True,
            locked=False,
            delFlag='0',
        )

    @staticmethod
    def _schema_primary_type(schema: dict[str, Any]) -> str:
        schema_type = schema.get('type')
        if isinstance(schema_type, list):
            return next((item for item in schema_type if item != 'null'), schema_type[0] if schema_type else 'string')
        if schema.get('$ref'):
            return 'ref'
        return schema_type or 'object' if isinstance(schema.get('properties'), dict) else schema_type or 'string'

    @staticmethod
    def _schema_composition_type(schema: dict[str, Any]) -> str:
        for key in ('allOf', 'anyOf', 'oneOf'):
            if isinstance(schema.get(key), list):
                return key
        return ''

    @staticmethod
    def _schema_nullable(schema: dict[str, Any]) -> bool:
        schema_type = schema.get('type')
        return bool(schema.get('nullable') or (isinstance(schema_type, list) and 'null' in schema_type))

    @staticmethod
    def _node_id(parent_id: str, field_name: str) -> str:
        normalized = re.sub(r'[^0-9a-zA-Z_]+', '_', str(field_name)).strip('_') or 'field'
        return f'{parent_id}_{normalized}'[:64]

    @classmethod
    async def move_schema_model_services(
        cls,
        query_db: AsyncSession,
        move_object: SchemaModelMoveRequestModel,
        operator: str | None = None,
    ):
        """
        移动数据模型到目标目录，只修改模型主信息。
        """
        source_model = await cls.schema_models_detail_services(query_db, move_object.model_id)
        if not source_model.model_id:
            raise ServiceException(message='JSON Schema 数据模型主不存在')

        next_version = int(source_model.version or 0) + 1
        now = datetime.now()
        payload = {
            'model_id': source_model.model_id,
            'group_id': move_object.target_group_id,
            'version': next_version,
            'update_by': operator or source_model.update_by,
            'update_time': now,
        }
        try:
            await Schema_modelsDao.edit_schema_models_dao(query_db, payload)
            await query_db.commit()
            result_payload = source_model.model_dump()
            result_payload.update(payload)
            return CrudResponseModel(
                is_success=True,
                message='移动成功',
                result=Schema_modelsModel.model_validate(result_payload).model_dump(by_alias=True),
            )
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def _load_referenced_nodes(
        cls,
        query_db: AsyncSession,
        nodes: list[Schema_nodesModel],
        max_models: int = 16,
    ) -> dict[str, list[Schema_nodesModel]]:
        ref_node_map: dict[str, list[Schema_nodesModel]] = {}
        pending = list(cls._collect_ref_model_ids(nodes))

        while pending and len(ref_node_map) < max_models:
            model_id = pending.pop(0)
            if model_id in ref_node_map:
                continue

            rows = await Schema_nodesDao.get_schema_nodes_list(
                query_db,
                Schema_nodesPageQueryModel(modelId=model_id, pageNum=1, pageSize=2000),
                is_page=False,
            )
            loaded_nodes = [Schema_nodesModel.model_validate(row) for row in rows or []]
            ref_node_map[model_id] = loaded_nodes

            for nested_model_id in cls._collect_ref_model_ids(loaded_nodes):
                if nested_model_id not in ref_node_map and nested_model_id not in pending:
                    pending.append(nested_model_id)

        return ref_node_map

    @staticmethod
    def _new_schema_id(prefix: str) -> str:
        return f'{prefix}_{uuid4().hex[:12]}'

    @staticmethod
    def _copy_name(value: str | None) -> str | None:
        return f'{value}_copy' if value else value

    @staticmethod
    def _clone_schema_node(
        source_node: Schema_nodesModel,
        new_model_id: str,
        node_id_map: dict[str, str],
        new_root_node_id: str | None,
        operator: str | None,
        now: datetime,
    ) -> Schema_nodesModel:
        payload = deepcopy(source_node.model_dump())
        old_node_id = source_node.node_id
        old_parent_id = source_node.parent_id
        old_root_id = source_node.root_id
        new_node_id = node_id_map.get(old_node_id)
        payload.update(
            {
                'node_id': new_node_id,
                'model_id': new_model_id,
                'parent_id': node_id_map.get(old_parent_id) if old_parent_id else None,
                'root_id': node_id_map.get(old_root_id) or new_root_node_id or new_node_id,
                'create_by': operator or source_node.create_by,
                'create_time': now,
                'update_by': operator or source_node.update_by,
                'update_time': now,
                'del_flag': '0',
            }
        )
        if source_node.node_kind == 'root':
            payload['parent_id'] = None
            payload['root_id'] = new_node_id
        return Schema_nodesModel.model_validate(payload)

    @staticmethod
    def _collect_ref_model_ids(nodes: list[Schema_nodesModel]) -> set[str]:
        ref_ids = set()
        for node in nodes or []:
            ref_config = node.ref_config if isinstance(node.ref_config, dict) else {}
            ref_model_id = ref_config.get('modelId') or ref_config.get('model_id')
            if ref_model_id:
                ref_ids.add(ref_model_id)
        return ref_ids

    @staticmethod
    async def export_schema_models_list_services(schema_models_list: List):
        """
        导出JSON Schema 数据模型主信息service

        :param schema_models_list: JSON Schema 数据模型主信息列表
        :return: JSON Schema 数据模型主信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'modelId': '模型ID',
            'projectId': '所属项目ID',
            'caseId': '关联的测试用例ID',
            'groupId': '所属分组ID',
            'branchId': '所属分支ID',
            'name': '模型唯一名称',
            'displayName': '展示名称',
            'title': 'JSON Schema标题',
            'schemaDraft': 'JSON Schema版本',
            'rootNodeId': '根节点ID',
            'modelCategory': '模型分类：request/response/common/enum/dto',
            'modelRole': '模型角色：input/output/entity/enum',
            'parentModelId': '派生来源模型ID',
            'sourceModelName': '来源模型名称',
            'codeClassName': '代码生成类名',
            'codeFileName': '代码生成文件名',
            'sourceTableName': '来源数据库表名',
            'visibility': '可见性：private/project/public',
            'status': '状态：draft/published/deprecated',
            'version': '内部版本号',
            'revision': '语义版本号',
            'sourceType': '来源类型：manual/json/openapi/database/code',
            'sourceId': '来源业务ID',
            'rawSchema': '原始JSON Schema',
            'rawSchemaExtras': '模型级扩展Schema关键字',
            'generatedSchema': '生成后的JSON Schema',
            'tags': '标签',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'sortNo': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(schema_models_list, mapping_dict)

        return binary_data
