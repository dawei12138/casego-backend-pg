import asyncio
import sys
import types

from sqlalchemy.dialects import postgresql


def _install_get_db_stub(monkeypatch):
    get_db_module = types.ModuleType('config.get_db')
    get_db_module.get_db = lambda: None
    monkeypatch.setitem(sys.modules, 'config.get_db', get_db_module)


def test_thread_list_orders_by_recent_update_time(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_get_db_stub(monkeypatch)
    from module_llm.chat_thread.dao import thread_dao

    captured = {}

    async def fake_paginate(db, query, page_num, page_size, is_page=False):
        captured['sql'] = str(
            query.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={'literal_binds': True},
            )
        )
        return []

    monkeypatch.setattr(thread_dao.PageUtil, 'paginate', fake_paginate)

    asyncio.run(
        thread_dao.ThreadDao.get_thread_list(
            object(),
            thread_dao.ThreadPageQueryModel(user_id=1),
            is_page=False,
        )
    )

    assert 'ORDER BY llm_chat_thread.update_time DESC, llm_chat_thread.create_time DESC' in captured['sql']


def test_touch_thread_updates_update_time(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    _install_get_db_stub(monkeypatch)
    from module_llm.chat_thread.dao import thread_dao

    captured = {}

    class FakeDb:
        async def execute(self, statement):
            captured['sql'] = str(
                statement.compile(
                    dialect=postgresql.dialect(),
                    compile_kwargs={'literal_binds': True},
                )
            )

    asyncio.run(thread_dao.ThreadDao.touch_thread_dao(FakeDb(), '11111111-1111-1111-1111-111111111111'))

    assert 'UPDATE llm_chat_thread SET update_time=' in captured['sql']
    assert "WHERE llm_chat_thread.thread_id = '11111111-1111-1111-1111-111111111111'" in captured['sql']
