from enum import StrEnum


class DatasetTier(StrEnum):
    CRITICAL = "critical"
    STANDARD = "standard"
    EXPERIMENTAL = "experimental"


class DatasetStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    FAILING = "failing"
    PAUSED = "paused"


class CheckType(StrEnum):
    FRESHNESS = "freshness"
    VOLUME = "volume"
    SCHEMA = "schema"
    NULL_RATE = "null_rate"
    UNIQUE_RATE = "unique_rate"


class CheckSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class RunStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


class IncidentStatus(StrEnum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    MONITORING = "monitoring"
    RESOLVED = "resolved"


class IncidentSeverity(StrEnum):
    SEV1 = "sev1"
    SEV2 = "sev2"
    SEV3 = "sev3"


class SLOStatus(StrEnum):
    MEETING = "meeting"
    AT_RISK = "at_risk"
    BREACHED = "breached"


class CostTrend(StrEnum):
    DOWN = "down"
    STABLE = "stable"
    UP = "up"
