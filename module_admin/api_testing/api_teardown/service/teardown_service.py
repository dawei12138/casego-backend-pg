from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_teardown.dao.teardown_dao import TeardownDao
from module_admin.api_testing.api_teardown.entity.vo.teardown_vo import DeleteTeardownModel, TeardownModel, TeardownPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class TeardownService:
    """
    接口后置操作模块服务层
    """

    @classmethod
    async def get_teardown_list_services(
        cls, query_db: AsyncSession, query_object: TeardownPageQueryModel, is_page: bool = False
    ):
        """
        获取接口后置操作列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口后置操作列表信息对象
        """
        teardown_list_result = await TeardownDao.get_teardown_list(query_db, query_object, is_page)

        return teardown_list_result


    @classmethod
    async def add_teardown_services(cls, query_db: AsyncSession, page_object: TeardownModel):
        """
        新增接口后置操作信息service

        :param query_db: orm对象
        :param page_object: 新增接口后置操作对象
        :return: 新增接口后置操作校验结果
        """
        try:
            await TeardownDao.add_teardown_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_teardown_services(cls, query_db: AsyncSession, page_object: TeardownModel):
        """
        编辑接口后置操作信息service

        :param query_db: orm对象
        :param page_object: 编辑接口后置操作对象
        :return: 编辑接口后置操作校验结果
        """
        edit_teardown = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        teardown_info = await cls.teardown_detail_services(query_db, page_object.teardown_id)
        if teardown_info.teardown_id:
            try:
                await TeardownDao.edit_teardown_dao(query_db, edit_teardown)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口后置操作不存在')

    @classmethod
    async def delete_teardown_services(cls, query_db: AsyncSession, page_object: DeleteTeardownModel):
        """
        删除接口后置操作信息service

        :param query_db: orm对象
        :param page_object: 删除接口后置操作对象
        :return: 删除接口后置操作校验结果
        """
        if page_object.teardown_ids:
            teardown_id_list = page_object.teardown_ids.split(',')
            try:
                for teardown_id in teardown_id_list:
                    await TeardownDao.delete_teardown_dao(query_db, TeardownModel(teardownId=teardown_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入操作ID为空')

    @classmethod
    async def teardown_detail_services(cls, query_db: AsyncSession, teardown_id: int):
        """
        获取接口后置操作详细信息service

        :param query_db: orm对象
        :param teardown_id: 操作ID
        :return: 操作ID对应的信息
        """
        teardown = await TeardownDao.get_teardown_detail_by_id(query_db, teardown_id=teardown_id)
        if teardown:
            result = TeardownModel(**CamelCaseUtil.transform_result(teardown))
        else:
            result = TeardownModel(**dict())

        return result

    @staticmethod
    async def export_teardown_list_services(teardown_list: List):
        """
        导出接口后置操作信息service

        :param teardown_list: 接口后置操作信息列表
        :return: 接口后置操作信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'teardownId': '操作ID',
            'name': '操作名称',
            'caseId': '关联的测试用例ID',
            'teardownType': '操作类型 (extract_variable, db_operation, custom_script, wait_time)',
            'extractVariableMethod': '提取响应的方法： response_textresponse_jsonresponse_xmlresponse_headerresponse_cookie',
            'jsonpath': 'jsonpath提取表达式',
            'extractIndex': '提取索引',
            'extractIndexIsRun': '是否执行提取索引操作',
            'variableName': '变量名称',
            'databaseId': '数据库连接ID',
            'dbOperation': '数据库操作语句',
            'script': '自定义脚本语句',
            'waitTime': '等待时间',
            'isRun': '是否执行该后置操作',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(teardown_list, mapping_dict)

        return binary_data
