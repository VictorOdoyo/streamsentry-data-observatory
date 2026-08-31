from fastapi import APIRouter, Request, status

from streamsentry.api.models import LineageCreate
from streamsentry.api.state import get_state
from streamsentry.domain.lineage import LineageEdge

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/lineage", tags=["lineage"])


@router.get("")
def list_lineage(workspace_id: str, request: Request) -> list[LineageEdge]:
    return get_state(request).store.list_lineage(workspace_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_lineage(workspace_id: str, body: LineageCreate, request: Request) -> LineageEdge:
    return get_state(request).services.lineage.connect(workspace_id, **body.model_dump())


@router.get("/{dataset_id}/impact")
def downstream_impact(
    workspace_id: str, dataset_id: str, request: Request
) -> dict[str, str | list[str]]:
    return {
        "dataset_id": dataset_id,
        "downstream_dataset_ids": get_state(request).services.lineage.downstream_impact(
            workspace_id, dataset_id
        ),
    }
