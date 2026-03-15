from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.cases.dao.cases_dao import CasesDao
from module_app.cases.entity.vo.cases_vo import DeleteCasesModel, CasesModel, CasesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class CasesService:
    """
    测试用例模块服务层
    """

    @classmethod
    async def get_cases_list_services(
        cls, query_db: AsyncSession, query_object: CasesPageQueryModel, is_page: bool = False
    ):
        """
        获取测试用例列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试用例列表信息对象
        """
        cases_list_result = await CasesDao.get_cases_list(query_db, query_object, is_page)

        return cases_list_result


    @classmethod
    async def add_cases_services(cls, query_db: AsyncSession, page_object: CasesModel):
        """
        新增测试用例信息service

        :param query_db: orm对象
        :param page_object: 新增测试用例对象
        :return: 新增测试用例校验结果
        """
        try:
            await CasesDao.add_cases_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_cases_services(cls, query_db: AsyncSession, page_object: CasesModel):
        """
        编辑测试用例信息service

        :param query_db: orm对象
        :param page_object: 编辑测试用例对象
        :return: 编辑测试用例校验结果
        """
        edit_cases = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        cases_info = await cls.cases_detail_services(query_db, page_object.id)
        if cases_info.id:
            try:
                await CasesDao.edit_cases_dao(query_db, edit_cases)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='测试用例不存在')

    @classmethod
    async def delete_cases_services(cls, query_db: AsyncSession, page_object: DeleteCasesModel):
        """
        删除测试用例信息service

        :param query_db: orm对象
        :param page_object: 删除测试用例对象
        :return: 删除测试用例校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await CasesDao.delete_cases_dao(query_db, CasesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def cases_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取测试用例详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        cases = await CasesDao.get_cases_detail_by_id(query_db, id=id)
        if cases:
            result = CasesModel(**CamelCaseUtil.transform_result(cases))
        else:
            result = CasesModel(**dict())

        return result

    @staticmethod
    async def export_cases_list_services(cases_list: List):
        """
        导出测试用例信息service

        :param cases_list: 测试用例信息列表
        :return: 测试用例信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'name': '用例名称',
            'des': '用例描述',
            'designer': '设计者',
            'platform': '平台类型',
            'projectId': '所属项目ID',
            'moduleId': '所属模块ID',
            'version': '版本号',
            'editTime': '最后编辑时间',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(cases_list, mapping_dict)

        return binary_data
