from module_llm.llm_observability.dao.observability_dao import ObservabilityDao


class ObservabilityService:
    @staticmethod
    async def create_trace_record(query_db, data):
        result = await ObservabilityDao.create_trace_record(query_db, data)
        await query_db.commit()
        return result

    @staticmethod
    async def create_cost_ledger(query_db, data):
        result = await ObservabilityDao.create_cost_ledger(query_db, data)
        await query_db.commit()
        return result

    @staticmethod
    async def create_tool_invoke_log(query_db, data):
        result = await ObservabilityDao.create_tool_invoke_log(query_db, data)
        await query_db.commit()
        return result

    @staticmethod
    async def get_trace_overview(
        query_db,
        session_id: str | None = None,
        agent_id: str | None = None,
        status: str | None = None,
        run_id: str | None = None,
    ):
        return await ObservabilityDao.list_traces(query_db, session_id, agent_id, status, run_id)

    @staticmethod
    async def get_cost_overview(
        query_db,
        provider_id: str | None = None,
        model_code: str | None = None,
        run_id: str | None = None,
    ):
        return await ObservabilityDao.list_costs(query_db, provider_id, model_code, run_id)

    @staticmethod
    async def get_run_event_overview(
        query_db,
        run_id: str | None = None,
        event_type: str | None = None,
    ):
        return await ObservabilityDao.list_run_events(query_db, run_id, event_type)

    @staticmethod
    async def get_run_status_summary(
        query_db,
        session_id: str | None = None,
        agent_id: str | None = None,
    ):
        return await ObservabilityDao.summarize_run_statuses(query_db, session_id, agent_id)

    @staticmethod
    async def get_run_issue_overview(
        query_db,
        status: str | None = None,
        provider_id: str | None = None,
        agent_id: str | None = None,
        session_id: str | None = None,
        model_code: str | None = None,
        failure_stage: str | None = None,
        failure_category: str | None = None,
    ):
        return await ObservabilityDao.list_issue_runs(
            query_db,
            status,
            provider_id,
            agent_id,
            session_id,
            model_code,
            failure_stage,
            failure_category,
        )

    @staticmethod
    async def get_run_governance_detail(query_db, run_id: str):
        return await ObservabilityDao.get_run_governance_detail(query_db, run_id)

    @staticmethod
    async def get_provider_cost_rankings(query_db):
        return await ObservabilityDao.rank_provider_costs(query_db)

    @staticmethod
    async def get_model_cost_rankings(query_db):
        return await ObservabilityDao.rank_model_costs(query_db)

    @staticmethod
    async def get_tool_failure_rankings(query_db):
        return await ObservabilityDao.rank_tool_failures(query_db)

    @staticmethod
    async def get_failure_stage_rankings(query_db):
        return await ObservabilityDao.rank_failure_stages(query_db)

    @staticmethod
    async def get_failure_category_rankings(query_db):
        return await ObservabilityDao.rank_failure_categories(query_db)
