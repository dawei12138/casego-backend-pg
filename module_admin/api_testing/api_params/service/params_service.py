from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_params.dao.params_dao import ParamsDao
from module_admin.api_testing.api_params.entity.vo.params_vo import DeleteParamsModel, ParamsModel, ParamsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ParamsService:
    """
    接口请求参数模块服务层
    """

    @classmethod
    async def get_params_list_services(
        cls, query_db: AsyncSession, query_object: ParamsPageQueryModel, is_page: bool = False
    ):
        """
        获取接口请求参数列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口请求参数列表信息对象
        """
        params_list_result = await ParamsDao.get_params_list(query_db, query_object, is_page)

        return params_list_result


    @classmethod
    async def add_params_services(cls, query_db: AsyncSession, page_object: ParamsModel):
        """
        新增接口请求参数信息service

        :param query_db: orm对象
        :param page_object: 新增接口请求参数对象
        :return: 新增接口请求参数校验结果
        """
        try:
            await ParamsDao.add_params_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_params_services(cls, query_db: AsyncSession, page_object: ParamsModel):
        """
        编辑接口请求参数信息service

        :param query_db: orm对象
        :param page_object: 编辑接口请求参数对象
        :return: 编辑接口请求参数校验结果
        """
        edit_params = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        params_info = await cls.params_detail_services(query_db, page_object.param_id)
        if params_info.param_id:
            try:
                await ParamsDao.edit_params_dao(query_db, edit_params)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口请求参数不存在')

    @classmethod
    async def delete_params_services(cls, query_db: AsyncSession, page_object: DeleteParamsModel):
        """
        删除接口请求参数信息service

        :param query_db: orm对象
        :param page_object: 删除接口请求参数对象
        :return: 删除接口请求参数校验结果
        """
        if page_object.param_ids:
            param_id_list = page_object.param_ids.split(',')
            try:
                for param_id in param_id_list:
                    await ParamsDao.delete_params_dao(query_db, ParamsModel(paramId=param_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def params_detail_services(cls, query_db: AsyncSession, param_id: int):
        """
        获取接口请求参数详细信息service

        :param query_db: orm对象
        :param param_id: ID
        :return: ID对应的信息
        """
        params = await ParamsDao.get_params_detail_by_id(query_db, param_id=param_id)
        if params:
            result = ParamsModel(**CamelCaseUtil.transform_result(params))
        else:
            result = ParamsModel(**dict())

        return result

    @staticmethod
    async def export_params_list_services(params_list: List):
        """
        导出接口请求参数信息service

        :param params_list: 接口请求参数信息列表
        :return: 接口请求参数信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'paramId': 'ID',
            'caseId': '关联的测试用例ID',
            'key': '参数键名',
            'value': '参数值',
            'isRun': '是否启用该参数',
            'description': '描述',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(params_list, mapping_dict)

        return binary_data
