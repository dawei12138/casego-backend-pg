from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_agent.entity.vo.agent_vo import AgentCreateModel
from module_llm.llm_agent.service.agent_service import AgentService
from utils.response_util import ResponseUtil

agentController = APIRouter(prefix='/llm/agents', tags=['AI执行策略管理'])


@agentController.get('')
async def list_agents(query_db: AsyncSession = Depends(get_db)):
    data = await AgentService.get_agent_overview(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@agentController.get('/{agent_id}')
async def get_agent_detail(agent_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await AgentService.get_agent_detail(query_db, agent_id)
    return ResponseUtil.success(data=data, msg='query success')


@agentController.post('')
async def create_agent(data: AgentCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await AgentService.create_agent(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')
