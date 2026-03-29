# -*- coding: utf-8 -*-
"""
Agent 执行引擎
基于 LangGraph StateGraph 实现 Agent 执行
"""

import asyncio
from typing import Dict, Any, List, Optional, Callable, TypedDict, Annotated
from enum import Enum
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage

from module_llm.llm_provider.service.provider_client import ProviderClientFactory
from module_llm.llm_mcp.service.mcp_client import MCPClientFactory
from module_llm.llm_run.service.run_stream import RunStreamWriter


# Agent 注册表
AGENT_REGISTRY: Dict[str, type] = {}


def register_agent(agent_type: str):
    """
    Agent 注册装饰器
    """
    def decorator(cls):
        AGENT_REGISTRY[agent_type] = cls
        return cls
    return decorator


class AgentState(TypedDict):
    """
    Agent 状态定义
    """
    messages: Annotated[List[Any], "对话消息列表"]
    current_step: Annotated[str, "当前步骤"]
    tool_calls: Annotated[List[Dict[str, Any]], "工具调用列表"]
    final_output: Annotated[Optional[str], "最终输出"]
    error: Annotated[Optional[str], "错误信息"]


class AgentExecutor:
    """
    Agent 执行器基类
    """

    def __init__(
        self,
        run_id: str,
        provider_client,
        mcp_clients: List[Any],
        stream_writer: RunStreamWriter,
        checkpointer: Optional[PostgresSaver] = None
    ):
        self.run_id = run_id
        self.provider_client = provider_client
        self.mcp_clients = mcp_clients
        self.stream_writer = stream_writer
        self.checkpointer = checkpointer
        self.graph = None

    def build_graph(self) -> StateGraph:
        """
        构建 StateGraph（子类实现）
        """
        raise NotImplementedError

    async def execute(self, input_message: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        执行 Agent
        """
        # 构建图
        if not self.graph:
            self.graph = self.build_graph()

        # 初始化状态
        initial_state = {
            'messages': [],
            'current_step': 'start',
            'tool_calls': [],
            'final_output': None,
            'error': None
        }

        # 添加系统消息
        if system_prompt:
            initial_state['messages'].append(SystemMessage(content=system_prompt))

        # 添加用户消息
        initial_state['messages'].append(HumanMessage(content=input_message))

        # 执行图
        try:
            config = {'configurable': {'thread_id': self.run_id}}
            final_state = await self.graph.ainvoke(initial_state, config=config)

            return {
                'success': True,
                'output': final_state.get('final_output'),
                'messages': final_state.get('messages'),
                'tool_calls': final_state.get('tool_calls'),
            }

        except Exception as e:
            await self.stream_writer.write_error(str(e), type(e).__name__)
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }

    async def _call_llm(self, state: AgentState) -> AgentState:
        """
        调用 LLM
        """
        messages = state['messages']

        # 转换为 API 格式
        api_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                api_messages.append({'role': 'system', 'content': msg.content})
            elif isinstance(msg, HumanMessage):
                api_messages.append({'role': 'user', 'content': msg.content})
            elif isinstance(msg, AIMessage):
                api_messages.append({'role': 'assistant', 'content': msg.content})
            elif isinstance(msg, ToolMessage):
                api_messages.append({'role': 'tool', 'content': msg.content})

        # 调用 LLM（流式）
        try:
            stream = await self.provider_client.chat_completion(
                messages=api_messages,
                stream=True
            )

            content_parts = []
            usage = None

            async for chunk in stream:
                if chunk['type'] == 'content':
                    content = chunk['content']
                    content_parts.append(content)
                    # 写入流
                    await self.stream_writer.write_content(content)

                elif chunk['type'] == 'done':
                    usage = chunk.get('usage')

            # 组装完整内容
            full_content = ''.join(content_parts)

            # 添加 AI 消息
            state['messages'].append(AIMessage(content=full_content))
            state['final_output'] = full_content

            return state

        except Exception as e:
            state['error'] = str(e)
            await self.stream_writer.write_error(str(e), type(e).__name__)
            return state


@register_agent('fast')
class FastAgent(AgentExecutor):
    """
    Fast Agent - 简单对话，不使用工具
    """

    def build_graph(self) -> StateGraph:
        """
        构建简单对话图
        """
        graph = StateGraph(AgentState)

        # 添加节点
        graph.add_node('llm', self._call_llm)

        # 添加边
        graph.add_edge(START, 'llm')
        graph.add_edge('llm', END)

        # 编译
        return graph.compile(checkpointer=self.checkpointer)


@register_agent('deep')
class DeepAgent(AgentExecutor):
    """
    Deep Agent - 支持工具调用的复杂 Agent
    """

    def build_graph(self) -> StateGraph:
        """
        构建工具调用图
        """
        graph = StateGraph(AgentState)

        # 添加节点
        graph.add_node('llm', self._call_llm_with_tools)
        graph.add_node('tools', self._call_tools)

        # 添加边
        graph.add_edge(START, 'llm')
        graph.add_conditional_edges(
            'llm',
            self._should_continue,
            {
                'continue': 'tools',
                'end': END
            }
        )
        graph.add_edge('tools', 'llm')

        # 编译
        return graph.compile(checkpointer=self.checkpointer)

    def _should_continue(self, state: AgentState) -> str:
        """
        判断是否继续执行工具
        """
        # 检查最后一条消息是否包含工具调用
        messages = state['messages']
        if not messages:
            return 'end'

        last_message = messages[-1]
        if isinstance(last_message, AIMessage):
            # 检查是否有工具调用（这里简化处理，实际需要解析 tool_calls）
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                return 'continue'

        return 'end'

    async def _call_llm_with_tools(self, state: AgentState) -> AgentState:
        """
        调用 LLM（带工具定义）
        """
        messages = state['messages']

        # 获取可用工具
        tools = await self._get_available_tools()

        # 转换为 API 格式
        api_messages = []
        for msg in messages:
            if isinstance(msg, SystemMessage):
                api_messages.append({'role': 'system', 'content': msg.content})
            elif isinstance(msg, HumanMessage):
                api_messages.append({'role': 'user', 'content': msg.content})
            elif isinstance(msg, AIMessage):
                api_messages.append({'role': 'assistant', 'content': msg.content})
            elif isinstance(msg, ToolMessage):
                api_messages.append({'role': 'tool', 'content': msg.content})

        # 调用 LLM（流式，带工具）
        try:
            stream = await self.provider_client.chat_completion(
                messages=api_messages,
                stream=True,
                tools=tools  # 传递工具定义
            )

            content_parts = []
            tool_calls = []
            usage = None

            async for chunk in stream:
                if chunk['type'] == 'content':
                    content = chunk['content']
                    content_parts.append(content)
                    await self.stream_writer.write_content(content)

                elif chunk['type'] == 'tool_call':
                    tool_call = chunk['tool_call']
                    tool_calls.append(tool_call)
                    await self.stream_writer.write_tool_call(
                        tool_call['name'],
                        tool_call['arguments']
                    )

                elif chunk['type'] == 'done':
                    usage = chunk.get('usage')

            # 组装完整内容
            full_content = ''.join(content_parts)

            # 创建 AI 消息
            ai_message = AIMessage(content=full_content)
            if tool_calls:
                ai_message.tool_calls = tool_calls

            state['messages'].append(ai_message)
            state['tool_calls'] = tool_calls

            return state

        except Exception as e:
            state['error'] = str(e)
            await self.stream_writer.write_error(str(e), type(e).__name__)
            return state

    async def _call_tools(self, state: AgentState) -> AgentState:
        """
        调用工具
        """
        tool_calls = state.get('tool_calls', [])

        for tool_call in tool_calls:
            tool_name = tool_call['name']
            arguments = tool_call['arguments']

            try:
                # 查找对应的 MCP 客户端
                result = await self._invoke_tool(tool_name, arguments)

                # 添加工具结果消息
                state['messages'].append(ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call.get('id', tool_name)
                ))

                await self.stream_writer.write_tool_result(tool_name, result)

            except Exception as e:
                # 工具调用失败
                error_msg = f"Tool {tool_name} failed: {str(e)}"
                state['messages'].append(ToolMessage(
                    content=error_msg,
                    tool_call_id=tool_call.get('id', tool_name)
                ))
                await self.stream_writer.write_error(error_msg, 'tool_error')

        # 清空 tool_calls
        state['tool_calls'] = []

        return state

    async def _get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取可用工具列表
        """
        all_tools = []

        for mcp_client in self.mcp_clients:
            try:
                tools = await mcp_client.discover_tools()
                all_tools.extend(tools)
            except Exception:
                # 忽略失败的 MCP 服务
                continue

        return all_tools

    async def _invoke_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        调用工具
        """
        # 遍历所有 MCP 客户端，找到对应的工具
        for mcp_client in self.mcp_clients:
            try:
                tools = await mcp_client.discover_tools()
                tool_names = [t['name'] for t in tools]

                if tool_name in tool_names:
                    result = await mcp_client.call_tool(tool_name, arguments)
                    return result

            except Exception:
                continue

        raise ValueError(f"Tool {tool_name} not found in any MCP server")


class AgentExecutorFactory:
    """
    Agent 执行器工厂
    """

    @staticmethod
    async def create_executor(
        agent_type: str,
        run_id: str,
        provider,
        provider_model,
        mcp_servers: List[Any],
        checkpointer: Optional[PostgresSaver] = None
    ) -> AgentExecutor:
        """
        创建 Agent 执行器
        """
        # 创建 provider 客户端
        provider_client = ProviderClientFactory.create_client(provider, provider_model)

        # 创建 MCP 客户端列表
        mcp_clients = []
        for server in mcp_servers:
            if server.enabled:
                try:
                    client = MCPClientFactory.create_client(server)
                    mcp_clients.append(client)
                except Exception:
                    # 忽略失败的 MCP 服务
                    continue

        # 创建流写入器
        stream_writer = RunStreamWriter(run_id)

        # 获取 Agent 类
        agent_class = AGENT_REGISTRY.get(agent_type)
        if not agent_class:
            raise ValueError(f"Unknown agent type: {agent_type}")

        # 创建执行器
        executor = agent_class(
            run_id=run_id,
            provider_client=provider_client,
            mcp_clients=mcp_clients,
            stream_writer=stream_writer,
            checkpointer=checkpointer
        )

        return executor
