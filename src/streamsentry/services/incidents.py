from streamsentry.domain.enums import IncidentSeverity, IncidentStatus
from streamsentry.domain.errors import InvalidTransitionError, ValidationError
from streamsentry.domain.incident import Incident

from .context import ServiceContext

TRANSITIONS: dict[IncidentStatus, set[IncidentStatus]] = {
    IncidentStatus.OPEN: {IncidentStatus.INVESTIGATING, IncidentStatus.RESOLVED},
    IncidentStatus.INVESTIGATING: {IncidentStatus.MONITORING, IncidentStatus.RESOLVED},
    IncidentStatus.MONITORING: {IncidentStatus.INVESTIGATING, IncidentStatus.RESOLVED},
    IncidentStatus.RESOLVED: set(),
}


class IncidentService:
    def __init__(self, context: ServiceContext) -> None:
        self.context = context

    def create(
        self,
        workspace_id: str,
        dataset_id: str,
        title: str,
        summary: str,
        severity: IncidentSeverity,
        check_id: str | None = None,
    ) -> Incident:
        self.context.store.get_dataset(workspace_id, dataset_id)
        if check_id is not None:
            self.context.store.get_check(workspace_id, check_id)
        if not title.strip() or not summary.strip():
            raise ValidationError("incident title and summary are required")
        now = self.context.clock.now()
        item = Incident(
            id=self.context.ids.new("incident"),
            workspace_id=workspace_id,
            dataset_id=dataset_id,
            check_id=check_id,
            title=title.strip(),
            summary=summary.strip(),
            severity=severity,
            status=IncidentStatus.OPEN,
            assignee_id=None,
            created_at=now,
            updated_at=now,
        )
        self.context.store.put_incident(item)
        return item

    def assign(self, workspace_id: str, incident_id: str, owner_id: str) -> Incident:
        self.context.store.get_owner(workspace_id, owner_id)
        current = self.context.store.get_incident(workspace_id, incident_id)
        updated = current.model_copy(
            update={"assignee_id": owner_id, "updated_at": self.context.clock.now()}
        )
        self.context.store.put_incident(updated)
        return updated

    def transition(
        self, workspace_id: str, incident_id: str, status: IncidentStatus
    ) -> Incident:
        current = self.context.store.get_incident(workspace_id, incident_id)
        if status not in TRANSITIONS[current.status]:
            raise InvalidTransitionError(f"cannot move incident from {current.status} to {status}")
        now = self.context.clock.now()
        updated = current.model_copy(
            update={
                "status": status,
                "updated_at": now,
                "resolved_at": now if status == IncidentStatus.RESOLVED else None,
            }
        )
        self.context.store.put_incident(updated)
        return updated
