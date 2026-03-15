from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_project_submodules.dao.project_submodules_dao import Project_submodulesDao
from module_admin.api_project_submodules.entity.vo.project_submodules_vo import DeleteProject_submodulesModel, Project_submodulesModel, Project_submodulesPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class Project_submodulesService:
    """
    项目模块模块服务层
    """

    @classmethod
    async def get_project_submodules_list_services(
        cls, query_db: AsyncSession, query_object: Project_submodulesPageQueryModel, is_page: bool = False
    ):
        """
        获取项目模块列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目模块列表信息对象
        """
        project_submodules_list_result = await Project_submodulesDao.get_project_submodules_list(query_db, query_object, is_page)

        return project_submodules_list_result


    @classmethod
    async def add_project_submodules_services(cls, query_db: AsyncSession, page_object: Project_submodulesModel):
        """
        新增项目模块信息service

        :param query_db: orm对象
        :param page_object: 新增项目模块对象
        :return: 新增项目模块校验结果
        """
        try:
            res = await Project_submodulesDao.add_project_submodules_dao(query_db, page_object)
            await query_db.commit()
            await query_db.refresh(res)
            return {"moduleId": res.id}
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_project_submodules_services(cls, query_db: AsyncSession, page_object: Project_submodulesModel):
        """
        编辑项目模块信息service

        :param query_db: orm对象
        :param page_object: 编辑项目模块对象
        :return: 编辑项目模块校验结果
        """
        edit_project_submodules = page_object.model_dump(exclude_unset=True, exclude={'ancestors', 'create_by', 'create_time', 'del_flag', })
        project_submodules_info = await cls.project_submodules_detail_services(query_db, page_object.id)
        if project_submodules_info.id:
            try:
                await Project_submodulesDao.edit_project_submodules_dao(query_db, edit_project_submodules)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='项目模块不存在')

    @classmethod
    async def delete_project_submodules_services(cls, query_db: AsyncSession, page_object: DeleteProject_submodulesModel):
        """
        删除项目模块信息service

        :param query_db: orm对象
        :param page_object: 删除项目模块对象
        :return: 删除项目模块校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await Project_submodulesDao.delete_project_submodules_dao(query_db, Project_submodulesModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def project_submodules_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取项目模块详细信息service

        :param query_db: orm对象
        :param id: ID
        :return: ID对应的信息
        """
        project_submodules = await Project_submodulesDao.get_project_submodules_detail_by_id(query_db, id=id)
        if project_submodules:
            result = Project_submodulesModel(**CamelCaseUtil.transform_result(project_submodules))
        else:
            result = Project_submodulesModel(**dict())

        return result

    @staticmethod
    async def export_project_submodules_list_services(project_submodules_list: List):
        """
        导出项目模块信息service

        :param project_submodules_list: 项目模块信息列表
        :return: 项目模块信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': 'ID',
            'name': '模块名称',
            'type': '模块类型 (1: 接口模块, 2: 套件模块, 3: UI模块)',
            'parentId': '父id',
            'ancestors': '祖级列表',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
            'projectId': '所属项目id',
        }
        binary_data = ExcelUtil.export_list2excel(project_submodules_list, mapping_dict)

        return binary_data
