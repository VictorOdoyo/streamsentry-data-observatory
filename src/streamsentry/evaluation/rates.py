from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import CheckType, RunStatus
from streamsentry.domain.errors import ValidationError

from .models import EvaluationResult, Observation


def evaluate_rate(check: QualityCheck, observation: Observation) -> EvaluationResult:
    if check.check_type == CheckType.NULL_RATE:
        observed = observation.null_rate
        maximum = float(check.configuration.get("maximum_rate", -1))
        if not 0 <= maximum <= 1:
            raise ValidationError("null-rate check requires maximum_rate between zero and one")
        passed = observed <= maximum
        message = "null rate is acceptable" if passed else "null rate exceeded its threshold"
        return EvaluationResult(
            status=RunStatus.PASSED if passed else RunStatus.FAILED,
            observed_value=observed,
            expected_value=maximum,
            message=message,
            metrics={"null_rate": observed, "maximum_rate": maximum},
        )
    minimum = float(check.configuration.get("minimum_rate", -1))
    if not 0 <= minimum <= 1:
        raise ValidationError("unique-rate check requires minimum_rate between zero and one")
    observed = observation.unique_rate
    passed = observed >= minimum
    return EvaluationResult(
        status=RunStatus.PASSED if passed else RunStatus.FAILED,
        observed_value=observed,
        expected_value=minimum,
        message="unique rate is acceptable" if passed else "unique rate fell below its threshold",
        metrics={"unique_rate": observed, "minimum_rate": minimum},
    )
