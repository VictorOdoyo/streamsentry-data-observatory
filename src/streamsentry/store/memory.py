from threading import RLock

from streamsentry.domain.check import QualityCheck
from streamsentry.domain.cost import CostSignal
from streamsentry.domain.dataset import Dataset
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
