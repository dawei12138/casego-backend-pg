from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.schema_model_refs.dao.schema_model_refs_dao import Schema_model_refsDao
from module_admin.api_testing.schema_model_refs.entity.vo.schema_model_refs_vo import DeleteSchema_model_refsModel, Schema_model_refsModel, Schema_model_refsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Schema_model_refsService:
    """
    JSON Schema 模型引用关系模块服务层
    """

    @classmethod
    async def get_schema_model_refs_list_services(
        cls, query_db: AsyncSession, query_object: Schema_model_refsPageQueryModel, is_page: bool = False
    ):
        """
        获取JSON Schema 模型引用关系列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 模型引用关系列表信息对象
        """
        schema_model_refs_list_result = await Schema_model_refsDao.get_schema_model_refs_list(query_db, query_object, is_page)

        return schema_model_refs_list_result


    @classmethod
    async def add_schema_model_refs_services(cls, query_db: AsyncSession, page_object: Schema_model_refsModel):
        """
        新增JSON Schema 模型引用关系信息service

        :param query_db: orm对象
        :param page_object: 新增JSON Schema 模型引用关系对象
        :return: 新增JSON Schema 模型引用关系校验结果
        """
        page_object = Schema_model_refsModel.model_validate(page_object.model_dump())
        try:
            await Schema_model_refsDao.add_schema_model_refs_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_schema_model_refs_services(cls, query_db: AsyncSession, page_object: Schema_model_refsModel):
        """
        编辑JSON Schema 模型引用关系信息service

        :param query_db: orm对象
        :param page_object: 编辑JSON Schema 模型引用关系对象
        :return: 编辑JSON Schema 模型引用关系校验结果
        """
        page_object = Schema_model_refsModel.model_validate(page_object.model_dump())
        edit_schema_model_refs = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        schema_model_refs_info = await cls.schema_model_refs_detail_services(query_db, page_object.ref_id)
        if schema_model_refs_info.ref_id:
            try:
                await Schema_model_refsDao.edit_schema_model_refs_dao(query_db, edit_schema_model_refs)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='JSON Schema 模型引用关系不存在')

    @classmethod
    async def delete_schema_model_refs_services(cls, query_db: AsyncSession, page_object: DeleteSchema_model_refsModel):
        """
        删除JSON Schema 模型引用关系信息service

        :param query_db: orm对象
        :param page_object: 删除JSON Schema 模型引用关系对象
        :return: 删除JSON Schema 模型引用关系校验结果
        """
        if page_object.ref_ids:
            ref_id_list = page_object.ref_ids.split(',')
            try:
                for ref_id in ref_id_list:
                    ref_id_obj = Schema_model_refsModel.model_validate({'ref_id': ref_id}).ref_id
                    await Schema_model_refsDao.delete_schema_model_refs_dao(query_db, Schema_model_refsModel(refId=ref_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入引用ID为空')

    @classmethod
    async def schema_model_refs_detail_services(cls, query_db: AsyncSession, ref_id: str):
        """
        获取JSON Schema 模型引用关系详细信息service

        :param query_db: orm对象
        :param ref_id: 引用ID
        :return: 引用ID对应的信息
        """
        schema_model_refs = await Schema_model_refsDao.get_schema_model_refs_detail_by_id(query_db, ref_id=ref_id)
        if schema_model_refs:
            result = Schema_model_refsModel(**CamelCaseUtil.transform_result(schema_model_refs))
        else:
            result = Schema_model_refsModel(**dict())

        return result

    @staticmethod
    async def export_schema_model_refs_list_services(schema_model_refs_list: List):
        """
        导出JSON Schema 模型引用关系信息service

        :param schema_model_refs_list: JSON Schema 模型引用关系信息列表
        :return: JSON Schema 模型引用关系信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'refId': '引用ID',
            'modelId': '模型ID',
            'refModelId': '被引用模型ID',
            'refPath': '引用路径',
            'refVersion': '引用版本',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'sortNo': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(schema_model_refs_list, mapping_dict)

        return binary_data
