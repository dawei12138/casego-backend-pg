from pydantic import BaseModel


class AgentCreateModel(BaseModel):
    agent_code: str
    display_name: str
    scenario: str
    default_model_code: str


class AgentListItemModel(BaseModel):
    agent_id: str
    agent_code: str
    display_name: str
    scenario: str
    default_model_code: str
    allow_tools: bool
    allow_memory: bool
    allow_skills: bool
    is_user_visible: bool
    is_recommended: bool
    is_enabled: bool
