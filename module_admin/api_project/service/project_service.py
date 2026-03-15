from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.api_testing.api_environments.dao.environments_dao import EnvironmentsDao
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.api_project.dao.project_dao import ProjectDao
from module_admin.api_project.entity.vo.project_vo import DeleteProjectModel, ProjectModel, ProjectPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class ProjectService:
    """
    项目模块服务层
    """

    @classmethod
    async def get_project_list_services(
        cls, query_db: AsyncSession, query_object: ProjectPageQueryModel, is_page: bool = False
    ):
        """
        获取项目列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        project_list_result = await ProjectDao.get_project_list(query_db, query_object, is_page)

        return project_list_result


    @classmethod
    async def add_project_services(cls, query_db: AsyncSession, page_object: ProjectModel,extra_dict: dict):
        """
        新增项目信息service

        :param extra_dict:
        :param query_db: orm对象
        :param page_object: 新增项目对象
        :return: 新增项目校验结果
        """
        try:

            res = await ProjectDao.add_project_dao(query_db, page_object)
            extra_dict["project_id"] = res.id
            result = await EnvironmentsDao.init_environments_dao(query_db, extra_dict=extra_dict)
            await query_db.commit()

            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_project_services(cls, query_db: AsyncSession, page_object: ProjectModel):
        """
        编辑项目信息service

        :param query_db: orm对象
        :param page_object: 编辑项目对象
        :return: 编辑项目校验结果
        """
        edit_project = page_object.model_dump(exclude_unset=True, exclude={'type', 'parent_id', 'create_by', 'create_time', 'remark', 'description', 'sort_no', 'del_flag', 'ancestors'})
        project_info = await cls.project_detail_services(query_db, page_object.id)
        if project_info.id:
            try:
                await ProjectDao.edit_project_dao(query_db, edit_project)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='项目不存在')

    @classmethod
    async def delete_project_services(cls, query_db: AsyncSession, page_object: DeleteProjectModel):
        """
        删除项目信息service

        :param query_db: orm对象
        :param page_object: 删除项目对象
        :return: 删除项目校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    id = int(id)
                    await ProjectDao.delete_project_dao(query_db, ProjectModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入ID为空')

    @classmethod
    async def project_detail_services(cls, query_db: AsyncSession, id: int):
        """
        获取项目详细信息service

        :param query_db: orm对象
        :param id: ID
        :return: ID对应的信息
        """
        project = await ProjectDao.get_project_detail_by_id(query_db, id=id)
        if project:
            result = ProjectModel(**CamelCaseUtil.transform_result(project))
        else:
            result = ProjectModel(**dict())

        return result

    @staticmethod
    async def export_project_list_services(project_list: List):
        """
        导出项目信息service

        :param project_list: 项目信息列表
        :return: 项目信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': 'ID',
            'name': '项目名称',
            'type': '项目类型',
            'parentId': '父部门id',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
            'ancestors': '祖级列表',
        }
        binary_data = ExcelUtil.export_list2excel(project_list, mapping_dict)

        return binary_data
