from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.elements.dao.elements_dao import ElementsDao
from module_app.elements.entity.vo.elements_vo import DeleteElementsModel, ElementsModel, ElementsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ElementsService:
    """
    控件元素模块服务层
    """

    @classmethod
    async def get_elements_list_services(
        cls, query_db: AsyncSession, query_object: ElementsPageQueryModel, is_page: bool = False
    ):
        """
        获取控件元素列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 控件元素列表信息对象
        """
        elements_list_result = await ElementsDao.get_elements_list(query_db, query_object, is_page)

        return elements_list_result


    @classmethod
    async def add_elements_services(cls, query_db: AsyncSession, page_object: ElementsModel):
        """
        新增控件元素信息service

        :param query_db: orm对象
        :param page_object: 新增控件元素对象
        :return: 新增控件元素校验结果
        """
        try:
            await ElementsDao.add_elements_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_elements_services(cls, query_db: AsyncSession, page_object: ElementsModel):
        """
        编辑控件元素信息service

        :param query_db: orm对象
        :param page_object: 编辑控件元素对象
        :return: 编辑控件元素校验结果
        """
        edit_elements = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag', })
        elements_info = await cls.elements_detail_services(query_db, page_object.id)
        if elements_info.id:
            try:
                await ElementsDao.edit_elements_dao(query_db, edit_elements)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='控件元素不存在')

    @classmethod
    async def delete_elements_services(cls, query_db: AsyncSession, page_object: DeleteElementsModel):
        """
        删除控件元素信息service

        :param query_db: orm对象
        :param page_object: 删除控件元素对象
        :return: 删除控件元素校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await ElementsDao.delete_elements_dao(query_db, ElementsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def elements_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取控件元素详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        elements = await ElementsDao.get_elements_detail_by_id(query_db, id=id)
        if elements:
            result = ElementsModel(**CamelCaseUtil.transform_result(elements))
        else:
            result = ElementsModel(**dict())

        return result

    @staticmethod
    async def export_elements_list_services(elements_list: List):
        """
        导出控件元素信息service

        :param elements_list: 控件元素信息列表
        :return: 控件元素信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'eleName': '元素名称',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
            'eleType': '定位类型',
            'eleValue': '定位值',
            'projectId': '所属项目ID',
            'moduleId': '所属模块ID',
        }
        binary_data = ExcelUtil.export_list2excel(elements_list, mapping_dict)

        return binary_data
