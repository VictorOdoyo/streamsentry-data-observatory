from fastapi import APIRouter, Request, Response, status

from streamsentry.api.models import DatasetCreate, DatasetStatusUpdate

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/datasets", tags=["datasets"])


@router.get("")
def list_datasets(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_datasets(workspace_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_dataset(workspace_id: str, body: DatasetCreate, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.datasets.create(workspace_id, **body.model_dump())


@router.patch("/{dataset_id}/status")
def update_status(
    workspace_id: str, dataset_id: str, body: DatasetStatusUpdate, request: Request
):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.datasets.set_status(
        workspace_id, dataset_id, body.status
    )


@router.options("", include_in_schema=False)
def options() -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)
