from pydantic import BaseModel


class TraceCreateModel(BaseModel):
    run_id: str
    session_id: str
    agent_id: str
    status: str


class CostCreateModel(BaseModel):
    run_id: str
    provider_id: str
    model_code: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0


class ToolInvokeLogCreateModel(BaseModel):
    run_id: str
    tool_id: str
    tool_name: str
    status: str = 'success'
    retry_count: int = 0


class TraceListItemModel(BaseModel):
    trace_id: str
    run_id: str
    session_id: str
    agent_id: str
    status: str


class CostLedgerItemModel(BaseModel):
    ledger_id: str
    run_id: str
    provider_id: str
    model_code: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


class RunEventListItemModel(BaseModel):
    event_id: str
    run_id: str
    seq_no: int
    event_type: str
    event_payload: str


class RunStatusSummaryItemModel(BaseModel):
    status: str
    count: int


class RunIssueListItemModel(BaseModel):
    run_id: str
    session_id: str
    agent_id: str
    provider_id: str
    model_code: str
    status: str
    failure_stage: str
    failure_category: str
    cost_summary: str


class RunGovernanceDetailModel(BaseModel):
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
    event_count: int
    latest_event_seq_no: int
    latest_event_type: str
    latest_event_payload: str


class ProviderCostRankingItemModel(BaseModel):
    provider_id: str
    run_count: int
    total_cost_usd: float


class ModelCostRankingItemModel(BaseModel):
    model_code: str
    run_count: int
    total_cost_usd: float


class ToolFailureRankingItemModel(BaseModel):
    tool_name: str
    failure_count: int
    total_retry_count: int


class FailureStageRankingItemModel(BaseModel):
    failure_stage: str
    failure_count: int


class FailureCategoryRankingItemModel(BaseModel):
    failure_category: str
    failure_count: int
