from sqlalchemy import select, update

from module_llm.llm_tool.entity.do.tool_do import LlmTool
from module_llm.llm_tool.entity.vo.tool_vo import ToolListItemModel, ToolUpdateModel


class ToolDao:
    @staticmethod
    async def list_tools(
        query_db,
        source_type: str | None = None,
        enabled: bool | None = None,
        risk_level: str | None = None,
        source_id: str | None = None,
    ):
        query = select(LlmTool).where(LlmTool.del_flag == '0')
        if source_type:
            query = query.where(LlmTool.source_type == source_type)
        if enabled is not None:
            query = query.where(LlmTool.enabled == enabled)
        if risk_level:
            query = query.where(LlmTool.risk_level == risk_level)
        if source_id:
            query = query.where(LlmTool.source_id == source_id)
        result = (await query_db.execute(query.order_by(LlmTool.name.asc()))).scalars().all()
        return [
            ToolListItemModel(
                tool_id=item.tool_id,
                name=item.name,
                source_type=item.source_type,
                source_id=item.source_id,
                description=item.description,
                enabled=item.enabled,
                risk_level=item.risk_level,
            )
            for item in result
        ]

    @staticmethod
    async def get_tool_detail(query_db, tool_id: str):
        item = (await query_db.execute(select(LlmTool).where(LlmTool.tool_id == tool_id))).scalars().first()
        if not item or item.del_flag != '0':
            return None
        return ToolListItemModel(
            tool_id=item.tool_id,
            name=item.name,
            source_type=item.source_type,
            source_id=item.source_id,
            description=item.description,
            enabled=item.enabled,
            risk_level=item.risk_level,
        )

    @staticmethod
    async def update_tool(query_db, tool_id: str, data: ToolUpdateModel):
        await query_db.execute(
            update(LlmTool)
            .where(LlmTool.tool_id == tool_id)
            .values(enabled=data.enabled, risk_level=data.risk_level)
        )
        return {
            'tool_id': tool_id,
            'enabled': data.enabled,
            'risk_level': data.risk_level,
            'status': 'updated',
        }
