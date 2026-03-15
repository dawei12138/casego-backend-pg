from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_cookies.dao.cookies_dao import CookiesDao
from module_admin.api_testing.api_cookies.entity.vo.cookies_vo import DeleteCookiesModel, CookiesModel, CookiesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class CookiesService:
    """
    接口请求Cookie模块服务层
    """

    @classmethod
    async def get_cookies_list_services(
        cls, query_db: AsyncSession, query_object: CookiesPageQueryModel, is_page: bool = False
    ):
        """
        获取接口请求Cookie列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口请求Cookie列表信息对象
        """
        cookies_list_result = await CookiesDao.get_cookies_list(query_db, query_object, is_page)

        return cookies_list_result


    @classmethod
    async def add_cookies_services(cls, query_db: AsyncSession, page_object: CookiesModel):
        """
        新增接口请求Cookie信息service

        :param query_db: orm对象
        :param page_object: 新增接口请求Cookie对象
        :return: 新增接口请求Cookie校验结果
        """
        try:
            await CookiesDao.add_cookies_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_cookies_services(cls, query_db: AsyncSession, page_object: CookiesModel):
        """
        编辑接口请求Cookie信息service

        :param query_db: orm对象
        :param page_object: 编辑接口请求Cookie对象
        :return: 编辑接口请求Cookie校验结果
        """
        edit_cookies = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        cookies_info = await cls.cookies_detail_services(query_db, page_object.cookie_id)
        if cookies_info.cookie_id:
            try:
                await CookiesDao.edit_cookies_dao(query_db, edit_cookies)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口请求Cookie不存在')

    @classmethod
    async def delete_cookies_services(cls, query_db: AsyncSession, page_object: DeleteCookiesModel):
        """
        删除接口请求Cookie信息service

        :param query_db: orm对象
        :param page_object: 删除接口请求Cookie对象
        :return: 删除接口请求Cookie校验结果
        """
        if page_object.cookie_ids:
            cookie_id_list = page_object.cookie_ids.split(',')
            try:
                for cookie_id in cookie_id_list:
                    await CookiesDao.delete_cookies_dao(query_db, CookiesModel(cookieId=cookie_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def cookies_detail_services(cls, query_db: AsyncSession, cookie_id: int):
        """
        获取接口请求Cookie详细信息service

        :param query_db: orm对象
        :param cookie_id: ID
        :return: ID对应的信息
        """
        cookies = await CookiesDao.get_cookies_detail_by_id(query_db, cookie_id=cookie_id)
        if cookies:
            result = CookiesModel(**CamelCaseUtil.transform_result(cookies))
        else:
            result = CookiesModel(**dict())

        return result

    @staticmethod
    async def export_cookies_list_services(cookies_list: List):
        """
        导出接口请求Cookie信息service

        :param cookies_list: 接口请求Cookie信息列表
        :return: 接口请求Cookie信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'cookieId': 'ID',
            'caseId': '关联的测试用例ID',
            'key': 'Cookie键名',
            'value': 'Cookie值',
            'domain': '作用域',
            'path': '路径',
            'isRun': '是否启用该Cookie',
            'description': '描述',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(cookies_list, mapping_dict)

        return binary_data
