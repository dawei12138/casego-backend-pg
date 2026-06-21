from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.schema_nodes.dao.schema_nodes_dao import Schema_nodesDao
from module_admin.api_testing.schema_nodes.entity.vo.schema_nodes_vo import DeleteSchema_nodesModel, Schema_nodesModel, Schema_nodesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Schema_nodesService:
    """
    JSON Schema 可视化节点模块服务层
    """

    @classmethod
    async def get_schema_nodes_list_services(
        cls, query_db: AsyncSession, query_object: Schema_nodesPageQueryModel, is_page: bool = False
    ):
        """
        获取JSON Schema 可视化节点列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 可视化节点列表信息对象
        """
        schema_nodes_list_result = await Schema_nodesDao.get_schema_nodes_list(query_db, query_object, is_page)

        return schema_nodes_list_result


    @classmethod
    async def add_schema_nodes_services(cls, query_db: AsyncSession, page_object: Schema_nodesModel):
        """
        新增JSON Schema 可视化节点信息service

        :param query_db: orm对象
        :param page_object: 新增JSON Schema 可视化节点对象
        :return: 新增JSON Schema 可视化节点校验结果
        """
        page_object = Schema_nodesModel.model_validate(page_object.model_dump())
        cls._validate_schema_node_business_rules(page_object)
        try:
            await Schema_nodesDao.add_schema_nodes_dao(query_db, page_object)
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
    async def edit_schema_nodes_services(cls, query_db: AsyncSession, page_object: Schema_nodesModel):
        """
        编辑JSON Schema 可视化节点信息service

        :param query_db: orm对象
        :param page_object: 编辑JSON Schema 可视化节点对象
        :return: 编辑JSON Schema 可视化节点校验结果
        """
        page_object = Schema_nodesModel.model_validate(page_object.model_dump())
        cls._validate_schema_node_business_rules(page_object)
        edit_schema_nodes = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        schema_nodes_info = await cls.schema_nodes_detail_services(query_db, page_object.node_id)
        if schema_nodes_info.node_id:
            try:
                await Schema_nodesDao.edit_schema_nodes_dao(query_db, edit_schema_nodes)
                await query_db.commit()
                result = Schema_nodesModel.model_validate(edit_schema_nodes).model_dump(by_alias=True)
                return CrudResponseModel(is_success=True, message='更新成功', result=result)
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='JSON Schema 可视化节点不存在')

    @staticmethod
    def _validate_schema_node_business_rules(node: Schema_nodesModel):
        if node.node_kind == 'property' and not str(node.field_name or '').strip():
            raise ServiceException(message='字段名不能为空')

    @classmethod
    async def delete_schema_nodes_services(cls, query_db: AsyncSession, page_object: DeleteSchema_nodesModel):
        """
        删除JSON Schema 可视化节点信息service

        :param query_db: orm对象
        :param page_object: 删除JSON Schema 可视化节点对象
        :return: 删除JSON Schema 可视化节点校验结果
        """
        if page_object.node_ids:
            node_id_list = page_object.node_ids.split(',')
            try:
                for node_id in node_id_list:
                    node_id_obj = Schema_nodesModel.model_validate({'node_id': node_id}).node_id
                    await Schema_nodesDao.delete_schema_nodes_dao(query_db, Schema_nodesModel(nodeId=node_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入节点ID为空')

    @classmethod
    async def schema_nodes_detail_services(cls, query_db: AsyncSession, node_id: str):
        """
        获取JSON Schema 可视化节点详细信息service

        :param query_db: orm对象
        :param node_id: 节点ID
        :return: 节点ID对应的信息
        """
        schema_nodes = await Schema_nodesDao.get_schema_nodes_detail_by_id(query_db, node_id=node_id)
        if schema_nodes:
            result = Schema_nodesModel(**CamelCaseUtil.transform_result(schema_nodes))
        else:
            result = Schema_nodesModel(**dict())

        return result

    @staticmethod
    async def export_schema_nodes_list_services(schema_nodes_list: List):
        """
        导出JSON Schema 可视化节点信息service

        :param schema_nodes_list: JSON Schema 可视化节点信息列表
        :return: JSON Schema 可视化节点信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'nodeId': '节点ID',
            'modelId': '所属模型ID',
            'parentId': '父节点ID',
            'rootId': '根节点ID',
            'nodeKind': '节点类型：root/property/items/composition/ref',
            'fieldName': '字段名',
            'displayName': '展示名',
            'alias': '字段映射名或代码生成别名',
            'sourceFieldName': '来源字段名',
            'sourceFieldType': '来源字段类型',
            'sourceFieldComment': '来源字段注释',
            'codeFieldName': '代码生成字段名',
            'title': 'JSON Schema title',
            'type': 'JSON Schema主类型',
            'typeList': '多类型列表',
            'nullable': '是否允许NULL',
            'required': '是否必填',
            'deprecated': '是否废弃',
            'accessMode': '读写行为',
            'format': 'format',
            'defaultValue': '默认值',
            'exampleValue': '示例值',
            'examples': '示例值列表',
            'enumEnabled': '是否启用枚举',
            'enumValues': '枚举值',
            'enumMeta': '枚举元数据',
            'constEnabled': '是否启用常量',
            'constValue': '常量值',
            'mockEnabled': '是否启用Mock',
            'mockType': 'Mock类型',
            'mockRule': 'Mock规则',
            'mockValue': '固定Mock值',
            'mockConfig': 'Mock配置',
            'constraints': '类型约束',
            'composition': '组合结构配置',
            'refConfig': '引用配置',
            'xmlConfig': 'XML配置',
            'source': '节点来源',
            'sourcePath': '来源路径',
            'importHint': '导入推断信息',
            'rawSchema': '当前节点原始Schema',
            'rawSchemaExtras': '不支持可视化的Schema关键字',
            'uiState': '前端临时状态',
            'path': '字段路径',
            'jsonPointer': 'JSON Pointer',
            'level': '层级',
            'expanded': '是否展开',
            'locked': '是否锁定',
            'sortNo': '排序号',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(schema_nodes_list, mapping_dict)

        return binary_data
