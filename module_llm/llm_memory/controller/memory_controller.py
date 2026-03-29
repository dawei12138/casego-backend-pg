from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_memory.entity.vo.memory_vo import MemoryCreateModel, MemoryDeleteModel
from module_llm.llm_memory.service.memory_service import MemoryService
from utils.response_util import ResponseUtil

memoryController = APIRouter(prefix='/llm/memory/items', tags=['AI记忆管理'])


@memoryController.get('')
async def list_memory_items(
    session_id: str | None = Query(default=None),
    memory_type: str | None = Query(default=None),
    source_run_id: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await MemoryService.get_memory_overview(query_db, session_id, memory_type, source_run_id)
    return ResponseUtil.success(data=data, msg='query success')


@memoryController.post('')
async def create_memory(data: MemoryCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await MemoryService.create_memory(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')


@memoryController.get('/{memory_id}')
async def get_memory_detail(memory_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await MemoryService.get_memory_detail(query_db, memory_id)
    return ResponseUtil.success(data=data, msg='query success')


@memoryController.delete('/{memory_id}')
async def delete_memory(memory_id: str, data: MemoryDeleteModel, query_db: AsyncSession = Depends(get_db)):
    result = await MemoryService.delete_memory(query_db, memory_id, data)
    return ResponseUtil.success(data=result, msg='delete success')
