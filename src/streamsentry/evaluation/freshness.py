from datetime import datetime

from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import RunStatus
from streamsentry.domain.errors import ValidationError

from .models import EvaluationResult, Observation


def evaluate_freshness(
    check: QualityCheck, observation: Observation, evaluated_at: datetime
) -> EvaluationResult:
    maximum_minutes = float(check.configuration.get("maximum_minutes", 0))
    if maximum_minutes <= 0:
        raise ValidationError("freshness check requires a positive maximum_minutes")
    age_minutes = max(0.0, (evaluated_at - observation.observed_at).total_seconds() / 60)
    passed = age_minutes <= maximum_minutes
    return EvaluationResult(
        status=RunStatus.PASSED if passed else RunStatus.FAILED,
        observed_value=round(age_minutes, 2),
        expected_value=maximum_minutes,
        message="dataset is fresh" if passed else "dataset freshness threshold was exceeded",
        metrics={"age_minutes": round(age_minutes, 2), "maximum_minutes": maximum_minutes},
    )
