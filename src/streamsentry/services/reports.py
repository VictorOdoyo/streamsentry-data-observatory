from pydantic import BaseModel, ConfigDict

from streamsentry.domain.enums import DatasetStatus, IncidentStatus, RunStatus, SLOStatus

from .context import ServiceContext


class DashboardMetrics(BaseModel):
    model_config = ConfigDict(frozen=True)

    datasets: int
    failing_datasets: int
    open_incidents: int
    failed_runs: int
    slo_breaches: int
    warehouse_cost_usd: float
    reliability_score: float


class ReportService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def dashboard(self, workspace_id: str) -> DashboardMetrics:
        datasets = self.context.store.list_datasets(workspace_id)
        incidents = self.context.store.list_incidents(workspace_id)
        runs = self.context.store.list_runs(workspace_id)
        slos = self.context.store.list_slos(workspace_id)
        costs = self.context.store.list_costs(workspace_id)
        completed = [run for run in runs if run.status != RunStatus.SKIPPED]
        passed = sum(run.status == RunStatus.PASSED for run in completed)
        reliability = 100.0 if not completed else round(passed / len(completed) * 100, 1)
        return DashboardMetrics(
            datasets=len(datasets),
            failing_datasets=sum(item.status == DatasetStatus.FAILING for item in datasets),
            open_incidents=sum(item.status != IncidentStatus.RESOLVED for item in incidents),
            failed_runs=sum(item.status == RunStatus.FAILED for item in runs),
            slo_breaches=sum(item.status == SLOStatus.BREACHED for item in slos),
            warehouse_cost_usd=round(sum(item.amount_usd for item in costs), 2),
            reliability_score=reliability,
        )
