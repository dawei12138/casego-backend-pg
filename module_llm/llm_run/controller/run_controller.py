from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_run.entity.vo.run_vo import RunCreateModel, RunStatusUpdateModel
from module_llm.llm_run.service.run_service import RunService
from utils.response_util import ResponseUtil

runController = APIRouter(prefix='/llm/runs', tags=['AI运行记录与执行'])


@runController.get('')
async def list_runs(
    session_id: str | None = Query(default=None),
    status: str | None = Query(default=None),
    provider_id: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    model_code: str | None = Query(default=None),
    failure_stage: str | None = Query(default=None),
    failure_category: str | None = Query(default=None),
    query_db: AsyncSession = Depends(get_db),
):
    data = await RunService.list_runs(
        query_db,
        session_id,
        status,
        provider_id,
        agent_id,
        model_code,
        failure_stage,
        failure_category,
    )
    return ResponseUtil.success(data=data, msg='query success')


@runController.post('')
async def create_run(data: RunCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await RunService.create_run(query_db, data.session_id, data.message)
    return ResponseUtil.success(data=result, msg='create success')


@runController.get('/{run_id}')
async def get_run_detail(run_id: str, query_db: AsyncSession = Depends(get_db)):
    result = await RunService.get_run_detail(query_db, run_id)
    return ResponseUtil.success(data=result, msg='query success')


@runController.get('/{run_id}/events')
async def get_run_events(run_id: str, query_db: AsyncSession = Depends(get_db)):
    result = await RunService.list_run_events(query_db, run_id)
    return ResponseUtil.success(data=result, msg='query success')


@runController.post('/{run_id}:status')
async def update_run_status(run_id: str, data: RunStatusUpdateModel, query_db: AsyncSession = Depends(get_db)):
    result = await RunService.update_run_status(query_db, run_id, data)
    return ResponseUtil.success(data=result, msg='update success')


@runController.post('/{run_id}:cancel')
async def cancel_run(run_id: str, query_db: AsyncSession = Depends(get_db)):
    result = await RunService.cancel_run(query_db, run_id)
    return ResponseUtil.success(data=result, msg='cancel success')
