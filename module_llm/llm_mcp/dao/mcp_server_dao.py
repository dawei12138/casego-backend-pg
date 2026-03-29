import uuid

from sqlalchemy import select

from module_llm.llm_mcp.entity.do.mcp_server_do import LlmMcpServer
from module_llm.llm_mcp.entity.vo.mcp_server_vo import McpServerCreateModel, McpServerListItemModel


class McpServerDao:
    @staticmethod
    async def list_servers(query_db):
        result = (await query_db.execute(select(LlmMcpServer).order_by(LlmMcpServer.name.asc()))).scalars().all()
        return [
            McpServerListItemModel(
                server_id=item.server_id,
                name=item.name,
                transport=item.transport,
                enabled=item.enabled,
                health_status=item.health_status,
            )
            for item in result
        ]

    @staticmethod
    async def get_server_detail(query_db, server_id: str):
        item = (await query_db.execute(select(LlmMcpServer).where(LlmMcpServer.server_id == server_id))).scalars().first()
        if not item:
            return None
        return McpServerListItemModel(
            server_id=item.server_id,
            name=item.name,
            transport=item.transport,
            enabled=item.enabled,
            health_status=item.health_status,
        )

    @staticmethod
    async def create_server(query_db, data: McpServerCreateModel):
        server = LlmMcpServer(
            server_id=str(uuid.uuid4()),
            name=data.name,
            transport=data.transport,
            enabled=True,
            health_status='healthy',
        )
        query_db.add(server)
        await query_db.flush()
        return {
            'server_id': server.server_id,
            'name': server.name,
            'transport': server.transport,
            'status': 'created',
        }
