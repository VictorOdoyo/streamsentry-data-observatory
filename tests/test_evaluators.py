from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import CheckSeverity, CheckType, RunStatus
from streamsentry.domain.errors import ValidationError
from streamsentry.evaluation.models import Observation
from streamsentry.evaluation.registry import evaluate_check

NOW = datetime(2026, 8, 18, 12, tzinfo=UTC)


def check(
    check_type: CheckType, configuration: dict[str, Any], *, enabled: bool = True
) -> QualityCheck:
    return QualityCheck(
        id="check_1",
        workspace_id="workspace_1",
        dataset_id="dataset_1",
        name="policy",
        check_type=check_type,
        severity=CheckSeverity.CRITICAL,
        enabled=enabled,
        configuration=configuration,
        created_at=NOW,
    )


@pytest.mark.parametrize(
    ("policy", "observation", "status"),
    [
        (
            check(CheckType.FRESHNESS, {"maximum_minutes": 10}),
            Observation(observed_at=NOW - timedelta(minutes=5), row_count=2),
            RunStatus.PASSED,
        ),
        (
            check(CheckType.FRESHNESS, {"maximum_minutes": 10}),
            Observation(observed_at=NOW - timedelta(minutes=11), row_count=2),
            RunStatus.FAILED,
        ),
        (
            check(CheckType.VOLUME, {"minimum_rows": 10, "maximum_rows": 20}),
            Observation(observed_at=NOW, row_count=14),
            RunStatus.PASSED,
        ),
        (
            check(CheckType.VOLUME, {"minimum_rows": 10, "maximum_rows": 20}),
            Observation(observed_at=NOW, row_count=30),
            RunStatus.FAILED,
        ),
        (
            check(CheckType.SCHEMA, {"required_fields": ["id", "email"]}),
            Observation(observed_at=NOW, row_count=1, schema_fields=("id", "email")),
            RunStatus.PASSED,
        ),
        (
            check(CheckType.SCHEMA, {"required_fields": ["id", "email"]}),
            Observation(observed_at=NOW, row_count=1, schema_fields=("id",)),
            RunStatus.FAILED,
        ),
        (
            check(CheckType.NULL_RATE, {"maximum_rate": 0.1}),
            Observation(observed_at=NOW, row_count=1, null_rate=0.04),
            RunStatus.PASSED,
        ),
        (
            check(CheckType.NULL_RATE, {"maximum_rate": 0.1}),
            Observation(observed_at=NOW, row_count=1, null_rate=0.2),
            RunStatus.FAILED,
        ),
        (
            check(CheckType.UNIQUE_RATE, {"minimum_rate": 0.9}),
            Observation(observed_at=NOW, row_count=1, unique_rate=0.95),
            RunStatus.PASSED,
        ),
        (
            check(CheckType.UNIQUE_RATE, {"minimum_rate": 0.9}),
            Observation(observed_at=NOW, row_count=1, unique_rate=0.8),
            RunStatus.FAILED,
        ),
    ],
)
def test_evaluates_quality_policies(
    policy: QualityCheck, observation: Observation, status: RunStatus
) -> None:
    assert evaluate_check(policy, observation, NOW).status == status


def test_disabled_check_is_skipped() -> None:
    result = evaluate_check(
        check(CheckType.VOLUME, {}, enabled=False), Observation(observed_at=NOW, row_count=1), NOW
    )
    assert result.status == RunStatus.SKIPPED
    assert result.metrics == {}


@pytest.mark.parametrize(
    "policy",
    [
        check(CheckType.FRESHNESS, {}),
        check(CheckType.VOLUME, {"minimum_rows": 5, "maximum_rows": 2}),
        check(CheckType.SCHEMA, {"required_fields": []}),
        check(CheckType.NULL_RATE, {"maximum_rate": 2}),
        check(CheckType.UNIQUE_RATE, {"minimum_rate": -1}),
    ],
)
def test_invalid_policy_configuration_is_rejected(policy: QualityCheck) -> None:
    with pytest.raises(ValidationError):
        evaluate_check(policy, Observation(observed_at=NOW, row_count=1), NOW)
