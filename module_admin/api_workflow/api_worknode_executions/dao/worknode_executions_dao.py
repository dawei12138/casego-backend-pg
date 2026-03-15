from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_workflow.api_worknode_executions.entity.do.worknode_executions_do import ApiWorknodeExecutions
from module_admin.api_workflow.api_worknode_executions.entity.vo.worknode_executions_vo import Worknode_executionsModel, Worknode_executionsPageQueryModel, Worknode_executionsQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class Worknode_executionsDao:
    """
    节点执行记录模块数据库操作层
    """

    @classmethod
    async def get_worknode_executions_detail_by_id(cls, db: AsyncSession, node_execution_id: int):
        """
        根据节点执行记录ID获取节点执行记录详细信息

        :param db: orm对象
        :param node_execution_id: 节点执行记录ID
        :return: 节点执行记录信息对象
        """
        worknode_executions_info = (
            (
                await db.execute(
                    select(ApiWorknodeExecutions)
                    .where(
                        ApiWorknodeExecutions.node_execution_id == node_execution_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return worknode_executions_info

    @classmethod
    async def get_worknode_executions_detail_by_info(cls, db: AsyncSession, worknode_executions: Worknode_executionsModel):
        """
        根据节点执行记录参数获取节点执行记录信息

        :param db: orm对象
        :param worknode_executions: 节点执行记录参数对象
        :return: 节点执行记录信息对象
        """
        worknode_executions_info = (
            (
                await db.execute(
                    select(ApiWorknodeExecutions).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return worknode_executions_info

    @classmethod
    async def get_worknode_executions_list(cls, db: AsyncSession, query_object: Worknode_executionsPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取节点执行记录列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 节点执行记录列表信息字典对象
        """
        query = (
            select(ApiWorknodeExecutions)
            .where(
                ApiWorknodeExecutions.workflow_execution_id == query_object.workflow_execution_id if query_object.workflow_execution_id else True,
                ApiWorknodeExecutions.node_id == query_object.node_id if query_object.node_id else True,
                ApiWorknodeExecutions.status == query_object.status if query_object.status else True,
                ApiWorknodeExecutions.start_time == query_object.start_time if query_object.start_time else True,
                ApiWorknodeExecutions.end_time == query_object.end_time if query_object.end_time else True,
                ApiWorknodeExecutions.duration == query_object.duration if query_object.duration else True,
                ApiWorknodeExecutions.input_data == query_object.input_data if query_object.input_data else True,
                ApiWorknodeExecutions.output_data == query_object.output_data if query_object.output_data else True,
                ApiWorknodeExecutions.context_snapshot == query_object.context_snapshot if query_object.context_snapshot else True,
                ApiWorknodeExecutions.loop_index == query_object.loop_index if query_object.loop_index else True,
                ApiWorknodeExecutions.loop_item == query_object.loop_item if query_object.loop_item else True,
                ApiWorknodeExecutions.condition_result == query_object.condition_result if query_object.condition_result else True,
                ApiWorknodeExecutions.error_message == query_object.error_message if query_object.error_message else True,
                ApiWorknodeExecutions.error_details == query_object.error_details if query_object.error_details else True,
                ApiWorknodeExecutions.retry_count == query_object.retry_count if query_object.retry_count else True,
                ApiWorknodeExecutions.created_at == query_object.created_at if query_object.created_at else True,
                ApiWorknodeExecutions.description == query_object.description if query_object.description else True,
                ApiWorknodeExecutions.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorknodeExecutions.del_flag == "0")
            .order_by(ApiWorknodeExecutions.node_execution_id)
            #.distinct()
        )
        worknode_executions_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return worknode_executions_list

    @classmethod
    async def get_worknode_executions_orm_list(cls, db: AsyncSession, query_object: Worknode_executionsQueryModel):
        """
        根据查询参数获取节点执行记录列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 节点执行记录列表信息orm对象
        """
        query = (
            select(ApiWorknodeExecutions)
            .where(
                ApiWorknodeExecutions.workflow_execution_id == query_object.workflow_execution_id if query_object.workflow_execution_id else True,
                ApiWorknodeExecutions.node_id == query_object.node_id if query_object.node_id else True,
                ApiWorknodeExecutions.status == query_object.status if query_object.status else True,
                ApiWorknodeExecutions.start_time == query_object.start_time if query_object.start_time else True,
                ApiWorknodeExecutions.end_time == query_object.end_time if query_object.end_time else True,
                ApiWorknodeExecutions.duration == query_object.duration if query_object.duration else True,
                ApiWorknodeExecutions.input_data == query_object.input_data if query_object.input_data else True,
                ApiWorknodeExecutions.output_data == query_object.output_data if query_object.output_data else True,
                ApiWorknodeExecutions.context_snapshot == query_object.context_snapshot if query_object.context_snapshot else True,
                ApiWorknodeExecutions.loop_index == query_object.loop_index if query_object.loop_index else True,
                ApiWorknodeExecutions.loop_item == query_object.loop_item if query_object.loop_item else True,
                ApiWorknodeExecutions.condition_result == query_object.condition_result if query_object.condition_result else True,
                ApiWorknodeExecutions.error_message == query_object.error_message if query_object.error_message else True,
                ApiWorknodeExecutions.error_details == query_object.error_details if query_object.error_details else True,
                ApiWorknodeExecutions.retry_count == query_object.retry_count if query_object.retry_count else True,
                ApiWorknodeExecutions.created_at == query_object.created_at if query_object.created_at else True,
                ApiWorknodeExecutions.description == query_object.description if query_object.description else True,
                ApiWorknodeExecutions.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorknodeExecutions.del_flag == "0")
            .order_by(ApiWorknodeExecutions.node_execution_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_worknode_executions_dao(cls, db: AsyncSession, worknode_executions: Worknode_executionsModel):
        """
        新增节点执行记录数据库操作

        :param db: orm对象
        :param worknode_executions: 节点执行记录对象
        :return:
        """
        db_worknode_executions = ApiWorknodeExecutions(**worknode_executions.model_dump(exclude={'del_flag'}))
        db.add(db_worknode_executions)
        await db.flush()

        return db_worknode_executions

    @classmethod
    async def edit_worknode_executions_dao(cls, db: AsyncSession, worknode_executions: dict):
        """
        编辑节点执行记录数据库操作

        :param db: orm对象
        :param worknode_executions: 需要更新的节点执行记录字典
        :return:
        """
        await db.execute(update(ApiWorknodeExecutions), [worknode_executions])

    @classmethod
    async def delete_worknode_executions_dao(cls, db: AsyncSession, worknode_executions: Worknode_executionsModel):
        """
        删除节点执行记录数据库操作

        :param db: orm对象
        :param worknode_executions: 节点执行记录对象
        :return:
        """
        #await db.execute(delete(ApiWorknodeExecutions).where(ApiWorknodeExecutions.node_execution_id.in_([worknode_executions.node_execution_id])))
        await db.execute(update(ApiWorknodeExecutions).where(ApiWorknodeExecutions.node_execution_id.in_([worknode_executions.node_execution_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = Worknode_executionsPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await Worknode_executionsDao.get_worknode_executions_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
