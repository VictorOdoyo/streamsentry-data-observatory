from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from streamsentry.domain.enums import RunStatus


class Observation(BaseModel):
    model_config = ConfigDict(frozen=True)

    observed_at: datetime
    row_count: int = Field(ge=0)
    schema_fields: tuple[str, ...] = ()
    null_rate: float = Field(default=0, ge=0, le=1)
    unique_rate: float = Field(default=1, ge=0, le=1)


class EvaluationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    status: RunStatus
    observed_value: float | str | None
    expected_value: float | str | None
    message: str
    metrics: dict[str, Any]
