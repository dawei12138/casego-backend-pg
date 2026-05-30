from uuid import UUID


def test_protocol_helpers_normalize_new_protocols_and_legacy_aliases():
    from module_llm.llm_provider.provider_protocol import (
        API_PROTOCOL_OPENAI,
        API_PROTOCOL_OPENAI_COMPATIBLE,
        normalize_api_protocol,
    )

    assert normalize_api_protocol('openai') == API_PROTOCOL_OPENAI
    assert normalize_api_protocol('responses') == API_PROTOCOL_OPENAI
    assert normalize_api_protocol('openai_chat', provider_key='openai') == API_PROTOCOL_OPENAI
    assert normalize_api_protocol('openai_chat', provider_key='proxy') == API_PROTOCOL_OPENAI_COMPATIBLE
    assert normalize_api_protocol('OpenAI-Compatible') == API_PROTOCOL_OPENAI_COMPATIBLE
    assert normalize_api_protocol(None, provider_key='deepseek') == 'deepseek'
    assert normalize_api_protocol(None, provider_key='openrouter') == 'openrouter'


def test_protocol_helpers_default_models_thinking_levels_and_base_url_cleanup():
    from module_llm.llm_provider.provider_protocol import (
        THINKING_LEVELS,
        default_models_for_protocol,
        generate_provider_key,
        normalize_base_url,
    )

    assert THINKING_LEVELS == ('low', 'medium', 'high', 'xhigh', 'max')
    assert default_models_for_protocol('openai')[:3] == ['gpt-5', 'gpt-5-mini', 'gpt-5-nano']
    assert default_models_for_protocol('claude')[0] == 'claude-sonnet-4.5'
    assert default_models_for_protocol('gemini')[0] == 'gemini-2.5-flash'
    assert default_models_for_protocol('deepseek')[0] == 'deepseek-chat'
    assert default_models_for_protocol('openrouter')[0] == 'openai/gpt-5'
    assert normalize_base_url('https://api.openai.com/v1/chat/completions') == 'https://api.openai.com'
    assert normalize_base_url('https://api.openai.com/v1/responses/') == 'https://api.openai.com'
    assert normalize_base_url('https://openrouter.ai/api/v1/chat/completions') == 'https://openrouter.ai/api'
    assert str(UUID(generate_provider_key()))
