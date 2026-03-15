from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from sqlalchemy.orm.attributes import flag_modified

from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.api_testing.api_test_cases.entity.vo.test_cases_vo import Test_casesModel
from module_admin.api_testing.api_test_cases.service.test_cases_service import Test_casesService
from module_admin.api_workflow.api_worknodes.entity.do.worknodes_do import NodeTypeEnum
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_workflow.api_worknodes.dao.worknodes_dao import WorknodesDao
from module_admin.api_workflow.api_worknodes.entity.vo.worknodes_vo import DeleteWorknodesModel, WorknodesModel, \
    WorknodesPageQueryModel, AddWorknodesModel, TaskTypeEnum, Task_config, CopyWorknodesModel
from utils.api_import.import_curl import parse_curl_command
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class WorknodesService:
    """
    执行器节点模块服务层
    """

    @classmethod
    async def get_worknodes_list_services(
            cls, query_db: AsyncSession, query_object: WorknodesPageQueryModel, is_page: bool = False
    ):
        """
        获取执行器节点列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 执行器节点列表信息对象
        """
        worknodes_list_result = await WorknodesDao.get_worknodes_list(query_db, query_object, is_page)

        return worknodes_list_result

    @classmethod
    async def add_worknodes_services(cls, query_db: AsyncSession, page_object: AddWorknodesModel):
        """
        新增执行器节点信息service

        :param query_db: orm对象
        :param page_object: 新增执行器节点对象
        :return: 新增执行器节点校验结果，包含新节点信息
        """
        try:
            # 计算新节点的 sort_no
            parent_id_str = str(page_object.parent_id) if page_object.parent_id else None

            if page_object.after_node_id:
                # 如果指定了 after_node_id，则插入到该节点之后
                after_node = await WorknodesDao.get_worknodes_detail_by_id(query_db, page_object.after_node_id)
                if after_node:
                    # 将 after_node 之后的同级节点的 sort_no 都 +1
                    await WorknodesDao.update_sibling_sort_no(
                        query_db,
                        page_object.workflow_id,
                        parent_id_str,
                        after_node.sort_no
                    )
                    # 新节点的 sort_no = after_node.sort_no + 1
                    page_object.sort_no = (after_node.sort_no or 0) + 1
                else:
                    # after_node 不存在，则插入到末尾
                    max_sort_no = await WorknodesDao.get_max_sort_no(query_db, page_object.workflow_id, parent_id_str)
                    page_object.sort_no = max_sort_no + 1
            elif page_object.sort_no is None:
                # 没有指定 after_node_id 也没有指定 sort_no，则插入到末尾
                max_sort_no = await WorknodesDao.get_max_sort_no(query_db, page_object.workflow_id, parent_id_str)
                page_object.sort_no = max_sort_no + 1

            new_node = None  # 用于保存新建的节点

            # 从测试用例导入 (task_type = APICASE)
            if page_object.type == NodeTypeEnum.TASK and page_object.config.task_config.task_type == TaskTypeEnum.APICASE:
                for idx, case_id in enumerate(page_object.case_ids):
                    res_node_case = await Test_casesService.test_cases_copy_services(query_db,
                                                                                     Test_casesModel(case_id=case_id),
                                                                                     is_copy_to_workflownode_case=True)
                    page_object.config.task_config.api_id = res_node_case.get("caseId")
                    page_object.name = res_node_case.get("caseName")
                    # 批量导入时，每个节点递增排序值
                    if idx > 0:
                        page_object.sort_no = page_object.sort_no + 1
                    new_node = await WorknodesDao.add_worknodes_dao(query_db, page_object)

            # 添加HTTP请求 (task_type = API, 创建type=3的空用例)
            elif page_object.type == NodeTypeEnum.TASK and page_object.config.task_config.task_type == TaskTypeEnum.API:
                new_case = await cls._create_http_request_case(query_db, page_object)
                page_object.config.task_config.api_id = new_case.get("caseId")
                new_node = await WorknodesDao.add_worknodes_dao(query_db, page_object)

            # 从curl导入 (解析curl后创建type=3的用例)
            elif page_object.type == NodeTypeEnum.TASK and page_object.curl_command:
                new_case = await cls._create_case_from_curl(query_db, page_object)
                page_object.config.task_config = Task_config(task_type=TaskTypeEnum.API)
                page_object.config.task_config.api_id = new_case.get("caseId")
                new_node = await WorknodesDao.add_worknodes_dao(query_db, page_object)

            # IF条件节点 (自动创建else子节点)
            elif page_object.type == NodeTypeEnum.IF:
                new_node = await WorknodesDao.add_worknodes_dao(query_db, page_object)
                page_object.type = NodeTypeEnum.ELSE
                page_object.parent_id = new_node.node_id
                page_object.config.bind_if_node_id = new_node.node_id
                page_object.sort_no = 1  # else 子节点排序为1
                res_else = await WorknodesDao.add_worknodes_dao(query_db, page_object)
                new_node.config['else_node_id'] = res_else.node_id
                new_node.config = dict(new_node.config)
                flag_modified(new_node, 'config')

            # 其他类型节点 (GROUP, FOR, FOREACH, 公共脚本, 自定义脚本, 数据库脚本, 等待时间等)
            # 这些直接保存config.taskConfig中的配置即可
            else:
                new_node = await WorknodesDao.add_worknodes_dao(query_db, page_object)

            # 在 commit 之前获取返回值（避免 session 关闭后无法访问）
            result_node_id = new_node.node_id if new_node else None
            result_sort_no = new_node.sort_no if new_node else None

            await query_db.commit()

            # 返回新增节点的信息
            return {
                'is_success': True,
                'message': '新增成功',
                'node_id': result_node_id,
                'sort_no': result_sort_no,
            }
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def _create_http_request_case(cls, query_db: AsyncSession, page_object: AddWorknodesModel):
        """
        创建HTTP请求用例 (case_type=3)

        :param query_db: orm对象
        :param page_object: 节点对象
        :return: 新建用例信息
        """
        new_case = Test_casesModel(
            name=page_object.name or "HTTP请求",
            case_type="3",  # 工作流节点用例
            project_id=page_object.project_id,
            create_by=page_object.create_by,
            create_time=page_object.create_time,
            update_by=page_object.update_by,
            update_time=page_object.update_time
        )
        return await Test_casesService.add_test_cases_services(query_db, new_case)

    @classmethod
    async def _create_case_from_curl(cls, query_db: AsyncSession, page_object: AddWorknodesModel):
        """
        从curl命令创建用例 (case_type=3)

        :param query_db: orm对象
        :param page_object: 节点对象
        :return: 新建用例信息
        """
        # 解析curl命令
        curl_result = parse_curl_command(page_object.curl_command)
        if not curl_result.success:
            raise ServiceException(message=f'解析cURL失败: {curl_result.msg}')

        curl_data = curl_result.data

        # 创建新用例
        new_case = Test_casesModel(
            name=page_object.name or curl_data.name or "cURL导入",
            case_type="3",  # 工作流节点用例
            project_id=page_object.project_id,
            path=curl_data.path,
            method=curl_data.method,
            request_type=curl_data.request_type,
            json_data=curl_data.json_data,
            create_by=page_object.create_by,
            create_time=page_object.create_time,
            update_by=page_object.update_by,
            update_time=page_object.update_time
        )
        result = await Test_casesService.add_test_cases_services(query_db, new_case)

        # 处理headers、cookies、params、formdata
        from module_admin.api_testing.api_headers.entity.do.headers_do import ApiHeaders
        from module_admin.api_testing.api_cookies.entity.do.cookies_do import ApiCookies
        from module_admin.api_testing.api_params.entity.do.params_do import ApiParams
        from module_admin.api_testing.api_formdata.entity.do.formdata_do import ApiFormdata

        new_case_id = result.get("caseId")

        for header in curl_data.headers_list:
            query_db.add(ApiHeaders(case_id=new_case_id, key=header.key, value=header.value,
                                    create_by=page_object.create_by, create_time=page_object.create_time))
        for cookie in curl_data.cookies_list:
            query_db.add(ApiCookies(case_id=new_case_id, key=cookie.key, value=cookie.value,
                                    create_by=page_object.create_by, create_time=page_object.create_time))
        for param in curl_data.params_list:
            query_db.add(ApiParams(case_id=new_case_id, key=param.key, value=param.value,
                                   create_by=page_object.create_by, create_time=page_object.create_time))
        for formdata in curl_data.formdata:
            query_db.add(ApiFormdata(case_id=new_case_id, key=formdata.key, value=formdata.value,
                                     create_by=page_object.create_by, create_time=page_object.create_time))

        return result

    @classmethod
    async def edit_worknodes_services(cls, query_db: AsyncSession, page_object: WorknodesModel):
        """
        编辑执行器节点信息service

        :param query_db: orm对象
        :param page_object: 编辑执行器节点对象
        :return: 编辑执行器节点校验结果
        """
        edit_worknodes = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        worknodes_info = await cls.worknodes_detail_services(query_db, page_object.node_id)
        if worknodes_info.node_id:
            try:
                await WorknodesDao.edit_worknodes_dao(query_db, edit_worknodes)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='执行器节点不存在')

    @classmethod
    async def delete_worknodes_services(cls, query_db: AsyncSession, page_object: DeleteWorknodesModel):
        """
        删除执行器节点信息service

        :param query_db: orm对象
        :param page_object: 删除执行器节点对象
        :return: 删除执行器节点校验结果
        """
        if page_object.node_ids:
            node_id_list = page_object.node_ids.split(',')
            try:
                for node_id in node_id_list:
                    node_info = await cls.worknodes_detail_services(query_db, int(node_id))
                    if node_info.type == NodeTypeEnum.ELSE:
                        continue
                    await WorknodesDao.delete_worknodes_dao(query_db, WorknodesModel(nodeId=node_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入节点ID为空')

    @classmethod
    async def worknodes_detail_services(cls, query_db: AsyncSession, node_id: int):
        """
        获取执行器节点详细信息service

        :param query_db: orm对象
        :param node_id: 节点ID
        :return: 节点ID对应的信息
        """
        worknodes = await WorknodesDao.get_worknodes_detail_by_id(query_db, node_id=node_id)
        if worknodes:
            result = WorknodesModel(**CamelCaseUtil.transform_result(worknodes))
        else:
            result = WorknodesModel(**dict())

        return result

    @classmethod
    async def copy_worknodes_services(
            cls, query_db: AsyncSession, copy_model: CopyWorknodesModel,
            create_by: str = None, create_time=None, update_by: str = None, update_time=None
    ):
        """
        复制执行器节点及其所有子节点service

        :param query_db: orm对象
        :param copy_model: 复制节点参数对象
        :param create_by: 创建者
        :param create_time: 创建时间
        :param update_by: 更新者
        :param update_time: 更新时间
        :return: 复制结果
        """
        try:
            # 获取源节点信息
            source_node = await WorknodesDao.get_worknodes_detail_by_id(query_db, copy_model.node_id)
            if not source_node:
                raise ServiceException(message='源节点不存在')

            # 如果是ELSE节点，不允许单独复制
            if source_node.type == NodeTypeEnum.ELSE:
                raise ServiceException(message='ELSE节点不能单独复制，请复制对应的IF节点')

            # 确定目标父节点ID
            target_parent_id = copy_model.target_parent_id if copy_model.target_parent_id else source_node.parent_id

            # 存储旧ID到新ID的映射关系
            id_mapping = {}

            # 递归复制节点
            new_root_node = await cls._copy_node_recursive(
                query_db, source_node, target_parent_id, id_mapping,
                create_by, create_time, update_by, update_time
            )

            # 更新所有节点的IF/ELSE关系引用
            await cls._update_if_else_references(query_db, id_mapping)

            await query_db.commit()
            return CrudResponseModel(is_success=True, message='复制成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def _copy_node_recursive(
            cls, query_db: AsyncSession, source_node, new_parent_id,
            id_mapping: dict, create_by: str, create_time, update_by: str, update_time,
            is_root: bool = True
    ):
        """
        递归复制节点

        :param query_db: orm对象
        :param source_node: 源节点ORM对象
        :param new_parent_id: 新的父节点ID
        :param id_mapping: 旧ID到新ID的映射字典
        :param create_by: 创建者
        :param create_time: 创建时间
        :param update_by: 更新者
        :param update_time: 更新时间
        :param is_root: 是否是根节点（被复制的起始节点）
        :return: 新创建的节点
        """
        # 在任何可能触发flush的操作之前，先保存source_node的属性值
        # 因为flush后ORM对象会过期，异步上下文中访问过期属性会导致MissingGreenlet错误
        source_node_id = source_node.node_id

        # 计算新节点的sort_no
        # 根节点：sort_no = 源节点sort_no + 0.01，使复制的节点排在原节点下方
        # 子节点：保持原有的sort_no值
        new_sort_no = None
        if source_node.sort_no is not None:
            new_sort_no = source_node.sort_no + 0.01 if is_root else source_node.sort_no

        # 复制节点基本信息
        new_node_data = WorknodesModel(
            workflow_id=source_node.workflow_id,
            parent_id=new_parent_id,
            name=f"{source_node.name}_copy" if source_node.type != NodeTypeEnum.ELSE else source_node.name,
            type=source_node.type,
            is_run=source_node.is_run,
            children_ids=[],  # 先设置为空，后续更新
            config=dict(source_node.config) if source_node.config else {},
            create_by=create_by,
            create_time=create_time,
            update_by=update_by,
            update_time=update_time,
            sort_no=new_sort_no,
        )

        # 检查是否需要复制测试用例（针对API和APICASE类型节点）
        if source_node.type == NodeTypeEnum.TASK and source_node.config:
            config = source_node.config
            task_config = config.get('task_config') or config.get('taskConfig')

            if task_config:
                task_type = task_config.get('task_type') or task_config.get('taskType')
                api_id = task_config.get('api_id') or task_config.get('apiId')

                # 复制APICASE类型的测试用例
                if task_type == TaskTypeEnum.APICASE and api_id:
                    res_node_case = await Test_casesService.test_cases_copy_services(
                        query_db,
                        Test_casesModel(case_id=api_id, create_by=create_by, create_time=create_time,
                                        update_by=update_by, update_time=update_time),
                        is_copy_to_workflownode_case=True
                    )
                    if res_node_case:
                        # 更新config中的api_id为新的caseId
                        if hasattr(new_node_data.config, 'task_config'):
                            new_node_data.config.task_config.api_id = res_node_case.get("caseId")
                        if hasattr(new_node_data.config, 'taskConfig'):
                            new_node_data.config.task_config.api_id = res_node_case.get("caseId")

                # 复制API类型的测试用例
                elif task_type == TaskTypeEnum.API and api_id:
                    res_node_case = await Test_casesService.test_cases_copy_services(
                        query_db,
                        Test_casesModel(case_id=api_id, create_by=create_by, create_time=create_time,
                                        update_by=update_by, update_time=update_time),
                        is_copy_to_workflownode_case=True
                    )
                    if res_node_case:
                        # 更新config中的api_id为新的caseId
                        if hasattr(new_node_data.config, 'task_config'):
                            new_node_data.config.task_config.api_id = res_node_case.get("caseId")
                        if hasattr(new_node_data.config, 'taskConfig'):
                            new_node_data.config.task_config.api_id = res_node_case.get("caseId")

        # 创建新节点
        new_node = await WorknodesDao.add_worknodes_dao(query_db, new_node_data)
        new_node_id = new_node.node_id

        # 记录旧ID到新ID的映射
        id_mapping[source_node_id] = new_node_id

        # 获取所有子节点
        children_nodes = await WorknodesDao.get_all_children_nodes(query_db, source_node_id)

        new_children_ids = []
        for child_node in children_nodes:
            # 递归复制子节点，is_root=False表示这是子节点
            new_child = await cls._copy_node_recursive(
                query_db, child_node, new_node_id, id_mapping,
                create_by, create_time, update_by, update_time,
                is_root=False
            )
            new_children_ids.append(new_child.node_id)

        # 更新新节点的children_ids
        if new_children_ids:
            new_node.children_ids = new_children_ids
            await query_db.flush()

        return new_node

    @classmethod
    async def _update_if_else_references(cls, query_db: AsyncSession, id_mapping: dict):
        """
        更新IF/ELSE节点之间的引用关系

        :param query_db: orm对象
        :param id_mapping: 旧ID到新ID的映射字典
        """
        for old_id, new_id in id_mapping.items():
            new_node = await WorknodesDao.get_worknodes_detail_by_id(query_db, new_id)
            if not new_node or not new_node.config:
                continue

            config = dict(new_node.config)
            updated = False

            # 处理IF节点：更新else_node_id
            if new_node.type == NodeTypeEnum.IF and 'else_node_id' in config:
                old_else_id = config.get('else_node_id')
                if old_else_id and old_else_id in id_mapping:
                    config['else_node_id'] = id_mapping[old_else_id]
                    updated = True

            # 处理ELSE节点：更新bind_if_node_id
            if new_node.type == NodeTypeEnum.ELSE and 'bind_if_node_id' in config:
                old_if_id = config.get('bind_if_node_id')
                if old_if_id and old_if_id in id_mapping:
                    config['bind_if_node_id'] = id_mapping[old_if_id]
                    updated = True

            if updated:
                new_node.config = config
                from sqlalchemy.orm.attributes import flag_modified
                flag_modified(new_node, 'config')
                await query_db.flush()

    @staticmethod
    async def export_worknodes_list_services(worknodes_list: List):
        """
        导出执行器节点信息service

        :param worknodes_list: 执行器节点信息列表
        :return: 执行器节点信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'nodeId': '节点ID',
            'workflowId': '所属执行器ID',
            'parentId': '父节点ID',
            'name': '节点名称',
            'type': '节点类型',
            'isRun': '是否启用执行',
            'childrenIds': '子结点列表',
            'config': '节点配置信息',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(worknodes_list, mapping_dict)

        return binary_data
