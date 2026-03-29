from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_mcp.entity.vo.mcp_server_vo import McpServerCreateModel
from module_llm.llm_mcp.service.mcp_server_service import McpServerService
from utils.response_util import ResponseUtil

mcpServerController = APIRouter(prefix='/llm/mcp/servers', tags=['AI MCP 服务管理'])


@mcpServerController.get('')
async def list_mcp_servers(query_db: AsyncSession = Depends(get_db)):
    data = await McpServerService.get_server_overview(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@mcpServerController.get('/{server_id}')
async def get_mcp_server_detail(server_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await McpServerService.get_server_detail(query_db, server_id)
    return ResponseUtil.success(data=data, msg='query success')


@mcpServerController.post('')
async def create_mcp_server(data: McpServerCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await McpServerService.create_server(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')


@mcpServerController.post('/{server_id}:refresh-tools')
async def refresh_mcp_server_tools(server_id: str, query_db: AsyncSession = Depends(get_db)):
    result = await McpServerService.refresh_tools(query_db, server_id)
    return ResponseUtil.success(data=result, msg='refresh success')
