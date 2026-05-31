# -*- coding: utf-8 -*-
"""
模型工厂 - 根据提供商配置创建LangChain聊天模型

职责：将数据库中的提供商配置转换为 init_chat_model 所需参数
"""
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage, AIMessage, AIMessageChunk
from langchain_core.prompt_values import PromptValue
from pydantic import Field

from module_llm.llm_provider.entity.vo.provider_config_vo import Provider_configModel
from module_llm.llm_provider.provider_protocol import (
    API_PROTOCOL_CLAUDE,
    API_PROTOCOL_DEEPSEEK,
    API_PROTOCOL_GEMINI,
    API_PROTOCOL_OPENAI_CHAT,
    API_PROTOCOL_OPENAI_COMPATIBLE,
    API_PROTOCOL_OPENROUTER,
    API_PROTOCOL_RESPONSES,
    normalize_api_protocol,
    normalize_thinking_level,
    sdk_base_url_for_protocol,
    thinking_budget_for_level,
)

try:
    from langchain_deepseek import ChatDeepSeek
except ModuleNotFoundError:
    ChatDeepSeek = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ModuleNotFoundError:
    ChatGoogleGenerativeAI = None

try:
    import openai
    from langchain_openai import ChatOpenAI
    from langchain_openai.chat_models import base as openai_chat_base
except ModuleNotFoundError:
    openai = None
    ChatOpenAI = None
    openai_chat_base = None

try:
    from utils.log_util import logger
except ModuleNotFoundError:
    import logging

    logger = logging.getLogger(__name__)

# 本项目 provider_key → langchain model_provider 映射
# 对于使用 OpenAI 兼容API的提供商，统一映射为 "openai"
PROVIDER_KEY_MAP = {
    "openai": "openai",
    "anthropic": "anthropic",
    "google": "google_genai",
    "deepseek": "openai",
    "qwen": "openai",
    "zhipu": "openai",
    "moonshot": "openai",
    "baichuan": "openai",
    "minimax": "openai",
    "ollama": "ollama",
    "azure_openai": "azure_openai",
    "custom": "openai",
    "gemini": "google_genai",
}


_DeepSeekBase = ChatDeepSeek if ChatDeepSeek is not None else object


def _extract_reasoning_delta(delta: dict | None) -> str | None:
    if not isinstance(delta, dict):
        return None

    reasoning = (
        delta.get("reasoning_content")
        or delta.get("thinking_content")
        or delta.get("thought")
    )
    if reasoning:
        return str(reasoning)

    raw_reasoning = delta.get("reasoning")
    if isinstance(raw_reasoning, str):
        return raw_reasoning
    if isinstance(raw_reasoning, dict):
        for key in ("content", "text", "summary"):
            value = raw_reasoning.get(key)
            if value:
                return str(value)
    return None


_OpenAIChatBase = ChatOpenAI if ChatOpenAI is not None else object


class _OpenAIChatWithReasoning(_OpenAIChatBase):
    """保留 OpenAI 兼容 Chat Completions 流中的 reasoning_content。"""

    def _convert_chunk_to_generation_chunk(
        self,
        chunk: dict,
        default_chunk_class: type,
        base_generation_info: dict | None,
    ):
        generation_chunk = super()._convert_chunk_to_generation_chunk(
            chunk,
            default_chunk_class,
            base_generation_info,
        )
        if generation_chunk is None:
            return None

        choices = chunk.get("choices", []) or chunk.get("chunk", {}).get("choices", [])
        if not choices:
            return generation_chunk

        reasoning = _extract_reasoning_delta((choices[0] or {}).get("delta"))
        if reasoning and isinstance(generation_chunk.message, AIMessageChunk):
            generation_chunk.message.additional_kwargs["reasoning_content"] = reasoning
        return generation_chunk

    def _create_chat_result(self, response, generation_info: dict | None = None):
        chat_result = super()._create_chat_result(response, generation_info)
        response_dict = response if isinstance(response, dict) else response.model_dump()

        for generation, choice in zip(chat_result.generations, response_dict.get("choices", [])):
            reasoning = _extract_reasoning_delta(choice.get("message"))
            if reasoning and isinstance(generation.message, AIMessage):
                generation.message.additional_kwargs["reasoning_content"] = reasoning
        return chat_result


def _ensure_responses_chunk_output_list(chunk) -> bool:
    """Guard LangChain Responses streaming against completed chunks with output=None."""
    if getattr(chunk, "type", None) not in {"response.completed", "response.incomplete"}:
        return False

    response = getattr(chunk, "response", None)
    if response is None or getattr(response, "output", None) is not None:
        return False

    try:
        response.output = []
    except Exception:  # noqa: BLE001 - pydantic/openai response objects may block setattr
        object.__setattr__(response, "output", [])
    return True


class _OpenAIResponsesStable(_OpenAIChatBase):
    """OpenAI Responses wrapper that tolerates final stream chunks with output=None."""

    def _stream_responses(
        self,
        messages,
        stop=None,
        run_manager=None,
        **kwargs: Any,
    ):
        if openai is None or openai_chat_base is None:
            raise RuntimeError('langchain_openai 未安装，无法创建 OpenAI Responses 模型')

        kwargs["stream"] = True
        payload = self._get_request_payload(messages, stop=stop, **kwargs)
        try:
            if self.include_response_headers:
                raw_context_manager = self.root_client.with_raw_response.responses.create(**payload)
                context_manager = raw_context_manager.parse()
                headers = {"headers": dict(raw_context_manager.headers)}
            else:
                context_manager = self.root_client.responses.create(**payload)
                headers = {}
            original_schema_obj = kwargs.get("response_format")

            with context_manager as response:
                is_first_chunk = True
                current_index = -1
                current_output_index = -1
                current_sub_index = -1
                has_reasoning = False
                for chunk in response:
                    metadata = headers if is_first_chunk else {}
                    normalized_null_output = _ensure_responses_chunk_output_list(chunk)
                    if normalized_null_output:
                        logger.warning('OpenAI Responses stream completed with output=None; normalized to empty output')
                    (
                        current_index,
                        current_output_index,
                        current_sub_index,
                        generation_chunk,
                    ) = openai_chat_base._convert_responses_chunk_to_generation_chunk(
                        chunk,
                        current_index,
                        current_output_index,
                        current_sub_index,
                        schema=original_schema_obj,
                        metadata=metadata,
                        has_reasoning=has_reasoning,
                        output_version=self.output_version,
                    )
                    if generation_chunk:
                        if run_manager:
                            run_manager.on_llm_new_token(
                                generation_chunk.text, chunk=generation_chunk
                            )
                        is_first_chunk = False
                        if "reasoning" in generation_chunk.message.additional_kwargs:
                            has_reasoning = True
                        yield generation_chunk
        except openai.BadRequestError as e:
            openai_chat_base._handle_openai_bad_request(e)
        except openai.APIError as e:
            openai_chat_base._handle_openai_api_error(e)

    async def _astream_responses(
        self,
        messages,
        stop=None,
        run_manager=None,
        **kwargs: Any,
    ):
        if openai is None or openai_chat_base is None:
            raise RuntimeError('langchain_openai 未安装，无法创建 OpenAI Responses 模型')

        kwargs["stream"] = True
        payload = self._get_request_payload(messages, stop=stop, **kwargs)
        try:
            if self.include_response_headers:
                raw_context_manager = await self.root_async_client.with_raw_response.responses.create(
                    **payload
                )
                context_manager = raw_context_manager.parse()
                headers = {"headers": dict(raw_context_manager.headers)}
            else:
                context_manager = await self.root_async_client.responses.create(**payload)
                headers = {}
            original_schema_obj = kwargs.get("response_format")

            async with context_manager as response:
                is_first_chunk = True
                current_index = -1
                current_output_index = -1
                current_sub_index = -1
                has_reasoning = False
                async for chunk in response:
                    metadata = headers if is_first_chunk else {}
                    normalized_null_output = _ensure_responses_chunk_output_list(chunk)
                    if normalized_null_output:
                        logger.warning('OpenAI Responses stream completed with output=None; normalized to empty output')
                    (
                        current_index,
                        current_output_index,
                        current_sub_index,
                        generation_chunk,
                    ) = openai_chat_base._convert_responses_chunk_to_generation_chunk(
                        chunk,
                        current_index,
                        current_output_index,
                        current_sub_index,
                        schema=original_schema_obj,
                        metadata=metadata,
                        has_reasoning=has_reasoning,
                        output_version=self.output_version,
                    )
                    if generation_chunk:
                        if run_manager:
                            await run_manager.on_llm_new_token(
                                generation_chunk.text, chunk=generation_chunk
                            )
                        is_first_chunk = False
                        if "reasoning" in generation_chunk.message.additional_kwargs:
                            has_reasoning = True
                        yield generation_chunk
        except openai.BadRequestError as e:
            openai_chat_base._handle_openai_bad_request(e)
        except openai.APIError as e:
            openai_chat_base._handle_openai_api_error(e)

    def _stream(self, *args: Any, **kwargs: Any):
        if self._use_responses_api({**kwargs, **self.model_kwargs}):
            yield from self._stream_responses(*args, **kwargs)
            return
        yield from super()._stream(*args, **kwargs)

    async def _astream(self, *args: Any, **kwargs: Any):
        if self._use_responses_api({**kwargs, **self.model_kwargs}):
            async for chunk in self._astream_responses(*args, **kwargs):
                yield chunk
            return
        async for chunk in super()._astream(*args, **kwargs):
            yield chunk


class _DeepSeekWithThinking(_DeepSeekBase):
    """
    ChatDeepSeek 扩展：仅解决 thinking 模式下多轮对话 reasoning_content 丢失的 400 报错。

    只在 is_thinking=True 时生效，非 thinking 模式行为与父类完全一致。
    """
    is_thinking: bool = Field(default=False, exclude=True)

    def _get_request_payload(
        self,
        input_: LanguageModelInput,
        *,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> dict:
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)

        if not self.is_thinking:
            return payload

        # 提取原始 LangChain 消息列表
        if isinstance(input_, PromptValue):
            lc_messages = input_.to_messages()
        elif isinstance(input_, list):
            lc_messages = [m for m in input_ if isinstance(m, BaseMessage)]
        else:
            return payload

        # 为 payload 中的 assistant 消息注入 reasoning_content
        lc_ai_iter = iter(m for m in lc_messages if isinstance(m, AIMessage))
        for msg_dict in payload["messages"]:
            if msg_dict.get("role") == "assistant":
                lc_ai_msg = next(lc_ai_iter, None)
                if lc_ai_msg is not None:
                    reasoning = lc_ai_msg.additional_kwargs.get("reasoning_content")
                    msg_dict["reasoning_content"] = reasoning if reasoning is not None else ""

        return payload


def create_chat_model(
    provider_config: Provider_configModel,
    model_name: str,
    enable_thinking: bool = False,
    thinking_level: str | None = None,
):
    """
    根据提供商配置创建 LangChain ChatModel

    :param provider_config: 数据库中的提供商配置
    :param model_name: 模型名称 (如 gpt-4o, deepseek-chat)
    :param enable_thinking: 是否开启扩展思考模式
    :param thinking_level: 思考程度(low/high/xhigh/max)
    :return: BaseChatModel 实例
    """
    return _create_chat_model(
        provider_config,
        model_name,
        enable_thinking=enable_thinking,
        thinking_level=thinking_level,
    )


def _get_extra_params(provider_config: Provider_configModel) -> dict:
    extra_params = getattr(provider_config, 'extra_params', None)
    return extra_params if isinstance(extra_params, dict) else {}


def _merge_extra_body(kwargs: dict, extra_params: dict) -> None:
    if not extra_params:
        return
    extra_body = kwargs.get("extra_body")
    if not isinstance(extra_body, dict):
        extra_body = {}
    kwargs["extra_body"] = {**extra_body, **extra_params}


def _merge_model_kwargs(kwargs: dict, extra_params: dict) -> None:
    if not extra_params:
        return
    model_kwargs = kwargs.get("model_kwargs")
    if not isinstance(model_kwargs, dict):
        model_kwargs = {}
    kwargs["model_kwargs"] = {**model_kwargs, **extra_params}


def _merge_claude_extra_params(kwargs: dict, extra_params: dict, *, thinking_enabled: bool) -> None:
    if not extra_params:
        return

    model_kwargs = kwargs.get("model_kwargs")
    if not isinstance(model_kwargs, dict):
        model_kwargs = {}

    for key, value in extra_params.items():
        if thinking_enabled and key == "thinking":
            continue
        if key == "output_config" and isinstance(value, dict):
            output_config = kwargs.get("output_config")
            if not isinstance(output_config, dict):
                output_config = {}
            extra_output_config = dict(value)
            if thinking_enabled:
                extra_output_config.pop("effort", None)
            if extra_output_config:
                kwargs["output_config"] = {**extra_output_config, **output_config}
            continue
        if thinking_enabled and key == "effort":
            continue
        model_kwargs[key] = value

    if model_kwargs:
        kwargs["model_kwargs"] = model_kwargs


def _merge_top_level_kwargs(kwargs: dict, extra_params: dict) -> None:
    for key, value in extra_params.items():
        kwargs.setdefault(key, value)


def _openai_chat_reasoning_effort(level: str | None) -> str:
    normalized = normalize_thinking_level(level) or 'high'
    if normalized in {'low', 'medium', 'high'}:
        return normalized
    return 'high'


def _claude_uses_adaptive_thinking(model_name: str) -> bool:
    model = (model_name or '').lower().replace('_', '-')
    adaptive_markers = (
        'opus-4.6',
        'opus-4-6',
        'opus-4.7',
        'opus-4-7',
        'opus-4.8',
        'opus-4-8',
    )
    return any(marker in model for marker in adaptive_markers)


def _claude_thinking_kwargs(model_name: str, level: str, budget_tokens: int) -> dict:
    if _claude_uses_adaptive_thinking(model_name):
        return {
            "thinking": {"type": "adaptive", "display": "summarized"},
            "effort": level,
            "output_config": {"effort": level},
        }
    return {
        "thinking": {"type": "enabled", "budget_tokens": budget_tokens},
    }


def _base_init_kwargs(
    provider_config: Provider_configModel,
    *,
    api_protocol: str | None = None,
    deepseek_api_base: bool = False,
) -> dict:
    kwargs = {}
    if provider_config.api_key:
        kwargs["api_key"] = provider_config.api_key
    base_url = sdk_base_url_for_protocol(provider_config.base_url, api_protocol or provider_config.api_protocol)
    if base_url:
        kwargs["api_base" if deepseek_api_base else "base_url"] = base_url
    kwargs["timeout"] = provider_config.timeout or 600
    if provider_config.max_retries:
        kwargs["max_retries"] = provider_config.max_retries
    if provider_config.extra_headers:
        kwargs["default_headers"] = provider_config.extra_headers
    kwargs["temperature"] = 0
    return kwargs


def _create_chat_model(
    provider_config: Provider_configModel,
    model_name: str,
    enable_thinking: bool = False,
    thinking_level: str | None = None,
):
    api_protocol = normalize_api_protocol(
        getattr(provider_config, 'api_protocol', None),
        provider_config.provider_key,
    )
    normalized_level = normalize_thinking_level(thinking_level) or 'high'
    budget_tokens = thinking_budget_for_level(normalized_level)
    thinking_enabled = enable_thinking or bool(thinking_level)
    extra_params = _get_extra_params(provider_config)

    # DeepSeek 单独处理：使用 _DeepSeekWithThinking，解决 reasoning_content 多轮兼容问题。
    # provider_key 现在是内部 UUID，运行时必须以 api_protocol 为准。
    if api_protocol == API_PROTOCOL_DEEPSEEK:
        if ChatDeepSeek is None:
            raise RuntimeError('langchain_deepseek 未安装，无法创建 DeepSeek 模型')
        kwargs = {}

        if provider_config.api_key:
            kwargs["api_key"] = provider_config.api_key
        base_url = sdk_base_url_for_protocol(provider_config.base_url, api_protocol)
        if base_url:
            kwargs["api_base"] = base_url
        kwargs["temperature"] = 0
        kwargs["timeout"] = provider_config.timeout or 600  # 默认 10 分钟，避免思考模型长时间推理超时
        if provider_config.max_retries:
            kwargs["max_retries"] = provider_config.max_retries
        if provider_config.extra_headers:
            kwargs["default_headers"] = provider_config.extra_headers

        is_reasoner = "reasoner" in model_name.lower() or "-r1" in model_name.lower()
        is_thinking = thinking_enabled or is_reasoner

        if thinking_enabled and not is_reasoner:
            kwargs["model_kwargs"] = {
                "extra_body": {
                    "thinking": {"type": "enabled", "budget_tokens": budget_tokens}
                }
            }
        if extra_params:
            model_kwargs = kwargs.setdefault("model_kwargs", {})
            extra_body = model_kwargs.setdefault("extra_body", {})
            extra_body.update(extra_params)

        return _DeepSeekWithThinking(model=model_name, is_thinking=is_thinking, **kwargs)

    if api_protocol == API_PROTOCOL_GEMINI:
        if ChatGoogleGenerativeAI is None:
            raise RuntimeError('langchain_google_genai 未安装，无法创建 Gemini 模型')
        kwargs = {}
        if provider_config.api_key:
            kwargs["google_api_key"] = provider_config.api_key
        if provider_config.base_url:
            kwargs["base_url"] = provider_config.base_url
        if provider_config.timeout:
            kwargs["timeout"] = provider_config.timeout
        if provider_config.max_retries:
            kwargs["max_retries"] = provider_config.max_retries
        if provider_config.extra_headers:
            kwargs["additional_headers"] = provider_config.extra_headers
        if thinking_enabled:
            kwargs["thinking_budget"] = budget_tokens
            kwargs["include_thoughts"] = True
        _merge_model_kwargs(kwargs, extra_params)

        logger.info(
            f'init_chat_model (gemini): model={model_name}, '
            f'thinking_level={normalized_level if thinking_enabled else None}'
        )
        return ChatGoogleGenerativeAI(model=model_name, **kwargs)

    if api_protocol == API_PROTOCOL_CLAUDE:
        kwargs = _base_init_kwargs(provider_config, api_protocol=api_protocol)
        if thinking_enabled:
            kwargs.pop("temperature", None)
            kwargs.update(_claude_thinking_kwargs(model_name, normalized_level, budget_tokens))
        _merge_claude_extra_params(kwargs, extra_params, thinking_enabled=thinking_enabled)
        logger.info(
            f'init_chat_model (claude): model={model_name}, '
            f'thinking_level={normalized_level if thinking_enabled else None}, '
            f'thinking={kwargs.get("thinking")}, effort={kwargs.get("effort")}, '
            f'output_config={kwargs.get("output_config")}'
        )
        return init_chat_model(
            model=model_name,
            model_provider="anthropic",
            **kwargs,
        )

    provider = PROVIDER_KEY_MAP.get(provider_config.provider_key, "openai")
    if api_protocol in {
        API_PROTOCOL_OPENAI_CHAT,
        API_PROTOCOL_RESPONSES,
        API_PROTOCOL_OPENAI_COMPATIBLE,
        API_PROTOCOL_OPENROUTER,
    }:
        provider = "openai"

    kwargs = _base_init_kwargs(provider_config, api_protocol=api_protocol)
    use_responses_api = api_protocol == API_PROTOCOL_RESPONSES
    if use_responses_api:
        kwargs["use_responses_api"] = True
        if thinking_enabled:
            kwargs["reasoning"] = {"effort": normalized_level}
        _merge_top_level_kwargs(kwargs, extra_params)
    elif api_protocol == API_PROTOCOL_OPENAI_CHAT:
        kwargs["use_responses_api"] = False
        if thinking_enabled:
            kwargs["reasoning_effort"] = _openai_chat_reasoning_effort(normalized_level)
        _merge_extra_body(kwargs, extra_params)
    elif thinking_enabled and api_protocol in {API_PROTOCOL_OPENAI_COMPATIBLE, API_PROTOCOL_OPENROUTER}:
        # OpenAI 兼容 Chat Completions API：thinking 通过 extra_body 传递。
        kwargs["extra_body"] = {
            "thinking": {"type": "enabled", "budget_tokens": budget_tokens}
        }
        _merge_extra_body(kwargs, extra_params)
    else:
        _merge_extra_body(kwargs, extra_params)

    logger.info(
        f'init_chat_model: model={model_name}, provider={provider}, '
        f'api_protocol={api_protocol}, thinking_level={normalized_level if thinking_enabled else None}'
    )
    if use_responses_api:
        if ChatOpenAI is None:
            raise RuntimeError('langchain_openai 未安装，无法创建 OpenAI Responses 模型')
        return _OpenAIResponsesStable(model=model_name, **kwargs)

    if (
        api_protocol in {API_PROTOCOL_OPENAI_CHAT, API_PROTOCOL_OPENAI_COMPATIBLE, API_PROTOCOL_OPENROUTER}
        and provider == "openai"
    ):
        if ChatOpenAI is None:
            raise RuntimeError('langchain_openai 未安装，无法创建 OpenAI 兼容模型')
        return _OpenAIChatWithReasoning(model=model_name, **kwargs)

    return init_chat_model(
        model=model_name,
        model_provider=provider,
        **kwargs
    )
