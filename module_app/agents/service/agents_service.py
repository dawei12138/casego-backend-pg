from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_app.agents.dao.agents_dao import AgentsDao
from module_app.agents.entity.vo.agents_vo import DeleteAgentsModel, AgentsModel, AgentsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class AgentsService:
    """
    Agent代理模块服务层
    """

    @classmethod
    async def get_agents_list_services(
        cls, query_db: AsyncSession, query_object: AgentsPageQueryModel, is_page: bool = False
    ):
        """
        获取Agent代理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: Agent代理列表信息对象
        """
        agents_list_result = await AgentsDao.get_agents_list(query_db, query_object, is_page)

        return agents_list_result


    @classmethod
    async def add_agents_services(cls, query_db: AsyncSession, page_object: AgentsModel):
        """
        新增Agent代理信息service

        :param query_db: orm对象
        :param page_object: 新增Agent代理对象
        :return: 新增Agent代理校验结果
        """
        try:
            await AgentsDao.add_agents_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_agents_services(cls, query_db: AsyncSession, page_object: AgentsModel):
        """
        编辑Agent代理信息service

        :param query_db: orm对象
        :param page_object: 编辑Agent代理对象
        :return: 编辑Agent代理校验结果
        """
        edit_agents = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        agents_info = await cls.agents_detail_services(query_db, page_object.id)
        if agents_info.id:
            try:
                await AgentsDao.edit_agents_dao(query_db, edit_agents)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='Agent代理不存在')

    @classmethod
    async def delete_agents_services(cls, query_db: AsyncSession, page_object: DeleteAgentsModel):
        """
        删除Agent代理信息service

        :param query_db: orm对象
        :param page_object: 删除Agent代理对象
        :return: 删除Agent代理校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await AgentsDao.delete_agents_dao(query_db, AgentsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def agents_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取Agent代理详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        agents = await AgentsDao.get_agents_detail_by_id(query_db, id=id)
        if agents:
            result = AgentsModel(**CamelCaseUtil.transform_result(agents))
        else:
            result = AgentsModel(**dict())

        return result

    @staticmethod
    async def export_agents_list_services(agents_list: List):
        """
        导出Agent代理信息service

        :param agents_list: Agent代理信息列表
        :return: Agent代理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'name': 'Agent名称',
            'host': 'Agent的IP地址',
            'port': 'Agent的端口',
            'secretKey': 'Agent的密钥',
            'status': 'Agent状态',
            'systemType': 'Agent系统类型: windows/linux/macos',
            'version': 'Agent端代码版本',
            'lockVersion': '乐观锁版本号',
            'highTemp': '高温预警阈值(摄氏度)',
            'highTempTime': '高温持续时间阈值(分钟)',
            'hasHub': '是否使用Sonic Hub: 0否 1是',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(agents_list, mapping_dict)

        return binary_data
