from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import RunStatus
from streamsentry.domain.errors import ValidationError

from .models import EvaluationResult, Observation


def evaluate_schema(check: QualityCheck, observation: Observation) -> EvaluationResult:
    configured = check.configuration.get("required_fields")
    if not isinstance(configured, list) or not configured:
        raise ValidationError("schema check requires required_fields")
    required = {str(field) for field in configured}
    observed = set(observation.schema_fields)
    missing = sorted(required - observed)
    passed = not missing
    return EvaluationResult(
        status=RunStatus.PASSED if passed else RunStatus.FAILED,
        observed_value=",".join(sorted(observed)),
        expected_value=",".join(sorted(required)),
        message="required schema is present" if passed else f"missing fields: {', '.join(missing)}",
        metrics={"missing_fields": missing, "observed_field_count": len(observed)},
    )
