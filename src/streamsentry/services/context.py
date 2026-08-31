from dataclasses import dataclass

from streamsentry.domain.identity import Clock, IDFactory
from streamsentry.store.protocol import Store


@dataclass(frozen=True, slots=True)
class ServiceContext:
    store: Store
    clock: Clock
    ids: IDFactory
