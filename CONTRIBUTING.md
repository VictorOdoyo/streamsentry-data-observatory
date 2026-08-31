# Contributing

## Development Setup

1. Install Python 3.13, uv, Node.js 20, and pnpm 9.
2. Run `uv sync --all-groups` in the repository root.
3. Run `pnpm install` in `web`.
4. Start the API with `uv run streamsentry-api` and the console with `pnpm dev`.

## Change Quality

Keep changes focused on one observable behavior. Domain rules belong in services or evaluators rather than route handlers. Storage-specific work should stay behind the store protocol. UI changes must preserve keyboard access, visible focus, responsive layout, and useful loading, error, and empty states.

Before opening a pull request, run:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src tests
uv run pytest
cd web
pnpm lint
pnpm test
pnpm build
```

Include tests for behavior changes. Do not commit credentials, private customer data, generated build output, or unrelated formatting churn.
