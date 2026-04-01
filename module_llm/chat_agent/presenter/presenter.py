# -*- coding: utf-8 -*-
"""Unified SSE event emitter with bounded queue backpressure."""
import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, AsyncGenerator
from uuid import uuid4

from .event_types import EventType, SSEEvent


@dataclass
class PresenterConfig:
    thread_id: str
    user_id: str
    run_id: str = ''
    trace_id: str = ''
    request_id: str = ''
    queue_size: int = 500
    interrupt_check_interval: float = 1.0

    def __post_init__(self):
        if not self.run_id:
            self.run_id = f'run_{uuid4().hex[:12]}'
        if not self.trace_id:
            self.trace_id = f'trace_{uuid4().hex[:12]}'
        if not self.request_id:
            self.request_id = str(uuid4())


class Presenter:
    """Unified SSE event emitter.

    Producer side: agent execution calls emit_*() methods.
    Consumer side: SSE endpoint iterates iter_sse().
    Bounded asyncio.Queue provides backpressure.
    """

    def __init__(self, config: PresenterConfig):
        self._config = config
        self._queue: asyncio.Queue[SSEEvent | None] = asyncio.Queue(
            maxsize=config.queue_size,
        )
        self._closed = False

    @property
    def run_id(self) -> str:
        return self._config.run_id

    @property
    def trace_id(self) -> str:
        return self._config.trace_id

    @property
    def request_id(self) -> str:
        return self._config.request_id

    @property
    def config(self) -> PresenterConfig:
        return self._config

    # ── Event emission ──

    async def emit_metadata(self, metadata: dict[str, Any]) -> None:
        await self._emit(EventType.METADATA, metadata)

    async def emit_content(self, text: str) -> None:
        await self._emit(EventType.CONTENT, {'content': text})

    async def emit_thinking(self, text: str) -> None:
        await self._emit(EventType.THINKING, {'content': text})

    async def emit_thinking_start(self) -> None:
        await self._emit(EventType.THINKING_START, {})

    async def emit_thinking_end(self) -> None:
        await self._emit(EventType.THINKING_END, {})

    async def emit_tool_start(self, tool_name: str, call_id: str, args: dict | None = None) -> None:
        await self._emit(EventType.TOOL_CALL, {'tool': tool_name, 'call_id': call_id, 'args': args or {}})

    async def emit_tool_call_args(self, tool_name: str, call_id: str, args: dict) -> None:
        await self._emit(EventType.TOOL_CALL_ARGS, {'tool': tool_name, 'call_id': call_id, 'args': args})

    async def emit_tool_result(self, tool_name: str, call_id: str, result: str, args: dict | None = None) -> None:
        await self._emit(EventType.TOOL_RESULT, {'tool': tool_name, 'call_id': call_id, 'args': args or {}, 'result': result})

    async def emit_ask_user(self, request_id: str, value: dict) -> None:
        await self._emit(EventType.ASK_USER, {'request_id': request_id, **value})

    async def emit_retry(self, request_id: str, attempt: int, max_retries: int, reason: str) -> None:
        await self._emit(EventType.RETRY, {'request_id': request_id, 'attempt': attempt, 'max_retries': max_retries, 'reason': reason})

    async def emit_error(self, message: str) -> None:
        await self._emit(EventType.ERROR, {'error': message})

    async def emit_stopped(self, request_id: str, content: str = '会话已终止') -> None:
        await self._emit(EventType.STOPPED, {'request_id': request_id, 'content': content})

    async def emit_done(self, token_usage: dict | None = None) -> None:
        data: dict[str, Any] = {}
        if token_usage:
            data['token_usage'] = token_usage
        await self._emit(EventType.DONE, data)
        await self.close()

    # ── SSE consumer ──

    async def iter_sse(self) -> AsyncGenerator[str, None]:
        while True:
            try:
                event = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=self._config.interrupt_check_interval,
                )
            except asyncio.TimeoutError:
                yield ': ping\n\n'
                continue
            if event is None:
                yield 'data: [DONE]\n\n'
                break
            yield self._format_sse(event)

    # ── Internals ──

    async def _emit(self, event_type: EventType, data: dict) -> None:
        if self._closed:
            return
        event = SSEEvent(
            event_type=event_type,
            data=data,
            trace_id=self._config.trace_id,
            run_id=self._config.run_id,
        )
        await self._queue.put(event)

    async def close(self) -> None:
        if not self._closed:
            self._closed = True
            await self._queue.put(None)

    def _format_sse(self, event: SSEEvent) -> str:
        payload: dict[str, Any] = {
            'request_id': self._config.request_id,
            'type': event.event_type.value,
            'trace_id': event.trace_id,
            'run_id': event.run_id,
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }
        payload.update(event.data)
        return f'data: {json.dumps(payload, ensure_ascii=False)}\n\n'
