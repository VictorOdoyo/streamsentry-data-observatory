from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from streamsentry.api.app import create_app
from streamsentry.api.state import ApplicationState, build_state
from streamsentry.domain.identity import SequentialIDFactory


@pytest.fixture
def state() -> ApplicationState:
    return build_state(SequentialIDFactory())


@pytest.fixture
def client(state: ApplicationState) -> Iterator[TestClient]:
    with TestClient(create_app(state)) as test_client:
        yield test_client
