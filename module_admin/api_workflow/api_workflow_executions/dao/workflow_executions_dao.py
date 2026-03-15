from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_workflow.api_workflow_executions.entity.do.workflow_executions_do import ApiWorkflowExecutions
from module_admin.api_workflow.api_workflow_executions.entity.vo.workflow_executions_vo import Workflow_executionsModel, Workflow_executionsPageQueryModel, Workflow_executionsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Workflow_executionsDao:
    """
    执行器执行记录模块数据库操作层
    """

    @classmethod
    async def get_workflow_executions_detail_by_id(cls, db: AsyncSession, workflow_execution_id: int):
        """
        根据执行记录ID获取执行器执行记录详细信息

        :param db: orm对象
        :param workflow_execution_id: 执行记录ID
        :return: 执行器执行记录信息对象
        """
        workflow_executions_info = (
            (
                await db.execute(
                    select(ApiWorkflowExecutions)
                    .where(
                        ApiWorkflowExecutions.workflow_execution_id == workflow_execution_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return workflow_executions_info

    @classmethod
    async def get_workflow_executions_detail_by_info(cls, db: AsyncSession, workflow_executions: Workflow_executionsModel):
        """
        根据执行器执行记录参数获取执行器执行记录信息

        :param db: orm对象
        :param workflow_executions: 执行器执行记录参数对象
        :return: 执行器执行记录信息对象
        """
        workflow_executions_info = (
            (
                await db.execute(
                    select(ApiWorkflowExecutions).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return workflow_executions_info

    @classmethod
    async def get_workflow_executions_list(cls, db: AsyncSession, query_object: Workflow_executionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取执行器执行记录列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 执行器执行记录列表信息字典对象
        """
        query = (
            select(ApiWorkflowExecutions)
            .where(
                ApiWorkflowExecutions.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiWorkflowExecutions.workflow_name.like(f'%{query_object.workflow_name}%') if query_object.workflow_name else True,
                ApiWorkflowExecutions.status == query_object.status if query_object.status else True,
                ApiWorkflowExecutions.start_time == query_object.start_time if query_object.start_time else True,
                ApiWorkflowExecutions.end_time == query_object.end_time if query_object.end_time else True,
                ApiWorkflowExecutions.duration == query_object.duration if query_object.duration else True,
                ApiWorkflowExecutions.input_data == query_object.input_data if query_object.input_data else True,
                ApiWorkflowExecutions.output_data == query_object.output_data if query_object.output_data else True,
                ApiWorkflowExecutions.context_data == query_object.context_data if query_object.context_data else True,
                ApiWorkflowExecutions.total_nodes == query_object.total_nodes if query_object.total_nodes else True,
                ApiWorkflowExecutions.success_nodes == query_object.success_nodes if query_object.success_nodes else True,
                ApiWorkflowExecutions.failed_nodes == query_object.failed_nodes if query_object.failed_nodes else True,
                ApiWorkflowExecutions.skipped_nodes == query_object.skipped_nodes if query_object.skipped_nodes else True,
                ApiWorkflowExecutions.error_message == query_object.error_message if query_object.error_message else True,
                ApiWorkflowExecutions.error_details == query_object.error_details if query_object.error_details else True,
                ApiWorkflowExecutions.description == query_object.description if query_object.description else True,
                ApiWorkflowExecutions.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorkflowExecutions.del_flag == "0")
            .order_by(ApiWorkflowExecutions.workflow_execution_id)
            #.distinct()
        )
        workflow_executions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return workflow_executions_list

    @classmethod
    async def get_workflow_executions_orm_list(cls, db: AsyncSession, query_object: Workflow_executionsQueryModel):
        """
        根据查询参数获取执行器执行记录列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 执行器执行记录列表信息orm对象
        """
        query = (
            select(ApiWorkflowExecutions)
            .where(
                ApiWorkflowExecutions.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiWorkflowExecutions.workflow_name.like(f'%{query_object.workflow_name}%') if query_object.workflow_name else True,
                ApiWorkflowExecutions.status == query_object.status if query_object.status else True,
                ApiWorkflowExecutions.start_time == query_object.start_time if query_object.start_time else True,
                ApiWorkflowExecutions.end_time == query_object.end_time if query_object.end_time else True,
                ApiWorkflowExecutions.duration == query_object.duration if query_object.duration else True,
                ApiWorkflowExecutions.input_data == query_object.input_data if query_object.input_data else True,
                ApiWorkflowExecutions.output_data == query_object.output_data if query_object.output_data else True,
                ApiWorkflowExecutions.context_data == query_object.context_data if query_object.context_data else True,
                ApiWorkflowExecutions.total_nodes == query_object.total_nodes if query_object.total_nodes else True,
                ApiWorkflowExecutions.success_nodes == query_object.success_nodes if query_object.success_nodes else True,
                ApiWorkflowExecutions.failed_nodes == query_object.failed_nodes if query_object.failed_nodes else True,
                ApiWorkflowExecutions.skipped_nodes == query_object.skipped_nodes if query_object.skipped_nodes else True,
                ApiWorkflowExecutions.error_message == query_object.error_message if query_object.error_message else True,
                ApiWorkflowExecutions.error_details == query_object.error_details if query_object.error_details else True,
                ApiWorkflowExecutions.description == query_object.description if query_object.description else True,
                ApiWorkflowExecutions.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorkflowExecutions.del_flag == "0")
            .order_by(ApiWorkflowExecutions.workflow_execution_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_workflow_executions_dao(cls, db: AsyncSession, workflow_executions: Workflow_executionsModel):
        """
        新增执行器执行记录数据库操作

        :param db: orm对象
        :param workflow_executions: 执行器执行记录对象
        :return:
        """
        db_workflow_executions = ApiWorkflowExecutions(**workflow_executions.model_dump(exclude={'del_flag'}))
        db.add(db_workflow_executions)
        await db.flush()

        return db_workflow_executions

    @classmethod
    async def edit_workflow_executions_dao(cls, db: AsyncSession, workflow_executions: dict):
        """
        编辑执行器执行记录数据库操作

        :param db: orm对象
        :param workflow_executions: 需要更新的执行器执行记录字典
        :return:
        """
        await db.execute(update(ApiWorkflowExecutions), [workflow_executions])

    @classmethod
    async def delete_workflow_executions_dao(cls, db: AsyncSession, workflow_executions: Workflow_executionsModel):
        """
        删除执行器执行记录数据库操作

        :param db: orm对象
        :param workflow_executions: 执行器执行记录对象
        :return:
        """
        #await db.execute(delete(ApiWorkflowExecutions).where(ApiWorkflowExecutions.workflow_execution_id.in_([workflow_executions.workflow_execution_id])))
        await db.execute(update(ApiWorkflowExecutions).where(ApiWorkflowExecutions.workflow_execution_id.in_([workflow_executions.workflow_execution_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Workflow_executionsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Workflow_executionsDao.get_workflow_executions_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
