# -*- coding: utf-8 -*-
"""
Agent 通用工具集 - 适配 deepagents

在此定义可绑定到 deep agent 的工具函数，使用 @tool 装饰器注册。
所有工具通过 get_tools() 统一导出，供 deepagent_factory 使用。

工具分为两类:
  1. 内置工具 (静态): get_current_time, delete_file 等
  2. MCP 工具 (异步): 从 MCP 服务器动态加载
  3. 联网搜索工具 (可选): 基于 Tavily API，需前端开启

注意：deepagents 自动提供文件系统工具（ls, read_file, write_file, edit_file, glob, grep）
     和 Skills 工具，无需手动添加。
"""
import json
import os
import platform
from datetime import datetime
from pathlib import Path
from typing import Literal, Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from config.env import LLMConfig
from module_llm.chat_agent.mcp.loader import load_mcp_tools
from utils.log_util import logger

# Skills 虚拟路径前缀与真实根目录（与 deepagent_factory 保持一致）
_SKILLS_VIRTUAL_PREFIX = "/skills/"
_SKILLS_ROOT = os.path.join("CaseGo", "skills")


# ── AskUserQuestion 工具的输入模式 ──

class _AskUserOption(BaseModel):
    """问题选项"""
    label: str = Field(description="选项显示文本（1-5个词）")
    description: str = Field(description="选项说明")


class _AskUserQuestionItem(BaseModel):
    """单个问题"""
    question: str = Field(description="完整的问题文本")
    header: str = Field(description="简短标签（最多12个字符）")
    options: list[_AskUserOption] = Field(description="2-6个选项")
    multi_select: bool = Field(default=False, description="是否允许多选")


class _AskUserInput(BaseModel):
    """ask_user_question 工具的输入模式"""
    questions: list[_AskUserQuestionItem] = Field(description="1-10个问题列表")


@tool
def get_current_time() -> str:
    """获取当前系统时间，返回格式为 YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
) -> str:
    """搜索互联网获取最新信息。可用于查询实时数据、新闻、技术文档等。

    Args:
        query: 搜索关键词
        max_results: 返回结果数量，默认5条
        topic: 搜索类型 - general(通用), news(新闻), finance(财经)
    """
    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=LLMConfig.TAVILY_API_KEY)
        response = client.search(
            query=query,
            max_results=max_results,
            topic=topic,
        )
        # 格式化结果，只保留关键字段
        results = []
        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            })
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"联网搜索失败: {e}")
        return f"搜索失败: {str(e)}"


@tool(args_schema=_AskUserInput)
def ask_user_question(questions: list) -> str:
    """向用户提问并等待回答。当你需要以下场景时使用此工具：
    1. 用户输入的关键词包含采访时
    2. 获取用户偏好或决策
    3. 让用户在多个实现方案中做选择
    4. 收集用户对实现方向的意见

    工具会暂停执行并向用户展示问题界面，用户回答后继续执行。
    用户始终可以选择"其他"来提供自定义文本输入。

    Args:
        questions: 1-10个问题的列表，每个问题包含：
            - question: 完整的问题文本
            - header: 简短标签（最多12个字符）
            - options: 2-6个选项，每个选项包含 label（显示文本）和 description（说明）
            - multi_select: 是否允许多选（默认 false）
    """
    from langgraph.types import interrupt

    # 将 Pydantic 模型转为 dict 以便序列化
    questions_data = []
    for q in questions:
        if hasattr(q, 'model_dump'):
            questions_data.append(q.model_dump())
        elif isinstance(q, dict):
            questions_data.append(q)
        else:
            questions_data.append({"question": str(q), "header": "问题", "options": [], "multi_select": False})

    # 中断图执行，等待用户回答
    # 首次调用：暂停图执行，interrupt_value 传递给前端
    # 恢复时：返回用户的回答
    response = interrupt({"questions": questions_data})

    if isinstance(response, dict):
        return json.dumps(response, ensure_ascii=False)
    return str(response)


@tool
def resolve_skills_path(virtual_path: str) -> str:
    """将 /skills/ 虚拟路径解析为操作系统上的真实绝对路径。

    Skills 目录通过虚拟挂载对 Agent 可见，但 shell 命令需要真实路径才能访问文件。
    此工具将虚拟路径转换为当前操作系统的绝对路径，自动处理 Windows/Linux 差异。

    Args:
        virtual_path: 以 /skills/ 开头的虚拟路径，例如 /skills/playwright-cli/cli.config.json
    """
    # 标准化输入：去除首尾空白，统一正斜杠
    cleaned = virtual_path.strip().replace("\\", "/")

    # 校验必须以 /skills/ 开头
    if not cleaned.startswith(_SKILLS_VIRTUAL_PREFIX):
        return f"错误: 路径必须以 {_SKILLS_VIRTUAL_PREFIX} 开头，收到: {virtual_path}"

    # 提取 /skills/ 之后的相对部分
    relative = cleaned[len(_SKILLS_VIRTUAL_PREFIX):]

    # 防止路径遍历攻击
    if ".." in relative.split("/"):
        return f"错误: 路径中不允许包含 '..'，收到: {virtual_path}"

    # 构建真实绝对路径：项目根目录 / CaseGo/skills / 相对路径
    project_root = Path(__file__).resolve().parent.parent.parent  # tools.py -> chat_agent -> module_llm -> 项目根
    real_path = project_root / _SKILLS_ROOT / relative

    # 检查文件/目录是否存在
    if not real_path.exists():
        return f"警告: 路径不存在 - {real_path}"

    # 返回当前操作系统格式的绝对路径
    return str(real_path)


def get_builtin_tools(enable_web_search: bool = False) -> list:
    """返回静态内置工具列表（启用错误处理）

    :param enable_web_search: 是否包含联网搜索工具
    """
    tools = [get_current_time, ask_user_question]
    if enable_web_search:
        tools.append(internet_search)
    # 为内置工具也启用错误处理，避免工具异常导致对话终止
    for t in tools:
        t.handle_tool_error = True
    return tools


async def get_tools(mcp_tools: list = None, enable_web_search: bool = False) -> list:
    """
    组装完整的工具列表（异步，因 MCP 工具需要异步加载）。

    :param mcp_tools: 外部传入的 MCP 工具列表（由 mcp_tools_context() 提供，session 持久有效）。
                      若为 None，则内部调用 load_mcp_tools() 加载（每次工具调用重建进程，
                      浏览器状态不保持）。
    :param enable_web_search: 是否包含联网搜索工具
    :return:          所有可用工具的列表
    """
    tools = get_builtin_tools(enable_web_search=enable_web_search)

    # MCP 工具：优先使用外部传入的持久 session 工具，否则降级加载
    if mcp_tools is not None:
        tools.extend(mcp_tools)
    else:
        tools.extend(await load_mcp_tools())

    return tools
