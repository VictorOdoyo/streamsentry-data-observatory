from collections.abc import Callable
from datetime import UTC, datetime
from threading import Lock
from typing import Protocol
from uuid import uuid4


class Clock(Protocol):
    def now(self) -> datetime: ...


class IDFactory(Protocol):
    def new(self, prefix: str) -> str: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class RandomIDFactory:
    def new(self, prefix: str) -> str:
        return f"{prefix}_{uuid4().hex[:16]}"


class FrozenClock:
    def __init__(self, current: datetime) -> None:
        self._current = current

    def now(self) -> datetime:
        return self._current

    def set(self, current: datetime) -> None:
        self._current = current


class SequentialIDFactory:
    def __init__(self) -> None:
        self._next = 0
        self._lock = Lock()

    def new(self, prefix: str) -> str:
        with self._lock:
            self._next += 1
            return f"{prefix}_{self._next:04d}"


Now = Callable[[], datetime]
