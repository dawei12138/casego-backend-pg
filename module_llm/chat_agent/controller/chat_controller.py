# -*- coding: utf-8 -*-
"""
对话控制器 - SSE 流式对话接口（基于 Presenter + StreamManager）
"""
import asyncio
import json
import math
from datetime import datetime
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
from module_llm.chat_agent.presenter.stream_manager import (
    StreamManager,
    StreamRun,
    make_sse_response,
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

_stream_manager = StreamManager()

_history_graph: Any | None = None
_history_graph_lock: asyncio.Lock | None = None


def _build_request_signature(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _assert_reconnectable(run: StreamRun, mode: str, request_signature: str):
    if run.mode != mode:
        raise ServiceException(message=f'会话当前正在执行 {run.mode} 任务，请稍后重试或先手动终止')
    if run.request_signature != request_signature:
        raise ServiceException(message='会话已有进行中的任务，请等待完成后再发起新的请求')


# ── Endpoints ──


@chatController.post('/completions', summary='流式对话', description='SSE流式对话接口，使用 deepagents 架构')
async def chat_completions(
        request: ChatRequest,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """流式对话接口 — 后台运行 + 可重连。"""
    request_signature = _build_request_signature(
        request.model_dump(mode='json', by_alias=True, exclude_none=False)
    )

    active_run = await _stream_manager.get_active_run_by_thread(request.thread_id)
    if active_run is not None:
        _assert_reconnectable(active_run, 'completions', request_signature)
        logger.info(f'[SSE] 检测到会话重连: thread_id={request.thread_id}')
        return make_sse_response(_stream_manager.stream_events(active_run))

    # Ensure thread exists
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

    # Load MCP configs
    mcp_connections = {}
    if request.mcp_config_ids:
        db_configs = await McpconfigDao.get_mcpconfig_by_ids(query_db, request.mcp_config_ids)
        mcp_connections = build_connections_from_db_configs(db_configs)
        logger.info(f'加载 {len(mcp_connections)} 个MCP服务器配置: {list(mcp_connections.keys())}')

    # Build message input
    if request.attachments:
        content_blocks, att_meta = await AttachmentService.build_message_content(
            message=request.message,
            attachments=request.attachments,
            user_id=current_user.user.user_id,
            thread_id=request.thread_id,
        )
        input_data = {
            'messages': [HumanMessage(content=content_blocks, additional_kwargs={'attachments': att_meta})]
        }
    else:
        input_data = {'messages': [{'role': 'user', 'content': request.message}]}

    # Capture variables for the background closure
    _request = request
    _input_data = input_data
    _mcp_connections = mcp_connections
    _current_user = current_user

    async def execute_fn(run: StreamRun):
        max_retries = 2
        attempt = 0
        agent = None
        pre_request_messages = None
        config = {'configurable': {'thread_id': _request.thread_id}}

        try:
            async with AsyncSessionLocal() as run_db:
                async with mcp_tools_context(servers=_mcp_connections) as mcp_tools:
                    _, agent = await create_agent_and_model(
                        run_db,
                        _request.provider_key,
                        _request.model,
                        _request.enable_thinking,
                        _request.enable_web_search,
                        _current_user.user.user_id,
                        _request.thread_id,
                        mcp_tools=mcp_tools if mcp_tools else None,
                        skill_ids=_request.skill_ids,
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
                                _input_data,
                                config,
                                request_id=run.request_id,
                                cancel_event=run.cancel_event,
                                enable_thinking=_request.enable_thinking,
                                user_id=_current_user.user.user_id,
                                thread_id=_request.thread_id,
                                log_prefix='[SSE]',
                                debug_chunks=10,
                            ):
                                await _stream_manager.publish(run, sse_line)
                            break
                        except RETRYABLE_EXCEPTIONS as retry_err:
                            attempt += 1
                            await rollback_checkpoint_state(agent, config, pre_request_messages, '[SSE]')
                            if attempt > max_retries:
                                raise
                            logger.warning(
                                f'[SSE] 第 {attempt}/{max_retries} 次重试 '
                                f'({type(retry_err).__name__}): thread_id={_request.thread_id}'
                            )
                            await _stream_manager.publish(run, _sse({
                                'request_id': run.request_id,
                                'type': 'retry',
                                'attempt': attempt,
                                'max_retries': max_retries,
                                'reason': type(retry_err).__name__,
                            }))
                            await asyncio.sleep(min(2 ** attempt, 8))

                    async for sse_line in check_interrupts(agent, config, run.request_id, '[SSE]'):
                        await _stream_manager.publish(run, sse_line)

            await _stream_manager.publish(run, 'data: [DONE]\n\n')
        except RETRYABLE_EXCEPTIONS:
            logger.error(f'对话超时（已重试 {max_retries} 次）: thread_id={_request.thread_id}')
            await _stream_manager.publish(run, _sse({
                'request_id': run.request_id,
                'type': 'error',
                'error': f'模型响应超时，请稍后重试（已自动重试 {max_retries} 次）',
            }))
            await _stream_manager.publish(run, 'data: [DONE]\n\n')
        except Exception as e:
            logger.exception(f'对话异常: {e}')
            if agent is not None and pre_request_messages is not None:
                await rollback_checkpoint_state(agent, config, pre_request_messages, '[SSE]')
            await _stream_manager.publish(run, _sse({'request_id': run.request_id, 'type': 'error', 'error': str(e)}))
            await _stream_manager.publish(run, 'data: [DONE]\n\n')

    run = await _stream_manager.start_run(
        thread_id=request.thread_id,
        user_id=str(current_user.user.user_id),
        request_id=str(uuid4()),
        mode='completions',
        request_signature=request_signature,
        execute_fn=execute_fn,
    )

    logger.info(f'[SSE] 后台任务已启动: thread_id={request.thread_id}, run_id={run.run_id}')
    return make_sse_response(_stream_manager.stream_events(run))


@chatController.post('/stop', summary='终止会话', description='终止指定会话的流式输出')
async def stop_chat(
        thread_id: str = Query(..., description='要终止的会话线程ID'),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    stopped = await _stream_manager.stop_by_thread(thread_id)
    if not stopped:
        return ResponseUtil.failure(msg=f'会话不在运行中: {thread_id}')
    logger.info(f'终止会话请求: thread_id={thread_id}, user={current_user.user.user_name}')
    return ResponseUtil.success(msg='会话终止请求已发送')


@chatController.get('/stream/reconnect', summary='重连流式会话', description='页面刷新后，重新订阅正在运行的会话流')
async def reconnect_chat_stream(
        thread_id: str = Query(..., description='会话线程ID'),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    run = await _stream_manager.get_active_run_by_thread(thread_id)
    if run is None:
        return ResponseUtil.failure(msg=f'会话不在运行中: {thread_id}')
    logger.info(f'会话流重连: thread_id={thread_id}, user={current_user.user.user_name}, mode={run.mode}')
    return make_sse_response(_stream_manager.stream_events(run))


@chatController.post('/answer', summary='回答问题', description='响应 ask_user_question 工具的提问，恢复被中断的对话')
async def answer_question(
        request: AnswerRequest,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    request_signature = _build_request_signature(
        request.model_dump(mode='json', by_alias=True, exclude_none=False)
    )

    active_run = await _stream_manager.get_active_run_by_thread(request.thread_id)
    if active_run is not None:
        _assert_reconnectable(active_run, 'answer', request_signature)
        logger.info(f'[Answer SSE] 检测到会话重连: thread_id={request.thread_id}')
        return make_sse_response(_stream_manager.stream_events(active_run))

    mcp_connections = {}
    if request.mcp_config_ids:
        db_configs = await McpconfigDao.get_mcpconfig_by_ids(query_db, request.mcp_config_ids)
        mcp_connections = build_connections_from_db_configs(db_configs)
        logger.info(f'[Answer] 加载 {len(mcp_connections)} 个MCP服务器配置: {list(mcp_connections.keys())}')

    _request = request
    _mcp_connections = mcp_connections
    _current_user = current_user

    async def execute_fn(run: StreamRun):
        config = {'configurable': {'thread_id': _request.thread_id}}
        try:
            async with AsyncSessionLocal() as run_db:
                async with mcp_tools_context(servers=_mcp_connections) as mcp_tools:
                    _, agent = await create_agent_and_model(
                        run_db,
                        _request.provider_key,
                        _request.model,
                        _request.enable_thinking,
                        _request.enable_web_search,
                        _current_user.user.user_id,
                        _request.thread_id,
                        log_prefix='[Answer] ',
                        mcp_tools=mcp_tools if mcp_tools else None,
                        skill_ids=_request.skill_ids,
                    )

                    async for sse_line in process_stream_chunks(
                        agent,
                        Command(resume=_request.answers),
                        config,
                        request_id=run.request_id,
                        cancel_event=run.cancel_event,
                        enable_thinking=_request.enable_thinking,
                        user_id=_current_user.user.user_id,
                        thread_id=_request.thread_id,
                        log_prefix='[Answer SSE]',
                    ):
                        await _stream_manager.publish(run, sse_line)

                    async for sse_line in check_interrupts(agent, config, run.request_id, '[Answer SSE]'):
                        await _stream_manager.publish(run, sse_line)

            await _stream_manager.publish(run, 'data: [DONE]\n\n')
        except Exception as e:
            logger.exception(f'[Answer] 对话恢复异常: {e}')
            await _stream_manager.publish(run, _sse({'request_id': run.request_id, 'type': 'error', 'error': str(e)}))
            await _stream_manager.publish(run, 'data: [DONE]\n\n')

    run = await _stream_manager.start_run(
        thread_id=request.thread_id,
        user_id=str(current_user.user.user_id),
        request_id=str(uuid4()),
        mode='answer',
        request_signature=request_signature,
        execute_fn=execute_fn,
    )

    logger.info(f'[Answer SSE] 后台任务已启动: thread_id={request.thread_id}, run_id={run.run_id}')
    return make_sse_response(_stream_manager.stream_events(run))


# ── History ──


def _get_msg_timestamp(msg, ts_map: dict[str, str] | None = None) -> Optional[str]:
    msg_id = getattr(msg, 'id', None)
    if ts_map and msg_id and msg_id in ts_map:
        return ts_map[msg_id]
    ts = _get_inline_msg_timestamp(msg)
    return ts if ts else None


def _get_inline_msg_timestamp(msg) -> Optional[str]:
    meta = getattr(msg, 'response_metadata', {}) or {}
    ts = meta.get('created_at') or meta.get('timestamp')
    if ts:
        return str(ts)
    ak = getattr(msg, 'additional_kwargs', {}) or {}
    ts = ak.get('created_at') or ak.get('timestamp')
    return str(ts) if ts else None


def _collect_turn_start_indices(messages: list) -> list[int]:
    return [idx for idx, msg in enumerate(messages) if isinstance(msg, HumanMessage)]


def _collect_missing_ts_message_ids(messages: list) -> set[str]:
    missing_ids: set[str] = set()
    for msg in messages:
        msg_id = getattr(msg, 'id', None)
        if not msg_id:
            continue
        if _get_inline_msg_timestamp(msg) is None:
            missing_ids.add(msg_id)
    return missing_ids


def _group_messages_to_turns(
    messages: list,
    ts_map: dict[str, str] | None = None,
) -> list[ConversationTurnModel]:
    turns: list[ConversationTurnModel] = []
    current_turn = None
    pending_tool_calls: dict[str, dict] = {}

    for msg in messages:
        if isinstance(msg, SystemMessage):
            continue

        if isinstance(msg, HumanMessage):
            additional_kwargs = getattr(msg, 'additional_kwargs', {})
            turn_attachments = None

            if isinstance(msg.content, str):
                user_text = msg.content
            elif isinstance(msg.content, list):
                text_parts = []
                for block in msg.content:
                    if not isinstance(block, dict):
                        continue
                    if block.get('type') == 'text':
                        text_val = block.get('text', '')
                        if not text_val.startswith('--- Content of '):
                            text_parts.append(text_val)
                user_text = '\n'.join(text_parts) if text_parts else ''
            else:
                user_text = str(msg.content)

            raw_attachments = additional_kwargs.get('attachments')
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
            continue

        if isinstance(msg, AIMessage):
            additional_kwargs = getattr(msg, 'additional_kwargs', {})
            msg_ts = _get_msg_timestamp(msg, ts_map)

            reasoning = (
                additional_kwargs.get('reasoning_content')
                or additional_kwargs.get('thinking_content')
                or additional_kwargs.get('thought')
            )
            if reasoning:
                current_turn.events.append(TurnEventModel(type='thinking', content=reasoning, timestamp=msg_ts))

            if isinstance(msg.content, list):
                for block in msg.content:
                    if not isinstance(block, dict):
                        continue
                    if block.get('type') == 'thinking' and block.get('thinking'):
                        current_turn.events.append(TurnEventModel(type='thinking', content=block['thinking'], timestamp=msg_ts))
                    elif block.get('type') == 'text' and block.get('text'):
                        current_turn.events.append(TurnEventModel(type='content', content=block['text'], timestamp=msg_ts))
            elif msg.content:
                current_turn.events.append(TurnEventModel(type='content', content=msg.content, timestamp=msg_ts))

            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    call_id = tc.get('id', '')
                    tc_name = tc.get('name', '')
                    tc_args = tc.get('args', {})
                    if call_id:
                        pending_tool_calls[call_id] = {'name': tc_name, 'args': tc_args}
                    current_turn.events.append(TurnEventModel(
                        type='tool_call', tool=tc_name, call_id=call_id, args=tc_args, timestamp=msg_ts,
                    ))

        elif isinstance(msg, ToolMessage):
            tool_call_id = getattr(msg, 'tool_call_id', '')
            tool_name = getattr(msg, 'name', '')
            msg_ts = _get_msg_timestamp(msg, ts_map)
            tc_info = pending_tool_calls.pop(tool_call_id, None)
            tool_args = tc_info['args'] if tc_info else {}
            current_turn.events.append(TurnEventModel(
                type='tool_result', tool=tool_name, call_id=tool_call_id,
                args=tool_args, result=msg.content, timestamp=msg_ts,
            ))

    return turns


def _create_minimal_graph():
    def noop(state: MessagesState):
        return state
    builder = StateGraph(MessagesState)
    builder.add_node('noop', noop)
    builder.add_node('tools', noop)
    builder.add_edge(START, 'noop')
    builder.add_edge('noop', END)
    return builder


async def _get_history_graph():
    global _history_graph, _history_graph_lock
    if _history_graph_lock is None:
        _history_graph_lock = asyncio.Lock()
    if _history_graph is not None:
        return _history_graph
    async with _history_graph_lock:
        if _history_graph is None:
            checkpointer = await get_checkpointer()
            builder = _create_minimal_graph()
            _history_graph = builder.compile(checkpointer=checkpointer)
    return _history_graph


async def _build_needed_timestamps(
    graph, config: dict, target_message_ids: set[str],
) -> dict[str, str]:
    unresolved_ids = set(target_message_ids)
    if not unresolved_ids:
        return {}
    ts_map: dict[str, str] = {}
    prev_msgs = None
    prev_ts = None
    async for snapshot in graph.aget_state_history(config):
        snap_ts = snapshot.created_at
        if not snap_ts:
            continue
        snap_msgs = (snapshot.values or {}).get('messages', []) or []
        if prev_msgs is not None and prev_ts:
            cur_len = len(snap_msgs)
            prev_len = len(prev_msgs)
            if cur_len <= prev_len:
                for msg in prev_msgs[cur_len:]:
                    msg_id = getattr(msg, 'id', None)
                    if msg_id and msg_id in unresolved_ids:
                        ts_map[msg_id] = prev_ts
                        unresolved_ids.remove(msg_id)
            else:
                prev_ids = {getattr(msg, 'id', None) for msg in prev_msgs if getattr(msg, 'id', None) in unresolved_ids}
                cur_ids = {getattr(msg, 'id', None) for msg in snap_msgs if getattr(msg, 'id', None) in unresolved_ids}
                for msg_id in prev_ids - cur_ids:
                    ts_map[msg_id] = prev_ts
                    unresolved_ids.remove(msg_id)
        if not unresolved_ids:
            break
        prev_msgs = snap_msgs
        prev_ts = snap_ts
    if unresolved_ids and prev_msgs and prev_ts:
        for msg in prev_msgs:
            msg_id = getattr(msg, 'id', None)
            if msg_id and msg_id in unresolved_ids:
                ts_map[msg_id] = prev_ts
                unresolved_ids.remove(msg_id)
                if not unresolved_ids:
                    break
    return ts_map


@chatController.get('/history', summary='获取聊天历史', description='按轮次分页获取指定会话的历史聊天记录')
async def get_chat_history(
        thread_id: str = Query(..., description='会话线程ID'),
        page: int = Query(default=1, ge=1, description='页码，从1开始'),
        page_size: int = Query(default=20, ge=1, le=100, description='每页轮次数量'),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    try:
        graph = await _get_history_graph()
        config = {'configurable': {'thread_id': thread_id}}
        state = await graph.aget_state(config)

        empty_response = ChatHistoryResponse(
            thread_id=thread_id, total=0, page=page, page_size=page_size,
            pages=0, has_more=False, turns=[],
        )

        if not state or not state.values:
            return ResponseUtil.success(data=empty_response.model_dump(by_alias=True))

        all_messages = state.values.get('messages', [])
        if not all_messages:
            return ResponseUtil.success(data=empty_response.model_dump(by_alias=True))

        turn_start_indices = _collect_turn_start_indices(all_messages)
        total = len(turn_start_indices)

        if total == 0:
            return ResponseUtil.success(data=empty_response.model_dump(by_alias=True))

        pages = math.ceil(total / page_size)
        start_turn_idx = max(0, total - page * page_size)
        end_turn_idx = max(0, total - (page - 1) * page_size)

        page_turns: list[ConversationTurnModel] = []
        if start_turn_idx < end_turn_idx:
            start_msg_idx = turn_start_indices[start_turn_idx]
            end_msg_idx = turn_start_indices[end_turn_idx] if end_turn_idx < total else len(all_messages)
            page_messages = all_messages[start_msg_idx:end_msg_idx]

            missing_ts_ids = _collect_missing_ts_message_ids(page_messages)
            ts_map = await _build_needed_timestamps(graph, config, missing_ts_ids) if missing_ts_ids else {}

            page_turns = _group_messages_to_turns(page_messages, ts_map=ts_map)
            page_turns = list(reversed(page_turns))

        response = ChatHistoryResponse(
            thread_id=thread_id, total=total, page=page, page_size=page_size,
            pages=pages, has_more=page < pages, turns=page_turns,
        )

        return ResponseUtil.success(data=response.model_dump(by_alias=True))

    except Exception as e:
        logger.error(f'获取聊天历史异常: {e}')
        raise ServiceException(message=f'获取聊天历史失败: {str(e)}')
