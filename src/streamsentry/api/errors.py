from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from streamsentry.domain.errors import (
    ConflictError,
    DomainError,
    InvalidTransitionError,
    NotFoundError,
    ValidationError,
)


def install_error_handlers(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_context(request: Request, call_next):  # type: ignore[no-untyped-def]
        supplied = request.headers.get("X-Request-ID", "").strip()
        request_id = supplied if 0 < len(supplied) <= 128 else uuid4().hex[:16]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(DomainError)
    async def domain_error(request: Request, error: DomainError) -> JSONResponse:
        status = 422
        code = "validation_error"
        if isinstance(error, NotFoundError):
            status, code = 404, "not_found"
        elif isinstance(error, (ConflictError, InvalidTransitionError)):
            status, code = 409, "conflict"
        elif not isinstance(error, ValidationError):
            status, code = 400, "domain_error"
        return JSONResponse(
            status_code=status,
            content={"code": code, "message": str(error), "request_id": request.state.request_id},
        )
