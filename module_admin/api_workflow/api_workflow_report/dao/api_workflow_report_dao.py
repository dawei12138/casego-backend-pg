from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.api_workflow.api_workflow_report.entity.do.api_workflow_report_do import ApiWorkflowReport
from module_admin.api_workflow.api_workflow_report.entity.vo.api_workflow_report_vo import Api_workflow_reportModel, \
    Api_workflow_reportPageQueryModel, Api_workflow_reportQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db


class Api_workflow_reportDao:
    """
    自动化测试执行报告模块数据库操作层
    """

    @classmethod
    async def get_api_workflow_report_detail_by_id(cls, db: AsyncSession, report_id: int):
        """
        根据报告ID获取自动化测试执行报告详细信息

        :param db: orm对象
        :param report_id: 报告ID
        :return: 自动化测试执行报告信息对象
        """
        api_workflow_report_info = (
            (
                await db.execute(
                    select(ApiWorkflowReport)
                    .where(
                        ApiWorkflowReport.report_id == report_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_workflow_report_info

    @classmethod
    async def get_api_workflow_report_detail_by_info(cls, db: AsyncSession,
                                                     api_workflow_report: Api_workflow_reportModel):
        """
        根据自动化测试执行报告参数获取自动化测试执行报告信息

        :param db: orm对象
        :param api_workflow_report: 自动化测试执行报告参数对象
        :return: 自动化测试执行报告信息对象
        """
        api_workflow_report_info = (
            (
                await db.execute(
                    select(ApiWorkflowReport).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return api_workflow_report_info

    @classmethod
    async def get_api_workflow_report_list(cls, db: AsyncSession, query_object: Api_workflow_reportPageQueryModel,
                                           is_page: bool = False):
        """
        根据查询参数获取自动化测试执行报告列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 自动化测试执行报告列表信息字典对象
        """
        query = (
            select(ApiWorkflowReport)
            .where(
                ApiWorkflowReport.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiWorkflowReport.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiWorkflowReport.start_time == query_object.start_time if query_object.start_time else True,
                ApiWorkflowReport.end_time == query_object.end_time if query_object.end_time else True,
                ApiWorkflowReport.total_cases == query_object.total_cases if query_object.total_cases else True,
                ApiWorkflowReport.success_cases == query_object.success_cases if query_object.success_cases else True,
                ApiWorkflowReport.failed_cases == query_object.failed_cases if query_object.failed_cases else True,
                ApiWorkflowReport.duration == query_object.duration if query_object.duration else True,
                ApiWorkflowReport.is_success == query_object.is_success if query_object.is_success else True,
                ApiWorkflowReport.report_data == query_object.report_data if query_object.report_data else True,
                ApiWorkflowReport.trigger_type == query_object.trigger_type if query_object.trigger_type else True,
                ApiWorkflowReport.description == query_object.description if query_object.description else True,
                ApiWorkflowReport.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorkflowReport.del_flag == "0")
            .order_by(ApiWorkflowReport.start_time.desc())
            #.distinct()
        )
        api_workflow_report_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return api_workflow_report_list
    @classmethod
    async def get_api_workflow_report_orm_list(cls, db: AsyncSession, query_object: Api_workflow_reportQueryModel) -> \
    List[Api_workflow_reportQueryModel]:
        """
        根据查询参数获取自动化测试执行报告列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 自动化测试执行报告列表信息orm对象
        """
        query = (
            select(ApiWorkflowReport)
            .where(
                ApiWorkflowReport.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiWorkflowReport.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiWorkflowReport.start_time == query_object.start_time if query_object.start_time else True,
                ApiWorkflowReport.end_time == query_object.end_time if query_object.end_time else True,
                ApiWorkflowReport.total_cases == query_object.total_cases if query_object.total_cases else True,
                ApiWorkflowReport.success_cases == query_object.success_cases if query_object.success_cases else True,
                ApiWorkflowReport.failed_cases == query_object.failed_cases if query_object.failed_cases else True,
                ApiWorkflowReport.duration == query_object.duration if query_object.duration else True,
                ApiWorkflowReport.is_success == query_object.is_success if query_object.is_success else True,
                ApiWorkflowReport.report_data == query_object.report_data if query_object.report_data else True,
                ApiWorkflowReport.trigger_type == query_object.trigger_type if query_object.trigger_type else True,
                ApiWorkflowReport.description == query_object.description if query_object.description else True,
                ApiWorkflowReport.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorkflowReport.del_flag == "0")
            .order_by(ApiWorkflowReport.report_id)
            #.distinct()
        )

        result = await db.execute(query)
        return [Api_workflow_reportQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_api_workflow_report_dao(cls, db: AsyncSession, api_workflow_report: Api_workflow_reportModel):
        """
        新增自动化测试执行报告数据库操作

        :param db: orm对象
        :param api_workflow_report: 自动化测试执行报告对象
        :return:
        """
        db_api_workflow_report = ApiWorkflowReport(**api_workflow_report.model_dump(exclude={}))
        db.add(db_api_workflow_report)
        await db.flush()

        return db_api_workflow_report

    @classmethod
    async def edit_api_workflow_report_dao(cls, db: AsyncSession, api_workflow_report: dict):
        """
        编辑自动化测试执行报告数据库操作

        :param db: orm对象
        :param api_workflow_report: 需要更新的自动化测试执行报告字典
        :return:
        """
        await db.execute(update(ApiWorkflowReport), [api_workflow_report])

    @classmethod
    async def delete_api_workflow_report_dao(cls, db: AsyncSession, api_workflow_report: Api_workflow_reportModel):
        """
        删除自动化测试执行报告数据库操作

        :param db: orm对象
        :param api_workflow_report: 自动化测试执行报告对象
        :return:
        """
        # await db.execute(delete(ApiWorkflowReport).where(ApiWorkflowReport.report_id.in_([api_workflow_report.report_id])))
        await db.execute(
            update(ApiWorkflowReport).where(ApiWorkflowReport.report_id.in_([api_workflow_report.report_id])).values(
                del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Api_workflow_reportPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Api_workflow_reportDao.get_api_workflow_report_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
