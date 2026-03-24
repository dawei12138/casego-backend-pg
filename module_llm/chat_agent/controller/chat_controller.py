# -*- coding: utf-8 -*-
"""
对话控制器 - SSE流式对话接口 + 测试页面（基于 deepagents）
"""
import asyncio
import json
import math
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import AsyncSessionLocal
from config.get_db import get_db
from exceptions.exception import ServiceException
from module_admin.system.entity.vo.user_vo import CurrentUserModel
from module_admin.system.service.login_service import LoginService
from module_llm.chat_agent.controller.stream_helpers import (
    RETRYABLE_EXCEPTIONS,
    _sse,
    check_interrupts,
    create_agent_and_model,
    make_sse_response,
    process_stream_chunks,
    rollback_checkpoint_state,
)
from module_llm.chat_agent.deepagent_factory import get_checkpointer
from module_llm.chat_agent.entity.vo.chat_vo import (
    AnswerRequest,
    AttachmentMeta,
    ChatHistoryResponse,
    ChatRequest,
    ConversationTurnModel,
    TurnEventModel,
)
from module_llm.chat_agent.mcp.loader import (
    build_connections_from_db_configs,
    mcp_tools_context,
)
from module_llm.chat_agent.service.attachment_service import AttachmentService
from module_llm.chat_mcp_config.dao.mcpconfig_dao import McpconfigDao
from module_llm.chat_thread.dao.thread_dao import ThreadDao
from module_llm.chat_thread.entity.vo.thread_vo import ThreadModel
from utils.log_util import logger
from utils.response_util import ResponseUtil

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command

chatController = APIRouter(prefix='/chat/agent')

# thread_id -> cancel_event. stop endpoint sets the event.
_cancel_events: dict[str, asyncio.Event] = {}
# thread_id -> active background run (single active run per thread)
_stream_runs: dict[str, "_StreamRun"] = {}
_stream_runs_lock = asyncio.Lock()

_STREAM_END = object()
_STREAM_QUEUE_MAXSIZE = 256
_STREAM_BACKLOG_MAXSIZE = 2000
_SSE_HEARTBEAT_SECONDS = 15


@dataclass(slots=True)
class _StreamRun:
    thread_id: str
    request_id: str
    mode: str  # "completions" | "answer"
    request_signature: str
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    subscribers: set[asyncio.Queue] = field(default_factory=set)
    backlog: deque[str] = field(default_factory=lambda: deque(maxlen=_STREAM_BACKLOG_MAXSIZE))
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    finished: bool = False
    task: asyncio.Task | None = None


def _queue_put_latest(queue: asyncio.Queue, item: Any):
    """Drop oldest item when queue is full so latest events still get delivered."""
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


async def _publish_run_event(run: _StreamRun, sse_line: str):
    async with run.lock:
        run.backlog.append(sse_line)
        subscribers = list(run.subscribers)

    for queue in subscribers:
        _queue_put_latest(queue, sse_line)


async def _finish_run(run: _StreamRun):
    async with run.lock:
        if run.finished:
            return
        run.finished = True
        subscribers = list(run.subscribers)

    for queue in subscribers:
        _queue_put_latest(queue, _STREAM_END)

    async with _stream_runs_lock:
        current = _stream_runs.get(run.thread_id)
        if current is run:
            _stream_runs.pop(run.thread_id, None)
            _cancel_events.pop(run.thread_id, None)


async def _subscribe_run(run: _StreamRun) -> asyncio.Queue:
    queue: asyncio.Queue = asyncio.Queue(maxsize=_STREAM_QUEUE_MAXSIZE)
    async with run.lock:
        run.subscribers.add(queue)
        cached_lines = list(run.backlog)
        finished = run.finished

    for line in cached_lines:
        _queue_put_latest(queue, line)
    if finished:
        _queue_put_latest(queue, _STREAM_END)
    return queue


async def _unsubscribe_run(run: _StreamRun, queue: asyncio.Queue):
    async with run.lock:
        run.subscribers.discard(queue)


async def _stream_events_from_run(run: _StreamRun):
    queue = await _subscribe_run(run)
    try:
        while True:
            try:
                item = await asyncio.wait_for(queue.get(), timeout=_SSE_HEARTBEAT_SECONDS)
            except asyncio.TimeoutError:
                # SSE comment heartbeat, helps keep proxies from closing idle streams.
                yield ": ping\n\n"
                continue

            if item is _STREAM_END:
                break
            yield item
    except asyncio.CancelledError:
        logger.info(f'[SSE] client disconnected, run continues in background: thread_id={run.thread_id}, mode={run.mode}')
        raise
    finally:
        await _unsubscribe_run(run, queue)


def _build_request_signature(payload: dict) -> str:
    """Stable signature used to detect reconnect of the same request."""
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _assert_reconnectable(run: _StreamRun, mode: str, request_signature: str):
    if run.mode != mode:
        raise ServiceException(message=f'会话当前正在执行 {run.mode} 任务，请稍后重试或先手动终止')
    if run.request_signature != request_signature:
        raise ServiceException(message='会话已有进行中的任务，请等待完成后再发起新的请求')


async def _get_active_run(thread_id: str) -> _StreamRun | None:
    async with _stream_runs_lock:
        run = _stream_runs.get(thread_id)
        if run is not None and run.finished:
            _stream_runs.pop(thread_id, None)
            _cancel_events.pop(thread_id, None)
            return None
        return run


async def _run_chat_completion(
    run: _StreamRun,
    request: ChatRequest,
    input_data: dict,
    mcp_connections: dict,
    current_user: CurrentUserModel,
):
    max_retries = 2
    attempt = 0
    agent = None
    pre_request_messages = None
    config = {"configurable": {"thread_id": request.thread_id}}

    try:
        async with AsyncSessionLocal() as run_db:
            async with mcp_tools_context(servers=mcp_connections) as mcp_tools:
                _, agent = await create_agent_and_model(
                    run_db,
                    request.provider_key,
                    request.model,
                    request.enable_thinking,
                    request.enable_web_search,
                    current_user.user.user_id,
                    request.thread_id,
                    mcp_tools=mcp_tools if mcp_tools else None,
                    skill_ids=request.skill_ids,
                )

                pre_request_messages = []
                try:
                    pre_state = await agent.aget_state(config)
                    if pre_state and pre_state.values:
                        pre_request_messages = list(pre_state.values.get('messages', []))
                except Exception as state_err:
                    logger.warning(f'[SSE] 获取请求前状态失败: {state_err}')

                while True:
                    try:
                        async for sse_line in process_stream_chunks(
                            agent,
                            input_data,
                            config,
                            request_id=run.request_id,
                            cancel_event=run.cancel_event,
                            enable_thinking=request.enable_thinking,
                            user_id=current_user.user.user_id,
                            thread_id=request.thread_id,
                            log_prefix='[SSE]',
                            debug_chunks=10,
                        ):
                            await _publish_run_event(run, sse_line)
                        break
                    except RETRYABLE_EXCEPTIONS as retry_err:
                        attempt += 1
                        await rollback_checkpoint_state(agent, config, pre_request_messages, '[SSE]')
                        if attempt > max_retries:
                            raise
                        logger.warning(
                            f'[SSE] 第 {attempt}/{max_retries} 次重试 '
                            f'({type(retry_err).__name__}): thread_id={request.thread_id}'
                        )
                        await _publish_run_event(run, _sse({
                            'request_id': run.request_id,
                            'type': 'retry',
                            'attempt': attempt,
                            'max_retries': max_retries,
                            'reason': type(retry_err).__name__,
                        }))
                        await asyncio.sleep(min(2 ** attempt, 8))

                async for sse_line in check_interrupts(agent, config, run.request_id, '[SSE]'):
                    await _publish_run_event(run, sse_line)

        await _publish_run_event(run, 'data: [DONE]\n\n')
    except RETRYABLE_EXCEPTIONS:
        logger.error(f'对话超时（已重试 {max_retries} 次）: thread_id={request.thread_id}')
        await _publish_run_event(run, _sse({
            'request_id': run.request_id,
            'type': 'error',
            'error': f'模型响应超时，请稍后重试（已自动重试 {max_retries} 次）',
        }))
        await _publish_run_event(run, 'data: [DONE]\n\n')
    except Exception as e:
        logger.exception(f'对话异常: {e}')
        if agent is not None and pre_request_messages is not None:
            await rollback_checkpoint_state(agent, config, pre_request_messages, '[SSE]')
        await _publish_run_event(run, _sse({'request_id': run.request_id, 'type': 'error', 'error': str(e)}))
        await _publish_run_event(run, 'data: [DONE]\n\n')
    finally:
        await _finish_run(run)


async def _run_answer_completion(
    run: _StreamRun,
    request: AnswerRequest,
    mcp_connections: dict,
    current_user: CurrentUserModel,
):
    config = {"configurable": {"thread_id": request.thread_id}}
    try:
        async with AsyncSessionLocal() as run_db:
            async with mcp_tools_context(servers=mcp_connections) as mcp_tools:
                _, agent = await create_agent_and_model(
                    run_db,
                    request.provider_key,
                    request.model,
                    request.enable_thinking,
                    request.enable_web_search,
                    current_user.user.user_id,
                    request.thread_id,
                    log_prefix='[Answer] ',
                    mcp_tools=mcp_tools if mcp_tools else None,
                    skill_ids=request.skill_ids,
                )

                async for sse_line in process_stream_chunks(
                    agent,
                    Command(resume=request.answers),
                    config,
                    request_id=run.request_id,
                    cancel_event=run.cancel_event,
                    enable_thinking=request.enable_thinking,
                    user_id=current_user.user.user_id,
                    thread_id=request.thread_id,
                    log_prefix='[Answer SSE]',
                ):
                    await _publish_run_event(run, sse_line)

                async for sse_line in check_interrupts(agent, config, run.request_id, '[Answer SSE]'):
                    await _publish_run_event(run, sse_line)

        await _publish_run_event(run, 'data: [DONE]\n\n')
    except Exception as e:
        logger.exception(f'[Answer] 对话恢复异常: {e}')
        await _publish_run_event(run, _sse({'request_id': run.request_id, 'type': 'error', 'error': str(e)}))
        await _publish_run_event(run, 'data: [DONE]\n\n')
    finally:
        await _finish_run(run)


@chatController.post('/completions', summary='流式对话', description='SSE流式对话接口，使用 deepagents 架构')
async def chat_completions(
        request: ChatRequest,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    流式对话接口（基于 deepagents）。

    关键行为：
    - 任务在后台协程中执行，不再绑定单个前端 SSE 连接生命周期
    - 前端断流/刷新后可重连，不会自动中断任务
    - 只有调用 /stop 才会触发真正取消
    """
    request_signature = _build_request_signature(
        request.model_dump(mode='json', by_alias=True, exclude_none=False)
    )

    # Reconnect to the same in-flight request if it already exists.
    active_run = await _get_active_run(request.thread_id)
    if active_run is not None:
        _assert_reconnectable(active_run, 'completions', request_signature)
        logger.info(f'[SSE] 检测到会话重连: thread_id={request.thread_id}, mode=completions')
        return make_sse_response(_stream_events_from_run(active_run))

    # Ensure thread exists.
    existing_thread = await ThreadDao.get_thread_detail_by_id(query_db, thread_id=request.thread_id)
    if not existing_thread:
        new_thread = ThreadModel(
            thread_id=request.thread_id,
            user_id=current_user.user.user_id,
            title=request.message,
            create_time=datetime.now(),
            create_by=current_user.user.user_name,
            update_time=datetime.now(),
        )
        await ThreadDao.add_thread_dao(query_db, new_thread)
        await query_db.commit()
        logger.info(f'新增聊天线程: thread_id={request.thread_id}')

    # Load MCP configs with request-scoped DB session.
    mcp_connections = {}
    if request.mcp_config_ids:
        db_configs = await McpconfigDao.get_mcpconfig_by_ids(query_db, request.mcp_config_ids)
        mcp_connections = build_connections_from_db_configs(db_configs)
        logger.info(f'加载 {len(mcp_connections)} 个MCP服务器配置: {list(mcp_connections.keys())}')

    # Build message input.
    if request.attachments:
        content_blocks, att_meta = await AttachmentService.build_message_content(
            message=request.message,
            attachments=request.attachments,
            user_id=current_user.user.user_id,
            thread_id=request.thread_id,
        )
        input_data = {
            'messages': [
                HumanMessage(content=content_blocks, additional_kwargs={'attachments': att_meta})
            ]
        }
    else:
        input_data = {'messages': [{'role': 'user', 'content': request.message}]}

    # Register the background run (double-check for concurrent requests).
    async with _stream_runs_lock:
        current_run = _stream_runs.get(request.thread_id)
        if current_run is not None and not current_run.finished:
            run = current_run
            created = False
        else:
            run = _StreamRun(
                thread_id=request.thread_id,
                request_id=str(uuid4()),
                mode='completions',
                request_signature=request_signature,
            )
            _stream_runs[request.thread_id] = run
            _cancel_events[request.thread_id] = run.cancel_event
            created = True

    if not created:
        _assert_reconnectable(run, 'completions', request_signature)
        logger.info(f'[SSE] 并发场景复用已存在运行: thread_id={request.thread_id}, mode=completions')
        return make_sse_response(_stream_events_from_run(run))

    run.task = asyncio.create_task(
        _run_chat_completion(run, request, input_data, mcp_connections, current_user),
        name=f'chat-completions-{request.thread_id}',
    )
    logger.info(f'[SSE] 后台任务已启动: thread_id={request.thread_id}, request_id={run.request_id}')
    return make_sse_response(_stream_events_from_run(run))


@chatController.post('/stop', summary='终止会话', description='终止指定会话的流式输出')
async def stop_chat(
        thread_id: str = Query(..., description='要终止的会话线程ID'),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """终止正在进行的流式对话"""
    cancel_event = _cancel_events.get(thread_id)
    if cancel_event is None:
        return ResponseUtil.failure(msg=f'会话不在运行中: {thread_id}')
    cancel_event.set()
    logger.info(f'终止会话请求: thread_id={thread_id}, user={current_user.user.user_name}')
    return ResponseUtil.success(msg='会话终止请求已发送')


@chatController.get('/stream/reconnect', summary='重连流式会话', description='页面刷新后，重新订阅正在运行的会话流')
async def reconnect_chat_stream(
        thread_id: str = Query(..., description='会话线程ID'),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """重连一个正在运行的流式会话（不会重新触发模型推理）。"""
    run = await _get_active_run(thread_id)
    if run is None:
        return ResponseUtil.failure(msg=f'会话不在运行中: {thread_id}')
    logger.info(f'会话流重连: thread_id={thread_id}, user={current_user.user.user_name}, mode={run.mode}')
    return make_sse_response(_stream_events_from_run(run))


@chatController.post('/answer', summary='回答问题', description='响应 ask_user_question 工具的提问，恢复被中断的对话')
async def answer_question(
        request: AnswerRequest,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    回答 ask_user_question 工具提问，恢复被中断对话。

    行为与 /completions 一致：后台运行 + 可重连流。
    """
    request_signature = _build_request_signature(
        request.model_dump(mode='json', by_alias=True, exclude_none=False)
    )

    active_run = await _get_active_run(request.thread_id)
    if active_run is not None:
        _assert_reconnectable(active_run, 'answer', request_signature)
        logger.info(f'[Answer SSE] 检测到会话重连: thread_id={request.thread_id}, mode=answer')
        return make_sse_response(_stream_events_from_run(active_run))

    mcp_connections = {}
    if request.mcp_config_ids:
        db_configs = await McpconfigDao.get_mcpconfig_by_ids(query_db, request.mcp_config_ids)
        mcp_connections = build_connections_from_db_configs(db_configs)
        logger.info(f'[Answer] 加载 {len(mcp_connections)} 个MCP服务器配置: {list(mcp_connections.keys())}')

    async with _stream_runs_lock:
        current_run = _stream_runs.get(request.thread_id)
        if current_run is not None and not current_run.finished:
            run = current_run
            created = False
        else:
            run = _StreamRun(
                thread_id=request.thread_id,
                request_id=str(uuid4()),
                mode='answer',
                request_signature=request_signature,
            )
            _stream_runs[request.thread_id] = run
            _cancel_events[request.thread_id] = run.cancel_event
            created = True

    if not created:
        _assert_reconnectable(run, 'answer', request_signature)
        logger.info(f'[Answer SSE] 并发场景复用已存在运行: thread_id={request.thread_id}, mode=answer')
        return make_sse_response(_stream_events_from_run(run))

    run.task = asyncio.create_task(
        _run_answer_completion(run, request, mcp_connections, current_user),
        name=f'chat-answer-{request.thread_id}',
    )
    logger.info(f'[Answer SSE] 后台任务已启动: thread_id={request.thread_id}, request_id={run.request_id}')
    return make_sse_response(_stream_events_from_run(run))

def _get_msg_timestamp(msg, ts_map: dict[str, str] | None = None) -> Optional[str]:
    """
    获取消息时间戳（ISO-8601 UTC）。

    优先从 ts_map（checkpoint 历史构建的 message_id→created_at 映射）中查找，
    其次尝试从消息自身的 response_metadata / additional_kwargs 中提取。
    """
    msg_id = getattr(msg, 'id', None)
    if ts_map and msg_id and msg_id in ts_map:
        return ts_map[msg_id]

    # response_metadata 里可能有 created_at / timestamp
    meta = getattr(msg, 'response_metadata', {}) or {}
    ts = meta.get('created_at') or meta.get('timestamp')
    if ts:
        return str(ts)
    # additional_kwargs 里可能有
    ak = getattr(msg, 'additional_kwargs', {}) or {}
    ts = ak.get('created_at') or ak.get('timestamp')
    if ts:
        return str(ts)
    return None


def _group_messages_to_turns(
    messages: list,
    ts_map: dict[str, str] | None = None,
) -> list[ConversationTurnModel]:
    """
    将 LangChain 消息列表按轮次分组，生成与 SSE 事件格式一致的 turn 列表。

    分组规则：每个 HumanMessage 开始一个新 turn，后续 AIMessage/ToolMessage 归入该 turn。
    """
    turns: list[ConversationTurnModel] = []
    current_turn = None
    # 缓存 AIMessage 的 tool_calls，供后续 ToolMessage 匹配 args
    pending_tool_calls: dict[str, dict] = {}  # call_id -> {name, args}

    for msg in messages:
        if isinstance(msg, SystemMessage):
            continue

        if isinstance(msg, HumanMessage):
            # 新一轮对话 —— 解析纯文本或多模态消息
            additional_kwargs = getattr(msg, 'additional_kwargs', {})
            turn_attachments = None

            if isinstance(msg.content, str):
                user_text = msg.content
            elif isinstance(msg.content, list):
                # 多模态消息：提取用户文本，跳过注入的文件内容块
                text_parts = []
                for block in msg.content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        text_val = block.get("text", "")
                        if not text_val.startswith("--- Content of "):
                            text_parts.append(text_val)
                user_text = "\n".join(text_parts) if text_parts else ""
            else:
                user_text = str(msg.content)

            # 从 additional_kwargs 提取附件元数据
            raw_attachments = additional_kwargs.get("attachments")
            if raw_attachments and isinstance(raw_attachments, list):
                try:
                    turn_attachments = [AttachmentMeta(**a) for a in raw_attachments]
                except Exception:
                    turn_attachments = None

            current_turn = ConversationTurnModel(
                request_id=getattr(msg, 'id', None) or str(uuid4()),
                user_message=user_text,
                attachments=turn_attachments,
                events=[],
                timestamp=_get_msg_timestamp(msg, ts_map),
            )
            turns.append(current_turn)
            pending_tool_calls = {}
            continue

        if current_turn is None:
            # 没有 HumanMessage 开头的孤立消息，跳过
            continue

        if isinstance(msg, AIMessage):
            additional_kwargs = getattr(msg, 'additional_kwargs', {})
            msg_ts = _get_msg_timestamp(msg, ts_map)

            # 1. 提取思考内容
            reasoning = (
                additional_kwargs.get("reasoning_content")
                or additional_kwargs.get("thinking_content")
                or additional_kwargs.get("thought")
            )
            if reasoning:
                current_turn.events.append(TurnEventModel(type="thinking", content=reasoning, timestamp=msg_ts))

            # 2. 处理 content
            if isinstance(msg.content, list):
                # Anthropic 格式：content 是 block 列表
                for block in msg.content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "thinking" and block.get("thinking"):
                        current_turn.events.append(TurnEventModel(type="thinking", content=block["thinking"], timestamp=msg_ts))
                    elif block.get("type") == "text" and block.get("text"):
                        current_turn.events.append(TurnEventModel(type="content", content=block["text"], timestamp=msg_ts))
            elif msg.content:
                current_turn.events.append(TurnEventModel(type="content", content=msg.content, timestamp=msg_ts))

            # 3. 处理 tool_calls
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    call_id = tc.get('id', '')
                    tc_name = tc.get('name', '')
                    tc_args = tc.get('args', {})
                    # 缓存以便后续 ToolMessage 匹配
                    if call_id:
                        pending_tool_calls[call_id] = {"name": tc_name, "args": tc_args}
                    current_turn.events.append(TurnEventModel(
                        type="tool_call",
                        tool=tc_name,
                        call_id=call_id,
                        args=tc_args,
                        timestamp=msg_ts,
                    ))

        elif isinstance(msg, ToolMessage):
            tool_call_id = getattr(msg, 'tool_call_id', '')
            tool_name = getattr(msg, 'name', '')
            msg_ts = _get_msg_timestamp(msg, ts_map)

            # 从缓存中匹配 args
            tc_info = pending_tool_calls.pop(tool_call_id, None)
            tool_args = tc_info["args"] if tc_info else {}

            current_turn.events.append(TurnEventModel(
                type="tool_result",
                tool=tool_name,
                call_id=tool_call_id,
                args=tool_args,
                result=msg.content,
                timestamp=msg_ts,
            ))

    return turns


def _create_minimal_graph():
    """创建最小化的图（仅用于读取历史）"""
    def noop(state: MessagesState):
        return state

    builder = StateGraph(MessagesState)
    builder.add_node("noop", noop)
    builder.add_node("tools", noop)  # 匹配实际 agent 图的节点名，避免 checkpoint 恢复时警告
    builder.add_edge(START, "noop")
    builder.add_edge("noop", END)
    return builder


@chatController.get('/history', summary='获取聊天历史', description='按轮次分页获取指定会话的历史聊天记录')
async def get_chat_history(
        thread_id: str = Query(..., description='会话线程ID'),
        page: int = Query(default=1, ge=1, description='页码，从1开始'),
        page_size: int = Query(default=20, ge=1, le=100, description='每页轮次数量'),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    获取聊天历史记录（按轮次分页）

    - 每轮包含用户消息 + AI 响应事件序列（与 SSE 事件格式一致）
    - 按时间倒序返回，最新的轮次在前
    - 支持懒加载，前端可以滚动加载更多历史轮次
    """
    try:
        checkpointer = await get_checkpointer()

        # 使用 checkpointer 编译最小图来读取状态
        builder = _create_minimal_graph()
        graph = builder.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": thread_id}}

        # 获取当前状态
        state = await graph.aget_state(config)

        empty_response = ChatHistoryResponse(
            thread_id=thread_id,
            total=0,
            page=page,
            page_size=page_size,
            pages=0,
            has_more=False,
            turns=[],
        )

        if not state or not state.values:
            return ResponseUtil.success(data=empty_response.model_dump(by_alias=True))

        all_messages = state.values.get("messages", [])
        if not all_messages:
            return ResponseUtil.success(data=empty_response.model_dump(by_alias=True))

        # 遍历 checkpoint 历史，构建 message_id → created_at 映射
        # 每个 snapshot 记录了当时累积的所有消息，通过对比前后差异找到「新增消息」对应的时间戳
        ts_map: dict[str, str] = {}
        prev_ids: set[str] = set()
        history_snapshots = []
        async for snapshot in graph.aget_state_history(config):
            history_snapshots.append(snapshot)

        # aget_state_history 按时间倒序返回，反转为正序以便逐步对比
        for snapshot in reversed(history_snapshots):
            snap_ts = snapshot.created_at
            if not snap_ts:
                continue
            snap_msgs = (snapshot.values or {}).get("messages", [])
            cur_ids = set()
            for m in snap_msgs:
                mid = getattr(m, 'id', None)
                if mid:
                    cur_ids.add(mid)
                    if mid not in prev_ids:
                        ts_map[mid] = snap_ts
            prev_ids = cur_ids

        # 按轮次分组
        all_turns = _group_messages_to_turns(all_messages, ts_map=ts_map)
        total = len(all_turns)

        if total == 0:
            return ResponseUtil.success(data=empty_response.model_dump(by_alias=True))

        # 计算分页（倒序，最新的在前）
        pages = math.ceil(total / page_size)
        start_idx = max(0, total - page * page_size)
        end_idx = total - (page - 1) * page_size

        # 获取分页数据并倒序（最新的轮次在前）
        page_turns = all_turns[start_idx:end_idx]
        page_turns = list(reversed(page_turns))

        response = ChatHistoryResponse(
            thread_id=thread_id,
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
            has_more=page < pages,
            turns=page_turns,
        )

        return ResponseUtil.success(data=response.model_dump(by_alias=True))

    except Exception as e:
        logger.error(f'获取聊天历史异常: {e}')
        raise ServiceException(message=f'获取聊天历史失败: {str(e)}')
