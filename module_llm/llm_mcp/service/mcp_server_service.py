from module_llm.llm_mcp.dao.mcp_server_dao import McpServerDao


class McpServerService:
    @staticmethod
    async def get_server_overview(query_db):
        return await McpServerDao.list_servers(query_db)

    @staticmethod
    async def get_server_detail(query_db, server_id: str):
        return await McpServerDao.get_server_detail(query_db, server_id)

    @staticmethod
    async def create_server(query_db, data):
        result = await McpServerDao.create_server(query_db, data)
        await query_db.commit()
        return result

    @staticmethod
    async def refresh_tools(query_db, server_id: str):
        server = await McpServerDao.get_server_detail(query_db, server_id)
        if not server:
            return {
                'server_id': server_id,
                'refresh_status': 'not_found',
            }
        return {
            'server_id': server.server_id,
            'refresh_status': 'done' if server.enabled else 'disabled',
        }
