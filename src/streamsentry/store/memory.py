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
