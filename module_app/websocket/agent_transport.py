# -*- coding: utf-8 -*-
"""
Agent WebSocket 传输控制器

负责处理 Sonic Agent 的 WebSocket 连接和消息路由
对应 Java: TransportServerController
"""
import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from module_app.websocket.agent_manager import agent_manager
from module_app.websocket.message_handler import AgentMessageHandler
from module_app.enums import AgentStatusEnum, DeviceStatusEnum
from utils.log_util import logger

agentTransportController = APIRouter(prefix='/server/websockets', tags=['Agent通信'])


# ==================== 辅助函数 ====================

async def get_agent_by_key(db: AsyncSession, agent_key: str):
    """
    根据 agent_key 获取 Agent 信息

    :param db: 数据库会话
    :param agent_key: Agent 密钥
    :return: Agent 信息或 None
    """
    from module_app.agents.entity.do.agents_do import AppAgents
    from sqlalchemy import select

    result = await db.execute(
        select(AppAgents).where(
            AppAgents.secret_key == agent_key,
            AppAgents.del_flag == "0"
        )
    )
    return result.scalars().first()


async def set_agent_offline(db: AsyncSession, agent_id: int):
    """
    设置 Agent 离线

    同时将该 Agent 下的所有设备设置为离线

    :param db: 数据库会话
    :param agent_id: Agent ID
    """
    from module_app.agents.entity.do.agents_do import AppAgents
    from module_app.devices.entity.do.devices_do import AppDevices
    from sqlalchemy import update

    try:
        # 更新 Agent 状态
        await db.execute(
            update(AppAgents)
            .where(AppAgents.id == agent_id)
            .values(status=AgentStatusEnum.OFFLINE)
        )

        # 更新该 Agent 下所有设备状态
        await db.execute(
            update(AppDevices)
            .where(AppDevices.agent_id == agent_id, AppDevices.del_flag == "0")
            .values(status=DeviceStatusEnum.OFFLINE, user='')
        )

        await db.commit()
        logger.info(f'Agent {agent_id} 及其设备已设置为离线')

    except Exception as e:
        await db.rollback()
        logger.error(f'设置 Agent {agent_id} 离线失败: {e}')


# ==================== WebSocket 端点 ====================

@agentTransportController.websocket('/agent/{agent_key}')
async def agent_websocket_endpoint(
    websocket: WebSocket,
    agent_key: str
):
    """
    Agent WebSocket 连接端点

    连接地址: ws://host/dev-api/server/api/agent/{agentKey}

    消息格式: JSON
    {
        "msg": "消息类型",
        ...其他字段
    }

    心跳机制（严格遵循原始Sonic设计）:
    - 客户端每10秒主动发送 {"msg":"ping"}
    - 服务端接收ping后立即回复 {"msg":"pong"}
    - 服务端不主动发送ping，只被动响应

    支持的消息类型:
    - ping: 客户端心跳（服务端回复pong）
    - heartBeat: 心跳状态更新
    - agentInfo: Agent 信息上报
    - deviceDetail: 设备详情上报
    - findSteps: 查找用例步骤
    - battery: 电池信息
    - debugUser: 调试用户更新
    - generateStep: 生成临时步骤
    - errCall: 错误回调
    """
    # 使用独立的数据库会话
    from config.database import async_engine
    from sqlalchemy.orm import sessionmaker

    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as db:
        # 1. 验证 Agent
        agent = await get_agent_by_key(db, agent_key)

        if not agent:
            await websocket.accept()
            await websocket.close(code=4001, reason='无效的 Agent Key')
            logger.warning(f'无效的 Agent Key 尝试连接: {agent_key}')
            return

        agent_id = agent.id

        # 2. 建立连接
        connected = await agent_manager.connect(agent_id, agent_key, websocket)
        if not connected:
            return

        # 3. 发送认证响应消息（关键步骤：agent期望收到此消息）
        # 这是Sonic协议的核心：agent连接后必须收到认证响应才会继续工作
        auth_response = {
            'msg': 'auth',
            'result': 'pass',
            'id': agent_id,
            'highTemp': agent.high_temp,
            'highTempTime': agent.high_temp_time,
            'remoteTimeout': 480  # 默认远程调试超时时间（秒）
        }

        try:
            await websocket.send_text(json.dumps(auth_response, ensure_ascii=False))
            logger.info(f'已向 Agent {agent_id} 发送认证响应: {auth_response}')
        except Exception as e:
            logger.error(f'发送认证响应失败: {e}')
            await agent_manager.disconnect(agent_id)
            return

        # 4. 更新 Agent 在线状态
        from module_app.agents.entity.do.agents_do import AppAgents
        from sqlalchemy import update

        await db.execute(
            update(AppAgents)
            .where(AppAgents.id == agent_id)
            .values(status=AgentStatusEnum.ONLINE)
        )
        await db.commit()

        # 5. 创建消息处理器
        handler = AgentMessageHandler(agent_id, db)

        try:
            # 6. 保持连接，处理消息
            # 原始Sonic设计：服务端只接收消息，不主动发送ping
            # 客户端每10秒发送ping，服务端回复pong即可保持连接
            while True:
                try:
                    # 等待接收消息（不设置超时，依赖客户端心跳）
                    data = await websocket.receive_text()

                    # 解析消息
                    try:
                        msg = json.loads(data)

                        # ping消息不记录日志，减少日志量
                        if msg.get('msg') != 'ping':
                            logger.info(f'收到 Agent {agent_id} 的消息: {msg}')

                    except json.JSONDecodeError:
                        logger.warning(f'Agent {agent_id} 发送了无效 JSON: {data[:100]}')
                        continue

                    # 处理消息
                    await handler.handle_message(msg)

                except asyncio.CancelledError:
                    logger.info(f'Agent {agent_id} 连接被取消')
                    raise

        except WebSocketDisconnect as e:
            logger.info(f'Agent {agent_id} 主动断开: code={e.code}')

        except Exception as e:
            logger.error(f'Agent {agent_id} WebSocket 异常: {e}')

        finally:
            # 7. 清理连接
            await agent_manager.disconnect(agent_id)

            # 8. 设置 Agent 及其设备离线
            await set_agent_offline(db, agent_id)


# ==================== Agent 状态查询 API ====================

@agentTransportController.get('/agents/online')
async def get_online_agents():
    """
    获取在线 Agent 列表

    返回:
    {
        "code": 200,
        "data": {
            "online_agents": [1, 2, 3],
            "online_count": 3
        }
    }
    """
    from utils.response_util import ResponseUtil

    return ResponseUtil.success(data={
        'online_agents': agent_manager.get_online_agent_ids(),
        'online_count': agent_manager.get_online_count()
    })


@agentTransportController.get('/agents/{agent_id}/online')
async def check_agent_online(agent_id: int):
    """
    检查指定 Agent 是否在线

    :param agent_id: Agent ID
    :return: Agent 在线状态
    """
    from utils.response_util import ResponseUtil

    is_online = agent_manager.is_agent_online(agent_id)
    return ResponseUtil.success(data={
        'agent_id': agent_id,
        'is_online': is_online
    })
