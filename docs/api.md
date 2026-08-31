# API Guide

All operational resources are under `/api/v1/workspaces/{workspace_id}`. The seeded workspace identifier is returned by `GET /api/v1/workspaces` and by the readiness endpoint.

## Health

- `GET /health/live` confirms the process is running.
- `GET /health/ready` confirms application state has been assembled.

Every response includes `X-Request-ID`. Clients may supply a request identifier of up to 128 characters; otherwise the API creates one.

## Catalog And Quality

- `GET|POST /api/v1/workspaces/{workspace_id}/datasets`
- `PATCH /api/v1/workspaces/{workspace_id}/datasets/{dataset_id}/status`
- `GET|POST /api/v1/workspaces/{workspace_id}/checks`
- `PATCH /api/v1/workspaces/{workspace_id}/checks/{check_id}/enabled`
- `POST /api/v1/workspaces/{workspace_id}/checks/{check_id}/runs`
- `GET /api/v1/workspaces/{workspace_id}/runs`

## Response Operations

- `GET|POST /api/v1/workspaces/{workspace_id}/incidents`
- `POST /api/v1/workspaces/{workspace_id}/incidents/{incident_id}/assignment`
- `POST /api/v1/workspaces/{workspace_id}/incidents/{incident_id}/transition`
- `GET|POST /api/v1/workspaces/{workspace_id}/lineage`
- `GET /api/v1/workspaces/{workspace_id}/lineage/{dataset_id}/impact`

## Reliability And Cost

- `GET /api/v1/workspaces/{workspace_id}/dashboard`
- `GET|POST /api/v1/workspaces/{workspace_id}/slos`
- `POST /api/v1/workspaces/{workspace_id}/slos/{slo_id}/evaluation`
- `GET|POST /api/v1/workspaces/{workspace_id}/costs`

Interactive request schemas and response examples are available at `/docs` when the API is running.

## Errors

Domain failures use one predictable shape:

```json
{
  "code": "not_found",
  "message": "dataset not found",
  "request_id": "trace-42"
}
```

Validation failures return `422`, missing resources return `404`, and transition or uniqueness conflicts return `409`.
