import sys
import types
from uuid import UUID


def _install_get_db_stub(monkeypatch):
    get_db_module = types.ModuleType('config.get_db')
    get_db_module.get_db = lambda: None
    monkeypatch.setitem(sys.modules, 'config.get_db', get_db_module)


def test_provider_config_normalization_auto_generates_key_and_defaults(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_get_db_stub(monkeypatch)
    from module_llm.llm_provider.entity.vo.provider_config_vo import Provider_configModel
    from module_llm.llm_provider.service.provider_config_service import Provider_configService

    model = Provider_configModel(
        providerName='OpenAI Responses',
        apiProtocol='responses',
        baseUrl='https://api.openai.com/v1/responses',
        models=[],
        defaultModel=None,
        thinkingLevels=None,
    )

    normalized = Provider_configService._normalize_provider_config(model)

    assert str(UUID(normalized.provider_key))
    assert normalized.api_protocol == 'responses'
    assert normalized.base_url == 'https://api.openai.com'
    assert normalized.models[:3] == ['gpt-5', 'gpt-5-mini', 'gpt-5-nano']
    assert normalized.default_model == 'gpt-5'
    assert normalized.thinking_levels == ['low', 'medium', 'high', 'xhigh', 'max']


def test_provider_config_normalization_keeps_existing_key_on_edit(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_get_db_stub(monkeypatch)
    from module_llm.llm_provider.entity.vo.provider_config_vo import Provider_configModel
    from module_llm.llm_provider.service.provider_config_service import Provider_configService

    model = Provider_configModel(
        providerId=10,
        providerKey='existing-key',
        providerName='OpenRouter',
        apiProtocol='openrouter',
        models=['anthropic/claude-opus-4.8'],
        defaultModel=None,
        thinkingLevels=['medium'],
    )

    normalized = Provider_configService._normalize_provider_config(model)

    assert normalized.provider_key == 'existing-key'
    assert normalized.api_protocol == 'openrouter'
    assert normalized.default_model == 'anthropic/claude-opus-4.8'
    assert normalized.thinking_levels == ['medium']
