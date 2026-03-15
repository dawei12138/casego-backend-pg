from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_llm.llm_provider.dao.provider_config_dao import Provider_configDao
from module_llm.llm_provider.entity.vo.provider_config_vo import DeleteProvider_configModel, Provider_configModel, Provider_configPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Provider_configService:
    """
    LLM提供商配置模块服务层
    """

    @classmethod
    async def get_provider_config_list_services(
        cls, query_db: AsyncSession, query_object: Provider_configPageQueryModel, is_page: bool = False
    ):
        """
        获取LLM提供商配置列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: LLM提供商配置列表信息对象
        """
        provider_config_list_result = await Provider_configDao.get_provider_config_list(query_db, query_object, is_page)

        return provider_config_list_result


    @classmethod
    async def add_provider_config_services(cls, query_db: AsyncSession, page_object: Provider_configModel):
        """
        新增LLM提供商配置信息service

        :param query_db: orm对象
        :param page_object: 新增LLM提供商配置对象
        :return: 新增LLM提供商配置校验结果
        """
        try:
            await Provider_configDao.add_provider_config_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_provider_config_services(cls, query_db: AsyncSession, page_object: Provider_configModel):
        """
        编辑LLM提供商配置信息service

        :param query_db: orm对象
        :param page_object: 编辑LLM提供商配置对象
        :return: 编辑LLM提供商配置校验结果
        """
        edit_provider_config = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        provider_config_info = await cls.provider_config_detail_services(query_db, page_object.provider_id)
        if provider_config_info.provider_id:
            try:
                await Provider_configDao.edit_provider_config_dao(query_db, edit_provider_config)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='LLM提供商配置不存在')

    @classmethod
    async def delete_provider_config_services(cls, query_db: AsyncSession, page_object: DeleteProvider_configModel):
        """
        删除LLM提供商配置信息service

        :param query_db: orm对象
        :param page_object: 删除LLM提供商配置对象
        :return: 删除LLM提供商配置校验结果
        """
        if page_object.provider_ids:
            provider_id_list = page_object.provider_ids.split(',')
            try:
                for provider_id in provider_id_list:
                    await Provider_configDao.delete_provider_config_dao(query_db, Provider_configModel(providerId=provider_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入提供商配置ID为空')

    @classmethod
    async def provider_config_detail_services(cls, query_db: AsyncSession, provider_id: int):
        """
        获取LLM提供商配置详细信息service

        :param query_db: orm对象
        :param provider_id: 提供商配置ID
        :return: 提供商配置ID对应的信息
        """
        provider_config = await Provider_configDao.get_provider_config_detail_by_id(query_db, provider_id=provider_id)
        if provider_config:
            result = Provider_configModel(**CamelCaseUtil.transform_result(provider_config))
        else:
            result = Provider_configModel(**dict())

        return result

    @classmethod
    async def provider_config_by_key_services(cls, query_db: AsyncSession, provider_key: str):
        """
        根据提供商标识获取配置信息service

        :param query_db: orm对象
        :param provider_key: 提供商标识(如openai/anthropic/deepseek等)
        :return: 提供商配置信息
        """
        provider_config = await Provider_configDao.get_provider_config_by_key(query_db, provider_key=provider_key)
        if provider_config:
            result = Provider_configModel(**CamelCaseUtil.transform_result(provider_config))
        else:
            result = Provider_configModel(**dict())

        return result

    @staticmethod
    async def export_provider_config_list_services(provider_config_list: List):
        """
        导出LLM提供商配置信息service

        :param provider_config_list: LLM提供商配置信息列表
        :return: LLM提供商配置信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'providerId': '提供商配置ID',
            'providerKey': '提供商标识(如openai/anthropic/google等)',
            'providerName': '提供商显示名称(如OpenAI/Anthropic/Google等)',
            'apiKey': 'API密钥(建议加密存储)',
            'apiSecret': 'API密钥对(部分提供商需要)',
            'baseUrl': 'API基础URL(自定义或代理时使用)',
            'apiVersion': 'API版本(Azure等需要)',
            'timeout': '请求超时时间(秒)',
            'maxRetries': '最大重试次数',
            'extraHeaders': '额外请求头(JSON格式)',
            'iconUrl': '提供商图标URL',
            'status': '状态',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(provider_config_list, mapping_dict)

        return binary_data
