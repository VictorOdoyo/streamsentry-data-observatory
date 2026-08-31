from fastapi import APIRouter, Request

from streamsentry.api.state import get_state
from streamsentry.domain.workspace import Owner, Workspace

router = APIRouter(prefix="/api/v1", tags=["workspaces"])


@router.get("/workspaces")
def workspaces(request: Request) -> list[Workspace]:
    return get_state(request).store.list_workspaces()


@router.get("/workspaces/{workspace_id}/owners")
def owners(workspace_id: str, request: Request) -> list[Owner]:
    return get_state(request).store.list_owners(workspace_id)
