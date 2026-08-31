from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .enums import DatasetStatus, DatasetTier


class Dataset(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    name: str
    fully_qualified_name: str
    platform: str
    tier: DatasetTier
    status: DatasetStatus
    owner_id: str
    description: str = ""
    tags: tuple[str, ...] = ()
    last_observed_at: datetime
    row_count: int = Field(default=0, ge=0)
    size_bytes: int = Field(default=0, ge=0)
    created_at: datetime
