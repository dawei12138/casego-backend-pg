from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.api_workflow_executions.dao.workflow_executions_dao import Workflow_executionsDao
from module_admin.api_workflow.api_workflow_executions.entity.vo.workflow_executions_vo import DeleteWorkflow_executionsModel, Workflow_executionsModel, Workflow_executionsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Workflow_executionsService:
    """
    执行器执行记录模块服务层
    """

    @classmethod
    async def get_workflow_executions_list_services(
        cls, query_db: AsyncSession, query_object: Workflow_executionsPageQueryModel, is_page: bool = False
    ):
        """
        获取执行器执行记录列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 执行器执行记录列表信息对象
        """
        workflow_executions_list_result = await Workflow_executionsDao.get_workflow_executions_list(query_db, query_object, is_page)

        return workflow_executions_list_result


    @classmethod
    async def add_workflow_executions_services(cls, query_db: AsyncSession, page_object: Workflow_executionsModel):
        """
        新增执行器执行记录信息service

        :param query_db: orm对象
        :param page_object: 新增执行器执行记录对象
        :return: 新增执行器执行记录校验结果
        """
        try:
            await Workflow_executionsDao.add_workflow_executions_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_workflow_executions_services(cls, query_db: AsyncSession, page_object: Workflow_executionsModel):
        """
        编辑执行器执行记录信息service

        :param query_db: orm对象
        :param page_object: 编辑执行器执行记录对象
        :return: 编辑执行器执行记录校验结果
        """
        edit_workflow_executions = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        workflow_executions_info = await cls.workflow_executions_detail_services(query_db, page_object.workflow_execution_id)
        if workflow_executions_info.workflow_execution_id:
            try:
                await Workflow_executionsDao.edit_workflow_executions_dao(query_db, edit_workflow_executions)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='执行器执行记录不存在')

    @classmethod
    async def delete_workflow_executions_services(cls, query_db: AsyncSession, page_object: DeleteWorkflow_executionsModel):
        """
        删除执行器执行记录信息service

        :param query_db: orm对象
        :param page_object: 删除执行器执行记录对象
        :return: 删除执行器执行记录校验结果
        """
        if page_object.workflow_execution_ids:
            workflow_execution_id_list = page_object.workflow_execution_ids.split(',')
            try:
                for workflow_execution_id in workflow_execution_id_list:
                    await Workflow_executionsDao.delete_workflow_executions_dao(query_db, Workflow_executionsModel(workflowExecutionId=workflow_execution_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入执行记录ID为空')

    @classmethod
    async def workflow_executions_detail_services(cls, query_db: AsyncSession, workflow_execution_id: int):
        """
        获取执行器执行记录详细信息service

        :param query_db: orm对象
        :param workflow_execution_id: 执行记录ID
        :return: 执行记录ID对应的信息
        """
        workflow_executions = await Workflow_executionsDao.get_workflow_executions_detail_by_id(query_db, workflow_execution_id=workflow_execution_id)
        if workflow_executions:
            result = Workflow_executionsModel(**CamelCaseUtil.transform_result(workflow_executions))
        else:
            result = Workflow_executionsModel(**dict())

        return result

    @staticmethod
    async def export_workflow_executions_list_services(workflow_executions_list: List):
        """
        导出执行器执行记录信息service

        :param workflow_executions_list: 执行器执行记录信息列表
        :return: 执行器执行记录信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'workflowExecutionId': '执行记录ID',
            'workflowId': '执行器ID',
            'workflowName': '执行名称',
            'status': '执行状态',
            'startTime': '开始时间',
            'endTime': '结束时间',
            'duration': '执行时长(秒)',
            'inputData': '输入数据',
            'outputData': '输出数据',
            'contextData': '上下文数据',
            'totalNodes': '总节点数',
            'successNodes': '成功节点数',
            'failedNodes': '失败节点数',
            'skippedNodes': '跳过节点数',
            'errorMessage': '错误信息',
            'errorDetails': '错误详情',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(workflow_executions_list, mapping_dict)

        return binary_data
