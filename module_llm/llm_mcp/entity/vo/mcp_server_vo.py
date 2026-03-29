from pydantic import BaseModel


class McpServerCreateModel(BaseModel):
    name: str
    transport: str


class McpServerListItemModel(BaseModel):
    server_id: str
    name: str
    transport: str
    enabled: bool
    health_status: str
