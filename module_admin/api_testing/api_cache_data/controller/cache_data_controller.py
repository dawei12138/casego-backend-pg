from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_testing.api_cache_data.service.cache_data_service import Cache_dataService
from module_admin.api_testing.api_cache_data.entity.vo.cache_data_vo import DeleteCache_dataModel, Cache_dataModel, \
    Cache_dataPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

cache_dataController = APIRouter(prefix='/api_cache_data/cache_data',
                                 dependencies=[Depends(LoginService.get_current_user)])


@cache_dataController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_cache_data:cache_data:list'))]
)
async def get_api_cache_data_cache_data_list(
        request: Request,
        cache_data_page_query: Cache_dataPageQueryModel = Depends(Cache_dataPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    cache_data_page_query.user_id = current_user.user.user_id
    redis = request.app.state.redis
    logger.info(cache_data_page_query.model_dump())
    # 获取分页数据
    cache_data_page_query_result = await Cache_dataService.get_redis_cache_list_services(redis, cache_data_page_query,
                                                                                         is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=cache_data_page_query_result)


@cache_dataController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_cache_data:cache_data:add'))])
@ValidateFields(validate_model='add_cache_data')
# @Log(title='环境缓存', business_type=BusinessType.INSERT)
async def add_api_cache_data_cache_data(
        request: Request,
        add_cache_data: Cache_dataModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_cache_data.user_id = current_user.user.user_id
    logger.info(add_cache_data.model_dump())
    redis = request.app.state.redis
    add_cache_data_result = await Cache_dataService.add_cache_data_services(redis, add_cache_data)
    logger.info(add_cache_data_result.message)

    return ResponseUtil.success(msg=add_cache_data_result.message)


@cache_dataController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_cache_data:cache_data:edit'))])
@ValidateFields(validate_model='edit_cache_data')
# @Log(title='环境缓存', business_type=BusinessType.UPDATE)
async def edit_api_cache_data_cache_data(
        request: Request,
        edit_cache_data: Cache_dataModel,
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
        query_db: AsyncSession = Depends(get_db),  # 不能去除，log装饰器对这里进行了封装
):
    logger.info(edit_cache_data.model_dump())
    edit_cache_data.update_by = current_user.user.user_name
    edit_cache_data.update_time = datetime.now()
    redis = request.app.state.redis
    edit_cache_data_result = await Cache_dataService.edit_cache_data_services(redis, edit_cache_data)
    logger.info(edit_cache_data_result.message)

    return ResponseUtil.success(msg=edit_cache_data_result.message)


@cache_dataController.delete('/{ids}',
                             dependencies=[Depends(CheckUserInterfaceAuth('api_cache_data:cache_data:remove'))])
# @Log(title='环境缓存', business_type=BusinessType.DELETE)
async def delete_api_cache_data_cache_data(request: Request,
                                           ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_cache_data = DeleteCache_dataModel(ids=ids)
    logger.info(delete_cache_data.model_dump())
    redis = request.app.state.redis
    delete_cache_data_result = await Cache_dataService.delete_cache_data_services(redis, delete_cache_data)
    logger.info(delete_cache_data_result.message)

    return ResponseUtil.success(msg=delete_cache_data_result.message)


@cache_dataController.get(

    '/{id}', response_model=Cache_dataModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_cache_data:cache_data:query'))]
)
async def query_detail_api_cache_data_cache_data(request: Request, id: str):
    logger.info(f"id:{id}")
    redis = request.app.state.redis
    cache_data_detail_result = await Cache_dataService.cache_data_detail_services(redis, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=cache_data_detail_result)


@cache_dataController.post('/export',
                           dependencies=[Depends(CheckUserInterfaceAuth('api_cache_data:cache_data:export'))])
# @Log(title='环境缓存', business_type=BusinessType.EXPORT)
async def export_api_cache_data_cache_data_list(
        request: Request,
        cache_data_page_query: Cache_dataPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    cache_data_query_result = await Cache_dataService.get_cache_data_list_services(query_db, cache_data_page_query,
                                                                                   is_page=False)
    cache_data_export_result = await Cache_dataService.export_cache_data_list_services(cache_data_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(cache_data_export_result))
