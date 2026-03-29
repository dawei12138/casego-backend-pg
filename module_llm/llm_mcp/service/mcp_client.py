# -*- coding: utf-8 -*-
"""
MCP (Model Context Protocol) 客户端
支持 stdio、http、sse 三种 transport
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
from enum import Enum
import subprocess
import httpx
from datetime import datetime, timedelta

from module_llm.llm_mcp.entity.do.mcp_server_do import LlmMcpServer


class TransportType(str, Enum):
    """Transport 类型"""
    STDIO = 'stdio'
    HTTP = 'http'
    SSE = 'sse'


class MCPClientError(Exception):
    """MCP 客户端错误"""
    pass


class MCPClient:
    """
    MCP 客户端基类
    """

    def __init__(self, server: LlmMcpServer):
        self.server = server
        self.tools_cache: Optional[List[Dict[str, Any]]] = None
        self.cache_time: Optional[datetime] = None
        self.cache_ttl = timedelta(minutes=5)  # 缓存5分钟

    async def discover_tools(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """
        发现工具列表
        """
        # 检查缓存
        if not force_refresh and self.tools_cache and self.cache_time:
            if datetime.now() - self.cache_time < self.cache_ttl:
                return self.tools_cache

        # 调用实现
        tools = await self._discover_tools_impl()

        # 更新缓存
        self.tools_cache = tools
        self.cache_time = datetime.now()

        return tools

    async def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        timeout: int = 300,  # 5分钟超时
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        调用工具（带重试）
        """
        last_error = None

        for attempt in range(max_retries):
            try:
                result = await asyncio.wait_for(
                    self._call_tool_impl(tool_name, arguments),
                    timeout=timeout
                )
                return result

            except asyncio.TimeoutError as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise MCPClientError(f'Tool call timeout after {timeout}s') from e
                # 重试前等待
                await asyncio.sleep(1 * (attempt + 1))

            except Exception as e:
                last_error = e
                if attempt == max_retries - 1:
                    raise MCPClientError(f'Tool call failed: {str(e)}') from e
                # 重试前等待
                await asyncio.sleep(1 * (attempt + 1))

        raise MCPClientError(f'Tool call failed after {max_retries} retries') from last_error

    async def test_connection(self) -> bool:
        """
        测试连接
        """
        try:
            tools = await self.discover_tools(force_refresh=True)
            return len(tools) >= 0  # 只要能获取工具列表就算成功
        except Exception:
            return False

    async def _discover_tools_impl(self) -> List[Dict[str, Any]]:
        """
        发现工具实现（子类重写）
        """
        raise NotImplementedError

    async def _call_tool_impl(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用工具实现（子类重写）
        """
        raise NotImplementedError


class StdioMCPClient(MCPClient):
    """
    Stdio Transport MCP 客户端
    """

    def __init__(self, server: LlmMcpServer):
        super().__init__(server)
        self.process: Optional[subprocess.Popen] = None
        self.request_id = 0

    async def _start_process(self):
        """
        启动子进程
        """
        if self.process and self.process.poll() is None:
            return  # 进程已运行

        config = self.server.config or {}
        command = config.get('command')
        args = config.get('args', [])
        env = config.get('env', {})

        if not command:
            raise MCPClientError('Stdio transport requires command in config')

        # 启动进程
        self.process = subprocess.Popen(
            [command] + args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1
        )

    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送 JSON-RPC 请求
        """
        await self._start_process()

        self.request_id += 1
        request = {
            'jsonrpc': '2.0',
            'id': self.request_id,
            'method': method,
            'params': params
        }

        # 发送请求
        request_line = json.dumps(request) + '\n'
        self.process.stdin.write(request_line)
        self.process.stdin.flush()

        # 读取响应
        response_line = self.process.stdout.readline()
        if not response_line:
            raise MCPClientError('No response from MCP server')

        response = json.loads(response_line)

        # 检查错误
        if 'error' in response:
            error = response['error']
            raise MCPClientError(f"MCP error: {error.get('message', 'Unknown error')}")

        return response.get('result', {})

    async def _discover_tools_impl(self) -> List[Dict[str, Any]]:
        """
        发现工具
        """
        result = await self._send_request('tools/list', {})
        return result.get('tools', [])

    async def _call_tool_impl(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用工具
        """
        result = await self._send_request('tools/call', {
            'name': tool_name,
            'arguments': arguments
        })
        return result

    def __del__(self):
        """
        清理进程
        """
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait(timeout=5)


class HttpMCPClient(MCPClient):
    """
    HTTP Transport MCP 客户端
    """

    def __init__(self, server: LlmMcpServer):
        super().__init__(server)
        self.client = httpx.AsyncClient(timeout=30.0)
        self.request_id = 0

    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送 HTTP 请求
        """
        config = self.server.config or {}
        url = config.get('url')

        if not url:
            raise MCPClientError('HTTP transport requires url in config')

        self.request_id += 1
        request = {
            'jsonrpc': '2.0',
            'id': self.request_id,
            'method': method,
            'params': params
        }

        # 发送请求
        response = await self.client.post(url, json=request)
        response.raise_for_status()

        result = response.json()

        # 检查错误
        if 'error' in result:
            error = result['error']
            raise MCPClientError(f"MCP error: {error.get('message', 'Unknown error')}")

        return result.get('result', {})

    async def _discover_tools_impl(self) -> List[Dict[str, Any]]:
        """
        发现工具
        """
        result = await self._send_request('tools/list', {})
        return result.get('tools', [])

    async def _call_tool_impl(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用工具
        """
        result = await self._send_request('tools/call', {
            'name': tool_name,
            'arguments': arguments
        })
        return result

    async def close(self):
        """
        关闭客户端
        """
        await self.client.aclose()


class SseMCPClient(MCPClient):
    """
    SSE Transport MCP 客户端
    """

    def __init__(self, server: LlmMcpServer):
        super().__init__(server)
        self.client = httpx.AsyncClient(timeout=30.0)
        self.request_id = 0

    async def _send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        发送 SSE 请求
        """
        config = self.server.config or {}
        url = config.get('url')

        if not url:
            raise MCPClientError('SSE transport requires url in config')

        self.request_id += 1
        request = {
            'jsonrpc': '2.0',
            'id': self.request_id,
            'method': method,
            'params': params
        }

        # 发送请求并接收 SSE 流
        async with self.client.stream('POST', url, json=request) as response:
            response.raise_for_status()

            result_data = None

            async for line in response.aiter_lines():
                if line.startswith('data: '):
                    data = line[6:]  # 去掉 "data: " 前缀
                    if data == '[DONE]':
                        break

                    try:
                        event = json.loads(data)
                        # 累积结果
                        if 'result' in event:
                            result_data = event['result']
                        elif 'error' in event:
                            error = event['error']
                            raise MCPClientError(f"MCP error: {error.get('message', 'Unknown error')}")
                    except json.JSONDecodeError:
                        continue

            if result_data is None:
                raise MCPClientError('No result received from SSE stream')

            return result_data

    async def _discover_tools_impl(self) -> List[Dict[str, Any]]:
        """
        发现工具
        """
        result = await self._send_request('tools/list', {})
        return result.get('tools', [])

    async def _call_tool_impl(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用工具
        """
        result = await self._send_request('tools/call', {
            'name': tool_name,
            'arguments': arguments
        })
        return result

    async def close(self):
        """
        关闭客户端
        """
        await self.client.aclose()


class MCPClientFactory:
    """
    MCP 客户端工厂
    """

    @staticmethod
    def create_client(server: LlmMcpServer) -> MCPClient:
        """
        根据 transport 类型创建客户端
        """
        transport = server.transport_type.lower()

        if transport == TransportType.STDIO:
            return StdioMCPClient(server)
        elif transport == TransportType.HTTP:
            return HttpMCPClient(server)
        elif transport == TransportType.SSE:
            return SseMCPClient(server)
        else:
            raise ValueError(f'Unsupported transport type: {transport}')
