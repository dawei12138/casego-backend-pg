from uuid import UUID


def test_protocol_helpers_normalize_new_protocols_and_legacy_aliases():
    from module_llm.llm_provider.provider_protocol import (
        API_PROTOCOL_OPENAI_CHAT,
        API_PROTOCOL_OPENAI_COMPATIBLE,
        API_PROTOCOL_RESPONSES,
        normalize_api_protocol,
    )

    assert normalize_api_protocol('openai') == API_PROTOCOL_OPENAI_CHAT
    assert normalize_api_protocol('responses') == API_PROTOCOL_RESPONSES
    assert normalize_api_protocol('openai_chat', provider_key='openai') == API_PROTOCOL_OPENAI_CHAT
    assert normalize_api_protocol('openai_chat', provider_key='proxy') == API_PROTOCOL_OPENAI_CHAT
    assert normalize_api_protocol('OpenAI-Compatible') == API_PROTOCOL_OPENAI_COMPATIBLE
    assert normalize_api_protocol(None, provider_key='deepseek') == 'deepseek'
    assert normalize_api_protocol(None, provider_key='openrouter') == 'openrouter'


def test_protocol_helpers_default_models_thinking_levels_and_base_url_cleanup():
    from module_llm.llm_provider.provider_protocol import (
        THINKING_LEVELS,
        default_models_for_protocol,
        generate_provider_key,
        normalize_base_url,
        normalize_thinking_levels,
    )

    assert THINKING_LEVELS == ('low', 'medium', 'high', 'xhigh', 'max')
    assert default_models_for_protocol('openai_chat')[:2] == ['gpt-4.1', 'gpt-4.1-mini']
    assert default_models_for_protocol('responses')[:3] == ['gpt-5', 'gpt-5-mini', 'gpt-5-nano']
    assert normalize_thinking_levels(['xhigh'], 'openai_chat') == ['xhigh']
    assert normalize_thinking_levels(None, 'openai_chat') == ['low', 'medium', 'high', 'xhigh', 'max']
    assert normalize_thinking_levels(None, 'responses') == ['low', 'medium', 'high', 'xhigh', 'max']
    assert default_models_for_protocol('claude')[0] == 'claude-sonnet-4.5'
    assert default_models_for_protocol('gemini')[0] == 'gemini-2.5-flash'
    assert default_models_for_protocol('deepseek')[0] == 'deepseek-chat'
    assert default_models_for_protocol('openrouter')[0] == 'openai/gpt-5'
    assert normalize_base_url('https://api.openai.com/v1/chat/completions') == 'https://api.openai.com'
    assert normalize_base_url('https://api.openai.com/v1/responses/') == 'https://api.openai.com'
    assert normalize_base_url('https://openrouter.ai/api/v1/chat/completions') == 'https://openrouter.ai/api'
    assert normalize_base_url('https://claude-proxy.example.com/v1/messages') == 'https://claude-proxy.example.com'
    assert str(UUID(generate_provider_key()))
