from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from module_admin.system.notification.entity.do.notification_do import ApiNotification
from module_admin.system.notification.entity.vo.notification_vo import NotificationModel, NotificationPageQueryModel, NotificationQueryModel
from utils.page_util import PageUtil
from datetime import datetime, time
from config.get_db import get_db

class NotificationDao:
    """
    通知消息模块数据库操作层
    """

    @classmethod
    async def get_notification_detail_by_id(cls, db: AsyncSession, notification_id: int):
        """
        根据通知ID获取通知消息详细信息

        :param db: orm对象
        :param notification_id: 通知ID
        :return: 通知消息信息对象
        """
        notification_info = (
            (
                await db.execute(
                    select(ApiNotification)
                    .where(
                        ApiNotification.notification_id == notification_id
                    )
                )
            )
            .scalars()
            .first()
        )

        return notification_info

    @classmethod
    async def get_notification_detail_by_info(cls, db: AsyncSession, notification: NotificationModel):
        """
        根据通知消息参数获取通知消息信息

        :param db: orm对象
        :param notification: 通知消息参数对象
        :return: 通知消息信息对象
        """
        notification_info = (
            (
                await db.execute(
                    select(ApiNotification).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return notification_info

    @classmethod
    async def get_notification_list(cls, db: AsyncSession, query_object: NotificationPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取通知消息列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 通知消息列表信息字典对象
        """
        query = (
            select(ApiNotification)
            .where(
                ApiNotification.user_id == query_object.user_id if query_object.user_id else True,
                ApiNotification.notification_type == query_object.notification_type if query_object.notification_type else True,
                ApiNotification.title == query_object.title if query_object.title else True,
                ApiNotification.message == query_object.message if query_object.message else True,
                ApiNotification.is_read == query_object.is_read if query_object.is_read else True,
                ApiNotification.create_time == query_object.create_time if query_object.create_time else True,
                ApiNotification.read_time == query_object.read_time if query_object.read_time else True,
                ApiNotification.business_type == query_object.business_type if query_object.business_type else True,
                ApiNotification.business_id == query_object.business_id if query_object.business_id else True,
                ApiNotification.extra_data == query_object.extra_data if query_object.extra_data else True,
                ApiNotification.description == query_object.description if query_object.description else True,
                ApiNotification.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiNotification.del_flag == "0")
            .order_by(
                #
                ApiNotification.is_read.asc(),  # False在前，True在后
                ApiNotification.create_time.desc(),
            )
        )
        notification_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return notification_list

    @classmethod
    async def get_notification_orm_list(cls, db: AsyncSession, query_object: NotificationQueryModel) -> List[NotificationQueryModel]:
        """
        根据查询参数获取通知消息列表orm对象

        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 通知消息列表信息orm对象
        """
        query = (
            select(ApiNotification)
            .where(
                ApiNotification.user_id == query_object.user_id if query_object.user_id else True,
                ApiNotification.notification_type == query_object.notification_type if query_object.notification_type else True,
                ApiNotification.title == query_object.title if query_object.title else True,
                ApiNotification.message == query_object.message if query_object.message else True,
                ApiNotification.is_read == query_object.is_read if query_object.is_read else True,
                ApiNotification.read_time == query_object.read_time if query_object.read_time else True,
                ApiNotification.business_type == query_object.business_type if query_object.business_type else True,
                ApiNotification.business_id == query_object.business_id if query_object.business_id else True,
                ApiNotification.extra_data == query_object.extra_data if query_object.extra_data else True,
                ApiNotification.description == query_object.description if query_object.description else True,
                ApiNotification.sort_no == query_object.sort_no if query_object.sort_no else True,
            )
            .where(ApiNotification.del_flag == "0")
            .order_by(ApiNotification.notification_id)
        )

        result = await db.execute(query)
        return [NotificationQueryModel.validate(i) for i in result.scalars().all()]  # 返回对象列表

    @classmethod
    async def add_notification_dao(cls, db: AsyncSession, notification: NotificationModel):
        """
        新增通知消息数据库操作

        :param db: orm对象
        :param notification: 通知消息对象
        :return:
        """
        db_notification = ApiNotification(**notification.model_dump(exclude={}))
        db.add(db_notification)
        await db.flush()

        return db_notification

    @classmethod
    async def edit_notification_dao(cls, db: AsyncSession, notification: dict):
        """
        编辑通知消息数据库操作

        :param db: orm对象
        :param notification: 需要更新的通知消息字典
        :return:
        """
        await db.execute(update(ApiNotification), [notification])

    @classmethod
    async def delete_notification_dao(cls, db: AsyncSession, notification: NotificationModel):
        """
        删除通知消息数据库操作

        :param db: orm对象
        :param notification: 通知消息对象
        :return:
        """
        #await db.execute(delete(ApiNotification).where(ApiNotification.notification_id.in_([notification.notification_id])))
        await db.execute(update(ApiNotification).where(ApiNotification.notification_id.in_([notification.notification_id])).values(del_flag="1"))

if __name__ == '__main__':
    import asyncio


    async def main():

        async for db in get_db():
            try:
                query = NotificationPageQueryModel(
                    page_num=1,
                    page_size=10,
                )
                # 测试查询
                result = await NotificationDao.get_notification_list(db, query, is_page=True)
                print(f"查询结果: {result}")

            except Exception as e:
                print(f"发生错误: {e}")
            finally:
                await db.close()

    asyncio.run(main())
