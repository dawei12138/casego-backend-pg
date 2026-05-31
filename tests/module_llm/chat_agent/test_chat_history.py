import asyncio
import sys
from types import SimpleNamespace

from langchain_core.messages import AIMessage, HumanMessage


def test_read_messages_from_checkpoint_replays_deep_agent_delta_messages(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    try:
        from module_llm.chat_agent.controller import chat_controller

        class FakeCheckpointer:
            async def aget_tuple(self, config):
                return SimpleNamespace(
                    config={
                        'configurable': {
                            'thread_id': config['configurable']['thread_id'],
                            'checkpoint_ns': '',
                            'checkpoint_id': 'checkpoint-1',
                        }
                    },
                    checkpoint={
                        'v': 4,
                        'id': 'checkpoint-1',
                        'ts': '2026-05-30T16:30:07.061430+00:00',
                        'channel_values': {},
                        'channel_versions': {},
                        'updated_channels': [],
                    },
                )

            async def aget_delta_channel_history(self, *, config, channels):
                assert channels == ['messages']
                return {
                    'messages': {
                        'writes': [
                            ('task-user', 'messages', [HumanMessage(content='111')]),
                            ('task-ai', 'messages', [AIMessage(content='收到')]),
                        ]
                    }
                }

        result = asyncio.run(
            chat_controller._read_messages_from_checkpoint(
                FakeCheckpointer(),
                {'configurable': {'thread_id': 'thread-a'}},
            )
        )

        assert [type(msg).__name__ for msg in result] == ['HumanMessage', 'AIMessage']
        assert [msg.content for msg in result] == ['111', '收到']
    finally:
        import module_llm.chat_agent as chat_agent_pkg

        if hasattr(chat_agent_pkg, 'model_factory'):
            delattr(chat_agent_pkg, 'model_factory')
        for module_name in [
            'module_llm.chat_agent.controller.chat_controller',
            'module_llm.chat_agent.controller.stream_helpers',
            'module_llm.chat_agent.model_factory',
        ]:
            sys.modules.pop(module_name, None)
