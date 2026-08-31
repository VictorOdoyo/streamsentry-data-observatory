from dataclasses import dataclass

from .checks import CheckService
from .context import ServiceContext
from .costs import CostService
from .datasets import DatasetService
from .incidents import IncidentService
from .lineage import LineageService
from .reports import ReportService
from .runs import RunService
from .slos import SLOService
from .workspaces import WorkspaceService


@dataclass(frozen=True, slots=True)
class Services:
    workspaces: WorkspaceService
    datasets: DatasetService
    checks: CheckService
    runs: RunService
    incidents: IncidentService
    lineage: LineageService
    slos: SLOService
    costs: CostService
    reports: ReportService


def build_services(context: ServiceContext) -> Services:
    return Services(
        workspaces=WorkspaceService(context),
        datasets=DatasetService(context),
        checks=CheckService(context),
        runs=RunService(context),
        incidents=IncidentService(context),
        lineage=LineageService(context),
        slos=SLOService(context),
        costs=CostService(context),
        reports=ReportService(context),
    )
