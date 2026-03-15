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
from module_admin.api_workflow.api_workflow_report.service.api_workflow_report_service import Api_workflow_reportService
from module_admin.api_workflow.api_workflow_report.entity.vo.api_workflow_report_vo import \
    DeleteApi_workflow_reportModel, Api_workflow_reportModel, Api_workflow_reportPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

api_workflow_reportController = APIRouter(prefix='/report/api_workflow_report',
                                          dependencies=[Depends(LoginService.get_current_user)])


@api_workflow_reportController.get(
    '/list', response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('report:api_workflow_report:list'))]
)
async def get_report_api_workflow_report_list(
        request: Request,
        api_workflow_report_page_query: Api_workflow_reportPageQueryModel = Depends(
            Api_workflow_reportPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    logger.info(api_workflow_report_page_query.model_dump())
    # 获取分页数据
    api_workflow_report_page_query_result = await Api_workflow_reportService.get_api_workflow_report_list_services(
        query_db, api_workflow_report_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=api_workflow_report_page_query_result)


@api_workflow_reportController.post('',
                                    dependencies=[Depends(CheckUserInterfaceAuth('report:api_workflow_report:add'))])
@ValidateFields(validate_model='add_api_workflow_report')
# @Log(title='自动化测试执行报告', business_type=BusinessType.INSERT)
async def add_report_api_workflow_report(
        request: Request,
        add_api_workflow_report: Api_workflow_reportModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_api_workflow_report.create_by = current_user.user.user_name
    add_api_workflow_report.create_time = datetime.now()
    add_api_workflow_report.update_by = current_user.user.user_name
    add_api_workflow_report.update_time = datetime.now()
    logger.info(add_api_workflow_report.model_dump())
    add_api_workflow_report_result = await Api_workflow_reportService.add_api_workflow_report_services(query_db,
                                                                                                       add_api_workflow_report)
    logger.info(add_api_workflow_report_result.message)

    return ResponseUtil.success(msg=add_api_workflow_report_result.message)


@api_workflow_reportController.put('',
                                   dependencies=[Depends(CheckUserInterfaceAuth('report:api_workflow_report:edit'))])
@ValidateFields(validate_model='edit_api_workflow_report')
# @Log(title='自动化测试执行报告', business_type=BusinessType.UPDATE)
async def edit_report_api_workflow_report(
        request: Request,
        edit_api_workflow_report: Api_workflow_reportModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_api_workflow_report.model_dump())
    edit_api_workflow_report.update_by = current_user.user.user_name
    edit_api_workflow_report.update_time = datetime.now()
    edit_api_workflow_report_result = await Api_workflow_reportService.edit_api_workflow_report_services(query_db,
                                                                                                         edit_api_workflow_report)
    logger.info(edit_api_workflow_report_result.message)

    return ResponseUtil.success(msg=edit_api_workflow_report_result.message)


@api_workflow_reportController.delete('/{report_ids}', dependencies=[
    Depends(CheckUserInterfaceAuth('report:api_workflow_report:remove'))])
# @Log(title='自动化测试执行报告', business_type=BusinessType.DELETE)
async def delete_report_api_workflow_report(request: Request, report_ids: str,
                                            query_db: AsyncSession = Depends(get_db)):
    delete_api_workflow_report = DeleteApi_workflow_reportModel(reportIds=report_ids)
    logger.info(delete_api_workflow_report.model_dump())
    delete_api_workflow_report_result = await Api_workflow_reportService.delete_api_workflow_report_services(query_db,
                                                                                                             delete_api_workflow_report)
    logger.info(delete_api_workflow_report_result.message)

    return ResponseUtil.success(msg=delete_api_workflow_report_result.message)


@api_workflow_reportController.get(
    '/{report_id}', response_model=Api_workflow_reportModel,
    dependencies=[Depends(CheckUserInterfaceAuth('report:api_workflow_report:query'))]
)
async def query_detail_report_api_workflow_report(request: Request, report_id: int,
                                                  query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    api_workflow_report_detail_result = await Api_workflow_reportService.api_workflow_report_detail_services(query_db,
                                                                                                             report_id)
    logger.info(f'获取report_id为{report_id}的信息成功')

    return ResponseUtil.success(data=api_workflow_report_detail_result)


@api_workflow_reportController.post('/export',
                                    dependencies=[Depends(CheckUserInterfaceAuth('report:api_workflow_report:export'))])
# @Log(title='自动化测试执行报告', business_type=BusinessType.EXPORT)
async def export_report_api_workflow_report_list(
        request: Request,
        api_workflow_report_page_query: Api_workflow_reportPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    api_workflow_report_query_result = await Api_workflow_reportService.get_api_workflow_report_list_services(query_db,
                                                                                                              api_workflow_report_page_query,
                                                                                                              is_page=False)
    api_workflow_report_export_result = await Api_workflow_reportService.export_api_workflow_report_list_services(
        api_workflow_report_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(api_workflow_report_export_result))
