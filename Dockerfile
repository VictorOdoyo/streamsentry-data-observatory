FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS runtime

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH" \
    STREAMSENTRY_ENVIRONMENT=production \
    STREAMSENTRY_HOST=0.0.0.0 \
    STREAMSENTRY_PORT=8080

WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

EXPOSE 8080
CMD ["streamsentry-api"]
