from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.service.dict_service import DictDataService
from module_admin.api_testing.api_databases.dao.api_databases_dao import Api_databasesDao
from module_admin.api_testing.api_databases.entity.vo.api_databases_vo import DeleteApi_databasesModel, \
    Api_databasesModel, Api_databasesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Api_databasesService:
    """
    数据库配置模块服务层
    """

    @classmethod
    async def get_api_databases_list_services(
            cls, query_db: AsyncSession, query_object: Api_databasesPageQueryModel, is_page: bool = False
    ):
        """
        获取数据库配置列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据库配置列表信息对象
        """
        api_databases_list_result = await Api_databasesDao.get_api_databases_list(query_db, query_object, is_page)

        return api_databases_list_result

    @classmethod
    async def add_api_databases_services(cls, query_db: AsyncSession, page_object: Api_databasesModel):
        """
        新增数据库配置信息service

        :param query_db: orm对象
        :param page_object: 新增数据库配置对象
        :return: 新增数据库配置校验结果
        """
        try:
            await Api_databasesDao.add_api_databases_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_api_databases_services(cls, query_db: AsyncSession, page_object: Api_databasesModel):
        """
        编辑数据库配置信息service

        :param query_db: orm对象
        :param page_object: 编辑数据库配置对象
        :return: 编辑数据库配置校验结果
        """
        edit_api_databases = page_object.model_dump(exclude_unset=True,
                                                    exclude={'create_by', 'create_time', 'description', 'sort_no',
                                                             'del_flag'})
        api_databases_info = await cls.api_databases_detail_services(query_db, page_object.id)
        if api_databases_info.id:
            try:
                await Api_databasesDao.edit_api_databases_dao(query_db, edit_api_databases)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='数据库配置不存在')

    @classmethod
    async def delete_api_databases_services(cls, query_db: AsyncSession, page_object: DeleteApi_databasesModel):
        """
        删除数据库配置信息service

        :param query_db: orm对象
        :param page_object: 删除数据库配置对象
        :return: 删除数据库配置校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await Api_databasesDao.delete_api_databases_dao(query_db, Api_databasesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入数据库ID为空')

    @classmethod
    async def api_databases_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取数据库配置详细信息service

        :param query_db: orm对象
        :param id: 数据库ID
        :return: 数据库ID对应的信息
        """
        api_databases = await Api_databasesDao.get_api_databases_detail_by_id(query_db, id=id)
        if api_databases:
            result = Api_databasesModel(**CamelCaseUtil.transform_result(api_databases))
        else:
            result = Api_databasesModel(**dict())

        return result

    @staticmethod
    async def export_api_databases_list_services(request: Request, api_databases_list: List):
        """
        导出数据库配置信息service

        :param api_databases_list: 数据库配置信息列表
        :return: 数据库配置信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '数据库ID',
            'name': '数据库名称',
            'dbType': '数据库类型',
            'host': '数据库主机',
            'port': '数据库端口',
            'username': '数据库用户名',
            'password': '数据库密码',
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
        database_type_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='database_type'
        )
        database_type_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in
                                database_type_list]
        database_type_option_dict = {item.get('value'): item for item in database_type_option}
        for item in api_databases_list:
            if str(item.get('dbType')) in database_type_option_dict.keys():
                item['dbType'] = database_type_option_dict.get(str(item.get('dbType'))).get('label')
        binary_data = ExcelUtil.export_list2excel(api_databases_list, mapping_dict)

        return binary_data
