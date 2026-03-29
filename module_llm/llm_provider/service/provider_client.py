# -*- coding: utf-8 -*-
"""
LLM Provider 客户端封装
支持 OpenAI 和 Anthropic API 调用
"""

import asyncio
from typing import AsyncIterator, Dict, Any, Optional, List
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
import tiktoken

from module_llm.llm_provider.entity.do.provider_do import LlmProvider
from module_llm.llm_provider.entity.do.provider_model_do import LlmProviderModel


class ProviderClient:
    """
    LLM Provider 客户端基类
    """

    def __init__(self, provider: LlmProvider, model: LlmProviderModel):
        self.provider = provider
        self.model = model

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any] | AsyncIterator[Dict[str, Any]]:
        """
        聊天补全接口
        """
        raise NotImplementedError

    def count_tokens(self, text: str) -> int:
        """
        计算 token 数量
        """
        raise NotImplementedError

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        计算成本
        """
        # 从 model 配置中获取价格
        input_price = self.model.input_price or 0.0
        output_price = self.model.output_price or 0.0

        # 价格单位: $/1M tokens
        input_cost = (input_tokens / 1_000_000) * input_price
        output_cost = (output_tokens / 1_000_000) * output_price

        return input_cost + output_cost


class OpenAIClient(ProviderClient):
    """
    OpenAI API 客户端
    """

    def __init__(self, provider: LlmProvider, model: LlmProviderModel):
        super().__init__(provider, model)

        # 解析配置
        config = provider.config or {}
        api_key = config.get('api_key')
        base_url = config.get('base_url')

        if not api_key:
            raise ValueError(f'Provider {provider.provider_name} missing api_key in config')

        # 初始化客户端
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url if base_url else None
        )

        # 初始化 tokenizer
        try:
            self.encoding = tiktoken.encoding_for_model(model.model_name)
        except KeyError:
            # 如果模型不支持，使用默认编码
            self.encoding = tiktoken.get_encoding('cl100k_base')

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        OpenAI 聊天补全
        """
        params = {
            'model': self.model.model_name,
            'messages': messages,
            'temperature': temperature,
            'stream': stream,
        }

        if max_tokens:
            params['max_tokens'] = max_tokens

        # 合并额外参数
        params.update(kwargs)

        if stream:
            return self._stream_completion(params)
        else:
            return await self._non_stream_completion(params)

    async def _non_stream_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        非流式补全
        """
        response = await self.client.chat.completions.create(**params)

        return {
            'content': response.choices[0].message.content,
            'finish_reason': response.choices[0].finish_reason,
            'usage': {
                'input_tokens': response.usage.prompt_tokens,
                'output_tokens': response.usage.completion_tokens,
                'total_tokens': response.usage.total_tokens,
            },
            'model': response.model,
        }

    async def _stream_completion(self, params: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        流式补全
        """
        stream = await self.client.chat.completions.create(**params)

        input_tokens = 0
        output_tokens = 0

        async for chunk in stream:
            delta = chunk.choices[0].delta

            if delta.content:
                output_tokens += 1  # 粗略估计
                yield {
                    'type': 'content',
                    'content': delta.content,
                }

            if chunk.choices[0].finish_reason:
                yield {
                    'type': 'done',
                    'finish_reason': chunk.choices[0].finish_reason,
                    'usage': {
                        'input_tokens': input_tokens,
                        'output_tokens': output_tokens,
                        'total_tokens': input_tokens + output_tokens,
                    },
                }

    def count_tokens(self, text: str) -> int:
        """
        计算 token 数量
        """
        return len(self.encoding.encode(text))


class AnthropicClient(ProviderClient):
    """
    Anthropic API 客户端
    """

    def __init__(self, provider: LlmProvider, model: LlmProviderModel):
        super().__init__(provider, model)

        # 解析配置
        config = provider.config or {}
        api_key = config.get('api_key')
        base_url = config.get('base_url')

        if not api_key:
            raise ValueError(f'Provider {provider.provider_name} missing api_key in config')

        # 初始化客户端
        self.client = AsyncAnthropic(
            api_key=api_key,
            base_url=base_url if base_url else None
        )

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        """
        Anthropic 聊天补全
        """
        # Anthropic 需要分离 system 消息
        system_message = None
        user_messages = []

        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                user_messages.append(msg)

        params = {
            'model': self.model.model_name,
            'messages': user_messages,
            'temperature': temperature,
            'max_tokens': max_tokens or 4096,  # Anthropic 要求必须提供
        }

        if system_message:
            params['system'] = system_message

        # 合并额外参数
        params.update(kwargs)

        if stream:
            return self._stream_completion(params)
        else:
            return await self._non_stream_completion(params)

    async def _non_stream_completion(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        非流式补全
        """
        response = await self.client.messages.create(**params)

        return {
            'content': response.content[0].text,
            'finish_reason': response.stop_reason,
            'usage': {
                'input_tokens': response.usage.input_tokens,
                'output_tokens': response.usage.output_tokens,
                'total_tokens': response.usage.input_tokens + response.usage.output_tokens,
            },
            'model': response.model,
        }

    async def _stream_completion(self, params: Dict[str, Any]) -> AsyncIterator[Dict[str, Any]]:
        """
        流式补全
        """
        async with self.client.messages.stream(**params) as stream:
            async for text in stream.text_stream:
                yield {
                    'type': 'content',
                    'content': text,
                }

            # 获取最终消息
            message = await stream.get_final_message()

            yield {
                'type': 'done',
                'finish_reason': message.stop_reason,
                'usage': {
                    'input_tokens': message.usage.input_tokens,
                    'output_tokens': message.usage.output_tokens,
                    'total_tokens': message.usage.input_tokens + message.usage.output_tokens,
                },
            }

    def count_tokens(self, text: str) -> int:
        """
        计算 token 数量
        Anthropic 使用自己的 tokenizer，这里使用粗略估计
        """
        # 粗略估计: 1 token ≈ 4 字符
        return len(text) // 4


class ProviderClientFactory:
    """
    Provider 客户端工厂
    """

    @staticmethod
    def create_client(provider: LlmProvider, model: LlmProviderModel) -> ProviderClient:
        """
        根据 provider 类型创建客户端
        """
        provider_type = provider.provider_type.lower()

        if provider_type == 'openai':
            return OpenAIClient(provider, model)
        elif provider_type == 'anthropic':
            return AnthropicClient(provider, model)
        else:
            raise ValueError(f'Unsupported provider type: {provider_type}')
