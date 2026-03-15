from sqlalchemy import update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.constant import CommonConstant
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.common_vo import CrudResponseModel
from module_admin.system.notification.dao.notification_dao import NotificationDao
from module_admin.system.notification.entity.do.notification_do import ApiNotification
from module_admin.system.notification.entity.vo.notification_vo import DeleteNotificationModel, NotificationModel, NotificationPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class NotificationService:
    """
    通知消息模块服务层
    """

    @classmethod
    async def get_notification_list_services(
        cls, query_db: AsyncSession, query_object: NotificationPageQueryModel, is_page: bool = False
    ):
        """
        获取通知消息列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 通知消息列表信息对象
        """
        notification_list_result = await NotificationDao.get_notification_list(query_db, query_object, is_page)

        return notification_list_result

    @classmethod
    async def get_unread_count(cls, db: AsyncSession, user_id: int) -> int:
        """
        获取用户未读通知数量

        :param db: 异步数据库会话
        :param user_id: 用户ID
        :return: 未读通知数量
        """
        from sqlalchemy import select, func

        # 构建查询
        query = (
            select(func.count(ApiNotification.notification_id))
            .where(ApiNotification.user_id == user_id)
            .where(ApiNotification.is_read == False)
            .where(ApiNotification.del_flag == "0")
        )

        # 执行查询并获取结果
        result = await db.execute(query)
        count = result.scalar()

        return count or 0
    @classmethod
    async def add_notification_services(cls, query_db: AsyncSession, page_object: NotificationModel):
        """
        新增通知消息信息service

        :param query_db: orm对象
        :param page_object: 新增通知消息对象
        :return: 新增通知消息校验结果
        """
        try:
            await NotificationDao.add_notification_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_notification_services(cls, query_db: AsyncSession, page_object: NotificationModel):
        """
        编辑通知消息信息service

        :param query_db: orm对象
        :param page_object: 编辑通知消息对象
        :return: 编辑通知消息校验结果
        """
        edit_notification = page_object.model_dump(exclude_unset=True, exclude={'create_by', 'create_time', 'del_flag'})
        notification_info = await cls.notification_detail_services(query_db, page_object.notification_id)
        if notification_info.notification_id:
            try:
                await NotificationDao.edit_notification_dao(query_db, edit_notification)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='通知消息不存在')

    @classmethod
    async def readall_notification_services(cls, query_db: AsyncSession, page_object: NotificationModel):
        """
        编辑通知消息信息service

        :param query_db: orm对象
        :param page_object: 编辑通知消息对象
        :return: 编辑通知消息校验结果
        """

        try:
            await query_db.execute(
                update(ApiNotification).where(ApiNotification.user_id.in_([page_object.user_id])).values(
                    is_read=1))
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def delete_notification_services(cls, query_db: AsyncSession, page_object: DeleteNotificationModel):
        """
        删除通知消息信息service

        :param query_db: orm对象
        :param page_object: 删除通知消息对象
        :return: 删除通知消息校验结果
        """
        if page_object.notification_ids:
            notification_id_list = page_object.notification_ids.split(',')
            try:
                for notification_id in notification_id_list:
                    await NotificationDao.delete_notification_dao(query_db, NotificationModel(notificationId=notification_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入通知ID为空')

    @classmethod
    async def notification_detail_services(cls, query_db: AsyncSession, notification_id: int):
        """
        获取通知消息详细信息service

        :param query_db: orm对象
        :param notification_id: 通知ID
        :return: 通知ID对应的信息
        """
        notification = await NotificationDao.get_notification_detail_by_id(query_db, notification_id=notification_id)
        if notification:
            result = NotificationModel(**CamelCaseUtil.transform_result(notification))
        else:
            result = NotificationModel(**dict())

        return result

    @staticmethod
    async def export_notification_list_services(notification_list: List):
        """
        导出通知消息信息service

        :param notification_list: 通知消息信息列表
        :return: 通知消息信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'notificationId': '通知ID',
            'userId': '接收用户ID',
            'notificationType': '通知类型(system/task/workflow/alert)',
            'title': '通知标题',
            'message': '通知内容',
            'isRead': '是否已读',
            'readTime': '阅读时间',
            'businessType': '关联业务类型(workflow/test_case/report等)',
            'businessId': '关联业务ID',
            'extraData': '扩展数据',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'description': '描述',
            'sortNo': '排序值',
            'delFlag': '删除标志 0正常 1删除 2代表删除',
        }
        binary_data = ExcelUtil.export_list2excel(notification_list, mapping_dict)

        return binary_data
