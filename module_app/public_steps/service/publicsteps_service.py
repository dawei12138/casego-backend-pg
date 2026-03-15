from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.public_steps.dao.publicsteps_dao import PublicstepsDao
from module_app.public_steps.entity.vo.publicsteps_vo import DeletePublicstepsModel, PublicstepsModel, PublicstepsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class PublicstepsService:
    """
    公共步骤模块服务层
    """

    @classmethod
    async def get_publicsteps_list_services(
        cls, query_db: AsyncSession, query_object: PublicstepsPageQueryModel, is_page: bool = False
    ):
        """
        获取公共步骤列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公共步骤列表信息对象
        """
        publicsteps_list_result = await PublicstepsDao.get_publicsteps_list(query_db, query_object, is_page)

        return publicsteps_list_result


    @classmethod
    async def add_publicsteps_services(cls, query_db: AsyncSession, page_object: PublicstepsModel):
        """
        新增公共步骤信息service

        :param query_db: orm对象
        :param page_object: 新增公共步骤对象
        :return: 新增公共步骤校验结果
        """
        try:
            await PublicstepsDao.add_publicsteps_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_publicsteps_services(cls, query_db: AsyncSession, page_object: PublicstepsModel):
        """
        编辑公共步骤信息service

        :param query_db: orm对象
        :param page_object: 编辑公共步骤对象
        :return: 编辑公共步骤校验结果
        """
        edit_publicsteps = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        publicsteps_info = await cls.publicsteps_detail_services(query_db, page_object.id)
        if publicsteps_info.id:
            try:
                await PublicstepsDao.edit_publicsteps_dao(query_db, edit_publicsteps)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='公共步骤不存在')

    @classmethod
    async def delete_publicsteps_services(cls, query_db: AsyncSession, page_object: DeletePublicstepsModel):
        """
        删除公共步骤信息service

        :param query_db: orm对象
        :param page_object: 删除公共步骤对象
        :return: 删除公共步骤校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await PublicstepsDao.delete_publicsteps_dao(query_db, PublicstepsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def publicsteps_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取公共步骤详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        publicsteps = await PublicstepsDao.get_publicsteps_detail_by_id(query_db, id=id)
        if publicsteps:
            result = PublicstepsModel(**CamelCaseUtil.transform_result(publicsteps))
        else:
            result = PublicstepsModel(**dict())

        return result

    @staticmethod
    async def export_publicsteps_list_services(publicsteps_list: List):
        """
        导出公共步骤信息service

        :param publicsteps_list: 公共步骤信息列表
        :return: 公共步骤信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'name': '公共步骤名称',
            'platform': '平台类型',
            'projectId': '所属项目ID',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(publicsteps_list, mapping_dict)

        return binary_data
