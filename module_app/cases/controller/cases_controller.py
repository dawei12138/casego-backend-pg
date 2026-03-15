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
from module_app.cases.service.cases_service import CasesService
from module_app.cases.entity.vo.cases_vo import DeleteCasesModel, CasesModel, CasesPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

casesController = APIRouter(prefix='/app/cases', dependencies=[Depends(LoginService.get_current_user)])


@casesController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:cases:list'))],
    summary='获取测试用例列表',
    description='根据查询条件获取测试用例分页列表数据',
)
async def get_app_cases_list(
        request: Request,
        cases_page_query: CasesPageQueryModel = Depends(CasesPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(cases_page_query.model_dump())
    # 获取分页数据
    cases_page_query_result = await CasesService.get_cases_list_services(query_db, cases_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=cases_page_query_result)


@casesController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:cases:add'))],
    summary='新增测试用例',
    description='创建一条新的测试用例记录',
)
@ValidateFields(validate_model='add_cases')
# @Log(title='测试用例', business_type=BusinessType.INSERT)
async def add_app_cases(
        request: Request,
        add_cases: CasesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_cases.create_by = current_user.user.user_name
    add_cases.create_time = datetime.now()
    add_cases.update_by = current_user.user.user_name
    add_cases.update_time = datetime.now()
    logger.info(add_cases.model_dump())
    add_cases_result = await CasesService.add_cases_services(query_db, add_cases)
    logger.info(add_cases_result.message)

    return ResponseUtil.success(msg=add_cases_result.message)


@casesController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('app:cases:edit'))],
    summary='修改测试用例',
    description='根据主键更新测试用例信息',
)
@ValidateFields(validate_model='edit_cases')
# @Log(title='测试用例', business_type=BusinessType.UPDATE)
async def edit_app_cases(
        request: Request,
        edit_cases: CasesModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_cases.model_dump())
    edit_cases.update_by = current_user.user.user_name
    edit_cases.update_time = datetime.now()
    edit_cases_result = await CasesService.edit_cases_services(query_db, edit_cases)
    logger.info(edit_cases_result.message)

    return ResponseUtil.success(msg=edit_cases_result.message)


@casesController.delete(
    '/{ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('app:cases:remove'))],
    summary='删除测试用例',
    description='根据主键批量删除测试用例记录，多个主键以逗号分隔',
)
# @Log(title='测试用例', business_type=BusinessType.DELETE)
async def delete_app_cases(request: Request, ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_cases = DeleteCasesModel(ids=ids)
    logger.info(delete_cases.model_dump())
    delete_cases_result = await CasesService.delete_cases_services(query_db, delete_cases)
    logger.info(delete_cases_result.message)

    return ResponseUtil.success(msg=delete_cases_result.message)


@casesController.get(
    '/{id}',
    response_model=CasesModel,
    dependencies=[Depends(CheckUserInterfaceAuth('app:cases:query'))],
    summary='获取测试用例详情',
    description='根据主键获取测试用例详细信息',
)
async def query_detail_app_cases(request: Request, id: int, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    cases_detail_result = await CasesService.cases_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=cases_detail_result)


@casesController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('app:cases:export'))],
    summary='导出测试用例',
    description='根据查询条件导出测试用例列表数据到Excel文件',
)
# @Log(title='测试用例', business_type=BusinessType.EXPORT)
async def export_app_cases_list(
        request: Request,
        cases_page_query: CasesPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    cases_query_result = await CasesService.get_cases_list_services(query_db, cases_page_query, is_page=False)
    cases_export_result = await CasesService.export_cases_list_services(cases_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(cases_export_result))
