from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.steps.dao.steps_dao import StepsDao
from module_app.steps.entity.vo.steps_vo import DeleteStepsModel, StepsModel, StepsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class StepsService:
    """
    测试步骤模块服务层
    """

    @classmethod
    async def get_steps_list_services(
        cls, query_db: AsyncSession, query_object: StepsPageQueryModel, is_page: bool = False
    ):
        """
        获取测试步骤列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试步骤列表信息对象
        """
        steps_list_result = await StepsDao.get_steps_list(query_db, query_object, is_page)

        return steps_list_result


    @classmethod
    async def add_steps_services(cls, query_db: AsyncSession, page_object: StepsModel):
        """
        新增测试步骤信息service

        :param query_db: orm对象
        :param page_object: 新增测试步骤对象
        :return: 新增测试步骤校验结果
        """
        try:
            await StepsDao.add_steps_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_steps_services(cls, query_db: AsyncSession, page_object: StepsModel):
        """
        编辑测试步骤信息service

        :param query_db: orm对象
        :param page_object: 编辑测试步骤对象
        :return: 编辑测试步骤校验结果
        """
        edit_steps = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        steps_info = await cls.steps_detail_services(query_db, page_object.id)
        if steps_info.id:
            try:
                await StepsDao.edit_steps_dao(query_db, edit_steps)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='测试步骤不存在')

    @classmethod
    async def delete_steps_services(cls, query_db: AsyncSession, page_object: DeleteStepsModel):
        """
        删除测试步骤信息service

        :param query_db: orm对象
        :param page_object: 删除测试步骤对象
        :return: 删除测试步骤校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await StepsDao.delete_steps_dao(query_db, StepsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def steps_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取测试步骤详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        steps = await StepsDao.get_steps_detail_by_id(query_db, id=id)
        if steps:
            result = StepsModel(**CamelCaseUtil.transform_result(steps))
        else:
            result = StepsModel(**dict())

        return result

    @staticmethod
    async def export_steps_list_services(steps_list: List):
        """
        导出测试步骤信息service

        :param steps_list: 测试步骤信息列表
        :return: 测试步骤信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'caseId': '所属测试用例ID',
            'projectId': '所属项目ID',
            'parentId': '父级步骤ID(用于条件分支)',
            'stepType': '步骤类型: click/sendKeys/swipe/getText等',
            'content': '输入内容/操作参数',
            'text': '附加信息(JSON格式)',
            'platform': '平台类型',
            'error': '异常处理方式',
            'conditionType': '条件类型',
            'disabled': '是否禁用',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(steps_list, mapping_dict)

        return binary_data
