from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_assertions.dao.assertions_dao import AssertionsDao
from module_admin.api_testing.api_assertions.entity.vo.assertions_vo import DeleteAssertionsModel, AssertionsModel, AssertionsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class AssertionsService:
    """
    接口断言模块服务层
    """

    @classmethod
    async def get_assertions_list_services(
        cls, query_db: AsyncSession, query_object: AssertionsPageQueryModel, is_page: bool = False
    ):
        """
        获取接口断言列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口断言列表信息对象
        """
        assertions_list_result = await AssertionsDao.get_assertions_list(query_db, query_object, is_page)

        return assertions_list_result


    @classmethod
    async def add_assertions_services(cls, query_db: AsyncSession, page_object: AssertionsModel):
        """
        新增接口断言信息service

        :param query_db: orm对象
        :param page_object: 新增接口断言对象
        :return: 新增接口断言校验结果
        """
        try:
            await AssertionsDao.add_assertions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_assertions_services(cls, query_db: AsyncSession, page_object: AssertionsModel):
        """
        编辑接口断言信息service

        :param query_db: orm对象
        :param page_object: 编辑接口断言对象
        :return: 编辑接口断言校验结果
        """
        edit_assertions = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        assertions_info = await cls.assertions_detail_services(query_db, page_object.assertion_id)
        if assertions_info.assertion_id:
            try:
                await AssertionsDao.edit_assertions_dao(query_db, edit_assertions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口断言不存在')

    @classmethod
    async def delete_assertions_services(cls, query_db: AsyncSession, page_object: DeleteAssertionsModel):
        """
        删除接口断言信息service

        :param query_db: orm对象
        :param page_object: 删除接口断言对象
        :return: 删除接口断言校验结果
        """
        if page_object.assertion_ids:
            assertion_id_list = page_object.assertion_ids.split(',')
            try:
                for assertion_id in assertion_id_list:
                    await AssertionsDao.delete_assertions_dao(query_db, AssertionsModel(assertionId=assertion_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入断言ID为空')

    @classmethod
    async def assertions_detail_services(cls, query_db: AsyncSession, assertion_id: int):
        """
        获取接口断言详细信息service

        :param query_db: orm对象
        :param assertion_id: 断言ID
        :return: 断言ID对应的信息
        """
        assertions = await AssertionsDao.get_assertions_detail_by_id(query_db, assertion_id=assertion_id)
        if assertions:
            result = AssertionsModel(**CamelCaseUtil.transform_result(assertions))
        else:
            result = AssertionsModel(**dict())

        return result

    @staticmethod
    async def export_assertions_list_services(assertions_list: List):
        """
        导出接口断言信息service

        :param assertions_list: 接口断言信息列表
        :return: 接口断言信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'assertionId': '断言ID',
            'caseId': '关联的测试用例ID',
            'jsonpath': 'JSONPath表达式OR提取方法',
            'jsonpathIndex': 'JSONPath提取索引',
            'assertionMethod': '断言 (==, !=, >等)',
            'value': '预期值',
            'assertType': '断言类型 (可选)',
            'isRun': '是否执行该断言',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(assertions_list, mapping_dict)

        return binary_data
