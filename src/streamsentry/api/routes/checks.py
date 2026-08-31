from fastapi import APIRouter, Request, status

from streamsentry.api.models import CheckCreate, CheckEnabledUpdate, ObservationRequest
from streamsentry.evaluation.models import Observation

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}", tags=["quality"])


@router.get("/checks")
def list_checks(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_checks(workspace_id)


@router.post("/checks", status_code=status.HTTP_201_CREATED)
def create_check(workspace_id: str, body: CheckCreate, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.checks.create(workspace_id, **body.model_dump())


@router.patch("/checks/{check_id}/enabled")
def set_enabled(
    workspace_id: str, check_id: str, body: CheckEnabledUpdate, request: Request
):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.checks.set_enabled(
        workspace_id, check_id, body.enabled
    )


@router.post("/checks/{check_id}/runs", status_code=status.HTTP_201_CREATED)
def execute_check(
    workspace_id: str, check_id: str, body: ObservationRequest, request: Request
):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.runs.execute(
        workspace_id, check_id, Observation(**body.model_dump())
    )


@router.get("/runs")
def list_runs(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_runs(workspace_id)
