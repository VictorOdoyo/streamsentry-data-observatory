from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field

from streamsentry.domain.enums import (
    CheckSeverity,
    CheckType,
    CostTrend,
    DatasetStatus,
    DatasetTier,
    IncidentSeverity,
    IncidentStatus,
)


class DatasetCreate(BaseModel):
    name: str
    fully_qualified_name: str
    platform: str
    tier: DatasetTier
    owner_id: str
    description: str = ""
    tags: tuple[str, ...] = ()


class DatasetStatusUpdate(BaseModel):
    status: DatasetStatus


class CheckCreate(BaseModel):
    dataset_id: str
    name: str
    check_type: CheckType
    severity: CheckSeverity
    configuration: dict[str, Any]


class CheckEnabledUpdate(BaseModel):
    enabled: bool


class ObservationRequest(BaseModel):
    observed_at: datetime
    row_count: int = Field(ge=0)
    schema_fields: tuple[str, ...] = ()
    null_rate: float = Field(default=0, ge=0, le=1)
    unique_rate: float = Field(default=1, ge=0, le=1)


class IncidentCreate(BaseModel):
    dataset_id: str
    check_id: str | None = None
    title: str
    summary: str
    severity: IncidentSeverity


class IncidentAssignment(BaseModel):
    owner_id: str


class IncidentTransition(BaseModel):
    status: IncidentStatus


class LineageCreate(BaseModel):
    upstream_dataset_id: str
    downstream_dataset_id: str
    transformation: str


class SLOCreate(BaseModel):
    dataset_id: str
    name: str
    freshness_minutes: int = Field(gt=0)
    success_rate_target: float = Field(gt=0, le=1)
    window_days: int = Field(default=30, gt=0)


class SLOEvaluation(BaseModel):
    current_success_rate: float = Field(ge=0, le=1)


class CostCreate(BaseModel):
    dataset_id: str
    period_start: date
    period_end: date
    amount_usd: float = Field(ge=0)
    query_count: int = Field(ge=0)
    scanned_bytes: int = Field(ge=0)
    trend: CostTrend
