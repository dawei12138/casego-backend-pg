from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_workflow.workflow.entity.do.workflow_do import ApiWorkflow
from module_admin.api_workflow.workflow.entity.vo.workflow_vo import WorkflowModel, WorkflowPageQueryModel, WorkflowQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class WorkflowDao:
    """
    测试执行器主模块数据库操作层
    """

    @classmethod
    async def get_workflow_detail_by_id(cls, db: AsyncSession, workflow_id: int):
        """
        根据执行器ID获取测试执行器主详细信息

        :param db: orm对象
        :param workflow_id: 执行器ID
        :return: 测试执行器主信息对象
        """
        workflow_info = (
            (
                await db.execute(
                    select(ApiWorkflow)
                    .where(
                        ApiWorkflow.workflow_id == workflow_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return workflow_info

    @classmethod
    async def get_workflow_detail_by_info(cls, db: AsyncSession, workflow: WorkflowModel):
        """
        根据测试执行器主参数获取测试执行器主信息

        :param db: orm对象
        :param workflow: 测试执行器主参数对象
        :return: 测试执行器主信息对象
        """
        workflow_info = (
            (
                await db.execute(
                    select(ApiWorkflow).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return workflow_info

    @classmethod
    async def get_workflow_list(cls, db: AsyncSession, query_object: WorkflowPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取测试执行器主列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试执行器主列表信息字典对象
        """
        query = (
            select(ApiWorkflow)
            .where(
                ApiWorkflow.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiWorkflow.parent_submodule_id == query_object.parent_submodule_id if query_object.parent_submodule_id else True,
            )
            .where(ApiWorkflow.del_flag == "0")
            .order_by(ApiWorkflow.workflow_id)
            #.distinct()
        )
        workflow_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return workflow_list

    @classmethod
    async def get_workflow_orm_list(cls, db: AsyncSession, query_object: WorkflowQueryModel):
        """
        根据查询参数获取测试执行器主列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 测试执行器主列表信息orm对象
        """
        query = (
            select(ApiWorkflow)
            .where(
                ApiWorkflow.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiWorkflow.parent_submodule_id == query_object.parent_submodule_id if query_object.parent_submodule_id else True,
            )
            .where(ApiWorkflow.del_flag == "0")
            .order_by(ApiWorkflow.workflow_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_workflow_dao(cls, db: AsyncSession, workflow: WorkflowModel):
        """
        新增测试执行器主数据库操作

        :param db: orm对象
        :param workflow: 测试执行器主对象
        :return:
        """
        x = workflow.model_dump(exclude={'del_flag'})
        db_workflow = ApiWorkflow(**x)
        db.add(db_workflow)
        await db.flush()

        return db_workflow

    @classmethod
    async def edit_workflow_dao(cls, db: AsyncSession, workflow: dict):
        """
        编辑测试执行器主数据库操作

        :param db: orm对象
        :param workflow: 需要更新的测试执行器主字典
        :return:
        """
        await db.execute(update(ApiWorkflow), [workflow])

    @classmethod
    async def delete_workflow_dao(cls, db: AsyncSession, workflow: WorkflowModel):
        """
        删除测试执行器主数据库操作

        :param db: orm对象
        :param workflow: 测试执行器主对象
        :return:
        """
        #await db.execute(delete(ApiWorkflow).where(ApiWorkflow.workflow_id.in_([workflow.workflow_id])))
        await db.execute(update(ApiWorkflow).where(ApiWorkflow.workflow_id.in_([workflow.workflow_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = WorkflowPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await WorkflowDao.get_workflow_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
