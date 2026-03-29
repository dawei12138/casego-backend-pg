from pydantic import BaseModel


class MemoryCreateModel(BaseModel):
    memory_type: str
    session_id: str
    run_id: str
    content: str
    source_type: str = 'run'
    source_run_id: str = ''
    write_reason: str = ''


class MemoryDeleteModel(BaseModel):
    delete_reason: str


class MemoryItemModel(BaseModel):
    memory_id: str
    memory_type: str
    session_id: str
    run_id: str
    content: str
    source_type: str
    source_run_id: str
    write_reason: str
    last_recalled_at: str
    delete_reason: str
