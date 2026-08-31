from fastapi import APIRouter, Request, Response, status

from streamsentry.api.models import DatasetCreate, DatasetStatusUpdate
from streamsentry.api.state import get_state
from streamsentry.domain.dataset import Dataset

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/datasets", tags=["datasets"])


@router.get("")
def list_datasets(workspace_id: str, request: Request) -> list[Dataset]:
    return get_state(request).store.list_datasets(workspace_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_dataset(workspace_id: str, body: DatasetCreate, request: Request) -> Dataset:
    return get_state(request).services.datasets.create(workspace_id, **body.model_dump())


@router.patch("/{dataset_id}/status")
def update_status(
    workspace_id: str, dataset_id: str, body: DatasetStatusUpdate, request: Request
) -> Dataset:
    return get_state(request).services.datasets.set_status(workspace_id, dataset_id, body.status)


@router.options("", include_in_schema=False)
def options() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
