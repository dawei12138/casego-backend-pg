from module_llm.llm_memory.dao.memory_dao import MemoryDao


class MemoryService:
    @staticmethod
    async def get_memory_overview(query_db, session_id: str | None = None, memory_type: str | None = None, source_run_id: str | None = None):
        return await MemoryDao.list_memory_items(query_db, session_id, memory_type, source_run_id)

    @staticmethod
    async def get_memory_detail(query_db, memory_id: str):
        return await MemoryDao.get_memory_detail(query_db, memory_id)

    @staticmethod
    async def create_memory(query_db, data):
        result = await MemoryDao.create_memory(query_db, data)
        await query_db.commit()
        return result

    @staticmethod
    async def delete_memory(query_db, memory_id: str, data):
        result = await MemoryDao.delete_memory(query_db, memory_id, data)
        await query_db.commit()
        return result
