from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_headers.dao.headers_dao import HeadersDao
from module_admin.api_testing.api_headers.entity.vo.headers_vo import DeleteHeadersModel, HeadersModel, HeadersPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class HeadersService:
    """
    接口请求头模块服务层
    """

    @classmethod
    async def get_headers_list_services(
        cls, query_db: AsyncSession, query_object: HeadersPageQueryModel, is_page: bool = False
    ):
        """
        获取接口请求头列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口请求头列表信息对象
        """
        headers_list_result = await HeadersDao.get_headers_list(query_db, query_object, is_page)

        return headers_list_result


    @classmethod
    async def add_headers_services(cls, query_db: AsyncSession, page_object: HeadersModel):
        """
        新增接口请求头信息service

        :param query_db: orm对象
        :param page_object: 新增接口请求头对象
        :return: 新增接口请求头校验结果
        """
        try:
            await HeadersDao.add_headers_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_headers_services(cls, query_db: AsyncSession, page_object: HeadersModel):
        """
        编辑接口请求头信息service

        :param query_db: orm对象
        :param page_object: 编辑接口请求头对象
        :return: 编辑接口请求头校验结果
        """
        edit_headers = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        headers_info = await cls.headers_detail_services(query_db, page_object.header_id)
        if headers_info.header_id:
            try:
                await HeadersDao.edit_headers_dao(query_db, edit_headers)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口请求头不存在')

    @classmethod
    async def delete_headers_services(cls, query_db: AsyncSession, page_object: DeleteHeadersModel):
        """
        删除接口请求头信息service

        :param query_db: orm对象
        :param page_object: 删除接口请求头对象
        :return: 删除接口请求头校验结果
        """
        if page_object.header_ids:
            header_id_list = page_object.header_ids.split(',')
            try:
                for header_id in header_id_list:
                    await HeadersDao.delete_headers_dao(query_db, HeadersModel(headerId=header_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def headers_detail_services(cls, query_db: AsyncSession, header_id: int):
        """
        获取接口请求头详细信息service

        :param query_db: orm对象
        :param header_id: ID
        :return: ID对应的信息
        """
        headers = await HeadersDao.get_headers_detail_by_id(query_db, header_id=header_id)
        if headers:
            result = HeadersModel(**CamelCaseUtil.transform_result(headers))
        else:
            result = HeadersModel(**dict())

        return result

    @staticmethod
    async def export_headers_list_services(headers_list: List):
        """
        导出接口请求头信息service

        :param headers_list: 接口请求头信息列表
        :return: 接口请求头信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'headerId': 'ID',
            'caseId': '关联的测试用例ID',
            'key': '请求头键名',
            'value': '请求头值',
            'isRun': '是否启用该请求头',
            'description': '描述',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(headers_list, mapping_dict)

        return binary_data
