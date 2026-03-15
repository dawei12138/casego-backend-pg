from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.api_testing.api_test_execution_log.dao.execution_log_dao import Execution_logDao
from module_admin.api_testing.api_test_execution_log.entity.vo.execution_log_vo import Execution_logQueryModel, \
    Execution_logPageQueryModel
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.api_workflow_report.dao.api_workflow_report_dao import Api_workflow_reportDao
from module_admin.api_workflow.api_workflow_report.entity.vo.api_workflow_report_vo import \
    DeleteApi_workflow_reportModel, Api_workflow_reportModel, Api_workflow_reportPageQueryModel, \
    Api_workflow_report_log_Model
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Api_workflow_reportService:
    """
    自动化测试执行报告模块服务层
    """

    @classmethod
    async def get_api_workflow_report_list_services(
            cls, query_db: AsyncSession, query_object: Api_workflow_reportPageQueryModel, is_page: bool = False
    ):
        """
        获取自动化测试执行报告列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 自动化测试执行报告列表信息对象
        """
        api_workflow_report_list_result = await Api_workflow_reportDao.get_api_workflow_report_list(query_db,
                                                                                                    query_object,
                                                                                                    is_page)

        return api_workflow_report_list_result

    @classmethod
    async def add_api_workflow_report_services(cls, query_db: AsyncSession, page_object: Api_workflow_reportModel):
        """
        新增自动化测试执行报告信息service

        :param query_db: orm对象
        :param page_object: 新增自动化测试执行报告对象
        :return: 新增自动化测试执行报告校验结果
        """
        try:
            await Api_workflow_reportDao.add_api_workflow_report_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def add_workflow_report_services(cls, query_db: AsyncSession, page_object: Api_workflow_reportModel):
        """
        新增自动化测试执行报告信息service

        :param query_db: orm对象
        :param page_object: 新增自动化测试执行报告对象
        :return: 新增自动化测试执行报告校验结果
        """
        try:
            res = await Api_workflow_reportDao.add_api_workflow_report_dao(query_db, page_object)
            await query_db.commit()
            await query_db.refresh(res)
            return res.report_id
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_api_workflow_report_services(cls, query_db: AsyncSession, page_object: Api_workflow_reportModel):
        """
        编辑自动化测试执行报告信息service

        :param query_db: orm对象
        :param page_object: 编辑自动化测试执行报告对象
        :return: 编辑自动化测试执行报告校验结果
        """
        edit_api_workflow_report = page_object.model_dump(exclude_unset=True,
                                                          exclude={'create_by', 'create_time', 'del_flag'})
        api_workflow_report_info = await cls.api_workflow_report_detail_services(query_db, page_object.report_id)
        if api_workflow_report_info.report_id:
            try:
                await Api_workflow_reportDao.edit_api_workflow_report_dao(query_db, edit_api_workflow_report)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='自动化测试执行报告不存在')

    @classmethod
    async def delete_api_workflow_report_services(cls, query_db: AsyncSession,
                                                  page_object: DeleteApi_workflow_reportModel):
        """
        删除自动化测试执行报告信息service

        :param query_db: orm对象
        :param page_object: 删除自动化测试执行报告对象
        :return: 删除自动化测试执行报告校验结果
        """
        if page_object.report_ids:
            report_id_list = page_object.report_ids.split(',')
            try:
                for report_id in report_id_list:
                    await Api_workflow_reportDao.delete_api_workflow_report_dao(query_db, Api_workflow_reportModel(
                        reportId=report_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入报告ID为空')

    @classmethod
    async def api_workflow_report_detail_services(cls, query_db: AsyncSession, report_id: int):
        """
        获取自动化测试执行报告详细信息service

        :param query_db: orm对象
        :param report_id: 报告ID
        :return: 报告ID对应的信息
        """
        api_workflow_report = await Api_workflow_reportDao.get_api_workflow_report_detail_by_id(query_db,
                                                                                                report_id=report_id)

        if api_workflow_report:
            result = Api_workflow_report_log_Model(**CamelCaseUtil.transform_result(api_workflow_report))
            result.report_logs = await Execution_logDao.get_execution_log_orm_list(query_db,
                                                                                   Execution_logPageQueryModel(
                                                                                       report_id=result.report_id))

        else:
            result = Api_workflow_reportModel(**dict())

        return result

    @staticmethod
    async def export_api_workflow_report_list_services(api_workflow_report_list: List):
        """
        导出自动化测试执行报告信息service

        :param api_workflow_report_list: 自动化测试执行报告信息列表
        :return: 自动化测试执行报告信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'reportId': '报告ID',
            'workflowId': '执行器ID',
            'name': '报告名称',
            'startTime': '开始时间',
            'endTime': '结束时间',
            'totalCases': '总用例数',
            'successCases': '成功用例数',
            'failedCases': '失败用例数',
            'duration': '总耗时(秒)',
            'isSuccess': '是否全部成功',
            'reportData': '完整报告JSON数据',
            'triggerType': '触发类型',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(api_workflow_report_list, mapping_dict)

        return binary_data
