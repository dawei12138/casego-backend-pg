from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict
from exceptions.exception import ServiceException
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel, Cache_dataModel
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from module_admin.api_testing.api_services.entity.vo.services_vo import ServicesPageQueryModel
from module_admin.api_testing.api_services.service.services_service import ServicesService
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.service.dict_service import DictDataService
from module_admin.api_testing.api_environments.dao.environments_dao import EnvironmentsDao
from module_admin.api_testing.api_environments.entity.vo.environments_vo import DeleteEnvironmentsModel, \
    EnvironmentsModel, \
    EnvironmentsPageQueryModel, EnvironmentsConfig, CookieItemModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class EnvironmentsService:
    """
    环境配置模块服务层
    """

    @classmethod
    async def get_environments_list_services(
            cls, query_db: AsyncSession, query_object: EnvironmentsPageQueryModel, is_page: bool = False
    ):
        """
        获取环境配置列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境配置列表信息对象
        """
        environments_list_result = await EnvironmentsDao.get_environments_list(query_db, query_object, is_page)

        return environments_list_result

    @classmethod
    async def get_environments_config_services(
            cls, cache_query: Cache_dataPageQueryModel, redis, query_db: AsyncSession, query_object: EnvironmentsConfig,
    ):
        """
        获取环境配置列表信息service

        :param cache_query:
        :param redis: reques里面的redis连接
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境配置列表信息对象
        """
        environment_info = await cls.environments_detail_services(query_db, query_object.id)
        resaults = EnvironmentsConfig(**environment_info.model_dump())
        resaults.url = await ServicesService.services_default_services(query_db, query_object.id)
        resaults.cache_list = await Cache_dataService.get_redis_cache_list_services(redis, cache_query)

        return resaults

    @classmethod
    async def get_request_config_services(
            cls, query_db: AsyncSession, query_object: EnvironmentsConfig,
    ):
        """
        获取环境配置列表信息service

        :param cache_query:
        :param redis: reques里面的redis连接
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境配置列表信息对象
        """
        environment_info = await cls.environments_detail_services(query_db, query_object.id)
        resaults = EnvironmentsConfig(**environment_info.model_dump())
        return resaults

    @classmethod
    async def edit_environments_config_services(cls, user_id, redis, query_db: AsyncSession,
                                                page_object: EnvironmentsModel,
                                                ):
        """
        编辑环境全部的配置信息service

        :param redis:
        :param query_db: orm对象
        :param page_object: 编辑环境配置对象
        :return: 编辑环境配置校验结果
        """
        edit_environments = page_object.model_dump(exclude_unset=True,
                                                   exclude={'create_by', 'create_time', 'sort_no',
                                                            'del_flag'})
        environments_info = await cls.environments_detail_services(query_db, page_object.id)
        if environments_info.id:
            try:
                await EnvironmentsDao.edit_environments_dao(query_db, edit_environments)

                # 改一下默认url，根据url查到第一个设为默认，
                url = page_object.url if page_object.url else ""
                services_model = ServicesPageQueryModel(url=url, environment_id=page_object.id)
                await ServicesService.edit_env_default_services(query_db, services_model)

                # 更新缓存
                if page_object.cache_list:
                    delete_cache_list = [cache.get("id") for cache in page_object.cache_list if cache.get("is_delete")]
                    cache_list = [cache for cache in page_object.cache_list if not cache.get("is_delete")]
                    for cache in cache_list:
                        edit_cache_data = Cache_dataModel(**cache, environment_id=page_object.id, user_id=user_id)
                        await Cache_dataService.add_cache_data_services(redis, edit_cache_data)
                    if delete_cache_list:
                        await redis.delete(*delete_cache_list)

                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='环境配置不存在')

    @classmethod
    async def add_environments_services(cls, query_db: AsyncSession, page_object: EnvironmentsModel):
        """
        新增环境配置信息service

        :param query_db: orm对象
        :param page_object: 新增环境配置对象
        :return: 新增环境配置校验结果
        """
        try:
            if page_object.is_default:
                await EnvironmentsDao.edit_environments_isdefault_dao(query_db, page_object)
            await EnvironmentsDao.add_environments_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_environments_services(cls, query_db: AsyncSession, page_object: EnvironmentsModel):
        """
        编辑环境配置信息service

        :param query_db: orm对象
        :param page_object: 编辑环境配置对象
        :return: 编辑环境配置校验结果
        """
        edit_environments = page_object.model_dump(exclude_unset=True,
                                                   exclude={'create_by', 'create_time', 'description', 'sort_no',
                                                            'del_flag'})
        environments_info = await cls.environments_detail_services(query_db, page_object.id)
        if environments_info.id:
            try:
                if page_object.is_default:
                    await EnvironmentsDao.edit_environments_isdefault_dao(query_db, page_object)
                await EnvironmentsDao.edit_environments_dao(query_db, edit_environments)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='环境配置不存在')

    @classmethod
    async def delete_environments_services(cls, query_db: AsyncSession, page_object: DeleteEnvironmentsModel):
        """
        删除环境配置信息service

        :param query_db: orm对象
        :param page_object: 删除环境配置对象
        :return: 删除环境配置校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for del_id in id_list:
                    del_id = int(del_id)
                    res = await EnvironmentsDao.get_environments_detail_by_id(query_db, del_id)
                    if res.is_default == 1:
                        await query_db.rollback()
                        return CrudResponseModel(is_success=False, message='删除失败，包含默认环境')
                    await EnvironmentsDao.delete_environments_dao(query_db, EnvironmentsModel(id=del_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入环境ID为空')

    @classmethod
    async def environments_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取环境配置详细信息service

        :param query_db: orm对象
        :param id: 环境ID
        :return: 环境ID对应的信息
        """
        environments = await EnvironmentsDao.get_environments_detail_by_id(query_db, id=id)
        if environments:
            result = EnvironmentsModel(**CamelCaseUtil.transform_result(environments))
        else:
            result = EnvironmentsModel(**dict())

        return result

    @staticmethod
    async def export_environments_list_services(request: Request, environments_list: List):
        """
        导出环境配置信息service

        :param request:
        :param environments_list: 环境配置信息列表
        :return: 环境配置信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '环境ID',
            'name': '环境名称',
            'projectId': '所属项目ID',
            'isDefault': '是否为默认环境',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        user_is_defalut_list = await DictDataService.query_dict_data_list_from_cache_services(
            request.app.state.redis, dict_type='user_is_defalut'
        )
        user_is_defalut_option = [dict(label=item.get('dictLabel'), value=item.get('dictValue')) for item in
                                  user_is_defalut_list]
        user_is_defalut_option_dict = {item.get('value'): item for item in user_is_defalut_option}
        for item in environments_list:
            if str(item.get('isDefault')) in user_is_defalut_option_dict.keys():
                item['isDefault'] = user_is_defalut_option_dict.get(str(item.get('isDefault'))).get('label')
        binary_data = ExcelUtil.export_list2excel(environments_list, mapping_dict)

        return binary_data

    @classmethod
    async def update_environment_cookies_services(cls, query_db: AsyncSession, env_id: int,
                                                  cookies_dict: Dict[str, str]):
        """
        更新环境的全局Cookies（用于请求完成后保存响应的cookies）

        :param query_db: orm对象
        :param env_id: 环境ID
        :param cookies_dict: 需要更新的cookies字典 {key: value}
        :return: 更新结果
        """
        try:
            # 获取当前环境信息
            environment_info = await cls.environments_detail_services(query_db, env_id)
            if not environment_info.id:
                return CrudResponseModel(is_success=False, message='环境不存在')

            # 获取现有的 global_cookies
            existing_cookies = environment_info.global_cookies or []
            existing_cookies_dict = {c.key: c for c in existing_cookies}

            # 合并新的 cookies（更新已存在的，添加新的）
            for key, value in cookies_dict.items():
                if key in existing_cookies_dict:
                    # 更新现有的 cookie
                    existing_cookies_dict[key].value = value
                else:
                    # 添加新的 cookie
                    existing_cookies_dict[key] = CookieItemModel(
                        key=key,
                        value=value,
                        description="Auto-saved from response",
                        is_run=True
                    )

            # 转换回列表并序列化
            updated_cookies = [c.model_dump() for c in existing_cookies_dict.values()]

            # 更新环境
            edit_environments = {'id': env_id, 'global_cookies': updated_cookies}
            await EnvironmentsDao.edit_environments_dao(query_db, edit_environments)
            await query_db.commit()

            return CrudResponseModel(is_success=True, message='Cookies更新成功')
        except Exception as e:
            await query_db.rollback()
            raise e
