from datetime import UTC, datetime

from sqlalchemy import text

from streamsentry.config import Settings
from streamsentry.domain.identity import (
    FrozenClock,
    RandomIDFactory,
    SequentialIDFactory,
    SystemClock,
)
from streamsentry.persistence.database import SessionFactory, create_database_engine


def test_database_session_commits_and_closes() -> None:
    engine = create_database_engine(Settings(database_url="sqlite+pysqlite:///:memory:"))
    with engine.begin() as connection:
        connection.execute(
            text("CREATE TABLE signals (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
        )
    sessions = SessionFactory(engine)
    with sessions.begin() as session:
        session.execute(text("INSERT INTO signals (name) VALUES ('freshness')"))
    with sessions.begin() as session:
        assert session.scalar(text("SELECT COUNT(*) FROM signals")) == 1
    engine.dispose()


def test_clock_and_identifier_adapters() -> None:
    now = datetime(2026, 8, 18, tzinfo=UTC)
    frozen = FrozenClock(now)
    assert frozen.now() == now
    later = datetime(2026, 8, 19, tzinfo=UTC)
    frozen.set(later)
    assert frozen.now() == later
    sequential = SequentialIDFactory()
    assert [sequential.new("run"), sequential.new("run")] == ["run_0001", "run_0002"]
    assert RandomIDFactory().new("dataset").startswith("dataset_")
    assert SystemClock().now().tzinfo is UTC
