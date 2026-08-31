from fastapi import APIRouter, Request, status

from streamsentry.api.models import LineageCreate

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/lineage", tags=["lineage"])


@router.get("")
def list_lineage(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_lineage(workspace_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_lineage(workspace_id: str, body: LineageCreate, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.lineage.connect(workspace_id, **body.model_dump())


@router.get("/{dataset_id}/impact")
def downstream_impact(workspace_id: str, dataset_id: str, request: Request):  # type: ignore[no-untyped-def]
    return {
        "dataset_id": dataset_id,
        "downstream_dataset_ids": request.app.state.container.services.lineage.downstream_impact(
            workspace_id, dataset_id
        ),
    }
