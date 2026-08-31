from dataclasses import dataclass

from streamsentry.domain.identity import IDFactory, RandomIDFactory, SystemClock
from streamsentry.seed import load_demo_workspace
from streamsentry.services.container import Services, build_services
from streamsentry.services.context import ServiceContext
from streamsentry.store.memory import MemoryStore


@dataclass(frozen=True, slots=True)
class ApplicationState:
    store: MemoryStore
    services: Services
    default_workspace_id: str


def build_state(ids: IDFactory | None = None) -> ApplicationState:
    store = MemoryStore()
    context = ServiceContext(
        store=store,
        clock=SystemClock(),
        ids=ids or RandomIDFactory(),
    )
    services = build_services(context)
    workspace_id = load_demo_workspace(services)
    return ApplicationState(store=store, services=services, default_workspace_id=workspace_id)
