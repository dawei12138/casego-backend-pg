from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.steps_elements.dao.steps_elements_dao import Steps_elementsDao
from module_app.steps_elements.entity.vo.steps_elements_vo import DeleteSteps_elementsModel, Steps_elementsModel, Steps_elementsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Steps_elementsService:
    """
    步骤-元素关联模块服务层
    """

    @classmethod
    async def get_steps_elements_list_services(
        cls, query_db: AsyncSession, query_object: Steps_elementsPageQueryModel, is_page: bool = False
    ):
        """
        获取步骤-元素关联列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 步骤-元素关联列表信息对象
        """
        steps_elements_list_result = await Steps_elementsDao.get_steps_elements_list(query_db, query_object, is_page)

        return steps_elements_list_result


    @classmethod
    async def add_steps_elements_services(cls, query_db: AsyncSession, page_object: Steps_elementsModel):
        """
        新增步骤-元素关联信息service

        :param query_db: orm对象
        :param page_object: 新增步骤-元素关联对象
        :return: 新增步骤-元素关联校验结果
        """
        try:
            await Steps_elementsDao.add_steps_elements_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_steps_elements_services(cls, query_db: AsyncSession, page_object: Steps_elementsModel):
        """
        编辑步骤-元素关联信息service

        :param query_db: orm对象
        :param page_object: 编辑步骤-元素关联对象
        :return: 编辑步骤-元素关联校验结果
        """
        edit_steps_elements = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        steps_elements_info = await cls.steps_elements_detail_services(query_db, page_object.steps_id)
        if steps_elements_info.steps_id:
            try:
                await Steps_elementsDao.edit_steps_elements_dao(query_db, edit_steps_elements)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='步骤-元素关联不存在')

    @classmethod
    async def delete_steps_elements_services(cls, query_db: AsyncSession, page_object: DeleteSteps_elementsModel):
        """
        删除步骤-元素关联信息service

        :param query_db: orm对象
        :param page_object: 删除步骤-元素关联对象
        :return: 删除步骤-元素关联校验结果
        """
        if page_object.steps_ids:
            steps_id_list = page_object.steps_ids.split(',')
            try:
                for steps_id in steps_id_list:
                    await Steps_elementsDao.delete_steps_elements_dao(query_db, Steps_elementsModel(stepsId=steps_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入步骤ID为空')

    @classmethod
    async def steps_elements_detail_services(cls, query_db: AsyncSession, steps_id: int):
        """
        获取步骤-元素关联详细信息service

        :param query_db: orm对象
        :param steps_id: 步骤ID
        :return: 步骤ID对应的信息
        """
        steps_elements = await Steps_elementsDao.get_steps_elements_detail_by_id(query_db, steps_id=steps_id)
        if steps_elements:
            result = Steps_elementsModel(**CamelCaseUtil.transform_result(steps_elements))
        else:
            result = Steps_elementsModel(**dict())

        return result

    @staticmethod
    async def export_steps_elements_list_services(steps_elements_list: List):
        """
        导出步骤-元素关联信息service

        :param steps_elements_list: 步骤-元素关联信息列表
        :return: 步骤-元素关联信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'stepsId': '步骤ID',
            'elementsId': '元素ID',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(steps_elements_list, mapping_dict)

        return binary_data
