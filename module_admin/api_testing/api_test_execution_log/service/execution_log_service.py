import json
from datetime import datetime, date
from enum import Enum

from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_testing.api_test_execution_log.dao.execution_log_dao import Execution_logDao
from module_admin.api_testing.api_test_execution_log.entity.vo.execution_log_vo import DeleteExecution_logModel, \
    Execution_logModel, Execution_logPageQueryModel
from utils.api_workflow_tools.models import StreamEvent, StreamEventType
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil
from utils.log_util import logger


class Execution_logService:
    """
    接口测试执行日志模块服务层
    """

    @staticmethod
    def _datetime_converter(o):
        """处理 datetime 对象的 JSON 序列化"""
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, Enum):
            return o.value
        raise TypeError(f"Type {type(o)} not serializable")

    @classmethod
    async def get_execution_log_list_services(
            cls, query_db: AsyncSession, query_object: Execution_logPageQueryModel, is_page: bool = False
    ):
        """
        获取接口测试执行日志列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口测试执行日志列表信息对象
        """
        execution_log_list_result = await Execution_logDao.get_execution_log_list(query_db, query_object, is_page)

        return execution_log_list_result

    @classmethod
    async def add_execution_log_services(cls, query_db: AsyncSession, page_object: Execution_logModel):
        """
        新增接口测试执行日志信息service

        :param query_db: orm对象
        :param page_object: 新增接口测试执行日志对象
        :return: 新增接口测试执行日志校验结果
        """
        try:
            await Execution_logDao.add_execution_log_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    # 在 Execution_logService 类中添加这个方法
    @classmethod
    async def add_event_log(cls, event: StreamEvent, query_db: AsyncSession, sort: int, report_id: int):
        """
        新增接口测试执行日志信息service
        """
        try:
            # 方案1: 直接传递原始数据,让数据库驱动处理序列化
            # 如果你的 execution_data 字段是 JSON 类型,SQLAlchemy 会自动处理

            if event.event_type == StreamEventType.CASE_RESULT:
                log_model = Execution_logModel(
                    case_id=event.case_id,
                    execution_data=event.data,  # 直接传递,不做预处理
                    method=event.method,
                    path=event.path,
                    name=event.name,
                    is_success=event.is_success,
                    response_status_code=event.response_status_code,
                    response_time=event.response_time,
                    assertion_success=event.assertion_success,
                    workflow_id=event.workflow_id,
                    event_type=event.event_type,
                    sort_no=sort,
                    report_id=report_id
                )
            else:
                log_model = Execution_logModel(
                    name=event.message,
                    is_success=event.is_success,
                    workflow_id=event.workflow_id,
                    event_type=event.event_type,
                    sort_no=sort,
                    report_id=report_id
                )

            res = await Execution_logDao.add_execution_log_dao(query_db, log_model)
            await query_db.commit()
            await query_db.refresh(res)  # 重新从数据库加载,**很重要，不然报错
            # await query_db.commit()
            return res.log_id

        except Exception as e:
            # 回滚事务
            await query_db.rollback()
            logger.error(f"记录执行日志失败: {str(e)}")
            return None

    @classmethod
    async def edit_execution_log_services(cls, query_db: AsyncSession, page_object: Execution_logModel):
        """
        编辑接口测试执行日志信息service

        :param query_db: orm对象
        :param page_object: 编辑接口测试执行日志对象
        :return: 编辑接口测试执行日志校验结果
        """
        edit_execution_log = page_object.model_dump(exclude_unset=True,
                                                    exclude={'create_by', 'create_time', 'del_flag'})
        execution_log_info = await cls.execution_log_detail_services(query_db, page_object.log_id)
        if execution_log_info.log_id:
            try:
                await Execution_logDao.edit_execution_log_dao(query_db, edit_execution_log)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='接口测试执行日志不存在')

    @classmethod
    async def delete_execution_log_services(cls, query_db: AsyncSession, page_object: DeleteExecution_logModel):
        """
        删除接口测试执行日志信息service

        :param query_db: orm对象
        :param page_object: 删除接口测试执行日志对象
        :return: 删除接口测试执行日志校验结果
        """
        if page_object.log_ids:
            log_id_list = page_object.log_ids.split(',')
            try:
                for log_id in log_id_list:
                    await Execution_logDao.delete_execution_log_dao(query_db, Execution_logModel(logId=log_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入执行日志ID为空')

    @classmethod
    async def execution_log_detail_services(cls, query_db: AsyncSession, log_id: int):
        """
        获取接口测试执行日志详细信息service

        :param query_db: orm对象
        :param log_id: 执行日志ID
        :return: 执行日志ID对应的信息
        """
        execution_log = await Execution_logDao.get_execution_log_detail_by_id(query_db, log_id=log_id)
        if execution_log:
            result = Execution_logModel(**CamelCaseUtil.transform_result(execution_log))
        else:
            result = Execution_logModel(**dict())

        return result

    @staticmethod
    async def export_execution_log_list_services(execution_log_list: List):
        """
        导出接口测试执行日志信息service

        :param execution_log_list: 接口测试执行日志信息列表
        :return: 接口测试执行日志信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'logId': '执行日志ID',
            'caseId': '测试用例ID',
            'caseName': '测试用例名称',
            'executionTime': '执行时间',
            'isSuccess': '是否执行成功',
            'executionData': '完整执行数据',
            'responseStatusCode': '响应状态码',
            'responseTime': '响应时间(秒)',
            'assertionSuccess': '断言是否成功',
            'projectId': '项目ID',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(execution_log_list, mapping_dict)

        return binary_data
