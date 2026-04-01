# -*- coding: utf-8 -*-
"""SSE event type definitions for the Presenter layer."""
from dataclasses import dataclass
from enum import Enum
from typing import Any


class EventType(str, Enum):
    METADATA = 'metadata'
    CONTENT = 'message:chunk'
    THINKING = 'thinking'
    THINKING_START = 'thinking_start'
    THINKING_END = 'thinking_end'
    TOOL_CALL = 'tool:start'
    TOOL_CALL_ARGS = 'tool_call_args'
    TOOL_RESULT = 'tool:result'
    ASK_USER = 'ask_user'
    RETRY = 'retry'
    ERROR = 'error'
    DONE = 'done'
    TOKEN_USAGE = 'token:usage'
    STOPPED = 'stopped'


@dataclass(slots=True)
class SSEEvent:
    event_type: EventType
    data: dict[str, Any]
    trace_id: str | None = None
    run_id: str | None = None
