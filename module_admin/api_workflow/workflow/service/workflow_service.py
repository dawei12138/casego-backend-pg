from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from config.enums import Assertion_Method
from exceptions.exception import ServiceException
from module_admin.api_project_submodules.entity.do.project_submodules_do import ApiProjectSubmodules
from module_admin.api_project_submodules.entity.vo.project_submodules_vo import Project_submodulesPageQueryModel, \
    Project_submodulesModel
from module_admin.api_project_submodules.service.project_submodules_service import Project_submodulesService
from module_admin.api_testing.api_test_cases.dao.test_cases_dao import Test_casesDao
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import ApiWorknodes
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import WorknodesModelWithChildren, TaskTypeEnum
from module_admin.api_workflow.workflow.entity.do.workflow_do import ApiWorkflow
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.workflow.dao.workflow_dao import WorkflowDao
from module_admin.api_workflow.workflow.entity.vo.workflow_vo import DeleteWorkflowModel, WorkflowModel, \
    WorkflowPageQueryModel, WorkflowTreeModel

from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import NodeTypeEnum


class WorkflowService:
    """
    测试执行器主模块服务层
    """

    @classmethod
    async def get_workflow_list_services(
            cls, query_db: AsyncSession, query_object: WorkflowPageQueryModel, is_page: bool = False
    ):
        """
        获取测试执行器主列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试执行器主列表信息对象
        """
        workflow_list_result = await WorkflowDao.get_workflow_list(query_db, query_object, is_page)

        return workflow_list_result

    @classmethod
    async def build_module_tree(cls, modules, workflows, parent_id=None):
        """
        构建模块树 + 模块下挂载的工作流
        """
        tree = []

        for module in modules:
            if module.parent_id == parent_id:
                # 当前模块下的工作流
                module_workflows = [
                    {
                        "workflowId": wf.workflow_id,
                        "name": wf.name,
                        "type": "workflow"
                    }
                    for wf in workflows
                    if wf.parent_submodule_id == module.id and wf.del_flag == "0"
                ]

                # 构建节点
                node = {
                    "moduleId": module.id,
                    "name": module.name,
                    "type": "module",
                    "children": await cls.build_module_tree(modules, workflows, module.id),
                    "workflows": module_workflows,
                }

                # 统计数量（当前模块的工作流数 + 子模块的总数）
                node["count"] = len(module_workflows) + sum(child["count"] for child in node["children"])

                tree.append(node)

        # 排序（如果有 sort_no）
        tree.sort(key=lambda x: getattr(next((m for m in modules if m.id == x["moduleId"]), None), "sort_no", 0) or 0)

        return tree

    @classmethod
    async def get_workflow_moduletree_services(
            cls, query_db: AsyncSession, query_object: Project_submodulesPageQueryModel, is_page: bool = False
    ):
        """
        获取项目下的模块 + 工作流树
        """
        # 1. 获取所有 type=2 的模块
        stmt_modules = select(ApiProjectSubmodules).where(
            and_(
                ApiProjectSubmodules.project_id == query_object.project_id,
                ApiProjectSubmodules.del_flag == "0",
                ApiProjectSubmodules.type == 2
            )
        )
        result_modules = await query_db.execute(stmt_modules)
        modules = result_modules.scalars().all()

        # 2. 获取所有工作流
        stmt_workflows = select(ApiWorkflow).where(
            and_(
                ApiWorkflow.del_flag == "0",
                ApiWorkflow.parent_submodule_id.in_([m.id for m in modules])
            )
        )
        result_workflows = await query_db.execute(stmt_workflows)
        workflows = result_workflows.scalars().all()

        # 3. 构建树
        tree_data = await cls.build_module_tree(modules, workflows, parent_id=None)

        # 4. 返回结果
        return {"rows": CamelCaseUtil.transform_result(tree_data)}

    @classmethod
    async def add_workflow_services(cls, query_db: AsyncSession, page_object: WorkflowModel):
        """
        新增测试执行器主信息service

        :param query_db: orm对象
        :param page_object: 新增测试执行器主对象
        :return: 新增测试执行器主校验结果
        """
        try:
            # if page_object.parent_submodule_id:
            workflow = await WorkflowDao.add_workflow_dao(query_db, page_object)
            await query_db.commit()
            await query_db.refresh(workflow)  # 显式刷新对象以获取数据库生成的值
            return {"workflowId": workflow.workflow_id}
            # else:
            #     submodules_query_object = Project_submodulesPageQueryModel(
            #         name="快速创建",
            #         project_id=page_object.project_id,
            #         type="2"
            #     )
            #     res_submodules = await Project_submodulesService.get_project_submodules_list_services(query_db,
            #                                                                                           submodules_query_object)
            #     if len(res_submodules) != 0:
            #         module_id = res_submodules[0].get("id")
            #     else:
            #         res_module = await Project_submodulesService.add_project_submodules_services(query_db,
            #                                                                                      Project_submodulesModel(
            #                                                                                          name="快速创建",
            #                                                                                          project_id=page_object.project_id,
            #                                                                                          type="2"), )
            #         module_id = res_module.get("moduleId")
            #     page_object.parent_submodule_id = module_id
            #     workflow = await WorkflowDao.add_workflow_dao(query_db, page_object)
            #     await query_db.commit()
            #     await query_db.refresh(workflow)  # 显式刷新对象以获取数据库生成的值
            #     return {"workflowId": workflow.workflow_id}
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_workflow_services(cls, query_db: AsyncSession, page_object: WorkflowModel):
        """
        编辑测试执行器主信息service

        :param query_db: orm对象
        :param page_object: 编辑测试执行器主对象
        :return: 编辑测试执行器主校验结果
        """
        edit_workflow = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        workflow_info = await cls.workflow_detail_services(query_db, page_object.workflow_id)
        if workflow_info.workflow_id:
            try:
                await WorkflowDao.edit_workflow_dao(query_db, edit_workflow)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='测试执行器主不存在')

    @classmethod
    async def delete_workflow_services(cls, query_db: AsyncSession, page_object: DeleteWorkflowModel):
        """
        删除测试执行器主信息service

        :param query_db: orm对象
        :param page_object: 删除测试执行器主对象
        :return: 删除测试执行器主校验结果
        """
        if page_object.workflow_ids:
            workflow_id_list = page_object.workflow_ids.split(',')
            try:
                for workflow_id in workflow_id_list:
                    await WorkflowDao.delete_workflow_dao(query_db, WorkflowModel(workflowId=workflow_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入执行器ID为空')

    @classmethod
    async def workflow_detail_services(cls, query_db: AsyncSession, workflow_id: int):
        """
        获取测试执行器主详细信息service

        :param query_db: orm对象
        :param workflow_id: 执行器ID
        :return: 执行器ID对应的信息
        """
        workflow = await WorkflowDao.get_workflow_detail_by_id(query_db, workflow_id=workflow_id)
        if workflow:
            result = WorkflowModel(**CamelCaseUtil.transform_result(workflow))
        else:
            result = WorkflowModel(**dict())

        return result

    @classmethod
    async def build_workflow_tree(cls, query_db, workflow_id):
        """
        递归构建树结构

        参数:
        - nodes: 所有节点的列表
        - parent_id: 父节点ID，根节点时为None

        返回:
        - 树形结构的列表
        """

        # model_id = workflow_id
        async def build_tree(db, module):
            # 排除已删除的子节点
            # 获取所有模块，排除已删除的模块
            children_stmt = select(ApiWorknodes).where(and_(ApiWorknodes.del_flag == "0",
                                                            ApiWorknodes.workflow_id == workflow_id,
                                                            ApiWorknodes.parent_id == str(module.node_id))).order_by(
                ApiWorknodes.sort_no)
            children_result = await query_db.execute(children_stmt)
            children = children_result.scalars().all()

            # 每一个子节点都会转化,
            res = WorknodesModelWithChildren.validate(module)
            if res.type == NodeTypeEnum.ELSE:
                res.name = ""
                res.sort_no = 0
            if res.type == NodeTypeEnum.IF:
                res.name = ""
                if res.config.condition in [Assertion_Method.EXIST, Assertion_Method.NOT_EXIST,
                                            Assertion_Method.IS_NULL, Assertion_Method.IS_NOT_NULL]:
                    res.name = f"{res.config.actual_value} {res.config.condition}"
                else:
                    res.name = f"{res.config.actual_value} {res.config.condition} {res.config.expected_value}"
            if res.type == NodeTypeEnum.FOREACH:
                res.name = f"循环元素{res.config.loop_array}"
            if res.type == NodeTypeEnum.FOR:
                res.name = f"循环{res.config.loop_count}次"

            if res.type == NodeTypeEnum.TASK and res.config.task_config.task_type in [TaskTypeEnum.APICASE,
                                                                                      TaskTypeEnum.API]:
                case_id = res.config.task_config.case_id or res.config.task_config.api_id
                testcase_obj = await Test_casesDao.get_test_cases_detail_by_id(db, case_id)
                # res.name = testcase_obj.name if testcase_obj else ""
            if res.type == NodeTypeEnum.TASK and res.config.task_config.task_type == TaskTypeEnum.WAIT:
                res.name = f"{res.config.task_config.wait_time}秒"

            res.children = [await build_tree(db, child) for child in children]

            return res

        # 获取所有1级模块，排除已删除的模块
        stmt = select(ApiWorknodes).where(and_(ApiWorknodes.workflow_id == workflow_id,
                                               ApiWorknodes.del_flag == "0",
                                               ApiWorknodes.parent_id == None)).order_by(ApiWorknodes.sort_no)
        result = await query_db.execute(stmt)
        modules = result.scalars().all()

        # 构建整个树
        tree = [await build_tree(query_db, root) for root in modules]
        # data = {"records": tree, "total": len(tree)}
        return tree

    @classmethod
    async def get_workflow_nodetree_services(cls, query_db: AsyncSession, workflow_id: int) -> WorkflowTreeModel:
        """
        node节点树展示
        :param workflow_id:
        :param query_db:
        :return:
        """
        workflow = await WorkflowDao.get_workflow_detail_by_id(query_db, workflow_id=workflow_id)
        if workflow:
            result_workflow = WorkflowTreeModel(**CamelCaseUtil.transform_result(workflow))
            tree_data = await cls.build_workflow_tree(query_db, workflow_id)
            result_workflow.worknodes = tree_data
            return result_workflow

        else:
            return WorkflowTreeModel(**dict())

    @staticmethod
    async def export_workflow_list_services(workflow_list: List):
        """
        导出测试执行器主信息service

        :param workflow_list: 测试执行器主信息列表
        :return: 测试执行器主信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'workflowId': '执行器ID',
            'name': '执行器名称',
            'executionConfig': '执行配置',
            'parentSubmoduleId': '父级模块ID',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(workflow_list, mapping_dict)

        return binary_data
