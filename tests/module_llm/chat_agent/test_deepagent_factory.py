import asyncio
import pytest
import sys

from deepagents.backends import CompositeBackend


def test_create_deep_agent_uses_backend_instance(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    from module_llm.chat_agent import deepagent_factory

    captured = {}

    async def fake_checkpointer():
        return object()

    def fake_create_deep_agent(**kwargs):
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(deepagent_factory, 'get_checkpointer', fake_checkpointer)
    monkeypatch.setattr(deepagent_factory, 'build_search_subagent', lambda model: {'name': 'search-agent'})
    monkeypatch.setattr(deepagent_factory, 'create_deep_agent', fake_create_deep_agent)

    asyncio.run(
        deepagent_factory.create_deep_agent_instance(
            model=object(),
            user_id=1,
            thread_id='thread-a',
            tools=[],
            skills_paths=['/skills/'],
            allowed_skill_names={'best-minds'},
        )
    )

    assert isinstance(captured['backend'], CompositeBackend)
    assert '/skills/' in captured['backend'].routes
