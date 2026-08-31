from datetime import UTC, date, datetime, timedelta

import pytest

from streamsentry.domain.enums import (
    CheckSeverity,
    CheckType,
    CostTrend,
    DatasetStatus,
    DatasetTier,
    IncidentSeverity,
    IncidentStatus,
    RunStatus,
    SLOStatus,
)
from streamsentry.domain.errors import ConflictError, InvalidTransitionError, ValidationError
from streamsentry.domain.identity import FrozenClock, SequentialIDFactory
from streamsentry.evaluation.models import Observation
from streamsentry.services.container import Services, build_services
from streamsentry.services.context import ServiceContext
from streamsentry.store.memory import MemoryStore

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def services() -> tuple[Services, FrozenClock]:
    clock = FrozenClock(NOW)
    context = ServiceContext(store=MemoryStore(), clock=clock, ids=SequentialIDFactory())
    return build_services(context), clock


def test_complete_reliability_workflow() -> None:
    app, clock = services()
    workspace = app.workspaces.create_workspace("data-team", "Data Team")
    owner = app.workspaces.create_owner(workspace.id, "Amina", "AMINA@example.com", "Platform")
    upstream = app.datasets.create(
        workspace.id,
        "Events",
        "raw.events",
        "Kafka",
        DatasetTier.CRITICAL,
        owner.id,
        tags=("pii", "pii", "stream"),
    )
    downstream = app.datasets.create(
        workspace.id, "Orders", "mart.orders", "Snowflake", DatasetTier.CRITICAL, owner.id
    )
    assert upstream.tags == ("pii", "stream")

    policy = app.checks.create(
        workspace.id,
        upstream.id,
        "Freshness",
        CheckType.FRESHNESS,
        CheckSeverity.CRITICAL,
        {"maximum_minutes": 5},
    )
    failed = app.runs.execute(
        workspace.id, policy.id, Observation(observed_at=NOW - timedelta(minutes=9), row_count=42)
    )
    assert failed.status == RunStatus.FAILED
    assert (
        app.datasets.context.store.get_dataset(workspace.id, upstream.id).status
        == DatasetStatus.FAILING
    )
    app.checks.set_enabled(workspace.id, policy.id, False)
    skipped = app.runs.execute(workspace.id, policy.id, Observation(observed_at=NOW, row_count=43))
    assert skipped.status == RunStatus.SKIPPED

    incident = app.incidents.create(
        workspace.id,
        upstream.id,
        "Late events",
        "Consumer lag exceeded policy",
        IncidentSeverity.SEV1,
        policy.id,
    )
    assigned = app.incidents.assign(workspace.id, incident.id, owner.id)
    assert assigned.assignee_id == owner.id
    clock.set(NOW + timedelta(minutes=5))
    investigating = app.incidents.transition(
        workspace.id, incident.id, IncidentStatus.INVESTIGATING
    )
    resolved = app.incidents.transition(workspace.id, investigating.id, IncidentStatus.RESOLVED)
    assert resolved.resolved_at == clock.now()
    with pytest.raises(InvalidTransitionError):
        app.incidents.transition(workspace.id, resolved.id, IncidentStatus.OPEN)

    app.lineage.connect(workspace.id, upstream.id, downstream.id, "normalize")
    third = app.datasets.create(
        workspace.id, "Revenue", "mart.revenue", "dbt", DatasetTier.STANDARD, owner.id
    )
    app.lineage.connect(workspace.id, downstream.id, third.id, "aggregate")
    assert app.lineage.downstream_impact(workspace.id, upstream.id) == [downstream.id, third.id]
    with pytest.raises(ConflictError):
        app.lineage.connect(workspace.id, upstream.id, downstream.id, "duplicate")

    slo = app.slos.create(workspace.id, downstream.id, "Order SLO", 30, 0.99)
    assert app.slos.evaluate(workspace.id, slo.id, 0.98).status == SLOStatus.AT_RISK
    assert app.slos.evaluate(workspace.id, slo.id, 0.8).status == SLOStatus.BREACHED
    assert app.slos.evaluate(workspace.id, slo.id, 0.995).status == SLOStatus.MEETING

    app.costs.record(
        workspace.id,
        downstream.id,
        date(2026, 8, 1),
        date(2026, 8, 31),
        125.45,
        200,
        4000,
        CostTrend.UP,
    )
    assert app.costs.total(workspace.id) == 125.45
    dashboard = app.reports.dashboard(workspace.id)
    assert dashboard.datasets == 3
    assert dashboard.warehouse_cost_usd == 125.45


def test_validation_boundaries() -> None:
    app, _ = services()
    with pytest.raises(ValidationError):
        app.workspaces.create_workspace("INVALID SLUG", "Name")
    workspace = app.workspaces.create_workspace("valid-workspace", "Valid")
    with pytest.raises(ValidationError):
        app.workspaces.create_owner(workspace.id, "", "wrong", "")
