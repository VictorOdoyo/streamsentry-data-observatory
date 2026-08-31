from fastapi import APIRouter, Request, status

from streamsentry.api.models import CostCreate, SLOCreate, SLOEvaluation

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}", tags=["reliability"])


@router.get("/dashboard")
def dashboard(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.reports.dashboard(workspace_id)


@router.get("/slos")
def list_slos(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_slos(workspace_id)


@router.post("/slos", status_code=status.HTTP_201_CREATED)
def create_slo(workspace_id: str, body: SLOCreate, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.slos.create(workspace_id, **body.model_dump())


@router.post("/slos/{slo_id}/evaluation")
def evaluate_slo(
    workspace_id: str, slo_id: str, body: SLOEvaluation, request: Request
):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.slos.evaluate(
        workspace_id, slo_id, body.current_success_rate
    )


@router.get("/costs")
def list_costs(workspace_id: str, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.store.list_costs(workspace_id)


@router.post("/costs", status_code=status.HTTP_201_CREATED)
def create_cost(workspace_id: str, body: CostCreate, request: Request):  # type: ignore[no-untyped-def]
    return request.app.state.container.services.costs.record(workspace_id, **body.model_dump())
