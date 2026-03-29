from pydantic import BaseModel


class SessionListItemModel(BaseModel):
    session_id: str
    title: str
    owner_id: str
    default_agent_id: str
    default_provider_id: str
    default_model_code: str
    status: str
    last_error_summary: str
