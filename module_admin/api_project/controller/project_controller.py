from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_project.service.project_service import ProjectService
from module_admin.api_project.entity.vo.project_vo import DeleteProjectModel, ProjectModel, ProjectPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

projectController = APIRouter(prefix='/api_project/project', dependencies=[Depends(LoginService.get_current_user)])


@projectController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_project:project:list'))]
)
async def get_api_project_project_list(
        request: Request,
        project_page_query: ProjectPageQueryModel = Depends(ProjectPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    project_page_query_result = await ProjectService.get_project_list_services(query_db, project_page_query,
                                                                               is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=project_page_query_result)


@projectController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_project:project:add'))])
@ValidateFields(validate_model='add_project')
# @Log(title='项目', business_type=BusinessType.INSERT)
async def add_api_project_project(
        request: Request,
        add_project: ProjectModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_project.create_by = current_user.user.user_name
    add_project.create_time = datetime.now()
    add_project.update_by = current_user.user.user_name
    add_project.update_time = datetime.now()
    extra_dict = add_project.model_dump(include={"create_by", "create_time", "update_time", "update_by", "project_id"})
    add_project_result = await ProjectService.add_project_services(query_db, add_project, extra_dict)
    logger.info(add_project_result.message)

    return ResponseUtil.success(msg=add_project_result.message)


@projectController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_project:project:edit'))])
@ValidateFields(validate_model='edit_project')
# @Log(title='项目', business_type=BusinessType.UPDATE)
async def edit_api_project_project(
        request: Request,
        edit_project: ProjectModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_project.update_by = current_user.user.user_name
    edit_project.update_time = datetime.now()
    edit_project_result = await ProjectService.edit_project_services(query_db, edit_project)
    logger.info(edit_project_result.message)

    return ResponseUtil.success(msg=edit_project_result.message)


@projectController.delete('/{ids}', dependencies=[Depends(CheckUserInterfaceAuth('api_project:project:remove'))])
# @Log(title='项目', business_type=BusinessType.DELETE)
async def delete_api_project_project(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_project = DeleteProjectModel(ids=ids)
    delete_project_result = await ProjectService.delete_project_services(query_db, delete_project)
    logger.info(delete_project_result.message)

    return ResponseUtil.success(msg=delete_project_result.message)


@projectController.get(
    '/{id}', response_model=ProjectModel, dependencies=[Depends(CheckUserInterfaceAuth('api_project:project:query'))]
)
async def query_detail_api_project_project(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    project_detail_result = await ProjectService.project_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=project_detail_result)


@projectController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('api_project:project:export'))])
# @Log(title='项目', business_type=BusinessType.EXPORT)
async def export_api_project_project_list(
        request: Request,
        project_page_query: ProjectPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    project_query_result = await ProjectService.get_project_list_services(query_db, project_page_query, is_page=False)
    project_export_result = await ProjectService.export_project_list_services(project_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(project_export_result))
