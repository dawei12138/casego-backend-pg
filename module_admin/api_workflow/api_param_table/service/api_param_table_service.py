from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import Api_param_itemPageQueryModel, \
    Api_param_itemModel
from module_admin.api_workflow.api_param_item.service.api_param_item_service import Api_param_itemService
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.api_param_table.dao.api_param_table_dao import Api_param_tableDao
from module_admin.api_workflow.api_param_table.entity.vo.api_param_table_vo import DeleteApi_param_tableModel, \
    Api_param_tableModel, Api_param_tablePageQueryModel, Api_param_table_itemModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Api_param_tableService:
    """
    参数化数据主模块服务层
    """

    @classmethod
    async def get_api_param_table_list_services(
            cls, query_db: AsyncSession, query_object: Api_param_tablePageQueryModel, is_page: bool = False
    ):
        """
        获取参数化数据主列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 参数化数据主列表信息对象
        """
        api_param_table_list_result = await Api_param_tableDao.get_api_param_table_list(query_db, query_object, is_page)

        return api_param_table_list_result

    @classmethod
    async def add_api_param_table_services(cls, query_db: AsyncSession, page_object: Api_param_tableModel):
        """
        新增参数化数据主信息service

        :param query_db: orm对象
        :param page_object: 新增参数化数据主对象
        :return: 新增参数化数据主校验结果
        """
        try:
            await Api_param_tableDao.add_api_param_table_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_api_param_table_services(cls, query_db: AsyncSession, page_object: Api_param_tableModel):
        """
        编辑参数化数据主信息service

        :param query_db: orm对象
        :param page_object: 编辑参数化数据主对象
        :return: 编辑参数化数据主校验结果
        """
        edit_api_param_table = page_object.model_dump(exclude_unset=True,
                                                      exclude={'create_by', 'create_time', 'del_flag'})
        api_param_table_info = await cls.api_param_table_detail_services(query_db, page_object.parameterization_id)
        if api_param_table_info.parameterization_id:
            try:
                await Api_param_tableDao.edit_api_param_table_dao(query_db, edit_api_param_table)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='参数化数据主不存在')

    @classmethod
    async def delete_api_param_table_services(cls, query_db: AsyncSession, page_object: DeleteApi_param_tableModel):
        """
        删除参数化数据主信息service

        :param query_db: orm对象
        :param page_object: 删除参数化数据主对象
        :return: 删除参数化数据主校验结果
        """
        if page_object.parameterization_ids:
            parameterization_id_list = page_object.parameterization_ids.split(',')
            try:
                for parameterization_id in parameterization_id_list:
                    await Api_param_tableDao.delete_api_param_table_dao(query_db, Api_param_tableModel(
                        parameterizationId=parameterization_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def api_param_table_detail_services(cls, query_db: AsyncSession, parameterization_id: int):
        """
        获取参数化数据主详细信息service

        :param query_db: orm对象
        :param parameterization_id: 主键ID
        :return: 主键ID对应的信息
        """
        api_param_table = await Api_param_tableDao.get_api_param_table_detail_by_id(query_db,
                                                                                    parameterization_id=parameterization_id)
        if api_param_table:
            result = Api_param_tableModel(**CamelCaseUtil.transform_result(api_param_table))
        else:
            result = Api_param_tableModel(**dict())

        return result

    @classmethod
    async def api_param_table_detail_all_services(cls, query_db: AsyncSession, parameterization_id: int,
                                                  api_param_table_page_query: Api_param_tablePageQueryModel):
        """
        获取参数化数据主详细信息service

        :param api_param_table_page_query:
        :param query_db: orm对象
        :param parameterization_id: 主键ID
        :return: 主键ID对应的信息
        """

        api_param_table = await Api_param_tableDao.get_api_param_table_detail_by_id(query_db,
                                                                                    parameterization_id=parameterization_id)
        api_param_item_page_query_result = await Api_param_itemService.get_api_param_item_list_services(query_db,
                                                                                                        Api_param_itemPageQueryModel(
                                                                                                            parameterization_id=parameterization_id,
                                                                                                            page_size=api_param_table_page_query.page_size,
                                                                                                            page_num=api_param_table_page_query.page_num),
                                                                                                        is_page=True)

        if api_param_table:
            api_param_table_result = Api_param_table_itemModel(**CamelCaseUtil.transform_result(api_param_table))
            api_param_table_result.page_num = api_param_table_page_query.page_num
            api_param_table_result.page_size = api_param_table_page_query.page_size
            api_param_table_result.total = api_param_item_page_query_result.total

            api_param_table_result.items = [Api_param_itemModel(**CamelCaseUtil.transform_result(i)) for i in
                                            api_param_item_page_query_result.rows]
        else:
            api_param_table_result = Api_param_tableModel(**dict())

        return api_param_table_result

    @staticmethod
    async def export_api_param_table_list_services(api_param_table_list: List):
        """
        导出参数化数据主信息service

        :param api_param_table_list: 参数化数据主信息列表
        :return: 参数化数据主信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'parameterizationId': '主键ID',
            'workflowId': '所属执行器ID',
            'name': '参数表名称',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(api_param_table_list, mapping_dict)

        return binary_data
