from module_llm.llm_session.dao.session_dao import SessionDao


class SessionService:
    @staticmethod
    async def get_session_overview(query_db):
        return await SessionDao.list_sessions(query_db)

    @staticmethod
    async def get_session_detail(query_db, session_id: str):
        return await SessionDao.get_session_detail(query_db, session_id)
