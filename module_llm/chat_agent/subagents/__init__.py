# -*- coding: utf-8 -*-
"""
子 Agent 模块

所有自定义子 Agent 在此注册，统一导出供 deepagent_factory 使用。
每个子 Agent 单独一个文件，保持隔离和可维护性。
"""
from module_llm.chat_agent.subagents.search_agent import build_search_subagent

__all__ = ["build_search_subagent"]
