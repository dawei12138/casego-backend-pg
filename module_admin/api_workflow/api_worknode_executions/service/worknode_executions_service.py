from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.api_worknode_executions.dao.worknode_executions_dao import Worknode_executionsDao
from module_admin.api_workflow.api_worknode_executions.entity.vo.worknode_executions_vo import DeleteWorknode_executionsModel, Worknode_executionsModel, Worknode_executionsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Worknode_executionsService:
    """
    节点执行记录模块服务层
    """

    @classmethod
    async def get_worknode_executions_list_services(
        cls, query_db: AsyncSession, query_object: Worknode_executionsPageQueryModel, is_page: bool = False
    ):
        """
        获取节点执行记录列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 节点执行记录列表信息对象
        """
        worknode_executions_list_result = await Worknode_executionsDao.get_worknode_executions_list(query_db, query_object, is_page)

        return worknode_executions_list_result


    @classmethod
    async def add_worknode_executions_services(cls, query_db: AsyncSession, page_object: Worknode_executionsModel):
        """
        新增节点执行记录信息service

        :param query_db: orm对象
        :param page_object: 新增节点执行记录对象
        :return: 新增节点执行记录校验结果
        """
        try:
            await Worknode_executionsDao.add_worknode_executions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_worknode_executions_services(cls, query_db: AsyncSession, page_object: Worknode_executionsModel):
        """
        编辑节点执行记录信息service

        :param query_db: orm对象
        :param page_object: 编辑节点执行记录对象
        :return: 编辑节点执行记录校验结果
        """
        edit_worknode_executions = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        worknode_executions_info = await cls.worknode_executions_detail_services(query_db, page_object.node_execution_id)
        if worknode_executions_info.node_execution_id:
            try:
                await Worknode_executionsDao.edit_worknode_executions_dao(query_db, edit_worknode_executions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='节点执行记录不存在')

    @classmethod
    async def delete_worknode_executions_services(cls, query_db: AsyncSession, page_object: DeleteWorknode_executionsModel):
        """
        删除节点执行记录信息service

        :param query_db: orm对象
        :param page_object: 删除节点执行记录对象
        :return: 删除节点执行记录校验结果
        """
        if page_object.node_execution_ids:
            node_execution_id_list = page_object.node_execution_ids.split(',')
            try:
                for node_execution_id in node_execution_id_list:
                    await Worknode_executionsDao.delete_worknode_executions_dao(query_db, Worknode_executionsModel(nodeExecutionId=node_execution_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入节点执行记录ID为空')

    @classmethod
    async def worknode_executions_detail_services(cls, query_db: AsyncSession, node_execution_id: int):
        """
        获取节点执行记录详细信息service

        :param query_db: orm对象
        :param node_execution_id: 节点执行记录ID
        :return: 节点执行记录ID对应的信息
        """
        worknode_executions = await Worknode_executionsDao.get_worknode_executions_detail_by_id(query_db, node_execution_id=node_execution_id)
        if worknode_executions:
            result = Worknode_executionsModel(**CamelCaseUtil.transform_result(worknode_executions))
        else:
            result = Worknode_executionsModel(**dict())

        return result

    @staticmethod
    async def export_worknode_executions_list_services(worknode_executions_list: List):
        """
        导出节点执行记录信息service

        :param worknode_executions_list: 节点执行记录信息列表
        :return: 节点执行记录信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'nodeExecutionId': '节点执行记录ID',
            'workflowExecutionId': '执行器执行记录ID',
            'nodeId': '节点ID',
            'status': '执行状态',
            'startTime': '开始时间',
            'endTime': '结束时间',
            'duration': '执行时长(毫秒)',
            'inputData': '输入数据',
            'outputData': '输出数据',
            'contextSnapshot': '执行时上下文快照',
            'loopIndex': '循环索引',
            'loopItem': '循环项数据',
            'conditionResult': '条件判断结果',
            'errorMessage': '错误信息',
            'errorDetails': '错误详情',
            'retryCount': '重试次数',
            'createdAt': '创建时间',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(worknode_executions_list, mapping_dict)

        return binary_data
