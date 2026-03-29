from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_tool.entity.vo.tool_vo import ToolUpdateModel
from module_llm.llm_tool.service.tool_service import ToolService
from utils.response_util import ResponseUtil

toolController = APIRouter(prefix='/llm/tools', tags=['AI工具治理'])


@toolController.get('')
async def list_tools(
    source_type: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    source_id: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await ToolService.get_tool_overview(query_db, source_type, enabled, risk_level, source_id)
    return ResponseUtil.success(data=data, msg='query success')


@toolController.get('/{tool_id}')
async def get_tool_detail(tool_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await ToolService.get_tool_detail(query_db, tool_id)
    return ResponseUtil.success(data=data, msg='query success')


@toolController.put('/{tool_id}')
async def update_tool(tool_id: str, data: ToolUpdateModel, query_db: AsyncSession = Depends(get_db)):
    result = await ToolService.update_tool(query_db, tool_id, data)
    return ResponseUtil.success(data=result, msg='update success')
