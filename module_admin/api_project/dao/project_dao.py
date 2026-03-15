from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_project.entity.do.project_do import ApiProject
from module_admin.api_project.entity.vo.project_vo import ProjectModel, ProjectPageQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db


class ProjectDao:
    """
    项目模块数据库操作层
    """

    @classmethod
    async def get_project_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据ID获取项目详细信息

        :param db: orm对象
        :param id: ID
        :return: 项目信息对象
        """
        project_info = (
            (
                await db.execute(
                    select(ApiProject)
                    .where(
                        ApiProject.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_info

    @classmethod
    async def get_project_detail_by_info(cls, db: AsyncSession, project: ProjectModel):
        """
        根据项目参数获取项目信息

        :param db: orm对象
        :param project: 项目参数对象
        :return: 项目信息对象
        """
        project_info = (
            (
                await db.execute(
                    select(ApiProject).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_info

    @classmethod
    async def get_project_list(cls, db: AsyncSession, query_object: ProjectPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取项目列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        query = (
            select(ApiProject)
            .where(
                ApiProject.name.like(f'%{query_object.name}%') if query_object.name else True,
            )
            .where(ApiProject.del_flag == "0")
            .order_by(ApiProject.id)
            #.distinct()
        )
        project_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return project_list

    @classmethod
    async def add_project_dao(cls, db: AsyncSession, project: ProjectModel):
        """
        新增项目数据库操作

        :param db: orm对象
        :param project: 项目对象
        :return:
        """
        db_project = ApiProject(
            **project.model_dump(exclude={'type', 'parent_id', 'remark', 'sort_no', 'del_flag', 'ancestors'}))
        db.add(db_project)
        await db.flush()

        return db_project

    @classmethod
    async def edit_project_dao(cls, db: AsyncSession, project: dict):
        """
        编辑项目数据库操作

        :param db: orm对象
        :param project: 需要更新的项目字典
        :return:
        """
        await db.execute(update(ApiProject), [project])

    @classmethod
    async def delete_project_dao(cls, db: AsyncSession, project: ProjectModel):
        """
        删除项目数据库操作

        :param db: orm对象
        :param project: 项目对象
        :return:
        """
        # await db.execute(delete(ApiProject).where(ApiProject.id.in_([project.id])))
        await db.execute(update(ApiProject).where(ApiProject.id.in_([project.id])).values(del_flag="1"))


if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = ProjectPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await ProjectDao.get_project_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()


    asyncio.run(main())
