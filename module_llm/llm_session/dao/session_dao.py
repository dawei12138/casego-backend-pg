from sqlalchemy import select

from module_llm.llm_session.entity.do.session_do import LlmSession
from module_llm.llm_session.entity.vo.session_vo import SessionListItemModel


class SessionDao:
    @staticmethod
    async def list_sessions(query_db):
        result = (await query_db.execute(select(LlmSession).order_by(LlmSession.create_time.desc()))).scalars().all()
        return [
            SessionListItemModel(
                session_id=item.session_id,
                title=item.title,
                owner_id=item.owner_id,
                default_agent_id=item.default_agent_id,
                default_provider_id=item.default_provider_id,
                default_model_code=item.default_model_code,
                status=item.status,
                last_error_summary=item.last_error_summary,
            )
            for item in result
            if item.del_flag == '0'
        ]

    @staticmethod
    async def get_session_detail(query_db, session_id: str):
        item = (await query_db.execute(select(LlmSession).where(LlmSession.session_id == session_id))).scalars().first()
        if not item or item.del_flag != '0':
            return None
        return SessionListItemModel(
            session_id=item.session_id,
            title=item.title,
            owner_id=item.owner_id,
            default_agent_id=item.default_agent_id,
            default_provider_id=item.default_provider_id,
            default_model_code=item.default_model_code,
            status=item.status,
            last_error_summary=item.last_error_summary,
        )
