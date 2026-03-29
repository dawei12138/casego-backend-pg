from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.get_db import get_db
from module_llm.llm_provider.entity.vo.provider_vo import ProviderCreateModel
from module_llm.llm_provider.service.provider_service import ProviderService
from utils.response_util import ResponseUtil

providerController = APIRouter(prefix='/llm/providers', tags=['AI模型提供方管理'])


@providerController.get('')
async def list_providers(query_db: AsyncSession = Depends(get_db)):
    data = await ProviderService.get_provider_overview(query_db)
    return ResponseUtil.success(data=data, msg='query success')


@providerController.get('/{provider_id}')
async def get_provider_detail(provider_id: str, query_db: AsyncSession = Depends(get_db)):
    data = await ProviderService.get_provider_detail(query_db, provider_id)
    return ResponseUtil.success(data=data, msg='query success')


@providerController.post('')
async def create_provider(data: ProviderCreateModel, query_db: AsyncSession = Depends(get_db)):
    result = await ProviderService.create_provider(query_db, data)
    return ResponseUtil.success(data=result, msg='create success')


@providerController.post('/{provider_id}:test')
async def test_provider(provider_id: str, query_db: AsyncSession = Depends(get_db)):
    result = await ProviderService.test_provider(query_db, provider_id)
    return ResponseUtil.success(data=result, msg='test success')
