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
from module_admin.system.notification.service.notification_service import NotificationService
from module_admin.system.notification.entity.vo.notification_vo import DeleteNotificationModel, NotificationModel, \
    NotificationPageQueryModel
from utils.common_util import bytes2file_response, CamelCaseUtil
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

notificationController = APIRouter(prefix='/task_notification/notification',
                                   dependencies=[Depends(LoginService.get_current_user)])


@notificationController.get(
    '/list', response_model=PageResponseModel
)
async def get_task_notification_notification_list(
        request: Request,
        notification_page_query: NotificationPageQueryModel = Depends(NotificationPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(notification_page_query.model_dump())
    notification_page_query.user_id = current_user.user.user_id
    # 获取分页数据
    notification_page_query_result = await NotificationService.get_notification_list_services(query_db,
                                                                                              notification_page_query,
                                                                                              is_page=True)
    res = notification_page_query_result.model_dump()
    res["totalUnRead"] = await NotificationService.get_unread_count(query_db,notification_page_query.user_id)

    logger.info('获取成功')

    return ResponseUtil.success(dict_content=CamelCaseUtil.transform_result(res))


@notificationController.post('', )
@ValidateFields(validate_model='add_notification')
# @Log(title='通知消息', business_type=BusinessType.INSERT)
async def add_task_notification_notification(
        request: Request,
        add_notification: NotificationModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    add_notification.create_by = current_user.user.user_name
    add_notification.create_time = datetime.now()
    add_notification.update_by = current_user.user.user_name
    add_notification.update_time = datetime.now()
    logger.info(add_notification.model_dump())
    add_notification_result = await NotificationService.add_notification_services(query_db, add_notification)
    logger.info(add_notification_result.message)

    return ResponseUtil.success(msg=add_notification_result.message)


@notificationController.put('', )
@ValidateFields(validate_model='edit_notification')
# @Log(title='通知消息', business_type=BusinessType.UPDATE)
async def edit_task_notification_notification(
        request: Request,
        edit_notification: NotificationModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_notification.model_dump())
    edit_notification.update_by = current_user.user.user_name
    edit_notification.update_time = datetime.now()
    edit_notification_result = await NotificationService.edit_notification_services(query_db, edit_notification)
    logger.info(edit_notification_result.message)

    return ResponseUtil.success(msg=edit_notification_result.message)


@notificationController.get('/readall', )
@ValidateFields(validate_model='edit_notification')
# @Log(title='通知消息', business_type=BusinessType.UPDATE)
async def edit_task_notification_notification(
        request: Request,
        edit_notification: NotificationPageQueryModel = Depends(NotificationPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    logger.info(edit_notification.model_dump())
    edit_notification.update_by = current_user.user.user_name
    edit_notification.update_time = datetime.now()
    edit_notification.user_id = current_user.user.user_id
    edit_notification_result = await NotificationService.readall_notification_services(query_db, edit_notification)
    logger.info(edit_notification_result.message)

    return ResponseUtil.success(msg=edit_notification_result.message)


@notificationController.delete('/{notification_ids}', )
# @Log(title='通知消息', business_type=BusinessType.DELETE)
async def delete_task_notification_notification(request: Request, notification_ids: str,
                                                query_db: AsyncSession = Depends(get_db)):
    delete_notification = DeleteNotificationModel(notificationIds=notification_ids)
    logger.info(delete_notification.model_dump())
    delete_notification_result = await NotificationService.delete_notification_services(query_db, delete_notification)
    logger.info(delete_notification_result.message)

    return ResponseUtil.success(msg=delete_notification_result.message)


@notificationController.get(
    '/{notification_id}', response_model=NotificationModel,
)
async def query_detail_task_notification_notification(request: Request, notification_id: int,
                                                      query_db: AsyncSession = Depends(get_db)):
    logger.info(f"id:{id}")
    notification_detail_result = await NotificationService.notification_detail_services(query_db, notification_id)
    logger.info(f'获取notification_id为{notification_id}的信息成功')

    return ResponseUtil.success(data=notification_detail_result)


@notificationController.post('/export', )
# @Log(title='通知消息', business_type=BusinessType.EXPORT)
async def export_task_notification_notification_list(
        request: Request,
        notification_page_query: NotificationPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    # 获取全量数据
    notification_query_result = await NotificationService.get_notification_list_services(query_db,
                                                                                         notification_page_query,
                                                                                         is_page=False)
    notification_export_result = await NotificationService.export_notification_list_services(notification_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(notification_export_result))
