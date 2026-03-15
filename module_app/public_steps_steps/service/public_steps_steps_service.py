from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.public_steps_steps.dao.public_steps_steps_dao import Public_steps_stepsDao
from module_app.public_steps_steps.entity.vo.public_steps_steps_vo import DeletePublic_steps_stepsModel, Public_steps_stepsModel, Public_steps_stepsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Public_steps_stepsService:
    """
    公共步骤-步骤关联模块服务层
    """

    @classmethod
    async def get_public_steps_steps_list_services(
        cls, query_db: AsyncSession, query_object: Public_steps_stepsPageQueryModel, is_page: bool = False
    ):
        """
        获取公共步骤-步骤关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 公共步骤-步骤关联列表信息对象
        """
        public_steps_steps_list_result = await Public_steps_stepsDao.get_public_steps_steps_list(query_db, query_object, is_page)

        return public_steps_steps_list_result


    @classmethod
    async def add_public_steps_steps_services(cls, query_db: AsyncSession, page_object: Public_steps_stepsModel):
        """
        新增公共步骤-步骤关联信息service

        :param query_db: orm对象
        :param page_object: 新增公共步骤-步骤关联对象
        :return: 新增公共步骤-步骤关联校验结果
        """
        try:
            await Public_steps_stepsDao.add_public_steps_steps_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_public_steps_steps_services(cls, query_db: AsyncSession, page_object: Public_steps_stepsModel):
        """
        编辑公共步骤-步骤关联信息service

        :param query_db: orm对象
        :param page_object: 编辑公共步骤-步骤关联对象
        :return: 编辑公共步骤-步骤关联校验结果
        """
        edit_public_steps_steps = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        public_steps_steps_info = await cls.public_steps_steps_detail_services(query_db, page_object.public_steps_id)
        if public_steps_steps_info.public_steps_id:
            try:
                await Public_steps_stepsDao.edit_public_steps_steps_dao(query_db, edit_public_steps_steps)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='公共步骤-步骤关联不存在')

    @classmethod
    async def delete_public_steps_steps_services(cls, query_db: AsyncSession, page_object: DeletePublic_steps_stepsModel):
        """
        删除公共步骤-步骤关联信息service

        :param query_db: orm对象
        :param page_object: 删除公共步骤-步骤关联对象
        :return: 删除公共步骤-步骤关联校验结果
        """
        if page_object.public_steps_ids:
            public_steps_id_list = page_object.public_steps_ids.split(',')
            try:
                for public_steps_id in public_steps_id_list:
                    await Public_steps_stepsDao.delete_public_steps_steps_dao(query_db, Public_steps_stepsModel(publicStepsId=public_steps_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入公共步骤ID为空')

    @classmethod
    async def public_steps_steps_detail_services(cls, query_db: AsyncSession, public_steps_id: int):
        """
        获取公共步骤-步骤关联详细信息service

        :param query_db: orm对象
        :param public_steps_id: 公共步骤ID
        :return: 公共步骤ID对应的信息
        """
        public_steps_steps = await Public_steps_stepsDao.get_public_steps_steps_detail_by_id(query_db, public_steps_id=public_steps_id)
        if public_steps_steps:
            result = Public_steps_stepsModel(**CamelCaseUtil.transform_result(public_steps_steps))
        else:
            result = Public_steps_stepsModel(**dict())

        return result

    @staticmethod
    async def export_public_steps_steps_list_services(public_steps_steps_list: List):
        """
        导出公共步骤-步骤关联信息service

        :param public_steps_steps_list: 公共步骤-步骤关联信息列表
        :return: 公共步骤-步骤关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'publicStepsId': '公共步骤ID',
            'stepsId': '步骤ID',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(public_steps_steps_list, mapping_dict)

        return binary_data
