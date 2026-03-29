from pydantic import BaseModel


class ToolUpdateModel(BaseModel):
    enabled: bool
    risk_level: str


class ToolListItemModel(BaseModel):
    tool_id: str
    name: str
    source_type: str
    source_id: str
    description: str
    enabled: bool
    risk_level: str
