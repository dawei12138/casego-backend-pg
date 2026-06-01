import asyncio
import sys

from sqlalchemy.dialects import postgresql


def test_gen_table_list_orders_by_recent_update_time(monkeypatch):
    monkeypatch.setattr(sys, 'argv', [sys.argv[0]])
    from module_generator.dao import gen_dao
    from module_generator.entity.vo.gen_vo import GenTablePageQueryModel

    captured = {}

    async def fake_paginate(db, query, page_num, page_size, is_page=False):
        captured['sql'] = str(
            query.compile(
                dialect=postgresql.dialect(),
                compile_kwargs={'literal_binds': True},
            )
        )
        return []

    monkeypatch.setattr(gen_dao.PageUtil, 'paginate', fake_paginate)

    asyncio.run(
        gen_dao.GenTableDao.get_gen_table_list(
            object(),
            GenTablePageQueryModel(pageNum=1, pageSize=10),
            is_page=True,
        )
    )

    assert (
        'ORDER BY gen_table.update_time DESC NULLS LAST, '
        'gen_table.create_time DESC NULLS LAST, gen_table.table_id DESC'
    ) in captured['sql']
