from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.globalparams.dao.globalparams_dao import GlobalparamsDao
from module_app.globalparams.entity.vo.globalparams_vo import DeleteGlobalparamsModel, GlobalparamsModel, GlobalparamsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class GlobalparamsService:
    """
    全局参数模块服务层
    """

    @classmethod
    async def get_globalparams_list_services(
        cls, query_db: AsyncSession, query_object: GlobalparamsPageQueryModel, is_page: bool = False
    ):
        """
        获取全局参数列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 全局参数列表信息对象
        """
        globalparams_list_result = await GlobalparamsDao.get_globalparams_list(query_db, query_object, is_page)

        return globalparams_list_result


    @classmethod
    async def add_globalparams_services(cls, query_db: AsyncSession, page_object: GlobalparamsModel):
        """
        新增全局参数信息service

        :param query_db: orm对象
        :param page_object: 新增全局参数对象
        :return: 新增全局参数校验结果
        """
        try:
            await GlobalparamsDao.add_globalparams_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_globalparams_services(cls, query_db: AsyncSession, page_object: GlobalparamsModel):
        """
        编辑全局参数信息service

        :param query_db: orm对象
        :param page_object: 编辑全局参数对象
        :return: 编辑全局参数校验结果
        """
        edit_globalparams = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        globalparams_info = await cls.globalparams_detail_services(query_db, page_object.id)
        if globalparams_info.id:
            try:
                await GlobalparamsDao.edit_globalparams_dao(query_db, edit_globalparams)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='全局参数不存在')

    @classmethod
    async def delete_globalparams_services(cls, query_db: AsyncSession, page_object: DeleteGlobalparamsModel):
        """
        删除全局参数信息service

        :param query_db: orm对象
        :param page_object: 删除全局参数对象
        :return: 删除全局参数校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await GlobalparamsDao.delete_globalparams_dao(query_db, GlobalparamsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def globalparams_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取全局参数详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        globalparams = await GlobalparamsDao.get_globalparams_detail_by_id(query_db, id=id)
        if globalparams:
            result = GlobalparamsModel(**CamelCaseUtil.transform_result(globalparams))
        else:
            result = GlobalparamsModel(**dict())

        return result

    @staticmethod
    async def export_globalparams_list_services(globalparams_list: List):
        """
        导出全局参数信息service

        :param globalparams_list: 全局参数信息列表
        :return: 全局参数信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'paramsKey': '参数键名',
            'paramsValue': '参数值',
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
        binary_data = ExcelUtil.export_list2excel(globalparams_list, mapping_dict)

        return binary_data
