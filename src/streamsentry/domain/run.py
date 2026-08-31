from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from .enums import RunStatus


class QualityRun(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    dataset_id: str
    check_id: str
    status: RunStatus
    observed_value: float | str | None
    expected_value: float | str | None
    message: str
    metrics: dict[str, Any]
    started_at: datetime
    finished_at: datetime
