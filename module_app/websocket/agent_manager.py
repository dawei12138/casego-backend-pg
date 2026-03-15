# -*- coding: utf-8 -*-
"""
Agent WebSocket 连接管理器

负责管理 Sonic Agent 的 WebSocket 连接，与现有的用户 WebSocket 管理器分离
"""
import asyncio
import json
import os
from typing import Dict, Optional, Set
from fastapi import WebSocket
from utils.log_util import logger


class AgentConnectionManager:
    """
    Agent WebSocket 连接管理器

    特点：
    - Agent 使用 agent_id 作为标识
    - 支持向指定 Agent 发送消息
    - 维护 Agent 在线状态
    """

    def __init__(self):
        # agent_id -> WebSocket 连接
        self.connections: Dict[int, WebSocket] = {}
        # agent_id -> agent_key (用于验证)
        self.agent_keys: Dict[int, str] = {}
        # 连接锁，防止并发问题
        self._lock = asyncio.Lock()
        # 当前进程ID
        self._pid = os.getpid()

    async def connect(
        self,
        agent_id: int,
        agent_key: str,
        websocket: WebSocket
    ) -> bool:
        """
        建立 Agent WebSocket 连接

        :param agent_id: Agent ID
        :param agent_key: Agent 密钥
        :param websocket: WebSocket 连接对象
        :return: 是否成功
        """
        async with self._lock:
            try:
                await websocket.accept()

                # 如果已有连接，先断开旧连接
                if agent_id in self.connections:
                    old_ws = self.connections[agent_id]
                    try:
                        await old_ws.close(code=1000, reason='新连接建立，断开旧连接')
                    except Exception:
                        pass
                    logger.info(f'[PID:{self._pid}] Agent 旧连接已断开: agent_id={agent_id}')

                # 存储新连接
                self.connections[agent_id] = websocket
                self.agent_keys[agent_id] = agent_key

                logger.info(
                    f'[PID:{self._pid}] Agent 连接建立: agent_id={agent_id}, '
                    f'当前连接数: {len(self.connections)}'
                )
                return True

            except Exception as e:
                logger.error(f'[PID:{self._pid}] Agent 连接失败: agent_id={agent_id}, error={e}')
                return False

    async def disconnect(self, agent_id: int) -> None:
        """
        断开 Agent WebSocket 连接

        :param agent_id: Agent ID
        """
        async with self._lock:
            if agent_id not in self.connections:
                return

            # 移除连接
            del self.connections[agent_id]
            if agent_id in self.agent_keys:
                del self.agent_keys[agent_id]

            logger.info(
                f'[PID:{self._pid}] Agent 连接断开: agent_id={agent_id}, '
                f'当前连接数: {len(self.connections)}'
            )

    async def send_to_agent(self, agent_id: int, message: dict) -> bool:
        """
        发送消息给指定 Agent

        :param agent_id: Agent ID
        :param message: 消息内容（字典）
        :return: 是否发送成功
        """
        if agent_id not in self.connections:
            logger.warning(f'[PID:{self._pid}] Agent 不在线: agent_id={agent_id}')
            return False

        websocket = self.connections[agent_id]
        try:
            await websocket.send_text(json.dumps(message, ensure_ascii=False))

            # pong消息不记录日志，减少日志量
            msg_type = message.get('msg')
            if msg_type != 'pong':
                logger.debug(f'[PID:{self._pid}] 发送消息到 Agent: agent_id={agent_id}, msg={msg_type}')

            return True
        except Exception as e:
            logger.error(f'[PID:{self._pid}] 发送消息到 Agent 失败: agent_id={agent_id}, error={e}')
            # 连接可能已断开，清理
            await self.disconnect(agent_id)
            return False

    async def broadcast_to_all(self, message: dict, exclude_agents: Set[int] = None) -> int:
        """
        广播消息给所有 Agent

        :param message: 消息内容
        :param exclude_agents: 排除的 Agent ID 集合
        :return: 成功发送的数量
        """
        exclude_agents = exclude_agents or set()
        success_count = 0
        agent_ids = list(self.connections.keys())

        for agent_id in agent_ids:
            if agent_id not in exclude_agents:
                if await self.send_to_agent(agent_id, message):
                    success_count += 1

        return success_count

    def is_agent_online(self, agent_id: int) -> bool:
        """检查 Agent 是否在线"""
        return agent_id in self.connections

    def get_online_agent_ids(self) -> list:
        """获取所有在线 Agent ID"""
        return list(self.connections.keys())

    def get_online_count(self) -> int:
        """获取在线 Agent 数量"""
        return len(self.connections)

    def get_agent_websocket(self, agent_id: int) -> Optional[WebSocket]:
        """获取 Agent 的 WebSocket 连接"""
        return self.connections.get(agent_id)


# 创建全局实例
agent_manager = AgentConnectionManager()
