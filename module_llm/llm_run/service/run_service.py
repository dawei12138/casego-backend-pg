import uuid

from module_llm.llm_run.dao.run_dao import RunDao
from module_llm.llm_run.entity.do.run_do import LlmRun
from module_llm.llm_session.service.session_service import SessionService


class RunService:
    @staticmethod
    async def create_run(query_db, session_id: str, message: str):
        session = await SessionService.get_session_detail(query_db, session_id)
        if not session:
            return {
                'run_id': '',
                'session_id': session_id,
                'message': message,
                'status': 'session_not_found',
            }

        run = LlmRun(
            run_id=str(uuid.uuid4()),
            session_id=session_id,
            agent_id=session.default_agent_id,
            provider_id=session.default_provider_id,
            model_code=session.default_model_code,
            status='created',
            input_summary=message[:255],
            output_summary='',
            failure_stage='',
            failure_category='',
            used_memory=False,
            used_tool=False,
            cost_summary='',
        )
        query_db.add(run)
        await query_db.commit()
        return {
            'run_id': run.run_id,
            'session_id': run.session_id,
            'agent_id': run.agent_id,
            'provider_id': run.provider_id,
            'model_code': run.model_code,
            'message': message,
            'status': run.status,
        }

    @staticmethod
    async def list_runs(
        query_db,
        session_id: str | None = None,
        status: str | None = None,
        provider_id: str | None = None,
        agent_id: str | None = None,
        model_code: str | None = None,
        failure_stage: str | None = None,
        failure_category: str | None = None,
    ):
        return await RunDao.list_runs(
            query_db,
            session_id,
            status,
            provider_id,
            agent_id,
            model_code,
            failure_stage,
            failure_category,
        )

    @staticmethod
    async def get_run_detail(query_db, run_id: str):
        return await RunDao.get_run_detail(query_db, run_id)

    @staticmethod
    async def list_run_events(query_db, run_id: str):
        return await RunDao.list_run_events(query_db, run_id)

    @staticmethod
    async def update_run_status(query_db, run_id: str, data):
        result = await RunDao.update_run_status(query_db, run_id, data)
        if not result:
            return {
                'run_id': run_id,
                'status': 'not_found',
            }
        await query_db.commit()
        return result

    @staticmethod
    async def cancel_run(query_db, run_id: str):
        result = await RunDao.cancel_run(query_db, run_id)
        if not result:
            return {
                'run_id': run_id,
                'status': 'not_found',
            }
        await query_db.commit()
        return result
