import asyncio

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.api_project_submodules.entity.do.project_submodules_do import ApiProjectSubmodules
from module_admin.api_project_submodules.entity.vo.project_submodules_vo import Project_submodulesModel, \
    Project_submodulesPageQueryModel
from module_admin.api_testing.api_test_cases.entity.do.test_cases_do import ApiTestCases
from module_admin.api_workflow.workflow.entity.do.workflow_do import ApiWorkflow
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil
from config.get_db import get_db


class Project_submodulesDao:
    """
    项目模块模块数据库操作层
    """

    @classmethod
    async def get_project_submodules_detail_by_id(cls, db: AsyncSession, id: int):
        """
        根据ID获取项目模块详细信息

        :param db: orm对象
        :param id: ID
        :return: 项目模块信息对象
        """
        project_submodules_info = (
            (
                await db.execute(
                    select(ApiProjectSubmodules)
                    .where(
                        ApiProjectSubmodules.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_submodules_info

    @classmethod
    async def get_project_submodules_detail_by_info(cls, db: AsyncSession, project_submodules: Project_submodulesModel):
        """
        根据项目模块参数获取项目模块信息

        :param db: orm对象
        :param project_submodules: 项目模块参数对象
        :return: 项目模块信息对象
        """
        project_submodules_info = (
            (
                await db.execute(
                    select(ApiProjectSubmodules).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return project_submodules_info

    @classmethod
    async def get_project_submodules_list(cls, db: AsyncSession, query_object: Project_submodulesPageQueryModel,
                                          is_page: bool = False):
        """
        根据查询参数获取项目模块列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目模块列表信息对象
        """
        query = (
            select(ApiProjectSubmodules)
            .where(
                ApiProjectSubmodules.name.like(f'%{query_object.name}%') if query_object.name else True,
                ApiProjectSubmodules.type == query_object.type if query_object.type else True,
                ApiProjectSubmodules.parent_id == query_object.parent_id if query_object.parent_id else True,
                ApiProjectSubmodules.description == query_object.description if query_object.description else True,
                ApiProjectSubmodules.sort_no == query_object.sort_no if query_object.sort_no else True,
                ApiProjectSubmodules.project_id == query_object.project_id if query_object.project_id else True,
            )
            .where(ApiProjectSubmodules.del_flag == "0")
            .order_by(ApiProjectSubmodules.id)
            #.distinct()
        )
        project_submodules_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size,
                                                          is_page)

        return project_submodules_list

    @classmethod
    async def add_project_submodules_dao(cls, db: AsyncSession, project_submodules: Project_submodulesModel):
        """
        新增项目模块数据库操作

        :param db: orm对象
        :param project_submodules: 项目模块对象
        :return:
        """
        db_project_submodules = ApiProjectSubmodules(
            **project_submodules.model_dump(exclude={'ancestors', 'del_flag', }))
        db.add(db_project_submodules)
        await db.flush()

        return db_project_submodules

    @classmethod
    async def edit_project_submodules_dao(cls, db: AsyncSession, project_submodules: dict):
        """
        编辑项目模块数据库操作

        :param db: orm对象
        :param project_submodules: 需要更新的项目模块字典
        :return:
        """
        await db.execute(update(ApiProjectSubmodules), [project_submodules])

    @classmethod
    async def delete_project_submodules_dao(cls, db: AsyncSession, project_submodules: Project_submodulesModel):
        """
        删除项目模块数据库操作

        :param db: orm对象
        :param project_submodules: 项目模块对象
        :return:
        """
        # await db.execute(delete(ApiProjectSubmodules).where(ApiProjectSubmodules.id.in_([project_submodules.id])))
        await db.execute(
            update(ApiProjectSubmodules).where(ApiProjectSubmodules.id.in_([project_submodules.id])).values(del_flag="1"))

    @classmethod
    def build_module_tree_optimized(cls, modules: list, parent_cases_map: dict, child_cases_map: dict, parent_id=None):
        """
        优化版本：使用预加载数据在内存中构建树，避免 N+1 查询问题

        :param modules: 所有模块列表
        :param parent_cases_map: 模块ID -> 父用例列表 的映射
        :param child_cases_map: 父用例ID -> 子用例列表 的映射
        :param parent_id: 当前父模块ID
        :return: 树结构
        """
        tree = []

        # 筛选当前层级的模块
        current_level_modules = [m for m in modules if m.parent_id == parent_id]
        # 按 sort_no 排序
        current_level_modules.sort(key=lambda x: x.sort_no if x.sort_no is not None else 0)

        for module in current_level_modules:
            node = {
                "moduleId": module.id,
                "name": module.name,
                "type": "module",
                "children": cls.build_module_tree_optimized(modules, parent_cases_map, child_cases_map, module.id),
                "testCases": [],
                "count": 0
            }

            # 从预加载的映射中获取父用例
            parent_cases = parent_cases_map.get(module.id, [])

            for pc in parent_cases:
                case_data = {
                    "caseId": pc.case_id,
                    "name": pc.name,
                    "method": pc.method,
                    "type": "api",
                    "children": [],
                    "count": 0
                }

                # 从预加载的映射中获取子用例
                children = child_cases_map.get(pc.case_id, [])

                for cc in children:
                    case_data["children"].append({
                        "caseId": cc.case_id,
                        "name": cc.name,
                        "method": cc.method,
                        "type": "case",
                    })

                case_data["count"] = len(case_data["children"])
                node["testCases"].append(case_data)

            # 计算 module 节点的 count
            api_count = len(node["testCases"])
            for child_module in node["children"]:
                api_count += cls._count_apis_in_module(child_module)

            node["count"] = api_count
            tree.append(node)

        return tree

    @classmethod
    def _count_apis_in_module(cls, module_node):
        """递归计算模块中所有api节点的个数"""
        count = len(module_node.get("testCases", []))  # 当前模块的api个数

        # 递归计算子模块中的api个数
        for child_module in module_node.get("children", []):
            count += cls._count_apis_in_module(child_module)

        return count

    @classmethod
    async def get_project_tree_by_project_id(cls, db: AsyncSession, project_id: int) -> dict:
        """
        优化版本：使用 4 次查询替代 N+1 查询，大幅提升性能
        一级层级展现模块和 parent_submodule_id 为空的接口（case_type='1'）并列

        :param db: 数据库会话
        :param project_id: 项目ID
        :return: 树结构数据
        """
        from collections import defaultdict

        # 查询1: 获取所有模块
        modules_stmt = select(ApiProjectSubmodules).where(
            and_(
                ApiProjectSubmodules.project_id == project_id,
                ApiProjectSubmodules.del_flag == "0",
                ApiProjectSubmodules.type == "1"
            )
        ).order_by(ApiProjectSubmodules.sort_no)
        modules_result = await db.execute(modules_stmt)
        modules = modules_result.scalars().all()

        # 提取所有模块ID
        module_ids = [m.id for m in modules]

        # 查询2: 一次性获取所有属于模块的父用例 (case_type='1')
        parent_cases_map = defaultdict(list)
        parent_case_ids = []
        if module_ids:
            parent_cases_stmt = select(ApiTestCases).where(
                and_(
                    ApiTestCases.parent_submodule_id.in_(module_ids),
                    ApiTestCases.case_type == "1",
                    ApiTestCases.del_flag == "0"
                )
            ).order_by(ApiTestCases.sort_no)
            parent_cases_result = await db.execute(parent_cases_stmt)
            parent_cases = parent_cases_result.scalars().all()

            # 构建 模块ID -> 父用例列表 的映射
            for pc in parent_cases:
                parent_cases_map[pc.parent_submodule_id].append(pc)
                parent_case_ids.append(pc.case_id)

        # 查询3: 获取根级别的接口 (parent_submodule_id 为空, case_type='1', project_id 匹配)
        root_cases_stmt = select(ApiTestCases).where(
            and_(
                ApiTestCases.project_id == project_id,
                ApiTestCases.parent_submodule_id.is_(None),
                ApiTestCases.case_type == "1",
                ApiTestCases.del_flag == "0"
            )
        ).order_by(ApiTestCases.sort_no)
        root_cases_result = await db.execute(root_cases_stmt)
        root_cases = root_cases_result.scalars().all()

        # 收集根级别接口的 case_id
        root_case_ids = [rc.case_id for rc in root_cases]
        all_parent_case_ids = parent_case_ids + root_case_ids

        # 查询4: 一次性获取所有子用例 (case_type='2')
        child_cases_map = defaultdict(list)
        if all_parent_case_ids:
            child_cases_stmt = select(ApiTestCases).where(
                and_(
                    ApiTestCases.parent_case_id.in_(all_parent_case_ids),
                    ApiTestCases.case_type == "2",
                    ApiTestCases.del_flag == "0"
                )
            ).order_by(ApiTestCases.sort_no)
            child_cases_result = await db.execute(child_cases_stmt)
            child_cases = child_cases_result.scalars().all()

            # 构建 父用例ID -> 子用例列表 的映射
            for cc in child_cases:
                child_cases_map[cc.parent_case_id].append(cc)

        # 在内存中构建模块树结构
        tree_data = cls.build_module_tree_optimized(modules, parent_cases_map, child_cases_map, parent_id=None)

        # 将根级别接口直接添加到 tree_data 中，和模块并列
        for rc in root_cases:
            case_data = {
                "caseId": rc.case_id,
                "name": rc.name,
                "method": rc.method,
                "type": "api",
                "children": [],
                "count": 0
            }

            # 获取该接口的子用例
            children = child_cases_map.get(rc.case_id, [])
            for cc in children:
                case_data["children"].append({
                    "caseId": cc.case_id,
                    "name": cc.name,
                    "method": cc.method,
                    "type": "case",
                })

            case_data["count"] = len(case_data["children"])
            tree_data.append(case_data)

        return {"rows": CamelCaseUtil.transform_result(tree_data)}

    @classmethod
    def build_module_api_tree_optimized(cls, modules: list, parent_cases_map: dict, parent_id=None):
        """
        构建只包含模块和接口的树结构（不包含case类型节点）

        :param modules: 所有模块列表
        :param parent_cases_map: 模块ID -> 接口列表 的映射
        :param parent_id: 当前父模块ID
        :return: 树结构
        """
        tree = []

        # 筛选当前层级的模块
        current_level_modules = [m for m in modules if m.parent_id == parent_id]
        # 按 sort_no 排序
        current_level_modules.sort(key=lambda x: x.sort_no if x.sort_no is not None else 0)

        for module in current_level_modules:
            node = {
                "moduleId": module.id,
                "name": module.name,
                "type": "module",
                "children": cls.build_module_api_tree_optimized(modules, parent_cases_map, module.id),
                "testCases": [],
                "count": 0
            }

            # 从预加载的映射中获取接口
            parent_cases = parent_cases_map.get(module.id, [])

            for pc in parent_cases:
                case_data = {
                    "caseId": pc.case_id,
                    "name": pc.name,
                    "method": pc.method,
                    "type": "api",
                }
                node["testCases"].append(case_data)

            # 计算 module 节点的 count（只统计api数量）
            api_count = len(node["testCases"])
            for child_module in node["children"]:
                api_count += cls._count_apis_in_module_simple(child_module)

            node["count"] = api_count
            tree.append(node)

        return tree

    @classmethod
    def _count_apis_in_module_simple(cls, module_node):
        """递归计算模块中所有api节点的个数（简化版，不含case子节点）"""
        count = len(module_node.get("testCases", []))

        for child_module in module_node.get("children", []):
            count += cls._count_apis_in_module_simple(child_module)

        return count

    @classmethod
    async def get_project_api_tree_by_project_id(cls, db: AsyncSession, project_id: int) -> dict:
        """
        获取只包含模块和接口的树结构（用于导入接口选择）
        不包含case类型节点

        :param db: 数据库会话
        :param project_id: 项目ID
        :return: 树结构数据
        """
        from collections import defaultdict

        # 查询1: 获取所有模块
        modules_stmt = select(ApiProjectSubmodules).where(
            and_(
                ApiProjectSubmodules.project_id == project_id,
                ApiProjectSubmodules.del_flag == "0",
                ApiProjectSubmodules.type == "1"
            )
        ).order_by(ApiProjectSubmodules.sort_no)
        modules_result = await db.execute(modules_stmt)
        modules = modules_result.scalars().all()

        # 提取所有模块ID
        module_ids = [m.id for m in modules]

        # 查询2: 一次性获取所有属于模块的接口 (case_type='1')
        parent_cases_map = defaultdict(list)
        if module_ids:
            parent_cases_stmt = select(ApiTestCases).where(
                and_(
                    ApiTestCases.parent_submodule_id.in_(module_ids),
                    ApiTestCases.case_type == "1",
                    ApiTestCases.del_flag == "0"
                )
            ).order_by(ApiTestCases.sort_no)
            parent_cases_result = await db.execute(parent_cases_stmt)
            parent_cases = parent_cases_result.scalars().all()

            # 构建 模块ID -> 接口列表 的映射
            for pc in parent_cases:
                parent_cases_map[pc.parent_submodule_id].append(pc)

        # 查询3: 获取根级别的接口 (parent_submodule_id 为空, case_type='1')
        root_cases_stmt = select(ApiTestCases).where(
            and_(
                ApiTestCases.project_id == project_id,
                ApiTestCases.parent_submodule_id.is_(None),
                ApiTestCases.case_type == "1",
                ApiTestCases.del_flag == "0"
            )
        ).order_by(ApiTestCases.sort_no)
        root_cases_result = await db.execute(root_cases_stmt)
        root_cases = root_cases_result.scalars().all()

        # 在内存中构建模块树结构
        tree_data = cls.build_module_api_tree_optimized(modules, parent_cases_map, parent_id=None)

        # 将根级别接口直接添加到 tree_data 中，和模块并列
        for rc in root_cases:
            case_data = {
                "caseId": rc.case_id,
                "name": rc.name,
                "method": rc.method,
                "type": "api",
            }
            tree_data.append(case_data)

        return {"rows": CamelCaseUtil.transform_result(tree_data)}

    @classmethod
    def build_module_workflow_tree_optimized(cls, modules: list, workflows_map: dict, parent_id=None):
        """
        优化版本：使用预加载数据在内存中构建模块-工作流树，避免 N+1 查询问题

        :param modules: 所有模块列表
        :param workflows_map: 模块ID -> 工作流列表 的映射
        :param parent_id: 当前父模块ID
        :return: 树结构
        """
        tree = []

        # 筛选当前层级的模块
        current_level_modules = [m for m in modules if m.parent_id == parent_id]
        # 按 sort_no 排序
        current_level_modules.sort(key=lambda x: x.sort_no if x.sort_no is not None else 0)

        for module in current_level_modules:
            node = {
                "moduleId": module.id,
                "name": module.name,
                "type": "module",
                "children": cls.build_module_workflow_tree_optimized(modules, workflows_map, module.id),
                "workflows": [],
                "count": 0
            }

            # 从预加载的映射中获取工作流
            workflows = workflows_map.get(module.id, [])

            for workflow in workflows:
                workflow_data = {
                    "workflowId": workflow.workflow_id,
                    "name": workflow.name,
                    "type": "workflow",
                }
                node["workflows"].append(workflow_data)

            # 计算统计信息 - 当前模块及其所有子模块的工作流总数
            workflow_count = len(node["workflows"])
            for child_module in node["children"]:
                workflow_count += cls._count_workflows_in_module(child_module)

            node["count"] = workflow_count
            tree.append(node)

        return tree

    @classmethod
    def _count_workflows_in_module(cls, module_node):
        """
        递归计算模块节点中工作流的总数
        """
        count = len(module_node.get("workflows", []))  # 当前模块的workflow数量

        # 递归计算子模块中的workflow数量
        for child_module in module_node.get("children", []):
            count += cls._count_workflows_in_module(child_module)

        return count

    @classmethod
    async def get_project_workflow_tree_by_project_id(
        cls,
        db: AsyncSession,
        project_id: int,
        type: str = "2",
        parent_id: int = None
    ) -> dict:
        """
        优化版本：使用 2 次查询替代 N+1 查询，大幅提升性能

        :param db: 数据库会话
        :param project_id: 项目ID
        :param type: 模块类型（默认为2，工作流模块）
        :param parent_id: 父模块ID（可选，用于构建树的起始点）
        :return: 树结构数据
        """
        from collections import defaultdict

        # 查询1: 一次性获取所有模块
        modules_stmt = select(ApiProjectSubmodules).where(
            and_(
                ApiProjectSubmodules.project_id == project_id,
                ApiProjectSubmodules.del_flag == "0",
                ApiProjectSubmodules.type == type
            )
        ).order_by(ApiProjectSubmodules.sort_no)
        modules_result = await db.execute(modules_stmt)
        modules = modules_result.scalars().all()

        # 查询2: 一次性获取该项目下所有工作流（包括有模块的和无模块的）
        workflows_stmt = select(ApiWorkflow).where(
            and_(
                ApiWorkflow.project_id == project_id,
                ApiWorkflow.del_flag == "0"
            )
        )
        workflows_result = await db.execute(workflows_stmt)
        workflows = workflows_result.scalars().all()

        # 构建 模块ID -> 工作流列表 的映射
        workflows_map = defaultdict(list)
        root_workflows = []  # 没有父模块的工作流（直接属于项目）

        for workflow in workflows:
            if workflow.parent_submodule_id is None:
                root_workflows.append(workflow)
            else:
                workflows_map[workflow.parent_submodule_id].append(workflow)

        # 在内存中构建模块树结构
        tree_data = cls.build_module_workflow_tree_optimized(modules, workflows_map, parent_id=parent_id)

        # 添加直接属于项目的工作流到根级别
        for workflow in root_workflows:
            workflow_node = {
                "workflowId": workflow.workflow_id,
                "name": workflow.name,
                "type": "workflow",
            }
            tree_data.append(workflow_node)

        return {"rows": CamelCaseUtil.transform_result(tree_data)}


async def main():
    async for db in get_db():
        try:
            project_id = 1  # 替换成你要测试的项目 ID
            result = await Project_submodulesDao.get_project_tree_by_project_id(db, project_id)
            print("查询结果:", result)
        except Exception as e:
            print(f"发生错误: {e}")
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(main())
