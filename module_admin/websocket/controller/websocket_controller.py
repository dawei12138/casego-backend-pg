import asyncio
import os
import jwt
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Optional, Any

from config.env import JwtConfig, AppConfig
from config.enums import RedisInitKeyConfig
from config.get_websocket import websocket_manager
from utils.log_util import logger
from utils.response_util import ResponseUtil

websocketController = APIRouter(prefix='/ws')

# 当前进程ID，用于调试多worker问题
WORKER_PID = os.getpid()


class WebSocketCloseCode:
    """
    WebSocket 关闭代码
    """
    NORMAL = 1000           # 正常关闭
    AUTH_FAILED = 4001      # 认证失败
    TOKEN_EXPIRED = 4002    # Token 已过期
    PARAM_ERROR = 4003      # 参数错误
    SERVER_ERROR = 4004     # 服务器错误


async def verify_websocket_token(
    redis: Any,
    token: str
) -> Optional[dict]:
    """
    验证 WebSocket 连接的 Token

    :param redis: Redis 连接对象
    :param token: JWT Token
    :return: 包含 user_id 和 session_id 的字典，验证失败返回 None
    """
    try:
        # 解析 JWT
        payload = jwt.decode(
            token,
            JwtConfig.jwt_secret_key,
            algorithms=[JwtConfig.jwt_algorithm]
        )

        user_id = payload.get('user_id')
        session_id = payload.get('session_id')

        if not user_id or not session_id:
            logger.warning('WebSocket Token 缺少 user_id 或 session_id')
            return None

        # 验证 Redis 中的 token
        if AppConfig.app_same_time_login:
            redis_key = f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}'
        else:
            redis_key = f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{user_id}'

        redis_token = await redis.get(redis_key)

        if token != redis_token:
            logger.warning('WebSocket Token 与 Redis 中不匹配')
            return None

        return {
            'user_id': int(user_id),
            'session_id': session_id
        }

    except jwt.ExpiredSignatureError:
        logger.warning('WebSocket Token 已过期')
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f'WebSocket Token 验证失败: {e}')
        return None
    except Exception as e:
        logger.error(f'WebSocket Token 验证异常: {e}')
        return None


@websocketController.websocket('/connect')
async def websocket_connect(
    websocket: WebSocket,
    token: str = None
):
    """
    WebSocket 连接端点

    连接地址: ws://host/ws/connect?token=xxx

    关闭代码:
    - 1000: 正常关闭
    - 4001: 认证失败
    - 4002: Token 已过期
    - 4003: 参数错误
    - 4004: 服务器错误
    """
    # 1. 参数检查
    if not token:
        await websocket.accept()
        await websocket.close(code=WebSocketCloseCode.PARAM_ERROR, reason='缺少 token 参数')
        return

    # 2. 从 websocket.scope 获取 app 对象，进而获取 redis
    app = websocket.scope.get('app')
    if not app or not hasattr(app.state, 'redis'):
        await websocket.accept()
        await websocket.close(code=WebSocketCloseCode.SERVER_ERROR, reason='服务器配置错误')
        return

    redis = app.state.redis

    # 3. 验证 Token
    auth_result = await verify_websocket_token(redis, token)

    if not auth_result:
        await websocket.accept()
        await websocket.close(code=WebSocketCloseCode.AUTH_FAILED, reason='认证失败')
        return

    user_id = auth_result['user_id']
    session_id = auth_result['session_id']

    # 4. 建立连接
    connected = await websocket_manager.connect(session_id, user_id, websocket)

    if not connected:
        return

    # 5. 发送连接成功消息
    await websocket_manager.send_to_session(session_id, {
        'type': 'connected',
        'message': 'WebSocket 连接成功',
        'data': {
            'session_id': session_id,
            'user_id': user_id
        }
    })

    try:
        # 6. 保持连接，处理消息
        while True:
            try:
                # 等待客户端消息（带超时，用于心跳检测）
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=60.0  # 60秒超时
                )

                # 处理心跳
                if data == 'ping':
                    await websocket.send_text('pong')
                    continue

                # 处理客户端主动发送的其他消息
                # logger.debug(f'收到客户端消息: session_id={session_id}, data={data}')

            except asyncio.TimeoutError:
                # 超时，发送心跳检测
                try:
                    await websocket.send_text('ping')
                except Exception:
                    # 发送失败，连接已断开
                    logger.info(f'WebSocket 心跳检测失败，断开连接: session_id={session_id}')
                    break

    except WebSocketDisconnect as e:
        logger.info(f'WebSocket 客户端主动断开: session_id={session_id}, code={e.code}')

    except Exception as e:
        logger.error(f'WebSocket 异常: session_id={session_id}, error={e}')

    finally:
        # 7. 清理连接
        await websocket_manager.disconnect(session_id)


@websocketController.websocket('/connect/{channel}')
async def websocket_connect_with_channel(
    websocket: WebSocket,
    channel: str,
    token: str = None
):
    """
    带频道的 WebSocket 连接

    可用于订阅特定类型的消息，如：
    - /ws/connect/workflow  订阅工作流通知
    - /ws/connect/task      订阅任务通知
    - /ws/connect/system    订阅系统通知

    连接地址: ws://host/ws/connect/{channel}?token=xxx
    """
    # 1. 参数检查
    if not token:
        await websocket.accept()
        await websocket.close(code=WebSocketCloseCode.PARAM_ERROR, reason='缺少 token 参数')
        return

    # 2. 从 websocket.scope 获取 app 对象
    app = websocket.scope.get('app')
    if not app or not hasattr(app.state, 'redis'):
        await websocket.accept()
        await websocket.close(code=WebSocketCloseCode.SERVER_ERROR, reason='服务器配置错误')
        return

    redis = app.state.redis

    # 3. 验证 Token
    auth_result = await verify_websocket_token(redis, token)

    if not auth_result:
        await websocket.accept()
        await websocket.close(code=WebSocketCloseCode.AUTH_FAILED, reason='认证失败')
        return

    user_id = auth_result['user_id']
    session_id = auth_result['session_id']

    # 4. 频道会话ID（区分不同频道的连接）
    channel_session_id = f'{session_id}:{channel}'

    # 5. 建立连接
    connected = await websocket_manager.connect(channel_session_id, user_id, websocket)

    if not connected:
        return

    # 6. 发送连接成功消息
    await websocket_manager.send_to_session(channel_session_id, {
        'type': 'connected',
        'message': f'WebSocket 连接成功，频道: {channel}',
        'data': {
            'session_id': session_id,
            'channel': channel,
            'user_id': user_id
        }
    })

    try:
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=60.0
                )

                if data == 'ping':
                    await websocket.send_text('pong')
                    continue

                # logger.debug(f'收到客户端消息: channel={channel}, session_id={session_id}, data={data}')

            except asyncio.TimeoutError:
                try:
                    await websocket.send_text('ping')
                except Exception:
                    break

    except WebSocketDisconnect as e:
        logger.info(f'WebSocket 客户端断开: channel={channel}, session_id={session_id}, code={e.code}')

    except Exception as e:
        logger.error(f'WebSocket 异常: channel={channel}, session_id={session_id}, error={e}')

    finally:
        await websocket_manager.disconnect(channel_session_id)


@websocketController.get('/debug/status')
async def get_websocket_debug_status():
    """
    WebSocket 连接状态调试接口

    用于诊断多 worker 或热重载导致的连接状态问题
    """
    return ResponseUtil.success(data={
        'worker_pid': WORKER_PID,
        'online_users': websocket_manager.get_online_user_ids(),
        'online_user_count': websocket_manager.get_online_user_count(),
        'connection_count': websocket_manager.get_connection_count(),
        'connections': list(websocket_manager.connections.keys()),
        'user_sessions': {
            str(k): list(v) for k, v in websocket_manager.user_sessions.items()
        },
        'session_user_map': {
            k: v for k, v in websocket_manager.session_user_map.items()
        }
    })
