from module_llm.llm_agent.dao.agent_dao import AgentDao


class AgentService:
    @staticmethod
    async def get_agent_overview(query_db):
        return await AgentDao.list_agents(query_db)

    @staticmethod
    async def get_agent_detail(query_db, agent_id: str):
        return await AgentDao.get_agent_detail(query_db, agent_id)

    @staticmethod
    async def create_agent(query_db, data):
        result = await AgentDao.create_agent(query_db, data)
        await query_db.commit()
        return result
