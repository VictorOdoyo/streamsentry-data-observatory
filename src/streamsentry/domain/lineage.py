from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LineageEdge(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    upstream_dataset_id: str
    downstream_dataset_id: str
    transformation: str
    observed_at: datetime
