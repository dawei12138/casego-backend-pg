import asyncio
import sys
import types
from types import SimpleNamespace


def _provider(**overrides):
    defaults = {
        'provider_id': 1,
        'provider_key': 'openai',
        'provider_name': 'OpenAI',
        'api_key': 'sk-secret',
        'api_secret': 'secret',
        'base_url': 'https://api.example.com/v1',
        'icon_url': None,
        'extra_params': {'metadata': {'source': 'test'}},
        'status': '1',
        'api_protocol': 'responses',
        'models': ['gpt-5.4', 'gpt-5.4-high'],
        'default_model': None,
        'thinking_levels': ['low', 'high', 'xhigh'],
    }
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_provider_options_return_enabled_model_metadata_without_secrets(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    db_module = types.ModuleType('config.get_db')
    db_module.get_db = lambda: None
    monkeypatch.setitem(sys.modules, 'config.get_db', db_module)
    from module_llm.llm_provider.dao import provider_config_dao
    from module_llm.llm_provider.service.provider_config_service import Provider_configService

    async def fake_options(_db):
        return [
            _provider(),
            _provider(provider_id=2, provider_key='disabled', status='0'),
        ]

    monkeypatch.setattr(provider_config_dao.Provider_configDao, 'get_provider_config_options', fake_options)

    result = asyncio.run(Provider_configService.get_provider_config_options_services(object()))

    assert len(result) == 1
    option = result[0].model_dump(by_alias=True)
    assert option['providerKey'] == 'openai'
    assert option['status'] == '1'
    assert option['apiProtocol'] == 'responses'
    assert option['models'] == ['gpt-5.4', 'gpt-5.4-high']
    assert option['defaultModel'] == 'gpt-5.4'
    assert option['thinkingLevels'] == ['low', 'high', 'xhigh']
    assert 'apiKey' not in option
    assert 'apiSecret' not in option
    assert 'extraParams' not in option


def test_provider_options_default_openai_chat_thinking_levels(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    db_module = types.ModuleType('config.get_db')
    db_module.get_db = lambda: None
    monkeypatch.setitem(sys.modules, 'config.get_db', db_module)
    from module_llm.llm_provider.dao import provider_config_dao
    from module_llm.llm_provider.service.provider_config_service import Provider_configService

    async def fake_options(_db):
        return [
            _provider(
                api_protocol='openai_chat',
                thinking_levels=None,
                models=['gpt-4.1'],
                default_model='gpt-4.1',
            ),
        ]

    monkeypatch.setattr(provider_config_dao.Provider_configDao, 'get_provider_config_options', fake_options)

    result = asyncio.run(Provider_configService.get_provider_config_options_services(object()))

    option = result[0].model_dump(by_alias=True)
    assert option['apiProtocol'] == 'openai_chat'
    assert option['thinkingLevels'] == ['low', 'medium', 'high', 'xhigh', 'max']


def test_provider_dao_ensures_model_metadata_columns(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    db_module = types.ModuleType('config.get_db')
    db_module.get_db = lambda: None
    monkeypatch.setitem(sys.modules, 'config.get_db', db_module)
    from module_llm.llm_provider.dao.provider_config_dao import Provider_configDao

    class FakeDb:
        def __init__(self):
            self.sql = []
            self.committed = False

        async def execute(self, statement):
            self.sql.append(str(statement))

        async def commit(self):
            self.committed = True

    fake_db = FakeDb()

    asyncio.run(Provider_configDao.ensure_provider_config_columns(fake_db))

    ddl = '\n'.join(fake_db.sql)
    assert 'ADD COLUMN IF NOT EXISTS api_protocol' in ddl
    assert 'ADD COLUMN IF NOT EXISTS models' in ddl
    assert 'ADD COLUMN IF NOT EXISTS default_model' in ddl
    assert 'ADD COLUMN IF NOT EXISTS thinking_levels' in ddl
    assert 'ADD COLUMN IF NOT EXISTS extra_params' in ddl
    assert fake_db.committed is True
