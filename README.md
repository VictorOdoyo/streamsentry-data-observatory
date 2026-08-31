# StreamSentry Data Observatory

StreamSentry is a production-oriented reference platform for operating reliable data products. It combines a versioned FastAPI service with a React control plane for dataset health, quality checks, incidents, lineage impact, service-level objectives, ownership, and warehouse cost signals.

The repository is self-contained. It starts with deterministic fictional telemetry, needs no private credentials, and supports both native development and Docker Compose.

## What It Demonstrates

- Dataset catalog with ownership, tier, platform, health, scale, and freshness metadata
- Freshness, volume, schema, null-rate, and uniqueness policy evaluation
- Immutable quality-run history and automatic dataset health updates
- Incident assignment and guarded response-state transitions
- Direct and transitive lineage impact analysis
- Reliability objectives with meeting, at-risk, and breached states
- Warehouse spend, scan volume, query count, and trend signals
- Versioned REST contracts, request IDs, structured errors, CORS, and health checks
- Thread-safe in-memory storage plus a normalized relational schema and session boundary
- Responsive React operator console with search, filtering, drawers, and empty states
- Strict Python typing, linting, API contract tests, frontend tests, and 85% coverage gate

## Stack

**Backend:** Python 3.13, FastAPI, Pydantic, SQLAlchemy, Uvicorn, uv, pytest, Ruff, mypy  
**Frontend:** React 19, TypeScript, Vite, Vitest, Oxlint, pnpm, Lucide  
**Delivery:** Docker, Nginx, Docker Compose, GitHub Actions, Dependabot

## Quick Start With Docker

```bash
docker compose up --build
```

Open the console at `http://localhost:4173`. The API and interactive OpenAPI documentation are available at `http://localhost:8080` and `http://localhost:8080/docs`.

## Native Development

Requirements:

- Python 3.13
- uv
- Node.js 20
- pnpm 9

Start the API:

```bash
uv sync --all-groups
uv run streamsentry-api
```

In another terminal, start the console:

```bash
cd web
pnpm install
pnpm dev
```

The development console runs at `http://localhost:5173` and reads the API from `http://localhost:8080` by default. Override it with `VITE_API_URL` when needed.

## Verification

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

The backend suite enforces a minimum of 85% statement coverage. CI also builds both production container images and validates the Compose configuration.

## Repository Map

```text
src/streamsentry/
  api/             Versioned HTTP routes and application state
  domain/          Immutable data reliability records and enums
  evaluation/      Deterministic quality policy evaluators
  persistence/     Transactional SQLAlchemy session boundary
  services/        Application workflows and state transitions
  store/           Storage protocol and thread-safe memory adapter
web/src/
  components/      Shared operator interface elements
  hooks/           API lifecycle state
  lib/             Typed API client and formatters
  views/           Operational console sections
migrations/        Normalized relational schema
tests/             Unit, workflow, persistence, and API contract tests
```

## Design Notes

The default process deliberately uses the memory adapter so a new contributor can run every workflow without provisioning infrastructure. The store protocol, SQLAlchemy session boundary, and normalized schema make the persistence seam explicit without pretending that the demo process writes to PostgreSQL today.

See [Architecture](docs/architecture.md) and [API Guide](docs/api.md) for deeper details.

## License

MIT
