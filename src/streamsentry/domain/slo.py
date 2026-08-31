from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .enums import SLOStatus


class ServiceLevelObjective(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    dataset_id: str
    name: str
    freshness_minutes: int = Field(gt=0)
    success_rate_target: float = Field(gt=0, le=1)
    current_success_rate: float = Field(ge=0, le=1)
    status: SLOStatus
    window_days: int = Field(default=30, gt=0)
    evaluated_at: datetime
