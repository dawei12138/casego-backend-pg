from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_session.service.session_service import SessionService
from utils.response_util import ResponseUtil

sessionController = APIRouter(prefix='/llm/sessions', tags=['AI会话管理'])


@sessionController.get('')
async def list_sessions(query_db: AsyncSession = Depends(get_db)):
    data = await SessionService.get_session_overview(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@sessionController.get('/{session_id}')
async def get_session_detail(session_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await SessionService.get_session_detail(query_db, session_id)
    return ResponseUtil.success(data=data, msg='query success')
