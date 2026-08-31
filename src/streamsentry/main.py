import uvicorn

from streamsentry.config import get_settings


def run() -> None:
    settings = get_settings()
    uvicorn.run(
        "streamsentry.api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
    )


if __name__ == "__main__":
    run()
