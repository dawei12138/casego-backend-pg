# -*- coding: utf-8 -*-
"""
搜索子 Agent - 专门负责互联网搜索任务

功能：
  - 使用 Tavily API 进行联网搜索
  - 独立于主 Agent 的 enable_web_search 开关
  - 主 Agent 可通过 task(name="search-agent", task="...") 委派搜索任务
  - 子 Agent 内部执行多次搜索，仅返回精炼摘要，保持主 Agent 上下文干净

使用场景：
  - 主 Agent 未开启联网搜索时，仍可通过子 Agent 搜索
  - 需要多步骤搜索并整合结果的复杂查询
  - 避免搜索结果污染主 Agent 的上下文窗口
"""
import json
from typing import Literal

from langchain_core.tools import tool

from config.env import LLMConfig
from utils.log_util import logger


# ── 子 Agent 专属工具 ────────────────────────────────────────────

@tool
def web_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
) -> str:
    """搜索互联网获取最新信息。

    Args:
        query: 搜索关键词或问题
        max_results: 返回结果数量（1-10），默认5条
        topic: 搜索类型 - general(通用), news(新闻), finance(财经)
        include_raw_content: 是否包含原始网页内容（用于深度分析）
    """
    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=LLMConfig.TAVILY_API_KEY)
        response = client.search(
            query=query,
            max_results=max_results,
            topic=topic,
            include_raw_content=include_raw_content,
        )
        results = []
        for item in response.get("results", []):
            entry = {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", ""),
            }
            if include_raw_content and item.get("raw_content"):
                entry["raw_content"] = item["raw_content"][:2000]
            results.append(entry)
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"[SearchAgent] 联网搜索失败: {e}")
        return f"搜索失败: {str(e)}"


# ── 子 Agent 系统提示词 ──────────────────────────────────────────

SEARCH_AGENT_SYSTEM_PROMPT = """你是一个专业的互联网搜索研究助手。你的职责是：

1. 分析用户的搜索需求，拆解为合适的搜索关键词
2. 使用 web_search 工具执行搜索
3. 如果首次搜索结果不够全面，可以用不同关键词进行多次搜索
4. 综合所有搜索结果，提炼出准确、有用的信息

输出要求：
- 用清晰的结构化格式返回结果
- 包含关键发现（要点列表）
- 引用信息来源（附 URL）
- 保持简洁，总字数控制在 500 字以内
- 使用中文回答（除非用户明确要求其他语言）

注意事项：
- 优先搜索最新信息
- 对于模糊查询，先搜索一次了解大致方向，再精确搜索
- 区分事实和观点，标注不确定的信息
"""


# ── 构建函数 ─────────────────────────────────────────────────────

def build_search_subagent(model=None) -> dict:
    """构建搜索子 Agent 配置字典。

    :param model: 可选，指定子 Agent 使用的模型（默认继承主 Agent 模型）
    :return: 符合 deepagents subagent 规范的字典
    """
    config = {
        "name": "search-agent",
        "description": (
            "专业互联网搜索助手。当需要查询实时信息、最新新闻、技术文档、"
            "产品信息或任何需要联网获取的数据时，委派给此 Agent。"
            "它会执行多步骤搜索并返回精炼摘要。"
        ),
        "system_prompt": SEARCH_AGENT_SYSTEM_PROMPT,
        "tools": [web_search],
    }
    if model is not None:
        config["model"] = model
    return config
