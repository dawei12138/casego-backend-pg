from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.dao.file_dao import FileDao
from module_admin.system.entity.vo.file_vo import DeleteFileModel, FileModel, FilePageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class FileService:
    """
    附件管理模块服务层
    """

    @classmethod
    async def get_file_list_services(
        cls, query_db: AsyncSession, query_object: FilePageQueryModel, is_page: bool = False
    ):
        """
        获取附件管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 附件管理列表信息对象
        """
        file_list_result = await FileDao.get_file_list(query_db, query_object, is_page)

        return file_list_result


    @classmethod
    async def add_file_services(cls, query_db: AsyncSession, page_object: FileModel):
        """
        新增附件管理信息service

        :param query_db: orm对象
        :param page_object: 新增附件管理对象
        :return: 新增附件管理校验结果
        """
        try:
            await FileDao.add_file_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_file_services(cls, query_db: AsyncSession, page_object: FileModel):
        """
        编辑附件管理信息service

        :param query_db: orm对象
        :param page_object: 编辑附件管理对象
        :return: 编辑附件管理校验结果
        """
        edit_file = page_object.model_dump(exclude_unset=True, exclude={'del_flag'})
        file_info = await cls.file_detail_services(query_db, page_object.file_id)
        if file_info.file_id:
            try:
                await FileDao.edit_file_dao(query_db, edit_file)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='附件管理不存在')

    @classmethod
    async def delete_file_services(cls, query_db: AsyncSession, page_object: DeleteFileModel):
        """
        删除附件管理信息service

        :param query_db: orm对象
        :param page_object: 删除附件管理对象
        :return: 删除附件管理校验结果
        """
        if page_object.file_ids:
            file_id_list = page_object.file_ids.split(',')
            try:
                for file_id in file_id_list:
                    await FileDao.delete_file_dao(query_db, FileModel(fileId=file_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入为空')

    @classmethod
    async def file_detail_services(cls, query_db: AsyncSession, file_id: int):
        """
        获取附件管理详细信息service

        :param query_db: orm对象
        :param file_id: 
        :return: 对应的信息
        """
        file = await FileDao.get_file_detail_by_id(query_db, file_id=file_id)
        if file:
            result = FileModel(**CamelCaseUtil.transform_result(file))
        else:
            result = FileModel(**dict())

        return result

    @staticmethod
    async def export_file_list_services(file_list: List):
        """
        导出附件管理信息service

        :param file_list: 附件管理信息列表
        :return: 附件管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'fileId': '',
            'originalName': '文件原始名称',
            'storedName': '文件存储名称',
            'fileExt': '文件扩展名',
            'mimeType': '文件 MIME 类型',
            'fileSize': '文件大小',
            'filePath': '文件存储路径',
            'fileUrl': '文件访问 URL',
            'storageType': '存储位置类型',
            'isTemp': '是否临时文件',
            'fileHash': '文件哈希值',
            'bizTag': '业务标签',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(file_list, mapping_dict)

        return binary_data
