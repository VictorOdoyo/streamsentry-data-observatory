from threading import RLock

from streamsentry.domain.check import QualityCheck
from streamsentry.domain.cost import CostSignal
from streamsentry.domain.dataset import Dataset
from streamsentry.domain.errors import ConflictError, NotFoundError
from streamsentry.domain.incident import Incident
from streamsentry.domain.lineage import LineageEdge
from streamsentry.domain.run import QualityRun
from streamsentry.domain.slo import ServiceLevelObjective
from streamsentry.domain.workspace import Owner, Workspace


class MemoryStore:
    def __init__(self) -> None:
        self._lock = RLock()
        self._workspaces: dict[str, Workspace] = {}
        self._owners: dict[str, Owner] = {}
        self._datasets: dict[str, Dataset] = {}
        self._checks: dict[str, QualityCheck] = {}
        self._runs: dict[str, QualityRun] = {}
        self._incidents: dict[str, Incident] = {}
        self._lineage: dict[str, LineageEdge] = {}
        self._slos: dict[str, ServiceLevelObjective] = {}
        self._costs: dict[str, CostSignal] = {}

    def create_workspace(self, workspace: Workspace) -> None:
        with self._lock:
            if workspace.id in self._workspaces or any(
                item.slug == workspace.slug for item in self._workspaces.values()
            ):
                raise ConflictError("workspace id or slug already exists")
            self._workspaces[workspace.id] = workspace

    def list_workspaces(self) -> list[Workspace]:
        with self._lock:
            return sorted(self._workspaces.values(), key=lambda item: item.name)

    def put_owner(self, owner: Owner) -> None:
        with self._lock:
            self._owners[owner.id] = owner

    def get_owner(self, workspace_id: str, owner_id: str) -> Owner:
        with self._lock:
            owner = self._owners.get(owner_id)
            if owner is None or owner.workspace_id != workspace_id:
                raise NotFoundError("owner not found")
            return owner

    def list_owners(self, workspace_id: str) -> list[Owner]:
        with self._lock:
            return sorted(
                (item for item in self._owners.values() if item.workspace_id == workspace_id),
                key=lambda item: item.name,
            )

    def put_dataset(self, dataset: Dataset) -> None:
        with self._lock:
            self._datasets[dataset.id] = dataset

    def get_dataset(self, workspace_id: str, dataset_id: str) -> Dataset:
        with self._lock:
            dataset = self._datasets.get(dataset_id)
            if dataset is None or dataset.workspace_id != workspace_id:
                raise NotFoundError("dataset not found")
            return dataset

    def list_datasets(self, workspace_id: str) -> list[Dataset]:
        with self._lock:
            return sorted(
                (item for item in self._datasets.values() if item.workspace_id == workspace_id),
                key=lambda item: (item.tier, item.name),
            )

    def put_check(self, check: QualityCheck) -> None:
        with self._lock:
            self._checks[check.id] = check

    def get_check(self, workspace_id: str, check_id: str) -> QualityCheck:
        with self._lock:
            check = self._checks.get(check_id)
            if check is None or check.workspace_id != workspace_id:
                raise NotFoundError("quality check not found")
            return check

    def list_checks(self, workspace_id: str) -> list[QualityCheck]:
        with self._lock:
            return sorted(
                (item for item in self._checks.values() if item.workspace_id == workspace_id),
                key=lambda item: (item.dataset_id, item.name),
            )

    def put_run(self, run: QualityRun) -> None:
        with self._lock:
            self._runs[run.id] = run

    def list_runs(self, workspace_id: str) -> list[QualityRun]:
        with self._lock:
            return sorted(
                (item for item in self._runs.values() if item.workspace_id == workspace_id),
                key=lambda item: item.finished_at,
                reverse=True,
            )

    def put_incident(self, incident: Incident) -> None:
        with self._lock:
            self._incidents[incident.id] = incident

    def get_incident(self, workspace_id: str, incident_id: str) -> Incident:
        with self._lock:
            incident = self._incidents.get(incident_id)
            if incident is None or incident.workspace_id != workspace_id:
                raise NotFoundError("incident not found")
            return incident

    def list_incidents(self, workspace_id: str) -> list[Incident]:
        with self._lock:
            return sorted(
                (item for item in self._incidents.values() if item.workspace_id == workspace_id),
                key=lambda item: item.updated_at,
                reverse=True,
            )

    def put_lineage(self, edge: LineageEdge) -> None:
        with self._lock:
            if edge.upstream_dataset_id == edge.downstream_dataset_id:
                raise ConflictError("lineage self-reference is not allowed")
            self._lineage[edge.id] = edge

    def list_lineage(self, workspace_id: str) -> list[LineageEdge]:
        with self._lock:
            return sorted(
                (item for item in self._lineage.values() if item.workspace_id == workspace_id),
                key=lambda item: (item.upstream_dataset_id, item.downstream_dataset_id),
            )

    def put_slo(self, slo: ServiceLevelObjective) -> None:
        with self._lock:
            self._slos[slo.id] = slo

    def get_slo(self, workspace_id: str, slo_id: str) -> ServiceLevelObjective:
        with self._lock:
            slo = self._slos.get(slo_id)
            if slo is None or slo.workspace_id != workspace_id:
                raise NotFoundError("service level objective not found")
            return slo

    def list_slos(self, workspace_id: str) -> list[ServiceLevelObjective]:
        with self._lock:
            return sorted(
                (item for item in self._slos.values() if item.workspace_id == workspace_id),
                key=lambda item: (item.status, item.name),
            )
