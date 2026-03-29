from pydantic import BaseModel


class ProviderCreateModel(BaseModel):
    name: str
    provider_type: str
    base_url: str


class ProviderListItemModel(BaseModel):
    provider_id: str
    name: str
    provider_type: str
    base_url: str
    is_enabled: bool
    is_default: bool


class ProviderModelListItemModel(BaseModel):
    model_id: str
    provider_id: str
    model_code: str
    display_name: str
    capabilities: str
    is_default: bool
