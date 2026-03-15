from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.api_param_item.dao.api_param_item_dao import Api_param_itemDao
from module_admin.api_workflow.api_param_item.entity.vo.api_param_item_vo import DeleteApi_param_itemModel, Api_param_itemModel, Api_param_itemPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Api_param_itemService:
    """
    参数化数据行模块服务层
    """

    @classmethod
    async def get_api_param_item_list_services(
        cls, query_db: AsyncSession, query_object: Api_param_itemPageQueryModel, is_page: bool = False
    ):
        """
        获取参数化数据行列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 参数化数据行列表信息对象
        """
        api_param_item_list_result = await Api_param_itemDao.get_api_param_item_list(query_db, query_object, is_page)

        return api_param_item_list_result


    @classmethod
    async def add_api_param_item_services(cls, query_db: AsyncSession, page_object: Api_param_itemModel):
        """
        新增参数化数据行信息service

        :param query_db: orm对象
        :param page_object: 新增参数化数据行对象
        :return: 新增参数化数据行校验结果
        """
        try:
            await Api_param_itemDao.add_api_param_item_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_api_param_item_services(cls, query_db: AsyncSession, page_object: Api_param_itemModel):
        """
        编辑参数化数据行信息service

        :param query_db: orm对象
        :param page_object: 编辑参数化数据行对象
        :return: 编辑参数化数据行校验结果
        """
        edit_api_param_item = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        api_param_item_info = await cls.api_param_item_detail_services(query_db, page_object.key_id)
        if api_param_item_info.key_id:
            try:
                await Api_param_itemDao.edit_api_param_item_dao(query_db, edit_api_param_item)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='参数化数据行不存在')

    @classmethod
    async def delete_api_param_item_services(cls, query_db: AsyncSession, page_object: DeleteApi_param_itemModel):
        """
        删除参数化数据行信息service

        :param query_db: orm对象
        :param page_object: 删除参数化数据行对象
        :return: 删除参数化数据行校验结果
        """
        if page_object.key_ids:
            key_id_list = page_object.key_ids.split(',')
            try:
                for key_id in key_id_list:
                    await Api_param_itemDao.delete_api_param_item_dao(query_db, Api_param_itemModel(keyId=key_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def api_param_item_detail_services(cls, query_db: AsyncSession, key_id: int):
        """
        获取参数化数据行详细信息service

        :param query_db: orm对象
        :param key_id: 主键ID
        :return: 主键ID对应的信息
        """
        api_param_item = await Api_param_itemDao.get_api_param_item_detail_by_id(query_db, key_id=key_id)
        if api_param_item:
            result = Api_param_itemModel(**CamelCaseUtil.transform_result(api_param_item))
        else:
            result = Api_param_itemModel(**dict())

        return result

    @staticmethod
    async def export_api_param_item_list_services(api_param_item_list: List):
        """
        导出参数化数据行信息service

        :param api_param_item_list: 参数化数据行信息列表
        :return: 参数化数据行信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'keyId': '主键ID',
            'parameterizationId': '所属参数表ID',
            'groupName': '参数分组',
            'key': '参数键',
            'value': '参数值',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(api_param_item_list, mapping_dict)

        return binary_data
