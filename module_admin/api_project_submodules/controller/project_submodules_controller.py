from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.api_project_submodules.dao.project_submodules_dao import Project_submodulesDao
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_project_submodules.service.project_submodules_service import Project_submodulesService
from module_admin.api_project_submodules.entity.vo.project_submodules_vo import DeleteProject_submodulesModel, \
    Project_submodulesModel, Project_submodulesPageQueryModel, AddProject_submodulesModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

project_submodulesController = APIRouter(prefix='/api_project_submodules/project_submodules',
                                         dependencies=[Depends(LoginService.get_current_user)])


@project_submodulesController.get(
    '/tree', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:list'))]
)
async def get_api_project_submodules_project_submodules_tree(
        request: Request,
        project_submodules_page_query: Project_submodulesPageQueryModel = Depends(
            Project_submodulesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(project_submodules_page_query.model_dump())
    # 获取分页数据
    project_submodules_page_query_result = await Project_submodulesDao.get_project_tree_by_project_id(query_db,
                                                                                                      project_submodules_page_query.project_id)
    logger.info('获取成功')

    return ResponseUtil.success(dict_content=project_submodules_page_query_result)


@project_submodulesController.get(
    '/api_tree', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:list'))]
)
async def get_api_project_submodules_api_tree(
        request: Request,
        project_submodules_page_query: Project_submodulesPageQueryModel = Depends(
            Project_submodulesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    """
    获取只包含模块和接口的树状结构（用于导入接口选择）
    不包含case类型的节点
    """
    logger.info(project_submodules_page_query.model_dump())
    # 获取只包含模块和接口的树
    project_submodules_page_query_result = await Project_submodulesDao.get_project_api_tree_by_project_id(
        query_db,
        project_submodules_page_query.project_id
    )
    logger.info('获取接口树成功')

    return ResponseUtil.success(dict_content=project_submodules_page_query_result)


@project_submodulesController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:list'))]
)
async def get_api_project_submodules_project_submodules_list(
        request: Request,
        project_submodules_page_query: Project_submodulesPageQueryModel = Depends(
            Project_submodulesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(project_submodules_page_query.model_dump())
    # 获取分页数据
    project_submodules_page_query_result = await Project_submodulesService.get_project_submodules_list_services(
        query_db, project_submodules_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=project_submodules_page_query_result)


@project_submodulesController.post('', dependencies=[
    Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:add'))])
@ValidateFields(validate_model='add_project_submodules')
# @Log(title='项目模块', business_type=BusinessType.INSERT)
async def add_api_project_submodules_project_submodules(
        request: Request,
        add_project_submodules: AddProject_submodulesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_project_submodules.create_by = current_user.user.user_name
    add_project_submodules.create_time = datetime.now()
    add_project_submodules.update_by = current_user.user.user_name
    add_project_submodules.update_time = datetime.now()

    logger.info(add_project_submodules.model_dump())
    add_project_submodules_result = await Project_submodulesService.add_project_submodules_services(query_db,
                                                                                                    add_project_submodules)
    logger.info(add_project_submodules_result)

    return ResponseUtil.success(dict_content=add_project_submodules_result)


@project_submodulesController.get(
    '/workflow_tree', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:list'))]
)
async def get_api_project_submodules_workflow_tree(
        request: Request,
        project_submodules_page_query: Project_submodulesPageQueryModel = Depends(
            Project_submodulesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(project_submodules_page_query.model_dump())
    # 获取分页数据
    project_submodules_page_query_result = await Project_submodulesDao.get_project_workflow_tree_by_project_id(query_db,
                                                                                                               project_submodules_page_query.project_id)
    logger.info('获取成功')

    return ResponseUtil.success(dict_content=project_submodules_page_query_result)


@project_submodulesController.put('/sort', dependencies=[
    Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:edit'))])
@ValidateFields(validate_model='edit_project_submodules')
@Log(title='项目模块', business_type=BusinessType.UPDATE)
async def edit_api_project_submodules_project_submodules_sort(
        request: Request,
        edit_project_submodules: List[AddProject_submodulesModel],
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    for i in edit_project_submodules:
        i.update_by = current_user.user.user_name
        i.update_time = datetime.now()
        edit_project_submodules_result = await Project_submodulesService.edit_project_submodules_services(query_db,
                                                                                                          i)
    logger.info(CrudResponseModel(is_success=True, message='更新成功').message)

    return ResponseUtil.success(msg=CrudResponseModel(is_success=True, message='更新成功').message)


@project_submodulesController.put('', dependencies=[
    Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:edit'))])
@ValidateFields(validate_model='edit_project_submodules')
@Log(title='项目模块', business_type=BusinessType.UPDATE)
async def edit_api_project_submodules_project_submodules(
        request: Request,
        edit_project_submodules: AddProject_submodulesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_project_submodules.model_dump())
    edit_project_submodules.update_by = current_user.user.user_name
    edit_project_submodules.update_time = datetime.now()
    edit_project_submodules_result = await Project_submodulesService.edit_project_submodules_services(query_db,
                                                                                                      edit_project_submodules)
    logger.info(edit_project_submodules_result.message)

    return ResponseUtil.success(msg=edit_project_submodules_result.message)


@project_submodulesController.delete('/{ids}', dependencies=[
    Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:remove'))])
@Log(title='项目模块', business_type=BusinessType.DELETE)
async def delete_api_project_submodules_project_submodules(request: Request, ids: str,
                                                           query_db: AsyncSession = Depends(get_db)):
    delete_project_submodules = DeleteProject_submodulesModel(ids=ids)
    logger.info(delete_project_submodules.model_dump())
    delete_project_submodules_result = await Project_submodulesService.delete_project_submodules_services(query_db,
                                                                                                          delete_project_submodules)
    logger.info(delete_project_submodules_result.message)

    return ResponseUtil.success(msg=delete_project_submodules_result.message)


@project_submodulesController.get(
    '/{id}', response_model=Project_submodulesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:query'))]
)
async def query_detail_api_project_submodules_project_submodules(request: Request, id: int,
                                                                 query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    project_submodules_detail_result = await Project_submodulesService.project_submodules_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=project_submodules_detail_result)


@project_submodulesController.post('/export', dependencies=[
    Depends(CheckUserInterfaceAuth('api_project_submodules:project_submodules:export'))])
@Log(title='项目模块', business_type=BusinessType.EXPORT)
async def export_api_project_submodules_project_submodules_list(
        request: Request,
        project_submodules_page_query: Project_submodulesPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    project_submodules_query_result = await Project_submodulesService.get_project_submodules_list_services(query_db,
                                                                                                           project_submodules_page_query,
                                                                                                           is_page=False)
    project_submodules_export_result = await Project_submodulesService.export_project_submodules_list_services(
        project_submodules_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(project_submodules_export_result))
