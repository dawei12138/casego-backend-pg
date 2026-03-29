import uuid

from sqlalchemy import select

from module_llm.llm_agent.entity.do.agent_do import LlmAgent
from module_llm.llm_agent.entity.vo.agent_vo import AgentCreateModel, AgentListItemModel


class AgentDao:
    @staticmethod
    async def list_agents(query_db):
        result = (await query_db.execute(select(LlmAgent).order_by(LlmAgent.sort_order.asc(), LlmAgent.create_time.desc()))).scalars().all()
        return [
            AgentListItemModel(
                agent_id=item.agent_id,
                agent_code=item.agent_code,
                display_name=item.display_name,
                scenario=item.scenario,
                default_model_code=item.default_model_code,
                allow_tools=item.allow_tools,
                allow_memory=item.allow_memory,
                allow_skills=item.allow_skills,
                is_user_visible=item.is_user_visible,
                is_recommended=item.is_recommended,
                is_enabled=item.is_enabled,
            )
            for item in result
            if item.del_flag == '0'
        ]

    @staticmethod
    async def get_agent_detail(query_db, agent_id: str):
        item = (await query_db.execute(select(LlmAgent).where(LlmAgent.agent_id == agent_id))).scalars().first()
        if not item or item.del_flag != '0':
            return None
        return AgentListItemModel(
            agent_id=item.agent_id,
            agent_code=item.agent_code,
            display_name=item.display_name,
            scenario=item.scenario,
            default_model_code=item.default_model_code,
            allow_tools=item.allow_tools,
            allow_memory=item.allow_memory,
            allow_skills=item.allow_skills,
            is_user_visible=item.is_user_visible,
            is_recommended=item.is_recommended,
            is_enabled=item.is_enabled,
        )

    @staticmethod
    async def create_agent(query_db, data: AgentCreateModel):
        agent = LlmAgent(
            agent_id=str(uuid.uuid4()),
            agent_code=data.agent_code,
            display_name=data.display_name,
            scenario=data.scenario,
            default_model_code=data.default_model_code,
            allow_tools=True,
            allow_memory=True,
            allow_skills=True,
            max_steps=8,
            max_tool_calls=4,
            timeout_seconds=60,
            is_user_visible=True,
            is_recommended=False,
            sort_order=100,
            is_enabled=True,
        )
        query_db.add(agent)
        await query_db.flush()
        return {
            'agent_id': agent.agent_id,
            'agent_code': agent.agent_code,
            'display_name': agent.display_name,
            'status': 'created',
        }
