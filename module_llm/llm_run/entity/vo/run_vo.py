from pydantic import BaseModel


class RunCreateModel(BaseModel):
    session_id: str
    message: str


class RunStatusUpdateModel(BaseModel):
    status: str
    output_summary: str = ''
    failure_stage: str = ''
    failure_category: str = ''
    cost_summary: str = ''
    used_memory: bool = False
    used_tool: bool = False
    event_type: str = ''
    event_payload: str = '{}'


class RunDetailModel(BaseModel):
    run_id: str
    session_id: str
    agent_id: str
    provider_id: str
    model_code: str
    status: str
    input_summary: str
    output_summary: str
    failure_stage: str
    failure_category: str
    used_memory: bool
    used_tool: bool
    cost_summary: str


class RunEventModel(BaseModel):
    event_id: str
    run_id: str
    seq_no: int
    event_type: str
    event_payload: str
