from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STREAMSENTRY_", env_file=".env")

    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = Field(default=8080, ge=1, le=65535)
    request_body_limit: int = Field(default=1_048_576, ge=1024)
    database_url: str = "sqlite+pysqlite:///./streamsentry.db"
    cors_origins: tuple[str, ...] = (
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
