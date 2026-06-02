from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.schema_model_usage.dao.schema_model_usage_dao import Schema_model_usageDao
from module_admin.api_testing.schema_model_usage.entity.vo.schema_model_usage_vo import DeleteSchema_model_usageModel, Schema_model_usageModel, Schema_model_usagePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Schema_model_usageService:
    """
    JSON Schema 模型使用关系模块服务层
    """

    @classmethod
    async def get_schema_model_usage_list_services(
        cls, query_db: AsyncSession, query_object: Schema_model_usagePageQueryModel, is_page: bool = False
    ):
        """
        获取JSON Schema 模型使用关系列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 模型使用关系列表信息对象
        """
        schema_model_usage_list_result = await Schema_model_usageDao.get_schema_model_usage_list(query_db, query_object, is_page)

        return schema_model_usage_list_result


    @classmethod
    async def add_schema_model_usage_services(cls, query_db: AsyncSession, page_object: Schema_model_usageModel):
        """
        新增JSON Schema 模型使用关系信息service

        :param query_db: orm对象
        :param page_object: 新增JSON Schema 模型使用关系对象
        :return: 新增JSON Schema 模型使用关系校验结果
        """
        page_object = Schema_model_usageModel.model_validate(page_object.model_dump())
        try:
            await Schema_model_usageDao.add_schema_model_usage_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_schema_model_usage_services(cls, query_db: AsyncSession, page_object: Schema_model_usageModel):
        """
        编辑JSON Schema 模型使用关系信息service

        :param query_db: orm对象
        :param page_object: 编辑JSON Schema 模型使用关系对象
        :return: 编辑JSON Schema 模型使用关系校验结果
        """
        page_object = Schema_model_usageModel.model_validate(page_object.model_dump())
        edit_schema_model_usage = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        schema_model_usage_info = await cls.schema_model_usage_detail_services(query_db, page_object.usage_id)
        if schema_model_usage_info.usage_id:
            try:
                await Schema_model_usageDao.edit_schema_model_usage_dao(query_db, edit_schema_model_usage)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='JSON Schema 模型使用关系不存在')

    @classmethod
    async def delete_schema_model_usage_services(cls, query_db: AsyncSession, page_object: DeleteSchema_model_usageModel):
        """
        删除JSON Schema 模型使用关系信息service

        :param query_db: orm对象
        :param page_object: 删除JSON Schema 模型使用关系对象
        :return: 删除JSON Schema 模型使用关系校验结果
        """
        if page_object.usage_ids:
            usage_id_list = page_object.usage_ids.split(',')
            try:
                for usage_id in usage_id_list:
                    usage_id_obj = Schema_model_usageModel.model_validate({'usage_id': usage_id}).usage_id
                    await Schema_model_usageDao.delete_schema_model_usage_dao(query_db, Schema_model_usageModel(usageId=usage_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入使用关系ID为空')

    @classmethod
    async def schema_model_usage_detail_services(cls, query_db: AsyncSession, usage_id: str):
        """
        获取JSON Schema 模型使用关系详细信息service

        :param query_db: orm对象
        :param usage_id: 使用关系ID
        :return: 使用关系ID对应的信息
        """
        schema_model_usage = await Schema_model_usageDao.get_schema_model_usage_detail_by_id(query_db, usage_id=usage_id)
        if schema_model_usage:
            result = Schema_model_usageModel(**CamelCaseUtil.transform_result(schema_model_usage))
        else:
            result = Schema_model_usageModel(**dict())

        return result

    @staticmethod
    async def export_schema_model_usage_list_services(schema_model_usage_list: List):
        """
        导出JSON Schema 模型使用关系信息service

        :param schema_model_usage_list: JSON Schema 模型使用关系信息列表
        :return: JSON Schema 模型使用关系信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'usageId': '使用关系ID',
            'modelId': '模型ID',
            'usageType': '使用类型',
            'usageTargetId': '使用目标ID',
            'usageTargetName': '使用目标名称',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'sortNo': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(schema_model_usage_list, mapping_dict)

        return binary_data
