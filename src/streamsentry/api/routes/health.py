from fastapi import APIRouter, Request

from streamsentry.api.state import get_state

router = APIRouter(tags=["health"])


@router.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok", "service": "StreamSentry Data Observatory"}


@router.get("/health/ready")
def ready(request: Request) -> dict[str, str]:
    return {
        "status": "ready",
        "workspace_id": get_state(request).default_workspace_id,
    }
