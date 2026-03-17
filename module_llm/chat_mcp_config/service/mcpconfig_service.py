from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_llm.chat_mcp_config.dao.mcpconfig_dao import McpconfigDao
from module_llm.chat_mcp_config.entity.vo.mcpconfig_vo import DeleteMcpconfigModel, McpconfigModel, \
    McpconfigPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class McpconfigService:
    """
    MCP服务器配置模块服务层
    """

    @classmethod
    async def get_mcpconfig_list_services(
            cls, query_db: AsyncSession, query_object: McpconfigPageQueryModel, is_page: bool = False
    ):
        """
        获取MCP服务器配置列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: MCP服务器配置列表信息对象
        """
        mcpconfig_list_result = await McpconfigDao.get_mcpconfig_list(query_db, query_object, is_page)

        return mcpconfig_list_result

    @classmethod
    async def get_mcpconfig_all_list_services(
            cls, query_db: AsyncSession, query_object: McpconfigPageQueryModel
    ):
        """
        获取MCP服务器配置列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: MCP服务器配置列表信息对象
        """
        mcpconfig_list_result = await McpconfigDao.get_mcpconfig_orm_list(query_db, query_object)
        mcpconfig_list = [config.model_dump(include={"config_id", "server_name"}, by_alias=True) for config in mcpconfig_list_result]
        return mcpconfig_list

    @classmethod
    async def add_mcpconfig_services(cls, query_db: AsyncSession, page_object: McpconfigModel):
        """
        新增MCP服务器配置信息service

        :param query_db: orm对象
        :param page_object: 新增MCP服务器配置对象
        :return: 新增MCP服务器配置校验结果
        """
        try:
            await McpconfigDao.add_mcpconfig_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_mcpconfig_services(cls, query_db: AsyncSession, page_object: McpconfigModel):
        """
        编辑MCP服务器配置信息service

        :param query_db: orm对象
        :param page_object: 编辑MCP服务器配置对象
        :return: 编辑MCP服务器配置校验结果
        """
        edit_mcpconfig = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        mcpconfig_info = await cls.mcpconfig_detail_services(query_db, page_object.config_id)
        if mcpconfig_info.config_id:
            try:
                await McpconfigDao.edit_mcpconfig_dao(query_db, edit_mcpconfig)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='MCP服务器配置不存在')

    @classmethod
    async def delete_mcpconfig_services(cls, query_db: AsyncSession, page_object: DeleteMcpconfigModel):
        """
        删除MCP服务器配置信息service

        :param query_db: orm对象
        :param page_object: 删除MCP服务器配置对象
        :return: 删除MCP服务器配置校验结果
        """
        if page_object.config_ids:
            config_id_list = page_object.config_ids.split(',')
            try:
                for config_id in config_id_list:
                    # config_id_int = int(config_id)
                    config_id_obj = McpconfigModel.model_validate({'config_id': config_id}).config_id
                    # await McpconfigDao.delete_mcpconfig_dao(query_db, McpconfigModel(configId=config_id_int))
                    await McpconfigDao.delete_mcpconfig_dao(query_db, McpconfigModel(configId=config_id_obj))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入配置唯一标识符(UUID)为空')

    @classmethod
    async def mcpconfig_detail_services(cls, query_db: AsyncSession, config_id: int):
        """
        获取MCP服务器配置详细信息service

        :param query_db: orm对象
        :param config_id: 配置唯一标识符(UUID)
        :return: 配置唯一标识符(UUID)对应的信息
        """
        mcpconfig = await McpconfigDao.get_mcpconfig_detail_by_id(query_db, config_id=config_id)
        if mcpconfig:
            result = McpconfigModel(**CamelCaseUtil.transform_result(mcpconfig))
        else:
            result = McpconfigModel(**dict())

        return result

    @staticmethod
    async def export_mcpconfig_list_services(mcpconfig_list: List):
        """
        导出MCP服务器配置信息service

        :param mcpconfig_list: MCP服务器配置信息列表
        :return: MCP服务器配置信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'configId': '配置唯一标识符(UUID)',
            'serverName': '服务器逻辑名称，作为工具名前缀',
            'enabled': '是否启用此服务器',
            'transport': '传输类型: stdio / streamable_http / sse / websocket',
            'command': 'stdio模式: 可执行文件路径',
            'args': 'stdio模式: 命令行参数列表，如 ["@playwright/mcp@latest", "--headless"]',
            'env': 'stdio模式: 子进程环境变量字典',
            'cwd': 'stdio模式: 子进程工作目录',
            'url': 'streamable_http/sse/websocket模式: 远程服务器URL',
            'headers': 'streamable_http/sse模式: 附加HTTP请求头',
            'timeout': '请求超时时间',
            'sseReadTimeout': 'SSE流读取超时时间',
            'sessionKwargs': '传递给MCP ClientSession的额外参数',
            'createBy': '',
            'createTime': '创建时间',
            'updateBy': '',
            'updateTime': '更新时间',
            'remark': '',
            'description': '',
            'sortNo': '',
            'delFlag': '',
        }
        binary_data = ExcelUtil.export_list2excel(mcpconfig_list, mapping_dict)

        return binary_data
