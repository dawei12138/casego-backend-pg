from typing import Union

from config.enums import NotificationType
from config.get_websocket import websocket_manager
from utils.log_util import logger


class WebSocketService:
    """
    WebSocket 通知服务
    """

    @staticmethod
    def _ensure_int(user_id: Union[int, str]) -> int:
        """确保 user_id 是 int 类型"""
        return int(user_id) if isinstance(user_id, str) else user_id

    # ============ 通用方法 ============

    @classmethod
    async def send_to_user(
            cls,
            user_id: Union[int, str],
            data: dict
    ) -> int:
        """
        发送消息给指定用户

        :param user_id: 用户ID
        :param data: 消息数据
        :return: 成功发送的设备数
        """
        user_id = cls._ensure_int(user_id)
        count = await websocket_manager.send_to_user(user_id, data)
        logger.info(f'通知用户: user_id={user_id}, type={data.get("type")}, sent={count}')
        return count

    @classmethod
    async def broadcast(cls, data: dict) -> int:
        """
        广播给所有在线用户

        :param data: 消息数据
        :return: 成功发送的数量
        """
        count = await websocket_manager.broadcast(data)
        logger.info(f'广播消息: type={data.get("type")}, sent={count}')
        return count

    # ============ 基础通知方法 ============

    @classmethod
    async def notify(
            cls,
            user_id: Union[int, str],
            title: str,
            message: str,
            notify_type: str = NotificationType.SUCCESS
    ) -> int:
        """
        发送简化格式的通知

        :param user_id: 用户ID
        :param title: 通知标题
        :param message: 通知内容
        :param notify_type: 通知类型 (success/error)
        :return: 成功发送的设备数
        """
        return await cls.send_to_user(user_id, {
            'title': title,
            'message': message,
            'type': notify_type
        })

    # ============ 工作流通知 ============

    @classmethod
    async def notify_workflow_complete(
            cls,
            user_id: Union[int, str],
            workflow_id: int,
            workflow_name: str,
            total: int,
            success: int,
            failed: int,
            duration: float
    ) -> int:
        """
        通知：工作流执行完成
        """
        title = '工作流执行完成'
        message = f'{workflow_name} 执行完成，共{total}条，成功{success}条，失败{failed}条，耗时{round(duration, 2)}秒'
        notify_type = NotificationType.SUCCESS if failed == 0 else NotificationType.ERROR
        return await cls.notify(user_id, title, message, notify_type)

    @classmethod
    async def notify_workflow_failed(
            cls,
            user_id: Union[int, str],
            workflow_id: int,
            workflow_name: str,
            error: str
    ) -> int:
        """
        通知：工作流执行失败
        """
        title = '工作流执行失败'
        message = f'{workflow_name} 执行异常: {error}'
        return await cls.notify(user_id, title, message, NotificationType.ERROR)

    # ============ 定时任务通知 ============

    @classmethod
    async def notify_task_complete(
            cls,
            user_id: Union[int, str],
            workflow_id: int,
            workflow_name: str,
            total: int,
            success: int,
            failed: int,
            duration: float
    ) -> int:
        """
        通知：定时任务执行完成
        """
        title = '定时任务执行完成'
        message = f'{workflow_name} 执行完成，共{total}条，成功{success}条，失败{failed}条，耗时{round(duration, 2)}秒'
        notify_type = NotificationType.SUCCESS if failed == 0 else NotificationType.ERROR

        return await cls.notify(user_id, title, message, notify_type)

    @classmethod
    async def notify_task_failed(
            cls,
            user_id: Union[int, str],
            task_id: int,
            task_name: str,
            error: str
    ) -> int:
        """
        通知：定时任务执行失败
        """
        title = '定时任务执行失败'
        message = f'{task_name} 执行异常: {error}'
        return await cls.notify(user_id, title, message, NotificationType.ERROR)

    # ============ 系统通知 ============

    @classmethod
    async def notify_system(cls, title: str, content: str) -> int:
        """
        系统公告（广播给所有人）
        """
        return await cls.broadcast({
            'title': title,
            'message': content,
            'type': NotificationType.SUCCESS
        })

    # ============ 状态查询 ============

    @classmethod
    def is_user_online(cls, user_id: Union[int, str]) -> bool:
        """检查用户是否在线"""
        return websocket_manager.is_user_online(cls._ensure_int(user_id))

    @classmethod
    def get_online_count(cls) -> int:
        """获取在线用户数量"""
        return websocket_manager.get_online_user_count()
