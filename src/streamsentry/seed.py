from datetime import timedelta

from streamsentry.domain.enums import (
    CheckSeverity,
    CheckType,
    CostTrend,
    DatasetTier,
    IncidentSeverity,
    IncidentStatus,
)
from streamsentry.evaluation.models import Observation
from streamsentry.services.container import Services


def load_demo_workspace(services: Services) -> str:
    now = services.workspaces.context.clock.now()
    workspace = services.workspaces.create_workspace("northstar-data", "Northstar Data Platform")
    amina = services.workspaces.create_owner(
        workspace.id, "Amina Yusuf", "amina@example.com", "Data Reliability"
    )
    marcus = services.workspaces.create_owner(
        workspace.id, "Marcus Chen", "marcus@example.com", "Analytics Engineering"
    )
    elena = services.workspaces.create_owner(
        workspace.id, "Elena Rossi", "elena@example.com", "Revenue Operations"
    )

    events = services.datasets.create(
        workspace.id,
        "Payment events",
        "raw.payments.events",
        "Kafka",
        DatasetTier.CRITICAL,
        amina.id,
        "Canonical payment event stream.",
        ("payments", "pii", "streaming"),
    )
    orders = services.datasets.create(
        workspace.id,
        "Orders fact",
        "analytics.commerce.fct_orders",
        "Snowflake",
        DatasetTier.CRITICAL,
        marcus.id,
        "One row per accepted order.",
        ("commerce", "finance"),
    )
    revenue = services.datasets.create(
        workspace.id,
        "Daily revenue",
        "analytics.finance.daily_revenue",
        "dbt",
        DatasetTier.CRITICAL,
        elena.id,
        "Daily recognized revenue by region.",
        ("executive", "finance"),
    )
    customers = services.datasets.create(
        workspace.id,
        "Customer dimension",
        "analytics.crm.dim_customers",
        "BigQuery",
        DatasetTier.STANDARD,
        marcus.id,
        "Conformed customer attributes.",
        ("crm", "pii"),
    )
    experiments = services.datasets.create(
        workspace.id,
        "Experiment assignments",
        "product.experiments.assignments",
        "PostgreSQL",
        DatasetTier.EXPERIMENTAL,
        amina.id,
        "Active product experiment cohorts.",
        ("experimentation",),
    )

    freshness = services.checks.create(
        workspace.id,
        events.id,
        "Payments arrive within ten minutes",
        CheckType.FRESHNESS,
        CheckSeverity.CRITICAL,
        {"maximum_minutes": 10},
    )
    volume = services.checks.create(
        workspace.id,
        orders.id,
        "Order volume envelope",
        CheckType.VOLUME,
        CheckSeverity.CRITICAL,
        {"minimum_rows": 40_000, "maximum_rows": 90_000},
    )
    schema = services.checks.create(
        workspace.id,
        revenue.id,
        "Revenue contract fields",
        CheckType.SCHEMA,
        CheckSeverity.CRITICAL,
        {"required_fields": ["date", "region", "gross_revenue", "currency"]},
    )
    nulls = services.checks.create(
        workspace.id,
        customers.id,
        "Customer email completeness",
        CheckType.NULL_RATE,
        CheckSeverity.WARNING,
        {"maximum_rate": 0.03},
    )
    services.checks.create(
        workspace.id,
        experiments.id,
        "Assignment uniqueness",
        CheckType.UNIQUE_RATE,
        CheckSeverity.INFO,
        {"minimum_rate": 0.99},
    )

    services.runs.execute(
        workspace.id,
        freshness.id,
        Observation(observed_at=now - timedelta(minutes=28), row_count=13_904),
    )
    services.runs.execute(
        workspace.id,
        volume.id,
        Observation(observed_at=now - timedelta(minutes=8), row_count=56_420),
    )
    services.runs.execute(
        workspace.id,
        schema.id,
        Observation(
            observed_at=now - timedelta(minutes=12),
            row_count=1_240,
            schema_fields=("date", "region", "gross_revenue"),
        ),
    )
    services.runs.execute(
        workspace.id,
        nulls.id,
        Observation(observed_at=now - timedelta(minutes=6), row_count=412_000, null_rate=0.012),
    )

    payment_incident = services.incidents.create(
        workspace.id,
        events.id,
        "Payment stream freshness breach",
        "Consumer lag moved the payment stream beyond its ten-minute freshness objective.",
        IncidentSeverity.SEV1,
        freshness.id,
    )
    services.incidents.assign(workspace.id, payment_incident.id, amina.id)
    services.incidents.transition(workspace.id, payment_incident.id, IncidentStatus.INVESTIGATING)
    services.incidents.create(
        workspace.id,
        revenue.id,
        "Revenue schema lost currency",
        "The daily revenue model no longer emits the required currency field.",
        IncidentSeverity.SEV2,
        schema.id,
    )

    services.lineage.connect(workspace.id, events.id, orders.id, "stream normalization")
    services.lineage.connect(workspace.id, orders.id, revenue.id, "daily revenue aggregation")
    services.lineage.connect(workspace.id, customers.id, revenue.id, "regional customer enrichment")

    revenue_slo = services.slos.create(
        workspace.id, revenue.id, "Revenue dashboard reliability", 60, 0.995
    )
    services.slos.evaluate(workspace.id, revenue_slo.id, 0.941)
    services.slos.create(workspace.id, orders.id, "Order model reliability", 30, 0.99)

    period_start = now.date() - timedelta(days=30)
    for dataset, amount, queries, trend in (
        (events, 1840.50, 821_000, CostTrend.UP),
        (orders, 1230.25, 96_000, CostTrend.STABLE),
        (revenue, 684.10, 42_500, CostTrend.DOWN),
        (customers, 412.80, 31_000, CostTrend.STABLE),
    ):
        services.costs.record(
            workspace.id,
            dataset.id,
            period_start,
            now.date(),
            amount,
            queries,
            int(amount * 1_000_000_000),
            trend,
        )
    return workspace.id
