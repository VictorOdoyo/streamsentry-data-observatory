from typing import Any

from streamsentry.domain.check import QualityCheck
from streamsentry.domain.enums import CheckSeverity, CheckType
from streamsentry.domain.errors import ValidationError

from .context import ServiceContext


class CheckService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def create(
        self,
        workspace_id: str,
        dataset_id: str,
        name: str,
        check_type: CheckType,
        severity: CheckSeverity,
        configuration: dict[str, Any],
    ) -> QualityCheck:
        self.context.store.get_dataset(workspace_id, dataset_id)
        if not name.strip():
            raise ValidationError("quality check name is required")
        item = QualityCheck(
            id=self.context.ids.new("check"),
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            name=name.strip(),
            check_type=check_type,
            severity=severity,
            configuration=configuration,
            created_at=self.context.clock.now(),
        )
        self.context.store.put_check(item)
        return item

    def set_enabled(self, workspace_id: str, check_id: str, enabled: bool) -> QualityCheck:
        current = self.context.store.get_check(workspace_id, check_id)
        updated = current.model_copy(update={"enabled": enabled})
        self.context.store.put_check(updated)
        return updated
