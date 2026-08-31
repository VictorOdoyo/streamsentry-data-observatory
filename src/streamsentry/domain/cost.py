from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from .enums import CostTrend


class CostSignal(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    dataset_id: str
    period_start: date
    period_end: date
    amount_usd: float = Field(ge=0)
    query_count: int = Field(ge=0)
    scanned_bytes: int = Field(ge=0)
    trend: CostTrend
    observed_at: datetime
