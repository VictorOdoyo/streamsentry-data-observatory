from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from .enums import CheckSeverity, CheckType


class QualityCheck(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    dataset_id: str
    name: str
    check_type: CheckType
    severity: CheckSeverity
    enabled: bool = True
    configuration: dict[str, Any]
    created_at: datetime
