from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_observability.entity.vo.observability_vo import CostCreateModel, ToolInvokeLogCreateModel, TraceCreateModel
from module_llm.llm_observability.service.observability_service import ObservabilityService
from utils.response_util import ResponseUtil

observabilityController = APIRouter(prefix='/llm/observability', tags=['AI运行治理控制台'])


@observabilityController.post('/traces')
async def create_trace_record(data: TraceCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await ObservabilityService.create_trace_record(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')


@observabilityController.get('/traces')
async def list_traces(
    session_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    run_id: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await ObservabilityService.get_trace_overview(query_db, session_id, agent_id, status, run_id)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.post('/costs')
async def create_cost_ledger(data: CostCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await ObservabilityService.create_cost_ledger(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')


@observabilityController.get('/costs')
async def list_costs(
    provider_id: str | None = Query(default=None),
    model_code: str | None = Query(default=None),
    run_id: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await ObservabilityService.get_cost_overview(query_db, provider_id, model_code, run_id)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/cost-rankings/providers')
async def list_provider_cost_rankings(query_db: AsyncSession = Depends(get_db)):
    data = await ObservabilityService.get_provider_cost_rankings(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/cost-rankings/models')
async def list_model_cost_rankings(query_db: AsyncSession = Depends(get_db)):
    data = await ObservabilityService.get_model_cost_rankings(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/events')
async def list_run_events(
    run_id: str | None = Query(default=None),
    event_type: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await ObservabilityService.get_run_event_overview(query_db, run_id, event_type)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.post('/tool-invoke-logs')
async def create_tool_invoke_log(data: ToolInvokeLogCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await ObservabilityService.create_tool_invoke_log(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')


@observabilityController.get('/tool-failure-rankings')
async def list_tool_failure_rankings(query_db: AsyncSession = Depends(get_db)):
    data = await ObservabilityService.get_tool_failure_rankings(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/failure-rankings/stages')
async def list_failure_stage_rankings(query_db: AsyncSession = Depends(get_db)):
    data = await ObservabilityService.get_failure_stage_rankings(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/failure-rankings/categories')
async def list_failure_category_rankings(query_db: AsyncSession = Depends(get_db)):
    data = await ObservabilityService.get_failure_category_rankings(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/run-statuses')
async def list_run_status_summary(
    session_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await ObservabilityService.get_run_status_summary(query_db, session_id, agent_id)
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/run-issues')
async def list_run_issues(
    status: str | None = Query(default=None),
    provider_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    session_id: str | None = Query(default=None),
    model_code: str | None = Query(default=None),
    failure_stage: str | None = Query(default=None),
    failure_category: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await ObservabilityService.get_run_issue_overview(
        query_db,
        status,
        provider_id,
        agent_id,
        session_id,
        model_code,
        failure_stage,
        failure_category,
    )
    return ResponseUtil.success(data=data, msg='query success')


@observabilityController.get('/runs/{run_id}')
async def get_run_governance_detail(run_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await ObservabilityService.get_run_governance_detail(query_db, run_id)
    return ResponseUtil.success(data=data, msg='query success')
