import asyncio
import json
import os
from typing import Dict, Set, Optional, Any, Union, List
from fastapi import WebSocket
from redis import asyncio as aioredis
from utils.log_util import logger
from config.env import AppSettings


# Redis Pub/Sub 频道名称（包含环境标识，避免不同环境的消息混淆）
# 注意：Redis Pub/Sub 不区分 db，所以必须在频道名中区分环境
_app_settings = AppSettings()
WEBSOCKET_CHANNEL = f"websocket:broadcast:{_app_settings.app_env}"


class WebSocketManager:
    """
    WebSocket 连接管理器（支持多 Worker 模式）

    使用 Redis Pub/Sub 实现跨进程通信：
    - 每个 worker 维护自己的本地 WebSocket 连接
    - 发送消息时通过 Redis Pub/Sub 广播到所有 worker
    - 每个 worker 检查自己是否持有目标连接，有则发送

    使用 session_id 作为连接标识，支持：
    - 同一用户多设备同时在线
    - 给指定会话发送消息
    - 给指定用户的所有设备发送消息
    - 广播消息
    """

    def __init__(self):
        # session_id -> WebSocket 连接（本地进程内）
        self.connections: Dict[str, WebSocket] = {}
        # user_id -> session_id 集合（本地进程内）
        self.user_sessions: Dict[int, Set[str]] = {}
        # session_id -> user_id 反向映射（本地进程内）
        self.session_user_map: Dict[str, int] = {}
        # 连接锁，防止并发问题
        self._lock = asyncio.Lock()
        # 当前进程ID
        self._pid = os.getpid()
        # Redis 连接（由 start_pubsub_listener 设置）
        self._redis: Optional[aioredis.Redis] = None
        # Pub/Sub 监听任务
        self._pubsub_task: Optional[asyncio.Task] = None

    async def init_redis(self, redis: aioredis.Redis):
        """
        初始化 Redis 连接并启动 Pub/Sub 监听

        :param redis: Redis 连接实例
        """
        # 如果是 RedisProxy，获取底层 Redis 实例
        if hasattr(redis, 'raw_redis'):
            self._redis = redis.raw_redis
        else:
            self._redis = redis

        # 启动 Pub/Sub 监听
        await self._start_pubsub_listener()
        logger.info(f'[PID:{self._pid}] WebSocket Pub/Sub 监听器已启动')

    async def _start_pubsub_listener(self):
        """启动 Redis Pub/Sub 监听"""
        if self._pubsub_task is not None:
            return

        async def listener():
            """Pub/Sub 监听协程"""
            while True:
                try:
                    pubsub = self._redis.pubsub()
                    await pubsub.subscribe(WEBSOCKET_CHANNEL)
                    logger.info(f'[PID:{self._pid}] 已订阅 Redis 频道: {WEBSOCKET_CHANNEL}')

                    async for message in pubsub.listen():
                        if message['type'] == 'message':
                            await self._handle_pubsub_message(message['data'])

                except asyncio.CancelledError:
                    logger.info(f'[PID:{self._pid}] Pub/Sub 监听器已停止')
                    break
                except Exception as e:
                    logger.error(f'[PID:{self._pid}] Pub/Sub 监听异常: {e}，5秒后重连...')
                    await asyncio.sleep(5)

        self._pubsub_task = asyncio.create_task(listener())

    async def _handle_pubsub_message(self, data: str):
        """
        处理来自 Redis Pub/Sub 的消息

        :param data: 消息数据（JSON字符串）
        """
        try:
            msg = json.loads(data)
            action = msg.get('action')
            payload = msg.get('payload', {})
            source_pid = msg.get('source_pid')

            # 忽略自己发布的消息（本地已经处理过了）
            if source_pid == self._pid:
                return

            if action == 'send_to_session':
                session_id = payload.get('session_id')
                message = payload.get('message')
                if session_id in self.connections:
                    await self._local_send_to_session(session_id, message)

            elif action == 'send_to_user':
                user_id = payload.get('user_id')
                message = payload.get('message')
                # 只处理本进程内有的连接
                if user_id in self.user_sessions:
                    await self._local_send_to_user(user_id, message)

            elif action == 'broadcast':
                message = payload.get('message')
                exclude_sessions = set(payload.get('exclude_sessions', []))
                await self._local_broadcast(message, exclude_sessions)

        except Exception as e:
            logger.error(f'[PID:{self._pid}] 处理 Pub/Sub 消息失败: {e}')

    async def _publish(self, action: str, payload: dict):
        """
        发布消息到 Redis Pub/Sub

        :param action: 动作类型
        :param payload: 消息负载
        """
        if self._redis is None:
            logger.warning(f'[PID:{self._pid}] Redis 未初始化，无法发布消息')
            return

        message = json.dumps({
            'action': action,
            'payload': payload,
            'source_pid': self._pid
        }, ensure_ascii=False)

        try:
            await self._redis.publish(WEBSOCKET_CHANNEL, message)
        except Exception as e:
            logger.error(f'[PID:{self._pid}] 发布消息到 Redis 失败: {e}')

    async def connect(
        self,
        session_id: str,
        user_id: int,
        websocket: WebSocket
    ) -> bool:
        """
        建立 WebSocket 连接

        :param session_id: 会话ID（从JWT中获取）
        :param user_id: 用户ID
        :param websocket: WebSocket 连接对象
        :return: 是否成功
        """
        async with self._lock:
            try:
                await websocket.accept()

                # 确保 user_id 是 int 类型
                user_id = int(user_id) if isinstance(user_id, str) else user_id

                # 存储连接（本地进程内）
                self.connections[session_id] = websocket
                self.session_user_map[session_id] = user_id

                # 维护用户的会话集合（本地进程内）
                if user_id not in self.user_sessions:
                    self.user_sessions[user_id] = set()
                self.user_sessions[user_id].add(session_id)

                logger.info(f'[PID:{self._pid}] WebSocket连接建立: session_id={session_id}, user_id={user_id}, 本进程连接数: {len(self.connections)}')
                return True

            except Exception as e:
                logger.error(f'[PID:{self._pid}] WebSocket连接失败: {e}')
                return False

    async def disconnect(self, session_id: str) -> None:
        """
        断开 WebSocket 连接

        :param session_id: 会话ID
        """
        async with self._lock:
            if session_id not in self.connections:
                return

            # 获取用户ID
            user_id = self.session_user_map.get(session_id)

            # 移除连接
            del self.connections[session_id]
            if session_id in self.session_user_map:
                del self.session_user_map[session_id]

            # 从用户会话集合中移除
            if user_id and user_id in self.user_sessions:
                self.user_sessions[user_id].discard(session_id)
                # 如果用户没有任何连接了，删除用户条目
                if not self.user_sessions[user_id]:
                    del self.user_sessions[user_id]

            logger.info(f'[PID:{self._pid}] WebSocket连接断开: session_id={session_id}, user_id={user_id}, 本进程连接数: {len(self.connections)}')

    # ============ 本地发送方法（仅处理本进程内的连接）============

    async def _local_send_to_session(self, session_id: str, message: Union[str, dict]) -> bool:
        """本地发送消息给指定会话"""
        if session_id not in self.connections:
            return False

        websocket = self.connections[session_id]
        try:
            if isinstance(message, dict):
                await websocket.send_json(message)
            else:
                await websocket.send_text(message)
            logger.debug(f'[PID:{self._pid}] 本地发送成功: session_id={session_id}')
            return True
        except Exception as e:
            logger.error(f'[PID:{self._pid}] 本地发送失败: session_id={session_id}, error={e}')
            # 连接可能已断开，清理
            await self.disconnect(session_id)
            return False

    async def _local_send_to_user(self, user_id: int, message: Union[str, dict]) -> int:
        """本地发送消息给指定用户的所有设备"""
        if user_id not in self.user_sessions:
            return 0

        success_count = 0
        session_ids = list(self.user_sessions.get(user_id, set()))

        for session_id in session_ids:
            if await self._local_send_to_session(session_id, message):
                success_count += 1

        if success_count > 0:
            logger.info(f'[PID:{self._pid}] 本地发送给用户{user_id}成功: {success_count}个会话')
        return success_count

    async def _local_broadcast(self, message: Union[str, dict], exclude_sessions: Set[str] = None) -> int:
        """本地广播消息"""
        exclude_sessions = exclude_sessions or set()
        success_count = 0
        session_ids = list(self.connections.keys())

        for session_id in session_ids:
            if session_id not in exclude_sessions:
                if await self._local_send_to_session(session_id, message):
                    success_count += 1

        return success_count

    # ============ 公开的发送方法（通过 Redis Pub/Sub 广播）============

    async def send_to_session(self, session_id: str, message: Union[str, dict]) -> bool:
        """
        发送消息给指定会话（跨进程）

        :param session_id: 会话ID
        :param message: 消息内容（字符串或字典）
        :return: 是否发送成功
        """
        # 先尝试本地发送
        if session_id in self.connections:
            return await self._local_send_to_session(session_id, message)

        # 本地没有，通过 Pub/Sub 广播
        await self._publish('send_to_session', {
            'session_id': session_id,
            'message': message
        })
        return True  # 无法确认是否成功，返回 True 表示已发送

    async def send_to_user(self, user_id: int, message: Union[str, dict]) -> int:
        """
        发送消息给指定用户的所有设备（跨进程）

        :param user_id: 用户ID
        :param message: 消息内容
        :return: 本进程成功发送的设备数量
        """
        # 确保 user_id 是 int 类型
        user_id = int(user_id) if isinstance(user_id, str) else user_id

        # 通过 Pub/Sub 广播到所有进程
        await self._publish('send_to_user', {
            'user_id': user_id,
            'message': message
        })

        # 同时本地也处理（避免消息延迟）
        local_count = await self._local_send_to_user(user_id, message)

        logger.info(f'[PID:{self._pid}] 发送消息给用户{user_id}（已广播到所有Worker），本地发送: {local_count}')
        return local_count

    async def broadcast(
        self,
        message: Union[str, dict],
        exclude_sessions: Optional[Set[str]] = None
    ) -> int:
        """
        广播消息给所有连接（跨进程）

        :param message: 消息内容
        :param exclude_sessions: 排除的会话ID集合
        :return: 本进程成功发送的数量
        """
        exclude_sessions = exclude_sessions or set()

        # 通过 Pub/Sub 广播
        await self._publish('broadcast', {
            'message': message,
            'exclude_sessions': list(exclude_sessions)
        })

        # 同时本地也处理
        return await self._local_broadcast(message, exclude_sessions)

    async def broadcast_to_users(
        self,
        user_ids: List[int],
        message: Union[str, dict]
    ) -> int:
        """
        广播消息给指定用户列表（跨进程）

        :param user_ids: 用户ID列表
        :param message: 消息内容
        :return: 本进程成功发送的总数量
        """
        success_count = 0
        for user_id in user_ids:
            success_count += await self.send_to_user(user_id, message)
        return success_count

    # ============ 状态查询方法（仅返回本进程状态）============

    def is_user_online(self, user_id: int) -> bool:
        """检查用户是否在线（仅本进程）"""
        return user_id in self.user_sessions and len(self.user_sessions[user_id]) > 0

    def is_session_online(self, session_id: str) -> bool:
        """检查会话是否在线（仅本进程）"""
        return session_id in self.connections

    def get_online_user_count(self) -> int:
        """获取在线用户数量（仅本进程）"""
        return len(self.user_sessions)

    def get_connection_count(self) -> int:
        """获取连接总数（仅本进程）"""
        return len(self.connections)

    def get_user_session_ids(self, user_id: int) -> Set[str]:
        """获取用户的所有会话ID（仅本进程）"""
        return self.user_sessions.get(user_id, set()).copy()

    def get_online_user_ids(self) -> List[int]:
        """获取所有在线用户ID（仅本进程）"""
        return list(self.user_sessions.keys())

    def get_user_id_by_session(self, session_id: str) -> Optional[int]:
        """根据会话ID获取用户ID（仅本进程）"""
        return self.session_user_map.get(session_id)

    async def close(self):
        """关闭管理器"""
        if self._pubsub_task:
            self._pubsub_task.cancel()
            try:
                await self._pubsub_task
            except asyncio.CancelledError:
                pass
        logger.info(f'[PID:{self._pid}] WebSocket 管理器已关闭')


# 创建全局实例
websocket_manager = WebSocketManager()
