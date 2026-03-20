# -*- coding: utf-8 -*-
"""
SSE 流式输出公共工具 —— /completions 和 /answer 共用的流处理逻辑。

提取自 chat_controller.py，避免两个端点维护相同的 chunk 解析 / 事件格式化代码。
"""
import asyncio
import json
from datetime import datetime, timezone
from typing import AsyncGenerator
from uuid import uuid4

from fastapi.responses import StreamingResponse
from httpcore import ReadTimeout as HttpcoreReadTimeout
from httpx import ReadTimeout as HttpxReadTimeout
from openai import (
    APIConnectionError as OpenAIConnectionError,
    APITimeoutError as OpenAITimeoutError,
    InternalServerError as OpenAIInternalServerError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.exception import ServiceException
from module_llm.chat_agent.deepagent_factory import create_deep_agent_instance
from module_llm.chat_agent.model_factory import create_chat_model
from module_llm.chat_agent.tools import get_builtin_tools
from module_llm.llm_provider.service.provider_config_service import Provider_configService
from module_llm.workspace.service.workspace_service import WorkspaceService
from utils.log_util import logger

# ── 常量 ──────────────────────────────────────────────────────────

RETRYABLE_EXCEPTIONS = (
    HttpxReadTimeout, HttpcoreReadTimeout, TimeoutError, ConnectionError,
    OpenAIConnectionError, OpenAITimeoutError, OpenAIInternalServerError,
)

FILE_TOOLS = frozenset({
    'write_file', 'create_file', 'edit_file', 'download_files', 'delete_file',
})

SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
    "Content-Encoding": "identity",
}


# ── 小工具 ────────────────────────────────────────────────────────

def _sse(payload: dict) -> str:
    """将 dict 格式化为 SSE data 行，自动注入 ISO-8601 时间戳。"""
    payload.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def _extract_tool_args(
    pending_tool_calls: dict,
    tool_call_id: str,
    tool_name: str,
) -> dict:
    """从累积的 pending_tool_calls 中匹配并提取工具入参。"""
    for idx, tc_info in list(pending_tool_calls.items()):
        if tc_info["id"] == tool_call_id or tc_info["name"] == tool_name:
            try:
                args = json.loads(tc_info["args"]) if tc_info["args"] else {}
            except (json.JSONDecodeError, TypeError):
                args = {"raw": tc_info["args"]}
            del pending_tool_calls[idx]
            return args
    return {}


# ── 共享设置 ──────────────────────────────────────────────────────

async def create_agent_and_model(
    query_db: AsyncSession,
    provider_key: str,
    model_name: str,
    enable_thinking: bool,
    enable_web_search: bool,
    user_id: int,
    thread_id: str,
    log_prefix: str = "",
    mcp_tools: list = None,
):
    """
    公共设置：查找提供商配置 → 创建模型 → 构建 agent。

    :param mcp_tools: 外部传入的 MCP 工具列表（由 mcp_tools_context 提供）。
                      若不为 None，则合并到内置工具中。
    :return: (model, agent)
    :raises ServiceException: 提供商配置不存在
    """
    provider_config = await Provider_configService.provider_config_by_key_services(
        query_db, provider_key,
    )
    if not provider_config.provider_id:
        raise ServiceException(message=f'提供商配置不存在: {provider_key}')

    model = create_chat_model(
        provider_config, model_name, enable_thinking=enable_thinking,
    )

    # 统一指定上下文长度限制，让 SummarizationMiddleware 的 ("fraction", 0.85) 触发器正常工作。
    # 无论什么模型都强制设置 max_input_tokens=128000，上下文 ≥ 85%（约 108K token）时自动压缩。
    model.profile = {"max_input_tokens": 128000}

    logger.info(
        f'{log_prefix}创建模型: provider={provider_config.provider_key}, '
        f'model={model_name}, enable_thinking={enable_thinking}'
    )

    tools = get_builtin_tools(enable_web_search=enable_web_search)
    if mcp_tools:
        tools.extend(mcp_tools)
        logger.info(f'{log_prefix}注入 {len(mcp_tools)} 个 MCP 工具')

    skills_paths = ["/skills/"]
    agent = await create_deep_agent_instance(
        model=model,
        user_id=user_id,
        thread_id=thread_id,
        tools=tools,
        skills_paths=skills_paths,
    )

    return model, agent


# ── 核心：流式 chunk 处理 ─────────────────────────────────────────

async def process_stream_chunks(
    agent,
    input_data,
    config: dict,
    *,
    request_id: str,
    cancel_event: asyncio.Event,
    enable_thinking: bool,
    user_id: int,
    thread_id: str,
    log_prefix: str = "[SSE]",
    debug_chunks: int = 0,
) -> AsyncGenerator[str, None]:
    """
    核心 SSE chunk 处理器。逐条 yield ``data: {...}\\n\\n`` 字符串。

    不含重试逻辑（由调用方包裹），不发送 ``[DONE]``。

    :param agent: 编译后的 LangGraph agent
    :param input_data: agent.astream() 的输入（dict 或 Command）
    :param config: LangGraph config（含 thread_id）
    :param request_id: 本次请求的唯一 ID
    :param cancel_event: 取消事件，set=True 表示用户请求终止
    :param enable_thinking: 是否开启思考模式
    :param user_id: 用于工作区变更通知
    :param thread_id: 用于工作区变更通知和日志
    :param log_prefix: 日志前缀
    :param debug_chunks: 前 N 个 chunk 打印详细调试日志（0 = 不打印）
    """
    chunk_count = 0
    thinking_notified = False
    pending_tool_calls: dict = {}  # index -> {name, args, id}

    async for msg_chunk, metadata in agent.astream(
        input_data, config=config, stream_mode="messages",
    ):
        # ── 取消检查 ──
        if cancel_event.is_set():
            logger.info(f'{log_prefix} 会话被用户终止: thread_id={thread_id}')
            yield _sse({"request_id": request_id, "type": "stopped", "content": "会话已终止"})
            return

        chunk_count += 1
        node = metadata.get("langgraph_node")
        has_tool_calls = bool(getattr(msg_chunk, "tool_call_chunks", None))
        additional_kwargs = getattr(msg_chunk, "additional_kwargs", {})

        # ── 调试日志 ──
        if debug_chunks and chunk_count <= debug_chunks:
            content_preview = str(msg_chunk.content)[:100] if msg_chunk.content else "(empty)"
            # logger.info(
            #     f'{log_prefix} #{chunk_count} node={node}, '
            #     f'type={type(msg_chunk).__name__}, has_tool_calls={has_tool_calls}, '
            #     f'content_preview={content_preview}'
            # )
            if enable_thinking:
                pass
                # logger.info(f'{log_prefix} #{chunk_count} additional_kwargs: {additional_kwargs}')

        # ── model 节点：累积工具调用 ──
        if node == "model" and has_tool_calls:
            for tc in msg_chunk.tool_call_chunks:
                idx = tc.get("index", 0)
                if idx not in pending_tool_calls:
                    pending_tool_calls[idx] = {"name": "", "args": "", "id": ""}
                if tc.get("name"):
                    pending_tool_calls[idx]["name"] = tc["name"]
                    yield _sse({
                        "request_id": request_id,
                        "type": "tool_call",
                        "tool": tc["name"],
                        "call_id": tc.get("id", ""),
                    })
                if tc.get("args"):
                    pending_tool_calls[idx]["args"] += tc["args"]
                if tc.get("id"):
                    pending_tool_calls[idx]["id"] = tc["id"]

        # ── tools 节点：工具执行结果 ──
        if node == "tools" and msg_chunk.content:
            tool_name = getattr(msg_chunk, "name", "")
            tool_call_id = getattr(msg_chunk, "tool_call_id", "")
            tool_args = _extract_tool_args(pending_tool_calls, tool_call_id, tool_name)

            yield _sse({
                "request_id": request_id,
                "type": "tool_result",
                "tool": tool_name,
                "args": tool_args,
                "result": msg_chunk.content,
            })

            if tool_name in FILE_TOOLS:
                await WorkspaceService.notify_agent_file_change(user_id, thread_id, tool_name)

        # ── model 节点：思考 + 文本内容 ──
        if node == "model":
            reasoning = (
                additional_kwargs.get("reasoning_content")
                or additional_kwargs.get("thinking_content")
                or additional_kwargs.get("thought")
            )
            if reasoning:
                thinking_notified = True
                yield _sse({"request_id": request_id, "type": "thinking", "content": reasoning})

            elif isinstance(msg_chunk.content, list):
                for block in msg_chunk.content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "thinking" and block.get("thinking"):
                        thinking_notified = True
                        yield _sse({"request_id": request_id, "type": "thinking", "content": block["thinking"]})
                    elif block.get("type") == "text" and block.get("text"):
                        yield _sse({"request_id": request_id, "type": "content", "content": block["text"]})

            elif msg_chunk.content:
                if enable_thinking and not thinking_notified and chunk_count > 1:
                    yield _sse({"request_id": request_id, "type": "thinking_end"})
                    thinking_notified = True
                yield _sse({"request_id": request_id, "type": "content", "content": msg_chunk.content})

            elif not msg_chunk.content and not has_tool_calls and enable_thinking and not thinking_notified:
                yield _sse({"request_id": request_id, "type": "thinking_start"})
                thinking_notified = True

    logger.info(f'{log_prefix} 流结束，共 {chunk_count} 个 chunk')


# ── Checkpoint 回滚 ──────────────────────────────────────────────

async def rollback_checkpoint_state(agent, config: dict, pre_messages: list, log_prefix: str = "[SSE]"):
    """
    将 checkpoint 状态回滚到请求前的消息列表。

    用于流式请求失败后清除被污染的对话历史（部分 AI 响应、重复用户消息等），
    防止后续请求基于残缺历史持续报错。
    """
    try:
        await agent.aupdate_state(config, {"messages": pre_messages})
        logger.info(f'{log_prefix} checkpoint 已回滚到请求前状态 (消息数: {len(pre_messages)})')
    except Exception as rollback_err:
        logger.error(f'{log_prefix} checkpoint 回滚失败: {rollback_err}')


# ── 中断检测 ──────────────────────────────────────────────────────

async def check_interrupts(
    agent,
    config: dict,
    request_id: str,
    log_prefix: str = "[SSE]",
) -> AsyncGenerator[str, None]:
    """流结束后检查 LangGraph interrupt，若存在则 yield ask_user 事件。"""
    try:
        _state = await agent.aget_state(config)
        if _state and _state.next:
            for _task in (_state.tasks or ()):
                if hasattr(_task, 'interrupts') and _task.interrupts:
                    for _intr in _task.interrupts:
                        _val = _intr.value if isinstance(_intr.value, dict) else {"content": _intr.value}
                        yield _sse({
                            "request_id": request_id,
                            "type": "ask_user",
                            **_val,
                        })
                        logger.info(f'{log_prefix} 检测到 interrupt，已发送 ask_user 事件')
    except Exception as _state_err:
        logger.warning(f'{log_prefix} 检查中断状态失败: {_state_err}')


# ── StreamingResponse 工厂 ────────────────────────────────────────

def make_sse_response(generator) -> StreamingResponse:
    """用标准 SSE 头创建 StreamingResponse。"""
    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )
