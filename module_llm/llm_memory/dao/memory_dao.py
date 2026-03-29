import uuid

from sqlalchemy import select, update

from module_llm.llm_memory.entity.do.memory_item_do import LlmMemoryItem
from module_llm.llm_memory.entity.vo.memory_vo import MemoryCreateModel, MemoryDeleteModel, MemoryItemModel


class MemoryDao:
    @staticmethod
    async def list_memory_items(query_db, session_id: str | None = None, memory_type: str | None = None, source_run_id: str | None = None):
        query = select(LlmMemoryItem).where(LlmMemoryItem.del_flag == '0', LlmMemoryItem.is_deleted.is_(False))
        if session_id:
            query = query.where(LlmMemoryItem.session_id == session_id)
        if memory_type:
            query = query.where(LlmMemoryItem.memory_type == memory_type)
        if source_run_id:
            query = query.where(LlmMemoryItem.source_run_id == source_run_id)
        result = (await query_db.execute(query.order_by(LlmMemoryItem.create_time.desc()))).scalars().all()
        return [
            MemoryItemModel(
                memory_id=item.memory_id,
                memory_type=item.memory_type,
                session_id=item.session_id,
                run_id=item.run_id,
                content=item.content,
                source_type=item.source_type,
                source_run_id=item.source_run_id,
                write_reason=item.write_reason,
                last_recalled_at=item.last_recalled_at,
                delete_reason=item.delete_reason,
            )
            for item in result
        ]

    @staticmethod
    async def get_memory_detail(query_db, memory_id: str):
        item = (await query_db.execute(select(LlmMemoryItem).where(LlmMemoryItem.memory_id == memory_id))).scalars().first()
        if not item or item.del_flag != '0' or item.is_deleted:
            return None
        return MemoryItemModel(
            memory_id=item.memory_id,
            memory_type=item.memory_type,
            session_id=item.session_id,
            run_id=item.run_id,
            content=item.content,
            source_type=item.source_type,
            source_run_id=item.source_run_id,
            write_reason=item.write_reason,
            last_recalled_at=item.last_recalled_at,
            delete_reason=item.delete_reason,
        )

    @staticmethod
    async def create_memory(query_db, data: MemoryCreateModel):
        item = LlmMemoryItem(
            memory_id=str(uuid.uuid4()),
            memory_type=data.memory_type,
            session_id=data.session_id,
            run_id=data.run_id,
            content=data.content,
            source_type=data.source_type,
            source_run_id=data.source_run_id or data.run_id,
            write_reason=data.write_reason,
            last_recalled_at='',
            delete_reason='',
            is_deleted=False,
        )
        query_db.add(item)
        return {
            'memory_id': item.memory_id,
            'session_id': item.session_id,
            'run_id': item.run_id,
            'status': 'created',
        }

    @staticmethod
    async def delete_memory(query_db, memory_id: str, data: MemoryDeleteModel):
        await query_db.execute(
            update(LlmMemoryItem)
            .where(LlmMemoryItem.memory_id == memory_id)
            .values(is_deleted=True, delete_reason=data.delete_reason)
        )
        return {
            'memory_id': memory_id,
            'delete_reason': data.delete_reason,
            'status': 'deleted',
        }
