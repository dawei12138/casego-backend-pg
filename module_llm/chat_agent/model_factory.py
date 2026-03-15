# -*- coding: utf-8 -*-
"""
模型工厂 - 根据提供商配置创建LangChain聊天模型

职责：将数据库中的提供商配置转换为 init_chat_model 所需参数
"""
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompt_values import PromptValue
from langchain_deepseek import ChatDeepSeek
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field

from module_llm.llm_provider.entity.vo.provider_config_vo import Provider_configModel
from utils.log_util import logger

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
    "gemini": "openai",
}


class _DeepSeekWithThinking(ChatDeepSeek):
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


def create_chat_model(provider_config: Provider_configModel, model_name: str, enable_thinking: bool = False):
    """
    根据提供商配置创建 LangChain ChatModel

    :param provider_config: 数据库中的提供商配置
    :param model_name: 模型名称 (如 gpt-4o, deepseek-chat)
    :param enable_thinking: 是否开启扩展思考模式
    :return: BaseChatModel 实例
    """
    # DeepSeek 单独处理：使用 _DeepSeekWithThinking
    if provider_config.provider_key == "deepseek" or provider_config.provider_key == "custom":
        kwargs = {}

        if provider_config.api_key:
            kwargs["api_key"] = provider_config.api_key
        if provider_config.base_url:
            kwargs["api_base"] = provider_config.base_url
        kwargs["temperature"] = 0
        kwargs["timeout"] = provider_config.timeout or 600  # 默认 10 分钟，避免思考模型长时间推理超时
        if provider_config.max_retries:
            kwargs["max_retries"] = provider_config.max_retries
        if provider_config.extra_headers:
            kwargs["default_headers"] = provider_config.extra_headers

        is_reasoner = "reasoner" in model_name.lower() or "-r1" in model_name.lower()
        is_thinking = enable_thinking or is_reasoner

        if enable_thinking and not is_reasoner:
            kwargs["model_kwargs"] = {
                "extra_body": {
                    "thinking": {"type": "enabled", "budget_tokens": 8000}
                }
            }

        return _DeepSeekWithThinking(model=model_name, is_thinking=is_thinking, **kwargs)

    # # Gemini 单独处理：使用原生 ChatGoogleGenerativeAI，支持 thinking_budget/include_thoughts
    # if provider_config.provider_key in ("gemini", "google"):
    #     kwargs = {}
    #     if provider_config.api_key:
    #         kwargs["google_api_key"] = provider_config.api_key
    #     if provider_config.base_url:
    #         kwargs["base_url"] = provider_config.base_url
    #     if provider_config.timeout:
    #         kwargs["timeout"] = provider_config.timeout
    #     if provider_config.max_retries:
    #         kwargs["max_retries"] = provider_config.max_retries
    #     if provider_config.extra_headers:
    #         kwargs["additional_headers"] = provider_config.extra_headers
    #     if enable_thinking:
    #         kwargs["thinking_budget"] = 8000
    #         kwargs["include_thoughts"] = True
    #
    #     logger.info(f'init_chat_model (google_genai): model={model_name}, enable_thinking={enable_thinking}')
    #     return ChatGoogleGenerativeAI(model=model_name, **kwargs)

    # ── 其他所有提供商：走 init_chat_model ──
    provider = PROVIDER_KEY_MAP.get(
        provider_config.provider_key,
        "openai"
    )

    kwargs = {}
    if provider_config.api_key:
        kwargs["api_key"] = provider_config.api_key
    if provider_config.base_url:
        kwargs["base_url"] = provider_config.base_url
    kwargs["timeout"] = provider_config.timeout or 600  # 默认 10 分钟，避免思考模型长时间推理超时
    if provider_config.max_retries:
        kwargs["max_retries"] = provider_config.max_retries
    if provider_config.extra_headers:
        kwargs["default_headers"] = provider_config.extra_headers
    kwargs["temperature"] = 0
    # OpenAI 提供商使用 Responses API 协议（/v1/responses），思考用 reasoning 参数
    if provider_config.provider_key.startswith('openai'):
        kwargs["use_responses_api"] = True
        if enable_thinking:
            kwargs["reasoning"] = {"effort": "high"}
    elif enable_thinking:
        # 其他 OpenAI 兼容提供商（Chat Completions API）：thinking 须通过 extra_body 传递
        kwargs["extra_body"] = {
            "thinking": {"type": "enabled", "budget_tokens": 10000}
        }

    logger.info(f'init_chat_model: model={model_name}, provider={provider}')
    return init_chat_model(
        model=model_name,
        model_provider=provider,
        **kwargs
    )
