import sys
import types
from types import SimpleNamespace

from langchain_core.messages import AIMessageChunk


def _install_provider_stubs(monkeypatch):
    deepseek_module = types.ModuleType('langchain_deepseek')
    class FakeDeepSeek:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            for key, value in kwargs.items():
                setattr(self, key, value)

    deepseek_module.ChatDeepSeek = FakeDeepSeek
    google_module = types.ModuleType('langchain_google_genai')
    google_module.ChatGoogleGenerativeAI = type('ChatGoogleGenerativeAI', (), {})
    monkeypatch.setitem(sys.modules, 'langchain_deepseek', deepseek_module)
    monkeypatch.setitem(sys.modules, 'langchain_google_genai', google_module)
    log_module = types.ModuleType('utils.log_util')
    log_module.logger = SimpleNamespace(info=lambda *args, **kwargs: None, warning=lambda *args, **kwargs: None)
    monkeypatch.setitem(sys.modules, 'utils.log_util', log_module)


def _provider(**overrides):
    defaults = {
        'provider_key': 'openai',
        'provider_name': 'OpenAI',
        'api_key': 'sk-test',
        'base_url': 'https://api.example.com/v1',
        'timeout': 30,
        'max_retries': 2,
        'extra_headers': {'X-Test': '1'},
        'api_protocol': 'responses',
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_model_factory_uses_responses_protocol_and_thinking_level(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    model = model_factory.create_chat_model(
        _provider(),
        'gpt-5.4',
        enable_thinking=True,
        thinking_level='xhigh',
    )

    assert isinstance(model, model_factory._OpenAIResponsesStable)
    assert model.model_name == 'gpt-5.4'
    assert model.use_responses_api is True
    assert model.reasoning == {'effort': 'xhigh'}
    assert model.extra_body is None


def test_openai_chat_protocol_does_not_auto_switch_to_responses_for_gpt5(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    model = model_factory.create_chat_model(
        _provider(provider_key='openai', api_protocol='openai_chat'),
        'gpt-5-thinking',
        enable_thinking=True,
        thinking_level='xhigh',
    )

    assert isinstance(model, model_factory._OpenAIChatWithReasoning)
    assert model.use_responses_api is False
    assert model.reasoning is None
    assert model.reasoning_effort == 'high'
    assert model.extra_body is None


def test_responses_completed_chunk_with_null_output_is_normalized(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    chunk = SimpleNamespace(
        type='response.completed',
        response=SimpleNamespace(output=None),
    )

    assert model_factory._ensure_responses_chunk_output_list(chunk) is True
    assert chunk.response.output == []


def test_model_factory_uses_native_gemini_protocol(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    captured = {}

    class FakeGemini:
        def __init__(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(model_factory, 'ChatGoogleGenerativeAI', FakeGemini)

    result = model_factory.create_chat_model(
        _provider(provider_key='google', api_protocol='gemini'),
        'gemini-3-pro-preview',
        enable_thinking=True,
        thinking_level='max',
    )

    assert isinstance(result, FakeGemini)
    assert captured['model'] == 'gemini-3-pro-preview'
    assert captured['google_api_key'] == 'sk-test'
    assert captured['thinking_budget'] == 32000
    assert captured['include_thoughts'] is True


def test_model_factory_uses_claude_opus_47_adaptive_thinking_effort(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    captured = {}

    def fake_init_chat_model(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(**kwargs)

    monkeypatch.setattr(model_factory, 'init_chat_model', fake_init_chat_model)

    model_factory.create_chat_model(
        _provider(
            provider_key='claude',
            api_protocol='claude',
            base_url='https://claude-proxy.example.com/v1/messages',
        ),
        'claude-opus-4.7',
        enable_thinking=True,
        thinking_level='medium',
    )

    assert captured['model'] == 'claude-opus-4.7'
    assert captured['model_provider'] == 'anthropic'
    assert captured['base_url'] == 'https://claude-proxy.example.com'
    assert captured['thinking'] == {'type': 'adaptive', 'display': 'summarized'}
    assert captured['effort'] == 'medium'
    assert captured['output_config'] == {'effort': 'medium'}
    assert 'temperature' not in captured


def test_model_factory_keeps_claude_selected_max_above_extra_params(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    captured = {}

    def fake_init_chat_model(**kwargs):
        captured.update(kwargs)
        return SimpleNamespace(**kwargs)

    monkeypatch.setattr(model_factory, 'init_chat_model', fake_init_chat_model)

    model_factory.create_chat_model(
        _provider(
            provider_key='claude',
            api_protocol='claude',
            base_url='https://claude-proxy.example.com',
            extra_params={
                'effort': 'xhigh',
                'thinking': {'type': 'enabled', 'budget_tokens': 16000},
                'output_config': {'effort': 'xhigh', 'task_budget': {'type': 'tokens', 'total': 128000}},
                'betas': ['task-budgets-2026-03-13'],
            },
        ),
        'claude-opus-4.7',
        enable_thinking=True,
        thinking_level='max',
    )

    assert captured['thinking'] == {'type': 'adaptive', 'display': 'summarized'}
    assert captured['effort'] == 'max'
    assert captured['output_config'] == {
        'effort': 'max',
        'task_budget': {'type': 'tokens', 'total': 128000},
    }
    assert captured['model_kwargs'] == {'betas': ['task-budgets-2026-03-13']}


def test_openai_chat_model_preserves_reasoning_content_stream_delta(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    model = model_factory.create_chat_model(
        _provider(provider_key='112233', api_protocol='openai_chat'),
        'deepseek-v4-pro',
        enable_thinking=True,
        thinking_level='max',
    )

    chunk = {
        'choices': [
            {
                'delta': {
                    'role': 'assistant',
                    'reasoning_content': '先分析问题',
                },
                'finish_reason': None,
            }
        ]
    }

    generation = model._convert_chunk_to_generation_chunk(chunk, AIMessageChunk, {})

    assert generation.message.additional_kwargs['reasoning_content'] == '先分析问题'
    assert generation.message.content == ''


def test_deepseek_protocol_does_not_depend_on_provider_key(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_provider_stubs(monkeypatch)
    from module_llm.chat_agent import model_factory

    result = model_factory.create_chat_model(
        _provider(provider_key='7e0f0d1a-6f4a-4884-8ea1-977c0d502134', api_protocol='deepseek'),
        'deepseek-reasoner',
        enable_thinking=False,
        thinking_level=None,
    )

    assert isinstance(result, model_factory._DeepSeekWithThinking)
    assert result.kwargs['model'] == 'deepseek-reasoner'
    assert result.is_thinking is True
