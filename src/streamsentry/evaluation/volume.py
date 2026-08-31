from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import RunStatus
from streamsentry.domain.errors import ValidationError

from .models import EvaluationResult, Observation


def evaluate_volume(check: QualityCheck, observation: Observation) -> EvaluationResult:
    minimum = int(check.configuration.get("minimum_rows", -1))
    maximum = int(check.configuration.get("maximum_rows", -1))
    if minimum < 0 or maximum < minimum:
        raise ValidationError("volume check requires a valid row range")
    passed = minimum <= observation.row_count <= maximum
    expected = f"{minimum}..{maximum}"
    return EvaluationResult(
        status=RunStatus.PASSED if passed else RunStatus.FAILED,
        observed_value=float(observation.row_count),
        expected_value=expected,
        message="row volume is within range" if passed else "row volume is outside range",
        metrics={
            "row_count": observation.row_count,
            "minimum_rows": minimum,
            "maximum_rows": maximum,
        },
    )
