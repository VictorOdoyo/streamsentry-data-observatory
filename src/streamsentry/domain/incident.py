from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .enums import IncidentSeverity, IncidentStatus


class Incident(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    dataset_id: str
    check_id: str | None
    title: str
    summary: str
    severity: IncidentSeverity
    status: IncidentStatus
    assignee_id: str | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None = None
