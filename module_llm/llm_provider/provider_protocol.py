# -*- coding: utf-8 -*-
"""
LLM provider protocol helpers.

Keep protocol normalization shared between provider configuration APIs and the
chat model factory so frontend selections and runtime assembly stay aligned.
"""

from typing import Iterable
from urllib.parse import urlsplit, urlunsplit
from uuid import uuid4


API_PROTOCOL_OPENAI = 'openai'
API_PROTOCOL_OPENAI_CHAT = 'openai_chat'
API_PROTOCOL_RESPONSES = 'responses'
API_PROTOCOL_CLAUDE = 'claude'
API_PROTOCOL_GEMINI = 'gemini'
API_PROTOCOL_DEEPSEEK = 'deepseek'
API_PROTOCOL_OPENROUTER = 'openrouter'
API_PROTOCOL_OPENAI_COMPATIBLE = 'openai_compatible'

API_PROTOCOLS = {
    API_PROTOCOL_OPENAI_CHAT,
    API_PROTOCOL_RESPONSES,
    API_PROTOCOL_CLAUDE,
    API_PROTOCOL_GEMINI,
    API_PROTOCOL_DEEPSEEK,
    API_PROTOCOL_OPENROUTER,
    API_PROTOCOL_OPENAI_COMPATIBLE,
}

THINKING_LEVELS = ('low', 'medium', 'high', 'xhigh', 'max')
THINKING_BUDGETS = {
    'low': 1024,
    'medium': 4096,
    'high': 8000,
    'xhigh': 16000,
    'max': 32000,
}

PROTOCOL_DEFAULT_THINKING_LEVELS = {
    API_PROTOCOL_OPENAI_CHAT: list(THINKING_LEVELS),
    API_PROTOCOL_RESPONSES: list(THINKING_LEVELS),
    API_PROTOCOL_CLAUDE: list(THINKING_LEVELS),
    API_PROTOCOL_GEMINI: list(THINKING_LEVELS),
    API_PROTOCOL_DEEPSEEK: list(THINKING_LEVELS),
    API_PROTOCOL_OPENROUTER: list(THINKING_LEVELS),
    API_PROTOCOL_OPENAI_COMPATIBLE: list(THINKING_LEVELS),
}

PROTOCOL_DEFAULT_MODELS = {
    API_PROTOCOL_OPENAI_CHAT: [
        'gpt-4.1',
        'gpt-4.1-mini',
        'gpt-4o',
        'gpt-4o-mini',
    ],
    API_PROTOCOL_RESPONSES: [
        'gpt-5',
        'gpt-5-mini',
        'gpt-5-nano',
        'gpt-5-thinking',
        'gpt-5-thinking-mini',
    ],
    API_PROTOCOL_CLAUDE: [
        'claude-sonnet-4.5',
        'claude-opus-4.1',
        'claude-opus-4.8',
        'claude-haiku-4',
    ],
    API_PROTOCOL_GEMINI: [
        'gemini-2.5-flash',
        'gemini-2.5-pro',
        'gemini-2.5-pro-thinking',
    ],
    API_PROTOCOL_DEEPSEEK: [
        'deepseek-chat',
        'deepseek-reasoner',
        'deepseek-v3',
        'deepseek-r1',
    ],
    API_PROTOCOL_OPENROUTER: [
        'openai/gpt-5',
        'anthropic/claude-opus-4.8',
        'google/gemini-2.5-pro',
        'deepseek/deepseek-r1',
    ],
    API_PROTOCOL_OPENAI_COMPATIBLE: [
        'gpt-5',
        'gpt-5-mini',
        'deepseek-chat',
        'deepseek-reasoner',
    ],
}


def normalize_api_protocol(api_protocol: str | None, provider_key: str | None = None) -> str:
    raw = (api_protocol or '').strip().lower()
    raw = raw.replace('-', '_')
    key = (provider_key or '').strip().lower()

    aliases = {
        'openai': API_PROTOCOL_OPENAI_CHAT,
        'openai_chat': API_PROTOCOL_OPENAI_CHAT,
        'chat': API_PROTOCOL_OPENAI_CHAT,
        'chat_completions': API_PROTOCOL_OPENAI_CHAT,
        '/chat/completions': API_PROTOCOL_OPENAI_CHAT,
        'openai_responses': API_PROTOCOL_RESPONSES,
        'response': API_PROTOCOL_RESPONSES,
        'responses': API_PROTOCOL_RESPONSES,
        '/responses': API_PROTOCOL_RESPONSES,
        'compatible': API_PROTOCOL_OPENAI_COMPATIBLE,
        'custom': API_PROTOCOL_OPENAI_COMPATIBLE,
        'openai_compatible': API_PROTOCOL_OPENAI_COMPATIBLE,
        'anthropic': API_PROTOCOL_CLAUDE,
        'claude': API_PROTOCOL_CLAUDE,
        'google': API_PROTOCOL_GEMINI,
        'google_genai': API_PROTOCOL_GEMINI,
        'gemini': API_PROTOCOL_GEMINI,
        'deepseek': API_PROTOCOL_DEEPSEEK,
        'openrouter': API_PROTOCOL_OPENROUTER,
    }
    if raw == API_PROTOCOL_OPENAI_CHAT:
        return API_PROTOCOL_OPENAI_CHAT
    if raw in aliases:
        return aliases[raw]

    if key in {'anthropic', 'claude'}:
        return API_PROTOCOL_CLAUDE
    if key in {'google', 'gemini'}:
        return API_PROTOCOL_GEMINI
    if key == API_PROTOCOL_DEEPSEEK:
        return API_PROTOCOL_DEEPSEEK
    if key == API_PROTOCOL_OPENROUTER:
        return API_PROTOCOL_OPENROUTER
    if key == 'openai':
        return API_PROTOCOL_OPENAI_CHAT
    return API_PROTOCOL_OPENAI_COMPATIBLE


def generate_provider_key() -> str:
    return str(uuid4())


def normalize_model_list(models: list | str | None) -> list[str]:
    if models is None:
        return []
    if isinstance(models, str):
        values = models.replace('\r', '\n').replace(',', '\n').split('\n')
    elif isinstance(models, Iterable):
        values = list(models)
    else:
        return []

    normalized = []
    seen = set()
    for value in values:
        model = str(value).strip()
        if not model or model in seen:
            continue
        normalized.append(model)
        seen.add(model)
    return normalized


def default_models_for_protocol(api_protocol: str | None) -> list[str]:
    normalized_protocol = normalize_api_protocol(api_protocol)
    return list(
        PROTOCOL_DEFAULT_MODELS.get(
            normalized_protocol,
            PROTOCOL_DEFAULT_MODELS[API_PROTOCOL_OPENAI_COMPATIBLE],
        )
    )


def normalize_base_url(base_url: str | None) -> str | None:
    value = (base_url or '').strip()
    if not value:
        return None

    parsed = urlsplit(value)
    if not parsed.scheme or not parsed.netloc:
        return value.rstrip('/')

    path = parsed.path.rstrip('/')
    lower_path = path.lower()
    endpoint_suffixes = (
        '/v1/chat/completions',
        '/chat/completions',
        '/v1/responses',
        '/responses',
        '/v1/messages',
        '/messages',
    )
    for suffix in endpoint_suffixes:
        if lower_path.endswith(suffix):
            path = path[: -len(suffix)]
            lower_path = path.lower()
            break

    if parsed.netloc.lower() in {'api.openai.com'} and lower_path == '/v1':
        path = ''

    path = path.rstrip('/')
    return urlunsplit((parsed.scheme, parsed.netloc, path, '', '')).rstrip('/')


def sdk_base_url_for_protocol(base_url: str | None, api_protocol: str | None) -> str | None:
    normalized_base = normalize_base_url(base_url)
    if not normalized_base:
        return None

    protocol = normalize_api_protocol(api_protocol)
    if protocol not in {
        API_PROTOCOL_OPENAI_CHAT,
        API_PROTOCOL_RESPONSES,
        API_PROTOCOL_OPENAI_COMPATIBLE,
        API_PROTOCOL_OPENROUTER,
    }:
        return normalized_base

    parsed = urlsplit(normalized_base)
    if not parsed.scheme or not parsed.netloc:
        return normalized_base

    path = parsed.path.rstrip('/')
    if not path.lower().endswith('/v1'):
        path = f'{path}/v1' if path else '/v1'
    return urlunsplit((parsed.scheme, parsed.netloc, path, '', '')).rstrip('/')


def normalize_thinking_level(level: str | None) -> str | None:
    value = (level or '').strip().lower()
    return value if value in THINKING_LEVELS else None


def normalize_thinking_levels(levels: list | str | None, api_protocol: str) -> list[str]:
    if levels is None:
        return list(PROTOCOL_DEFAULT_THINKING_LEVELS.get(api_protocol, []))
    if isinstance(levels, str):
        values = levels.replace('\r', '\n').replace(',', '\n').split('\n')
    elif isinstance(levels, Iterable):
        values = list(levels)
    else:
        values = []

    normalized = []
    for value in values:
        level = normalize_thinking_level(str(value))
        if level and level not in normalized:
            normalized.append(level)
    if normalized:
        return normalized
    return list(PROTOCOL_DEFAULT_THINKING_LEVELS.get(api_protocol, []))


def thinking_budget_for_level(level: str | None) -> int:
    return THINKING_BUDGETS.get(normalize_thinking_level(level) or 'high', THINKING_BUDGETS['high'])
