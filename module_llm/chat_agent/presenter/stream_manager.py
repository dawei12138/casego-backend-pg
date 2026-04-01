# -*- coding: utf-8 -*-
"""Stream lifecycle management: start, stop, reconnect, pub/sub, retry."""
import asyncio
import json
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Callable, Coroutine
from uuid import uuid4

from fastapi.responses import StreamingResponse

from utils.log_util import logger

from .presenter import Presenter, PresenterConfig

MAX_RETRIES = 2
RETRY_BASE_DELAY = 2

_STREAM_END = object()
_STREAM_QUEUE_MAXSIZE = 256
_STREAM_BACKLOG_MAXSIZE = 2000
_SSE_HEARTBEAT_SECONDS = 15

SSE_HEADERS = {
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no',
    'Content-Encoding': 'identity',
}


def make_sse_response(generator) -> StreamingResponse:
    return StreamingResponse(generator, media_type='text/event-stream', headers=SSE_HEADERS)


@dataclass(slots=True)
class StreamRun:
    run_id: str
    thread_id: str
    request_id: str
    mode: str
    request_signature: str
    presenter: Presenter
    task: asyncio.Task | None = None
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    created_at: float = field(default_factory=time.time)
    subscribers: set[asyncio.Queue] = field(default_factory=set)
    backlog: deque[str] = field(default_factory=lambda: deque(maxlen=_STREAM_BACKLOG_MAXSIZE))
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    finished: bool = False


class StreamManager:
    """Manages all active SSE stream runs."""

    def __init__(self):
        self._runs: dict[str, StreamRun] = {}
        self._thread_runs: dict[str, StreamRun] = {}
        self._lock = asyncio.Lock()

    # ── Public API ──

    async def start_run(
        self,
        thread_id: str,
        user_id: str,
        request_id: str,
        *,
        mode: str = 'completions',
        request_signature: str = '',
        execute_fn: Callable[['StreamRun'], Coroutine] | None = None,
    ) -> StreamRun:
        """Create a StreamRun and launch background execution via execute_fn.

        execute_fn receives the StreamRun and is responsible for:
        - Creating the agent (inside mcp_tools_context)
        - Streaming chunks and publishing via self.publish()
        - Sending 'data: [DONE]\\n\\n' at the end
        - Error handling
        """
        presenter_config = PresenterConfig(
            thread_id=thread_id,
            user_id=user_id,
            request_id=request_id,
        )
        presenter = Presenter(presenter_config)

        run = StreamRun(
            run_id=presenter.run_id,
            thread_id=thread_id,
            request_id=request_id,
            mode=mode,
            request_signature=request_signature,
            presenter=presenter,
        )

        task = asyncio.create_task(
            self._execute_wrapper(run, execute_fn),
            name=f'stream-{mode}-{thread_id}',
        )
        run.task = task

        async with self._lock:
            self._runs[run.run_id] = run
            self._thread_runs[thread_id] = run

        return run

    async def stop_run(self, run_id: str) -> bool:
        run = self._runs.get(run_id)
        if run is None:
            return False
        run.cancel_event.set()
        if run.task and not run.task.done():
            run.task.cancel()
        return True

    async def stop_by_thread(self, thread_id: str) -> bool:
        run = self._thread_runs.get(thread_id)
        if run is None:
            return False
        return await self.stop_run(run.run_id)

    async def reconnect(self, run_id: str) -> Presenter | None:
        run = self._runs.get(run_id)
        if run and not run.finished:
            return run.presenter
        return None

    async def get_active_run_by_thread(self, thread_id: str) -> StreamRun | None:
        async with self._lock:
            run = self._thread_runs.get(thread_id)
            if run is not None and run.finished:
                self._thread_runs.pop(thread_id, None)
                self._runs.pop(run.run_id, None)
                return None
            return run

    # ── Pub/sub ──

    async def publish(self, run: StreamRun, sse_line: str):
        async with run.lock:
            run.backlog.append(sse_line)
            subscribers = list(run.subscribers)
        for queue in subscribers:
            self._queue_put_latest(queue, sse_line)

    async def subscribe(self, run: StreamRun) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue(maxsize=_STREAM_QUEUE_MAXSIZE)
        async with run.lock:
            run.subscribers.add(queue)
            cached_lines = list(run.backlog)
            finished = run.finished
        for line in cached_lines:
            self._queue_put_latest(queue, line)
        if finished:
            self._queue_put_latest(queue, _STREAM_END)
        return queue

    async def unsubscribe(self, run: StreamRun, queue: asyncio.Queue) -> None:
        async with run.lock:
            run.subscribers.discard(queue)

    async def stream_events(self, run: StreamRun) -> AsyncGenerator[str, None]:
        queue = await self.subscribe(run)
        try:
            while True:
                try:
                    item = await asyncio.wait_for(queue.get(), timeout=_SSE_HEARTBEAT_SECONDS)
                except asyncio.TimeoutError:
                    yield ': ping\n\n'
                    continue
                if item is _STREAM_END:
                    break
                yield item
        except asyncio.CancelledError:
            logger.info(f'[SSE] client disconnected, run continues: thread_id={run.thread_id}')
            raise
        finally:
            await self.unsubscribe(run, queue)

    # ── Background execution ──

    async def _execute_wrapper(self, run: StreamRun, execute_fn):
        try:
            if execute_fn:
                await execute_fn(run)
            else:
                await self.publish(run, 'data: [DONE]\n\n')
        except asyncio.CancelledError:
            stopped_line = self._format_sse_line(run.request_id, {'type': 'stopped', 'content': '会话已终止'})
            await self.publish(run, stopped_line)
            await self.publish(run, 'data: [DONE]\n\n')
        except Exception as e:
            logger.exception(f'Stream error: {e}')
            error_line = self._format_sse_line(run.request_id, {'type': 'error', 'error': str(e)})
            await self.publish(run, error_line)
            await self.publish(run, 'data: [DONE]\n\n')
        finally:
            await self._finish_run(run)

    async def _finish_run(self, run: StreamRun):
        async with run.lock:
            if run.finished:
                return
            run.finished = True
            subscribers = list(run.subscribers)
        for queue in subscribers:
            self._queue_put_latest(queue, _STREAM_END)
        async with self._lock:
            current = self._thread_runs.get(run.thread_id)
            if current is run:
                self._thread_runs.pop(run.thread_id, None)
            self._runs.pop(run.run_id, None)

    # ── Helpers ──

    @staticmethod
    def _queue_put_latest(queue: asyncio.Queue, item: Any):
        try:
            queue.put_nowait(item)
        except asyncio.QueueFull:
            try:
                queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            try:
                queue.put_nowait(item)
            except asyncio.QueueFull:
                pass

    @staticmethod
    def _format_sse_line(request_id: str, payload: dict) -> str:
        payload['request_id'] = request_id
        payload.setdefault('timestamp', datetime.now(timezone.utc).isoformat())
        return f'data: {json.dumps(payload, ensure_ascii=False)}\n\n'
