from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Workspace(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    slug: str
    name: str
    created_at: datetime


class Owner(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    workspace_id: str
    name: str
    email: str
    team: str
    created_at: datetime
