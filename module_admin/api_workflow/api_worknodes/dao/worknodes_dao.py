from sqlalchemy import delete, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import ApiWorknodes
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import WorknodesModel, WorknodesPageQueryModel, WorknodesQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class WorknodesDao:
    """
    执行器节点模块数据库操作层
    """

    @classmethod
    async def get_worknodes_detail_by_id(cls, db: AsyncSession, node_id: int):
        """
        根据节点ID获取执行器节点详细信息

        :param db: orm对象
        :param node_id: 节点ID
        :return: 执行器节点信息对象
        """
        worknodes_info = (
            (
                await db.execute(
                    select(ApiWorknodes)
                    .where(
                        ApiWorknodes.node_id == node_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return worknodes_info

    @classmethod
    async def get_worknodes_detail_by_info(cls, db: AsyncSession, worknodes: WorknodesModel):
        """
        根据执行器节点参数获取执行器节点信息

        :param db: orm对象
        :param worknodes: 执行器节点参数对象
        :return: 执行器节点信息对象
        """
        worknodes_info = (
            (
                await db.execute(
                    select(ApiWorknodes).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return worknodes_info

    @classmethod
    async def get_worknodes_list(cls, db: AsyncSession, query_object: WorknodesPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取执行器节点列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 执行器节点列表信息字典对象
        """
        query = (
            select(ApiWorknodes)
            .where(
                ApiWorknodes.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiWorknodes.parent_id == str(query_object.parent_id) if query_object.parent_id else True,
                ApiWorknodes.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiWorknodes.type == query_object.type if query_object.type else True,
                ApiWorknodes.is_run == query_object.is_run if query_object.is_run else True,
                ApiWorknodes.description == query_object.description if query_object.description else True,
                ApiWorknodes.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorknodes.del_flag == "0")
            .order_by(ApiWorknodes.node_id)
            #.distinct()
        )
        worknodes_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return worknodes_list

    @classmethod
    async def get_worknodes_orm_list(cls, db: AsyncSession, query_object: WorknodesQueryModel):
        """
        根据查询参数获取执行器节点列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 执行器节点列表信息orm对象
        """
        query = (
            select(ApiWorknodes)
            .where(
                ApiWorknodes.workflow_id == query_object.workflow_id if query_object.workflow_id else True,
                ApiWorknodes.parent_id == str(query_object.parent_id) if query_object.parent_id else True,
                ApiWorknodes.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiWorknodes.type == query_object.type if query_object.type else True,
                ApiWorknodes.is_run == query_object.is_run if query_object.is_run else True,
                ApiWorknodes.children_ids == query_object.children_ids if query_object.children_ids else True,
                ApiWorknodes.config == query_object.config if query_object.config else True,
                ApiWorknodes.description == query_object.description if query_object.description else True,
                ApiWorknodes.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiWorknodes.del_flag == "0")
            .order_by(ApiWorknodes.node_id)
            #.distinct()
        )

        result = await db.execute(query)
        return result.scalars().all()  # 返回 ORM 对象列表

    @classmethod
    async def add_worknodes_dao(cls, db: AsyncSession, worknodes: WorknodesModel):
        """
        新增执行器节点数据库操作

        :param db: orm对象
        :param worknodes: 执行器节点对象
        :return:
        """
        x = worknodes.model_dump(exclude={'del_flag', 'case_ids', 'project_id', 'curl_command', 'after_node_id'})
        if isinstance(x.get("parent_id"), int):
            x["parent_id"] = str(x["parent_id"])

        if isinstance(x.get('workflow_id'), str):
            x["workflow_id"] = int(x["workflow_id"])
        db_worknodes = ApiWorknodes(**x)
        db.add(db_worknodes)
        await db.flush()
        await db.refresh(db_worknodes)

        return db_worknodes

    @classmethod
    async def edit_worknodes_dao(cls, db: AsyncSession, worknodes: dict):
        """
        编辑执行器节点数据库操作

        :param db: orm对象
        :param worknodes: 需要更新的执行器节点字典
        :return:
        """
        await db.execute(update(ApiWorknodes), [worknodes])

    @classmethod
    async def delete_worknodes_dao(cls, db: AsyncSession, worknodes: WorknodesModel):
        """
        删除执行器节点数据库操作

        :param db: orm对象
        :param worknodes: 执行器节点对象
        :return:
        """
        #await db.execute(delete(ApiWorknodes).where(ApiWorknodes.node_id.in_([worknodes.node_id])))
        await db.execute(update(ApiWorknodes).where(ApiWorknodes.node_id.in_([worknodes.node_id])).values(del_flag="1"))

    @classmethod
    async def get_all_children_nodes(cls, db: AsyncSession, parent_id: int):
        """
        获取某个节点下的所有直接子节点

        :param db: orm对象
        :param parent_id: 父节点ID
        :return: 子节点列表
        """
        query = (
            select(ApiWorknodes)
            .where(
                ApiWorknodes.parent_id == str(parent_id),
                ApiWorknodes.del_flag == "0"
            )
            .order_by(ApiWorknodes.node_id)
        )
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_max_sort_no(cls, db: AsyncSession, workflow_id: int, parent_id: str = None) -> float:
        """
        获取同级节点中的最大排序值

        :param db: orm对象
        :param workflow_id: 所属工作流ID
        :param parent_id: 父节点ID（可选，为None或空字符串表示顶级节点）
        :return: 最大排序值，如果没有同级节点则返回0
        """
        query = select(func.max(ApiWorknodes.sort_no)).where(
            ApiWorknodes.workflow_id == workflow_id,
            ApiWorknodes.del_flag == "0"
        )

        if parent_id:
            query = query.where(ApiWorknodes.parent_id == str(parent_id))
        else:
            query = query.where(
                (ApiWorknodes.parent_id == None) | (ApiWorknodes.parent_id == '')
            )

        result = await db.execute(query)
        max_sort_no = result.scalar()

        return max_sort_no if max_sort_no is not None else 0

    @classmethod
    async def update_sibling_sort_no(cls, db: AsyncSession, workflow_id: int, parent_id: str,
                                     after_sort_no: float) -> None:
        """
        将指定排序值之后的同级节点的排序值都+1

        :param db: orm对象
        :param workflow_id: 所属工作流ID
        :param parent_id: 父节点ID
        :param after_sort_no: 在此排序值之后的节点都需要更新
        """
        query = (
            update(ApiWorknodes)
            .where(
                ApiWorknodes.workflow_id == workflow_id,
                ApiWorknodes.sort_no > after_sort_no,
                ApiWorknodes.del_flag == "0"
            )
            .values(sort_no=ApiWorknodes.sort_no + 1)
        )

        if parent_id:
            query = query.where(ApiWorknodes.parent_id == str(parent_id))
        else:
            query = query.where(
                (ApiWorknodes.parent_id == None) | (ApiWorknodes.parent_id == '')
            )

        await db.execute(query)

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = WorknodesPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await WorknodesDao.get_worknodes_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
