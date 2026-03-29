import uuid

from sqlalchemy import select

from module_llm.llm_provider.entity.do.provider_do import LlmProvider
from module_llm.llm_provider.entity.do.provider_model_do import LlmProviderModel
from module_llm.llm_provider.entity.vo.provider_vo import ProviderCreateModel, ProviderListItemModel, ProviderModelListItemModel


class ProviderDao:
    @staticmethod
    async def list_providers(query_db):
        result = (await query_db.execute(select(LlmProvider).order_by(LlmProvider.name.asc()))).scalars().all()
        return [
            ProviderListItemModel(
                provider_id=item.provider_id,
                name=item.name,
                provider_type=item.provider_type,
                base_url=item.base_url,
                is_enabled=item.is_enabled,
                is_default=item.is_default,
            )
            for item in result
        ]

    @staticmethod
    async def get_provider_detail(query_db, provider_id: str):
        item = (await query_db.execute(select(LlmProvider).where(LlmProvider.provider_id == provider_id))).scalars().first()
        if not item:
            return None
        return ProviderListItemModel(
            provider_id=item.provider_id,
            name=item.name,
            provider_type=item.provider_type,
            base_url=item.base_url,
            is_enabled=item.is_enabled,
            is_default=item.is_default,
        )

    @staticmethod
    async def list_provider_models(query_db):
        result = (await query_db.execute(select(LlmProviderModel).order_by(LlmProviderModel.display_name.asc()))).scalars().all()
        return [
            ProviderModelListItemModel(
                model_id=item.model_id,
                provider_id=item.provider_id,
                model_code=item.model_code,
                display_name=item.display_name,
                capabilities=item.capabilities,
                is_default=item.is_default,
            )
            for item in result
        ]

    @staticmethod
    async def create_provider(query_db, data: ProviderCreateModel):
        provider = LlmProvider(
            provider_id=str(uuid.uuid4()),
            name=data.name,
            provider_type=data.provider_type,
            base_url=data.base_url,
            api_key_masked='',
            is_enabled=True,
            is_default=False,
        )
        query_db.add(provider)
        await query_db.flush()
        return {
            'provider_id': provider.provider_id,
            'name': provider.name,
            'provider_type': provider.provider_type,
            'base_url': provider.base_url,
            'status': 'created',
        }
