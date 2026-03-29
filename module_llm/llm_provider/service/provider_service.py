from module_llm.llm_provider.dao.provider_dao import ProviderDao


class ProviderService:
    @staticmethod
    async def get_provider_overview(query_db):
        providers = await ProviderDao.list_providers(query_db)
        models = await ProviderDao.list_provider_models(query_db)
        return {
            'providers': providers,
            'models': models,
        }

    @staticmethod
    async def get_provider_detail(query_db, provider_id: str):
        return await ProviderDao.get_provider_detail(query_db, provider_id)

    @staticmethod
    async def create_provider(query_db, data):
        result = await ProviderDao.create_provider(query_db, data)
        await query_db.commit()
        return result

    @staticmethod
    async def test_provider(query_db, provider_id: str):
        provider = await ProviderDao.get_provider_detail(query_db, provider_id)
        if not provider:
            return {
                'provider_id': provider_id,
                'health_status': 'not_found',
            }
        return {
            'provider_id': provider.provider_id,
            'health_status': 'healthy' if provider.is_enabled else 'disabled',
        }
