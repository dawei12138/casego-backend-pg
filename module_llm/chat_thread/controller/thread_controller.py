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
from module_llm.chat_thread.service.thread_service import ThreadService
from module_llm.chat_thread.entity.vo.thread_vo import DeleteThreadModel, ThreadModel, ThreadPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

threadController = APIRouter(prefix='/chat/thread', dependencies=[Depends(LoginService.get_current_user)])


@threadController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('chat:thread:list'))],
    summary='获取LLM聊天线程列表',
    description='根据查询条件获取LLM聊天线程分页列表数据',
)
async def get_chat_thread_list(
        request: Request,
        thread_page_query: ThreadPageQueryModel = Depends(ThreadPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    # 添加userid
    thread_page_query.user_id = current_user.user.user_id
    logger.info(thread_page_query.model_dump())

    # 获取分页数据
    thread_page_query_result = await ThreadService.get_thread_list_services(query_db, thread_page_query, is_page=False)
    logger.info('获取成功')

    return ResponseUtil.success(rows=thread_page_query_result)


@threadController.post(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('chat:thread:add'))],
    summary='新增LLM聊天线程',
    description='创建一条新的LLM聊天线程记录',
)
@ValidateFields(validate_model='add_thread')
# @Log(title='LLM聊天线程', business_type=BusinessType.INSERT)
async def add_chat_thread(
        request: Request,
        add_thread: ThreadModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_thread.create_by = current_user.user.user_name
    add_thread.create_time = datetime.now()
    add_thread.update_by = current_user.user.user_name
    add_thread.update_time = datetime.now()
    logger.info(add_thread.model_dump())
    add_thread_result = await ThreadService.add_thread_services(query_db, add_thread)
    logger.info(add_thread_result.message)

    return ResponseUtil.success(msg=add_thread_result.message)


@threadController.put(
    '',
    dependencies=[Depends(CheckUserInterfaceAuth('chat:thread:edit'))],
    summary='修改LLM聊天线程',
    description='根据主键更新LLM聊天线程信息',
)
@ValidateFields(validate_model='edit_thread')
# @Log(title='LLM聊天线程', business_type=BusinessType.UPDATE)
async def edit_chat_thread(
        request: Request,
        edit_thread: ThreadModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_thread.model_dump())
    edit_thread.update_by = current_user.user.user_name
    edit_thread.update_time = datetime.now()
    edit_thread_result = await ThreadService.edit_thread_services(query_db, edit_thread)
    logger.info(edit_thread_result.message)

    return ResponseUtil.success(msg=edit_thread_result.message)


@threadController.delete(
    '/{thread_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('chat:thread:remove'))],
    summary='删除LLM聊天线程',
    description='根据主键批量删除LLM聊天线程记录，多个主键以逗号分隔',
)
# @Log(title='LLM聊天线程', business_type=BusinessType.DELETE)
async def delete_chat_thread(request: Request, thread_ids: str, query_db: AsyncSession = Depends(get_db)):
    delete_thread = DeleteThreadModel(threadIds=thread_ids)
    logger.info(delete_thread.model_dump())
    delete_thread_result = await ThreadService.delete_thread_services(query_db, delete_thread)
    logger.info(delete_thread_result.message)

    return ResponseUtil.success(msg=delete_thread_result.message)


@threadController.get(
    '/{thread_id}',
    response_model=ThreadModel,
    dependencies=[Depends(CheckUserInterfaceAuth('chat:thread:query'))],
    summary='获取LLM聊天线程详情',
    description='根据主键获取LLM聊天线程详细信息',
)
async def query_detail_chat_thread(request: Request, thread_id: str, query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    thread_detail_result = await ThreadService.thread_detail_services(query_db, thread_id)
    logger.info(f'获取thread_id为{thread_id}的信息成功')

    return ResponseUtil.success(data=thread_detail_result)


@threadController.post(
    '/export',
    dependencies=[Depends(CheckUserInterfaceAuth('chat:thread:export'))],
    summary='导出LLM聊天线程',
    description='根据查询条件导出LLM聊天线程列表数据到Excel文件',
)
# @Log(title='LLM聊天线程', business_type=BusinessType.EXPORT)
async def export_chat_thread_list(
        request: Request,
        thread_page_query: ThreadPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    thread_query_result = await ThreadService.get_thread_list_services(query_db, thread_page_query, is_page=False)
    thread_export_result = await ThreadService.export_thread_list_services(thread_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(thread_export_result))
