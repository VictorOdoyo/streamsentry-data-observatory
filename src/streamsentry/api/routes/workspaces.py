from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/v1", tags=["workspaces"])


@router.get("/workspaces")
def workspaces(request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_workspaces()


@router.get("/workspaces/{workspace_id}/owners")
def owners(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_owners(workspace_id)
