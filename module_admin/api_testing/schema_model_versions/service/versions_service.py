from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.schema_model_versions.dao.versions_dao import VersionsDao
from module_admin.api_testing.schema_model_versions.entity.vo.versions_vo import DeleteVersionsModel, VersionsModel, VersionsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class VersionsService:
    """
    JSON Schema 模型版本模块服务层
    """

    @classmethod
    async def get_versions_list_services(
        cls, query_db: AsyncSession, query_object: VersionsPageQueryModel, is_page: bool = False
    ):
        """
        获取JSON Schema 模型版本列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: JSON Schema 模型版本列表信息对象
        """
        versions_list_result = await VersionsDao.get_versions_list(query_db, query_object, is_page)

        return versions_list_result


    @classmethod
    async def add_versions_services(cls, query_db: AsyncSession, page_object: VersionsModel):
        """
        新增JSON Schema 模型版本信息service

        :param query_db: orm对象
        :param page_object: 新增JSON Schema 模型版本对象
        :return: 新增JSON Schema 模型版本校验结果
        """
        page_object = VersionsModel.model_validate(page_object.model_dump())
        try:
            await VersionsDao.add_versions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_versions_services(cls, query_db: AsyncSession, page_object: VersionsModel):
        """
        编辑JSON Schema 模型版本信息service

        :param query_db: orm对象
        :param page_object: 编辑JSON Schema 模型版本对象
        :return: 编辑JSON Schema 模型版本校验结果
        """
        page_object = VersionsModel.model_validate(page_object.model_dump())
        edit_versions = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        versions_info = await cls.versions_detail_services(query_db, page_object.version_id)
        if versions_info.version_id:
            try:
                await VersionsDao.edit_versions_dao(query_db, edit_versions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='JSON Schema 模型版本不存在')

    @classmethod
    async def delete_versions_services(cls, query_db: AsyncSession, page_object: DeleteVersionsModel):
        """
        删除JSON Schema 模型版本信息service

        :param query_db: orm对象
        :param page_object: 删除JSON Schema 模型版本对象
        :return: 删除JSON Schema 模型版本校验结果
        """
        if page_object.version_ids:
            version_id_list = page_object.version_ids.split(',')
            try:
                for version_id in version_id_list:
                    version_id_obj = VersionsModel.model_validate({'version_id': version_id}).version_id
                    await VersionsDao.delete_versions_dao(query_db, VersionsModel(versionId=version_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入版本ID为空')

    @classmethod
    async def versions_detail_services(cls, query_db: AsyncSession, version_id: str):
        """
        获取JSON Schema 模型版本详细信息service

        :param query_db: orm对象
        :param version_id: 版本ID
        :return: 版本ID对应的信息
        """
        versions = await VersionsDao.get_versions_detail_by_id(query_db, version_id=version_id)
        if versions:
            result = VersionsModel(**CamelCaseUtil.transform_result(versions))
        else:
            result = VersionsModel(**dict())

        return result

    @staticmethod
    async def export_versions_list_services(versions_list: List):
        """
        导出JSON Schema 模型版本信息service

        :param versions_list: JSON Schema 模型版本信息列表
        :return: JSON Schema 模型版本信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'versionId': '版本ID',
            'modelId': '模型ID',
            'version': '内部版本号',
            'revision': '语义版本号',
            'schemaSnapshot': 'Schema快照',
            'nodesSnapshot': '节点快照',
            'changeLog': '变更说明',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'sortNo': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(versions_list, mapping_dict)

        return binary_data
