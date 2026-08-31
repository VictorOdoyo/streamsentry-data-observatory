from fastapi import APIRouter, Request, status

from streamsentry.api.models import CostCreate, SLOCreate, SLOEvaluation
from streamsentry.api.state import get_state
from streamsentry.domain.cost import CostSignal
from streamsentry.domain.slo import ServiceLevelObjective
from streamsentry.services.reports import DashboardMetrics

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}", tags=["reliability"])


@router.get("/dashboard")
def dashboard(workspace_id: str, request: Request) -> DashboardMetrics:
    return get_state(request).services.reports.dashboard(workspace_id)


@router.get("/slos")
def list_slos(workspace_id: str, request: Request) -> list[ServiceLevelObjective]:
    return get_state(request).store.list_slos(workspace_id)


@router.post("/slos", status_code=status.HTTP_201_CREATED)
def create_slo(workspace_id: str, body: SLOCreate, request: Request) -> ServiceLevelObjective:
    return get_state(request).services.slos.create(workspace_id, **body.model_dump())


@router.post("/slos/{slo_id}/evaluation")
def evaluate_slo(
    workspace_id: str, slo_id: str, body: SLOEvaluation, request: Request
) -> ServiceLevelObjective:
    return get_state(request).services.slos.evaluate(
        workspace_id, slo_id, body.current_success_rate
    )


@router.get("/costs")
def list_costs(workspace_id: str, request: Request) -> list[CostSignal]:
    return get_state(request).store.list_costs(workspace_id)


@router.post("/costs", status_code=status.HTTP_201_CREATED)
def create_cost(workspace_id: str, body: CostCreate, request: Request) -> CostSignal:
    return get_state(request).services.costs.record(workspace_id, **body.model_dump())
