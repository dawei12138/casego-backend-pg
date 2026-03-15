from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_admin.api_testing.api_databases.service.api_databases_service import Api_databasesService
from module_admin.api_testing.api_databases.entity.vo.api_databases_vo import DeleteApi_databasesModel, Api_databasesModel, \
    Api_databasesPageQueryModel, ExecuteScriptModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil
from utils.api_tools.executors.db_mysql_control import MysqlDB
from utils.api_tools.executors.db_redis_control import RedisDB

api_databasesController = APIRouter(prefix='/api_databases/api_databases',
                                    dependencies=[Depends(LoginService.get_current_user)])


@api_databasesController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:list'))]
)
async def get_api_databases_api_databases_list(
        request: Request,
        api_databases_page_query: Api_databasesPageQueryModel = Depends(Api_databasesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(api_databases_page_query.model_dump())
    # 获取分页数据
    api_databases_page_query_result = await Api_databasesService.get_api_databases_list_services(query_db,
                                                                                                 api_databases_page_query,
                                                                                                 is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=api_databases_page_query_result)


@api_databasesController.post('', dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:add'))])
@ValidateFields(validate_model='add_api_databases')
# @Log(title='数据库配置', business_type=BusinessType.INSERT)
async def add_api_databases_api_databases(
        request: Request,
        add_api_databases: Api_databasesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_api_databases.create_by = current_user.user.user_name
    add_api_databases.create_time = datetime.now()
    add_api_databases.update_by = current_user.user.user_name
    add_api_databases.update_time = datetime.now()
    add_api_databases_result = await Api_databasesService.add_api_databases_services(query_db, add_api_databases)
    logger.info(add_api_databases_result.message)

    return ResponseUtil.success(msg=add_api_databases_result.message)


@api_databasesController.put('', dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:edit'))])
@ValidateFields(validate_model='edit_api_databases')
@Log(title='数据库配置', business_type=BusinessType.UPDATE)
async def edit_api_databases_api_databases(
        request: Request,
        edit_api_databases: Api_databasesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    edit_api_databases.update_by = current_user.user.user_name
    edit_api_databases.update_time = datetime.now()
    edit_api_databases_result = await Api_databasesService.edit_api_databases_services(query_db, edit_api_databases)
    logger.info(edit_api_databases_result.message)

    return ResponseUtil.success(msg=edit_api_databases_result.message)


@api_databasesController.delete('/{ids}',
                                dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:remove'))])
@Log(title='数据库配置', business_type=BusinessType.DELETE)
async def delete_api_databases_api_databases(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_api_databases = DeleteApi_databasesModel(ids=ids)
    delete_api_databases_result = await Api_databasesService.delete_api_databases_services(query_db,
                                                                                           delete_api_databases)
    logger.info(delete_api_databases_result.message)

    return ResponseUtil.success(msg=delete_api_databases_result.message)


@api_databasesController.get(
    '/{id}', response_model=Api_databasesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:query'))]
)
async def query_detail_api_databases_api_databases(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    api_databases_detail_result = await Api_databasesService.api_databases_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=api_databases_detail_result)


@api_databasesController.post('/export',
                              dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:export'))])
@Log(title='数据库配置', business_type=BusinessType.EXPORT)
async def export_api_databases_api_databases_list(
        request: Request,
        api_databases_page_query: Api_databasesPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    api_databases_query_result = await Api_databasesService.get_api_databases_list_services(query_db,
                                                                                            api_databases_page_query,
                                                                                            is_page=False)
    api_databases_export_result = await Api_databasesService.export_api_databases_list_services(request,
                                                                                                api_databases_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(api_databases_export_result))


@api_databasesController.get(
    '/test/{id}',
    dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:query'))]
)
async def test_api_databases_connection(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    """
    测试数据库连接
    :param request: Request对象
    :param id: 数据库配置ID
    :param query_db: 数据库会话
    :return: 连接测试结果
    """
    # 获取数据库配置详情
    api_databases_detail = await Api_databasesService.api_databases_detail_services(query_db, id)
    if not api_databases_detail.id:
        return ResponseUtil.failure(msg='数据库配置不存在')

    db_type = str(api_databases_detail.db_type)

    # 根据数据库类型选择测试方法
    if db_type == '1':
        # MySQL
        result = MysqlDB.test_connection(
            host=api_databases_detail.host,
            port=api_databases_detail.port,
            username=api_databases_detail.username,
            password=api_databases_detail.password
        )
    elif db_type == '2':
        # Redis
        result = RedisDB.test_connection(
            host=api_databases_detail.host,
            port=api_databases_detail.port,
            password=api_databases_detail.password
        )
    else:
        return ResponseUtil.failure(msg=f'不支持的数据库类型: {db_type}')

    if result['success']:
        logger.info(f'数据库连接测试成功，id={id}, db_type={db_type}')
        return ResponseUtil.success(msg=result['message'])
    else:
        logger.warning(f'数据库连接测试失败，id={id}, db_type={db_type}, 原因: {result["message"]}')
        return ResponseUtil.failure(msg=result['message'])


@api_databasesController.post(
    '/execute',
    dependencies=[Depends(CheckUserInterfaceAuth('api_databases:api_databases:query'))]
)
async def execute_api_databases_script(
        request: Request,
        execute_script: ExecuteScriptModel,
        query_db: AsyncSession = Depends(get_db)
):
    """
    执行数据库脚本
    :param request: Request对象
    :param execute_script: 执行脚本请求模型
    :param query_db: 数据库会话
    :return: 执行结果
    """
    # 获取数据库配置详情
    api_databases_detail = await Api_databasesService.api_databases_detail_services(query_db, execute_script.db_id)
    if not api_databases_detail.id:
        return ResponseUtil.failure(msg='数据库配置不存在')

    db_type = str(api_databases_detail.db_type)

    # 目前仅支持 MySQL 执行脚本
    if db_type == '1':
        # MySQL
        result = MysqlDB.execute_script(
            host=api_databases_detail.host,
            port=api_databases_detail.port,
            username=api_databases_detail.username,
            password=api_databases_detail.password,
            script=execute_script.script
        )
    else:
        return ResponseUtil.failure(msg=f'暂不支持该数据库类型执行脚本: {db_type}')

    if result['success']:
        logger.info(f'SQL执行成功，db_id={execute_script.db_id}')
        return ResponseUtil.success(msg=result['message'], data=result['data'])
    else:
        logger.warning(f'SQL执行失败，db_id={execute_script.db_id}, 原因: {result["message"]}')
        return ResponseUtil.failure(msg=result['message'], data=result.get('data'))
