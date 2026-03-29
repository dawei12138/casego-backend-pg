# -*- coding: utf-8 -*-
"""
Run 流式传输
支持 SSE (Server-Sent Events) 实时推送执行事件
"""

import asyncio
import json
from typing import AsyncIterator, Dict, Any, Optional
from datetime import datetime
from redis import asyncio as aioredis
from fastapi import Response
from fastapi.responses import StreamingResponse

from config.redis_config import get_redis_client


class RunStreamWriter:
    """
    Run 事件流写入器
    将事件写入 Redis Stream
    """

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.stream_key = f'run:stream:{run_id}'
        self.redis: Optional[aioredis.Redis] = None

    async def _get_redis(self) -> aioredis.Redis:
        """
        获取 Redis 客户端
        """
        if not self.redis:
            self.redis = await get_redis_client()
        return self.redis

    async def write_event(self, event_type: str, data: Dict[str, Any]):
        """
        写入事件到 Redis Stream
        """
        redis = await self._get_redis()

        event = {
            'type': event_type,
            'data': json.dumps(data, ensure_ascii=False),
            'timestamp': datetime.now().isoformat()
        }

        # 写入 Redis Stream
        await redis.xadd(self.stream_key, event, maxlen=10000)  # 最多保留10000条

    async def write_start(self, agent_name: str, model_name: str):
        """
        写入开始事件
        """
        await self.write_event('run_start', {
            'run_id': self.run_id,
            'agent_name': agent_name,
            'model_name': model_name,
        })

    async def write_content(self, content: str):
        """
        写入内容事件
        """
        await self.write_event('content', {
            'content': content,
        })

    async def write_tool_call(self, tool_name: str, arguments: Dict[str, Any]):
        """
        写入工具调用事件
        """
        await self.write_event('tool_call', {
            'tool_name': tool_name,
            'arguments': arguments,
        })

    async def write_tool_result(self, tool_name: str, result: Any):
        """
        写入工具结果事件
        """
        await self.write_event('tool_result', {
            'tool_name': tool_name,
            'result': result,
        })

    async def write_error(self, error_message: str, error_type: str = 'unknown'):
        """
        写入错误事件
        """
        await self.write_event('error', {
            'error_message': error_message,
            'error_type': error_type,
        })

    async def write_done(self, finish_reason: str, usage: Dict[str, int]):
        """
        写入完成事件
        """
        await self.write_event('done', {
            'finish_reason': finish_reason,
            'usage': usage,
        })

    async def close(self):
        """
        关闭写入器
        """
        if self.redis:
            await self.redis.close()


class RunStreamReader:
    """
    Run 事件流读取器
    从 Redis Stream 读取事件并生成 SSE
    """

    def __init__(self, run_id: str):
        self.run_id = run_id
        self.stream_key = f'run:stream:{run_id}'
        self.redis: Optional[aioredis.Redis] = None
        self.last_id = '0-0'  # 从头开始读取

    async def _get_redis(self) -> aioredis.Redis:
        """
        获取 Redis 客户端
        """
        if not self.redis:
            self.redis = await get_redis_client()
        return self.redis

    async def read_events(
        self,
        timeout: int = 30000,  # 30秒超时
        heartbeat_interval: int = 15  # 15秒心跳
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        读取事件流
        """
        redis = await self._get_redis()
        done = False
        last_heartbeat = asyncio.get_event_loop().time()

        while not done:
            current_time = asyncio.get_event_loop().time()

            # 发送心跳
            if current_time - last_heartbeat >= heartbeat_interval:
                yield {
                    'type': 'heartbeat',
                    'timestamp': datetime.now().isoformat()
                }
                last_heartbeat = current_time

            # 读取事件
            try:
                # XREAD 阻塞读取，block 参数单位是毫秒
                result = await redis.xread(
                    {self.stream_key: self.last_id},
                    count=10,  # 每次最多读取10条
                    block=1000  # 阻塞1秒
                )

                if result:
                    for stream_key, messages in result:
                        for message_id, message_data in messages:
                            self.last_id = message_id.decode() if isinstance(message_id, bytes) else message_id

                            # 解析事件
                            event_type = message_data.get(b'type', b'').decode()
                            data_str = message_data.get(b'data', b'{}').decode()
                            timestamp = message_data.get(b'timestamp', b'').decode()

                            try:
                                data = json.loads(data_str)
                            except json.JSONDecodeError:
                                data = {}

                            event = {
                                'type': event_type,
                                'data': data,
                                'timestamp': timestamp
                            }

                            yield event

                            # 检查是否完成
                            if event_type in ['done', 'error']:
                                done = True
                                break

            except asyncio.TimeoutError:
                # 超时，继续循环
                continue
            except Exception as e:
                # 发生错误，返回错误事件
                yield {
                    'type': 'error',
                    'data': {
                        'error_message': str(e),
                        'error_type': 'stream_read_error'
                    },
                    'timestamp': datetime.now().isoformat()
                }
                done = True

    async def close(self):
        """
        关闭读取器
        """
        if self.redis:
            await self.redis.close()


def create_sse_response(run_id: str) -> StreamingResponse:
    """
    创建 SSE 响应
    """
    async def event_generator():
        """
        SSE 事件生成器
        """
        reader = RunStreamReader(run_id)

        try:
            async for event in reader.read_events():
                # 格式化为 SSE 格式
                event_type = event.get('type', 'message')
                event_data = event.get('data', {})

                # SSE 格式: event: <type>\ndata: <json>\n\n
                sse_message = f"event: {event_type}\n"
                sse_message += f"data: {json.dumps(event_data, ensure_ascii=False)}\n\n"

                yield sse_message

                # 如果是完成或错误事件，结束流
                if event_type in ['done', 'error']:
                    break

        except Exception as e:
            # 发生错误，发送错误事件
            error_event = {
                'error_message': str(e),
                'error_type': 'generator_error'
            }
            yield f"event: error\ndata: {json.dumps(error_event, ensure_ascii=False)}\n\n"

        finally:
            await reader.close()

    return StreamingResponse(
        event_generator(),
        media_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no',  # 禁用 nginx 缓冲
        }
    )


async def cleanup_stream(run_id: str, ttl: int = 3600):
    """
    清理 Redis Stream
    设置过期时间，避免占用过多内存
    """
    redis = await get_redis_client()
    stream_key = f'run:stream:{run_id}'

    # 设置过期时间（默认1小时）
    await redis.expire(stream_key, ttl)

    await redis.close()
