from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import Cache_dataPageQueryModel
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_testing.api_environments.service.environments_service import EnvironmentsService
from module_admin.api_testing.api_environments.entity.vo.environments_vo import DeleteEnvironmentsModel, \
    EnvironmentsModel, \
    EnvironmentsPageQueryModel, EnvironmentsConfig
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

environmentsController = APIRouter(prefix='/api_environments/environments',
                                   dependencies=[Depends(LoginService.get_current_user)])


@environmentsController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:list'))]
)
async def get_api_environments_environments_list(
        request: Request,
        environments_page_query: EnvironmentsPageQueryModel = Depends(EnvironmentsPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取分页数据
    environments_page_query_result = await EnvironmentsService.get_environments_list_services(query_db,
                                                                                              environments_page_query,
                                                                                              is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=environments_page_query_result)


@environmentsController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:add'))])
@ValidateFields(validate_model='add_environments')
# @Log(title='环境配置', business_type=BusinessType.INSERT)
async def add_api_environments_environments(
        request: Request,
        add_environments: EnvironmentsModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_environments.create_by = current_user.user.user_name
    add_environments.create_time = datetime.now()
    add_environments.update_by = current_user.user.user_name
    add_environments.update_time = datetime.now()
    add_environments_result = await EnvironmentsService.add_environments_services(query_db, add_environments)
    logger.info(add_environments_result.message)

    return ResponseUtil.success(msg=add_environments_result.message)


@environmentsController.get('/config',
                            dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:add'))])
@ValidateFields(validate_model='EnvironmentsConfig')
async def add_api_environments_environments(
        request: Request,
        environments_page_query: EnvironmentsPageQueryModel = Depends(EnvironmentsPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):

    environments_config = EnvironmentsConfig(id=environments_page_query.id)
    redis = request.app.state.redis
    cache_query = Cache_dataPageQueryModel(user_id=current_user.user.user_id, environment_id=environments_config.id)
    environments_config = await EnvironmentsService.get_environments_config_services(cache_query, redis, query_db,
                                                                                     environments_config)
    logger.info(environments_config)

    return ResponseUtil.success(model_content=environments_config)


@environmentsController.put('/config',
                            dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:add'))])
@ValidateFields(validate_model='EnvironmentsConfig')
async def get_api_environments_config(
        request: Request,
        edit_environmentsconfig: EnvironmentsConfig,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    user_id = current_user.user.user_id
    edit_environmentsconfig.update_by = current_user.user.user_name
    edit_environmentsconfig.update_time = datetime.now()
    redis = request.app.state.redis

    environments_config = await EnvironmentsService.edit_environments_config_services(user_id, redis, query_db,
                                                                                      edit_environmentsconfig, )
    logger.info(environments_config.message)

    return ResponseUtil.success(msg=environments_config.message)


@environmentsController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:edit'))])
@ValidateFields(validate_model='edit_environments')
@Log(title='环境配置', business_type=BusinessType.UPDATE)
async def edit_api_environments_environments(
        request: Request,
        edit_environments: EnvironmentsModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_environments.update_by = current_user.user.user_name
    edit_environments.update_time = datetime.now()
    logger.info(edit_environments.model_dump())
    edit_environments_result = await EnvironmentsService.edit_environments_services(query_db, edit_environments)
    logger.info(edit_environments_result.message)

    return ResponseUtil.success(msg=edit_environments_result.message)


@environmentsController.delete('/{ids}',
                               dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:remove'))])
@Log(title='环境配置', business_type=BusinessType.DELETE)
async def delete_api_environments_environments(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_environments = DeleteEnvironmentsModel(ids=ids)
    delete_environments_result = await EnvironmentsService.delete_environments_services(query_db, delete_environments)
    logger.info(delete_environments_result.message)
    res = ResponseUtil.success(
        msg=delete_environments_result.message) if delete_environments_result.is_success else ResponseUtil.failure(
        msg=delete_environments_result.message)

    return res


@environmentsController.get(
    '/{id}', response_model=EnvironmentsModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:query'))]
)
async def query_detail_api_environments_environments(request: Request, id: int,
                                                     query_db: AsyncSession = Depends(get_db)):
    environments_detail_result = await EnvironmentsService.environments_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=environments_detail_result)


@environmentsController.post('/export',
                             dependencies=[Depends(CheckUserInterfaceAuth('api_environments:environments:export'))])
@Log(title='环境配置', business_type=BusinessType.EXPORT)
async def export_api_environments_environments_list(
        request: Request,
        environments_page_query: EnvironmentsPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    environments_query_result = await EnvironmentsService.get_environments_list_services(query_db,
                                                                                         environments_page_query,
                                                                                         is_page=False)
    environments_export_result = await EnvironmentsService.export_environments_list_services(request,
                                                                                             environments_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(environments_export_result))
