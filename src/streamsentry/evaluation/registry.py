from datetime import datetime

from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import CheckType, RunStatus

from .freshness import evaluate_freshness
from .models import EvaluationResult, Observation
from .rates import evaluate_rate
from .schema import evaluate_schema
from .volume import evaluate_volume


def evaluate_check(
    check: QualityCheck, observation: Observation, evaluated_at: datetime
) -> EvaluationResult:
    if not check.enabled:
        return EvaluationResult(
            status=RunStatus.SKIPPED,
            observed_value=None,
            expected_value=None,
            message="quality check is disabled",
            metrics={},
        )
    if check.check_type == CheckType.FRESHNESS:
        return evaluate_freshness(check, observation, evaluated_at)
    if check.check_type == CheckType.VOLUME:
        return evaluate_volume(check, observation)
    if check.check_type == CheckType.SCHEMA:
        return evaluate_schema(check, observation)
    return evaluate_rate(check, observation)
