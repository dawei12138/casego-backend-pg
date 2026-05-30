import sys
import types
import asyncio
from types import SimpleNamespace


def test_binary_body_without_file_config_returns_none(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    get_db_module = types.ModuleType('config.get_db')
    get_db_module.get_db = None
    monkeypatch.setitem(sys.modules, 'config.get_db', get_db_module)

    from config.enums import Request_Type
    from utils.api_tools.executors.api_request_exector import APIExecutor

    context = SimpleNamespace(
        user_id=82,
        case_id=771,
        env_id=21,
        mysql_obj=None,
        redis_obj=None,
        parameterization=None,
        session=None,
        env_config=None,
    )
    test_case = SimpleNamespace(
        request_type=Request_Type.Binary,
        case_file_config=None,
    )

    executor = APIExecutor(test_case, context)

    assert asyncio.run(executor._build_request_body()) is None
