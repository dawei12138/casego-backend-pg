import uuid

from sqlalchemy import func, select

from module_llm.llm_observability.entity.do.cost_ledger_do import LlmCostLedger
from module_llm.llm_observability.entity.do.trace_record_do import LlmTraceRecord
from module_llm.llm_observability.entity.vo.observability_vo import (
    CostCreateModel,
    CostLedgerItemModel,
    FailureCategoryRankingItemModel,
    FailureStageRankingItemModel,
    ModelCostRankingItemModel,
    ProviderCostRankingItemModel,
    RunEventListItemModel,
    RunGovernanceDetailModel,
    RunIssueListItemModel,
    RunStatusSummaryItemModel,
    ToolFailureRankingItemModel,
    ToolInvokeLogCreateModel,
    TraceCreateModel,
    TraceListItemModel,
)
from module_llm.llm_run.entity.do.run_do import LlmRun
from module_llm.llm_run.entity.do.run_event_do import LlmRunEvent
from module_llm.llm_tool.entity.do.tool_invoke_log_do import LlmToolInvokeLog


class ObservabilityDao:
    @staticmethod
    async def create_trace_record(query_db, data: TraceCreateModel):
        item = LlmTraceRecord(
            trace_id=str(uuid.uuid4()),
            run_id=data.run_id,
            session_id=data.session_id,
            agent_id=data.agent_id,
            status=data.status,
        )
        query_db.add(item)
        return {
            'trace_id': item.trace_id,
            'run_id': item.run_id,
            'status': 'created',
        }

    @staticmethod
    async def create_cost_ledger(query_db, data: CostCreateModel):
        item = LlmCostLedger(
            ledger_id=str(uuid.uuid4()),
            run_id=data.run_id,
            provider_id=data.provider_id,
            model_code=data.model_code,
            input_tokens=data.input_tokens,
            output_tokens=data.output_tokens,
            cost_usd=data.cost_usd,
        )
        query_db.add(item)
        return {
            'ledger_id': item.ledger_id,
            'run_id': item.run_id,
            'status': 'created',
        }

    @staticmethod
    async def create_tool_invoke_log(query_db, data: ToolInvokeLogCreateModel):
        item = LlmToolInvokeLog(
            log_id=str(uuid.uuid4()),
            run_id=data.run_id,
            tool_id=data.tool_id,
            tool_name=data.tool_name,
            status=data.status,
            retry_count=data.retry_count,
        )
        query_db.add(item)
        return {
            'log_id': item.log_id,
            'run_id': item.run_id,
            'status': 'created',
        }

    @staticmethod
    async def list_traces(
        query_db,
        session_id: str | None = None,
        agent_id: str | None = None,
        status: str | None = None,
        run_id: str | None = None,
    ):
        query = select(LlmTraceRecord).where(LlmTraceRecord.del_flag == '0')
        if session_id:
            query = query.where(LlmTraceRecord.session_id == session_id)
        if agent_id:
            query = query.where(LlmTraceRecord.agent_id == agent_id)
        if status:
            query = query.where(LlmTraceRecord.status == status)
        if run_id:
            query = query.where(LlmTraceRecord.run_id == run_id)
        result = (await query_db.execute(query.order_by(LlmTraceRecord.create_time.desc()))).scalars().all()
        return [
            TraceListItemModel(
                trace_id=item.trace_id,
                run_id=item.run_id,
                session_id=item.session_id,
                agent_id=item.agent_id,
                status=item.status,
            )
            for item in result
        ]

    @staticmethod
    async def list_costs(
        query_db,
        provider_id: str | None = None,
        model_code: str | None = None,
        run_id: str | None = None,
    ):
        query = select(LlmCostLedger).where(LlmCostLedger.del_flag == '0')
        if provider_id:
            query = query.where(LlmCostLedger.provider_id == provider_id)
        if model_code:
            query = query.where(LlmCostLedger.model_code == model_code)
        if run_id:
            query = query.where(LlmCostLedger.run_id == run_id)
        result = (await query_db.execute(query.order_by(LlmCostLedger.create_time.desc()))).scalars().all()
        return [
            CostLedgerItemModel(
                ledger_id=item.ledger_id,
                run_id=item.run_id,
                provider_id=item.provider_id,
                model_code=item.model_code,
                input_tokens=item.input_tokens,
                output_tokens=item.output_tokens,
                cost_usd=item.cost_usd,
            )
            for item in result
        ]

    @staticmethod
    async def rank_provider_costs(query_db):
        result = await query_db.execute(
            select(
                LlmCostLedger.provider_id,
                func.count(func.distinct(LlmCostLedger.run_id)),
                func.coalesce(func.sum(LlmCostLedger.cost_usd), 0.0),
            )
            .where(LlmCostLedger.del_flag == '0')
            .group_by(LlmCostLedger.provider_id)
            .order_by(func.coalesce(func.sum(LlmCostLedger.cost_usd), 0.0).desc())
        )
        return [
            ProviderCostRankingItemModel(provider_id=provider_id, run_count=run_count, total_cost_usd=float(total_cost_usd or 0.0))
            for provider_id, run_count, total_cost_usd in result.all()
        ]

    @staticmethod
    async def rank_model_costs(query_db):
        result = await query_db.execute(
            select(
                LlmCostLedger.model_code,
                func.count(func.distinct(LlmCostLedger.run_id)),
                func.coalesce(func.sum(LlmCostLedger.cost_usd), 0.0),
            )
            .where(LlmCostLedger.del_flag == '0')
            .group_by(LlmCostLedger.model_code)
            .order_by(func.coalesce(func.sum(LlmCostLedger.cost_usd), 0.0).desc())
        )
        return [
            ModelCostRankingItemModel(model_code=model_code, run_count=run_count, total_cost_usd=float(total_cost_usd or 0.0))
            for model_code, run_count, total_cost_usd in result.all()
        ]

    @staticmethod
    async def list_run_events(
        query_db,
        run_id: str | None = None,
        event_type: str | None = None,
    ):
        query = select(LlmRunEvent).where(LlmRunEvent.del_flag == '0')
        if run_id:
            query = query.where(LlmRunEvent.run_id == run_id)
        if event_type:
            query = query.where(LlmRunEvent.event_type == event_type)
        result = (await query_db.execute(query.order_by(LlmRunEvent.seq_no.asc()))).scalars().all()
        return [
            RunEventListItemModel(
                event_id=item.event_id,
                run_id=item.run_id,
                seq_no=item.seq_no,
                event_type=item.event_type,
                event_payload=item.event_payload,
            )
            for item in result
        ]

    @staticmethod
    async def rank_tool_failures(query_db):
        result = await query_db.execute(
            select(
                LlmToolInvokeLog.tool_name,
                func.count(LlmToolInvokeLog.log_id),
                func.coalesce(func.sum(LlmToolInvokeLog.retry_count), 0),
            )
            .where(LlmToolInvokeLog.del_flag == '0', LlmToolInvokeLog.status != 'success')
            .group_by(LlmToolInvokeLog.tool_name)
            .order_by(func.count(LlmToolInvokeLog.log_id).desc(), func.coalesce(func.sum(LlmToolInvokeLog.retry_count), 0).desc())
        )
        return [
            ToolFailureRankingItemModel(tool_name=tool_name, failure_count=failure_count, total_retry_count=total_retry_count)
            for tool_name, failure_count, total_retry_count in result.all()
        ]

    @staticmethod
    async def rank_failure_stages(query_db):
        result = await query_db.execute(
            select(LlmRun.failure_stage, func.count(LlmRun.run_id))
            .where(LlmRun.del_flag == '0', LlmRun.failure_stage != '')
            .group_by(LlmRun.failure_stage)
            .order_by(func.count(LlmRun.run_id).desc())
        )
        return [
            FailureStageRankingItemModel(failure_stage=failure_stage, failure_count=failure_count)
            for failure_stage, failure_count in result.all()
        ]

    @staticmethod
    async def rank_failure_categories(query_db):
        result = await query_db.execute(
            select(LlmRun.failure_category, func.count(LlmRun.run_id))
            .where(LlmRun.del_flag == '0', LlmRun.failure_category != '')
            .group_by(LlmRun.failure_category)
            .order_by(func.count(LlmRun.run_id).desc())
        )
        return [
            FailureCategoryRankingItemModel(failure_category=failure_category, failure_count=failure_count)
            for failure_category, failure_count in result.all()
        ]

    @staticmethod
    async def summarize_run_statuses(query_db, session_id: str | None = None, agent_id: str | None = None):
        query = select(LlmRun.status, func.count(LlmRun.run_id)).where(LlmRun.del_flag == '0')
        if session_id:
            query = query.where(LlmRun.session_id == session_id)
        if agent_id:
            query = query.where(LlmRun.agent_id == agent_id)
        grouped_query = query.group_by(LlmRun.status).order_by(LlmRun.status.asc())
        result = await query_db.execute(grouped_query)
        return [RunStatusSummaryItemModel(status=status, count=count) for status, count in result.all()]

    @staticmethod
    async def list_issue_runs(
        query_db,
        status: str | None = None,
        provider_id: str | None = None,
        agent_id: str | None = None,
        session_id: str | None = None,
        model_code: str | None = None,
        failure_stage: str | None = None,
        failure_category: str | None = None,
    ):
        issue_statuses = ['failed', 'cancelled']
        query = select(LlmRun).where(LlmRun.del_flag == '0', LlmRun.status.in_(issue_statuses))
        if status:
            query = query.where(LlmRun.status == status)
        if provider_id:
            query = query.where(LlmRun.provider_id == provider_id)
        if agent_id:
            query = query.where(LlmRun.agent_id == agent_id)
        if session_id:
            query = query.where(LlmRun.session_id == session_id)
        if model_code:
            query = query.where(LlmRun.model_code == model_code)
        if failure_stage:
            query = query.where(LlmRun.failure_stage == failure_stage)
        if failure_category:
            query = query.where(LlmRun.failure_category == failure_category)
        result = (await query_db.execute(query.order_by(LlmRun.create_time.desc()))).scalars().all()
        return [
            RunIssueListItemModel(
                run_id=item.run_id,
                session_id=item.session_id,
                agent_id=item.agent_id,
                provider_id=item.provider_id,
                model_code=item.model_code,
                status=item.status,
                failure_stage=item.failure_stage,
                failure_category=item.failure_category,
                cost_summary=item.cost_summary,
            )
            for item in result
        ]

    @staticmethod
    async def get_run_governance_detail(query_db, run_id: str):
        run = (
            await query_db.execute(select(LlmRun).where(LlmRun.run_id == run_id, LlmRun.del_flag == '0'))
        ).scalars().first()
        if not run:
            return None
        event_count = await query_db.scalar(
            select(func.count(LlmRunEvent.event_id)).where(LlmRunEvent.run_id == run_id, LlmRunEvent.del_flag == '0')
        )
        latest_event = (
            await query_db.execute(
                select(LlmRunEvent)
                .where(LlmRunEvent.run_id == run_id, LlmRunEvent.del_flag == '0')
                .order_by(LlmRunEvent.seq_no.desc())
            )
        ).scalars().first()
        return RunGovernanceDetailModel(
            run_id=run.run_id,
            session_id=run.session_id,
            agent_id=run.agent_id,
            provider_id=run.provider_id,
            model_code=run.model_code,
            status=run.status,
            input_summary=run.input_summary,
            output_summary=run.output_summary,
            failure_stage=run.failure_stage,
            failure_category=run.failure_category,
            used_memory=run.used_memory,
            used_tool=run.used_tool,
            cost_summary=run.cost_summary,
            event_count=event_count or 0,
            latest_event_seq_no=latest_event.seq_no if latest_event else 0,
            latest_event_type=latest_event.event_type if latest_event else '',
            latest_event_payload=latest_event.event_payload if latest_event else '',
        )
