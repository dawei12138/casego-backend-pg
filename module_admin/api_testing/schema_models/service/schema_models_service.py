from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.schema_models.dao.schema_models_dao import Schema_modelsDao
from module_admin.api_testing.schema_models.entity.vo.schema_models_vo import DeleteSchema_modelsModel, Schema_modelsModel, Schema_modelsPageQueryModel
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
            return CrudResponseModel(is_success=True, message='新增成功')
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
            try:
                await Schema_modelsDao.edit_schema_models_dao(query_db, edit_schema_models)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
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
