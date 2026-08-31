from fastapi import APIRouter, Request, status

from streamsentry.api.models import IncidentAssignment, IncidentCreate, IncidentTransition
from streamsentry.api.state import get_state
from streamsentry.domain.incident import Incident

router = APIRouter(prefix="/api/v1/workspaces/{workspace_id}/incidents", tags=["incidents"])


@router.get("")
def list_incidents(workspace_id: str, request: Request) -> list[Incident]:
    return get_state(request).store.list_incidents(workspace_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_incident(workspace_id: str, body: IncidentCreate, request: Request) -> Incident:
    return get_state(request).services.incidents.create(workspace_id, **body.model_dump())


@router.post("/{incident_id}/assignment")
def assign_incident(
    workspace_id: str, incident_id: str, body: IncidentAssignment, request: Request
) -> Incident:
    return get_state(request).services.incidents.assign(workspace_id, incident_id, body.owner_id)


@router.post("/{incident_id}/transition")
def transition_incident(
    workspace_id: str, incident_id: str, body: IncidentTransition, request: Request
) -> Incident:
    return get_state(request).services.incidents.transition(workspace_id, incident_id, body.status)
