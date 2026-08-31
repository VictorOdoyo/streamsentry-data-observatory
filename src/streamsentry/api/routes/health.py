from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health/live")
def live() -> dict[str, str]:
    return {"status": "ok", "service": "StreamSentry Data Observatory"}


@router.get("/health/ready")
def ready(request: Request) -> dict[str, str]:
    return {
        "status": "ready",
        "workspace_id": request.app.state.container.default_workspace_id,
    }
