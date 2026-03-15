from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.api_testing.api_services.entity.do.services_do import ApiServices
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.service.dict_service import DictDataService
from module_admin.api_testing.api_services.dao.services_dao import ServicesDao
from module_admin.api_testing.api_services.entity.vo.services_vo import DeleteServicesModel, ServicesModel, ServicesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ServicesService:
    """
    环境服务地址模块服务层
    """

    @classmethod
    async def get_services_list_services(
            cls, query_db: AsyncSession, query_object: ServicesPageQueryModel, is_page: bool = False
    ):
        """
        获取环境服务地址列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境服务地址列表信息对象
        """
        services_list_result = await ServicesDao.get_services_list(query_db, query_object, is_page)

        return services_list_result

    @classmethod
    async def add_services_services(cls, query_db: AsyncSession, page_object: ServicesModel):
        """
        新增环境服务地址信息service

        :param query_db: orm对象
        :param page_object: 新增环境服务地址对象
        :return: 新增环境服务地址校验结果
        """
        try:
            # 全部改为取消默认
            if page_object.is_default:
                await ServicesDao.update_service_default(query_db, page_object)
            if not await ServicesDao.get_services_list(query_db, ServicesPageQueryModel(
                    environment_id=page_object.environment_id)):
                page_object.is_default = True
            await ServicesDao.add_services_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_services_services(cls, query_db: AsyncSession, page_object: ServicesModel):
        """
        编辑环境服务地址信息service

        :param query_db: orm对象
        :param page_object: 编辑环境服务地址对象
        :return: 编辑环境服务地址校验结果
        """
        edit_services = page_object.model_dump(exclude_unset=True,
                                               exclude={'create_by', 'create_time', 'remark', 'description', 'sort_no',
                                                        'del_flag'})
        services_info = await cls.services_detail_services(query_db, page_object.id)
        if services_info.id:
            try:
                # 全部改为取消默认
                if page_object.is_default:
                    await ServicesDao.update_service_default(query_db, page_object)
                    pass
                await ServicesDao.edit_services_dao(query_db, edit_services)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='环境服务地址不存在')


    @classmethod
    async def edit_env_default_services(cls, query_db: AsyncSession, page_object: ServicesPageQueryModel):
        """
        编辑环境服务地址信息service
        需要url和环境id，is_default为真
        :param query_db: orm对象
        :param page_object: 编辑环境服务地址对象
        :return: 编辑环境服务地址校验结果
        """
        edit_services = page_object.model_dump(exclude_unset=True,
                                               exclude={'create_by', 'create_time', 'remark', 'description', 'sort_no',
                                                        'del_flag'})
        services_info = await cls.get_services_list_services(query_db, page_object)

        if len(services_info) > 0:
            try:

                services_info[0]["is_default"] = True
                # 全部改为取消默认
                await ServicesDao.update_service_default(query_db, page_object)
                await ServicesDao.edit_services_dao(query_db, services_info[0])
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            # 直接创建
            try:
                pass
            except Exception as e:
                await query_db.rollback()
                raise e

    @classmethod
    async def delete_services_services(cls, query_db: AsyncSession, page_object: DeleteServicesModel):
        """
        删除环境服务地址信息service

        :param query_db: orm对象
        :param page_object: 删除环境服务地址对象
        :return: 删除环境服务地址校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id_int = int(id)
                    res = await ServicesDao.get_services_detail_by_id(query_db, id_int)
                    if res.is_default == True:
                        raise Exception("包含默认服务不可删除")
                    await ServicesDao.delete_services_dao(query_db, ServicesModel(id=id_int))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入服务ID为空')

    @classmethod
    async def services_default_services(cls, query_db: AsyncSession, environment_id: int):
        """
        获取环境服务地址默认的服务地址

        :param environment_id:
        :param query_db: orm对象
        :return: 服务ID对应的信息
        """
        services_info = (
            (
                await query_db.execute(
                    select(ApiServices)
                    .where(
                        ApiServices.environment_id == environment_id,
                        ApiServices.is_default == True,
                        ApiServices.del_flag == "0"
                    )
                )
            )
            .scalars()
            .first()
        )
        return services_info.url if services_info else None
    @classmethod
    async def services_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取环境服务地址详细信息service

        :param query_db: orm对象
        :param id: 服务ID
        :return: 服务ID对应的信息
        """
        services = await ServicesDao.get_services_detail_by_id(query_db, id=id)
        if services:
            result = ServicesModel(**CamelCaseUtil.transform_result(services))
        else:
            result = ServicesModel(**dict())

        return result

    @staticmethod
    async def export_services_list_services(request: Request, services_list: List):
        """
        导出环境服务地址信息service

        :param services_list: 环境服务地址信息列表
        :return: 环境服务地址信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '服务ID',
            'name': '服务名称',
            'url': '服务地址',
            'environmentId': '所属环境ID',
            'isDefault': '是否为默认服务',
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
        for item in services_list:
            if str(item.get('isDefault')) in user_is_defalut_option_dict.keys():
                item['isDefault'] = user_is_defalut_option_dict.get(str(item.get('isDefault'))).get('label')
        binary_data = ExcelUtil.export_list2excel(services_list, mapping_dict)

        return binary_data
