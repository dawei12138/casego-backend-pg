from module_llm.llm_tool.dao.tool_dao import ToolDao


class ToolService:
    @staticmethod
    async def get_tool_overview(
        query_db,
        source_type: str | None = None,
        enabled: bool | None = None,
        risk_level: str | None = None,
        source_id: str | None = None,
    ):
        return await ToolDao.list_tools(query_db, source_type, enabled, risk_level, source_id)

    @staticmethod
    async def get_tool_detail(query_db, tool_id: str):
        return await ToolDao.get_tool_detail(query_db, tool_id)

    @staticmethod
    async def update_tool(query_db, tool_id: str, data):
        result = await ToolDao.update_tool(query_db, tool_id, data)
        await query_db.commit()
        return result
