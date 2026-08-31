from fastapi.testclient import TestClient

from streamsentry.api.state import ApplicationState


def workspace_path(state: ApplicationState) -> str:
    return f"/api/v1/workspaces/{state.default_workspace_id}"


def test_health_and_observatory_reads(client: TestClient, state: ApplicationState) -> None:
    response = client.get("/health/live", headers={"X-Request-ID": "trace-42"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "trace-42"
    assert client.get("/health/ready").json()["workspace_id"] == state.default_workspace_id
    assert len(client.get("/api/v1/workspaces").json()) == 1
    path = workspace_path(state)
    expected_non_empty = (
        "owners",
        "datasets",
        "checks",
        "runs",
        "incidents",
        "lineage",
        "slos",
        "costs",
    )
    for resource in expected_non_empty:
        result = client.get(f"{path}/{resource}")
        assert result.status_code == 200
        assert result.json()
    metrics = client.get(f"{path}/dashboard").json()
    assert metrics["datasets"] == 5
    assert metrics["reliability_score"] == 50.0


def test_dataset_and_check_mutations(client: TestClient, state: ApplicationState) -> None:
    path = workspace_path(state)
    owner_id = client.get(f"{path}/owners").json()[0]["id"]
    dataset = client.post(
        f"{path}/datasets",
        json={
            "name": "Shipment facts",
            "fully_qualified_name": "analytics.logistics.fct_shipments",
            "platform": "Snowflake",
            "tier": "standard",
            "owner_id": owner_id,
            "tags": ["logistics"],
        },
    )
    assert dataset.status_code == 201
    dataset_id = dataset.json()["id"]
    changed = client.patch(f"{path}/datasets/{dataset_id}/status", json={"status": "degraded"})
    assert changed.json()["status"] == "degraded"
    check = client.post(
        f"{path}/checks",
        json={
            "dataset_id": dataset_id,
            "name": "Shipment volume",
            "check_type": "volume",
            "severity": "warning",
            "configuration": {"minimum_rows": 10, "maximum_rows": 100},
        },
    )
    assert check.status_code == 201
    check_id = check.json()["id"]
    assert (
        client.patch(f"{path}/checks/{check_id}/enabled", json={"enabled": True}).status_code == 200
    )
    run = client.post(
        f"{path}/checks/{check_id}/runs",
        json={"observed_at": "2026-08-18T12:00:00Z", "row_count": 50},
    )
    assert run.status_code == 201
    assert run.json()["status"] == "passed"


def test_incident_lineage_slo_and_cost_mutations(
    client: TestClient, state: ApplicationState
) -> None:
    path = workspace_path(state)
    datasets = client.get(f"{path}/datasets").json()
    owners = client.get(f"{path}/owners").json()
    first, second = datasets[0], datasets[1]
    incident = client.post(
        f"{path}/incidents",
        json={
            "dataset_id": first["id"],
            "title": "Warehouse delay",
            "summary": "The reporting load missed its expected completion window.",
            "severity": "sev2",
        },
    )
    assert incident.status_code == 201
    incident_id = incident.json()["id"]
    assigned = client.post(
        f"{path}/incidents/{incident_id}/assignment", json={"owner_id": owners[0]["id"]}
    )
    assert assigned.json()["assignee_id"] == owners[0]["id"]
    transitioned = client.post(
        f"{path}/incidents/{incident_id}/transition", json={"status": "investigating"}
    )
    assert transitioned.json()["status"] == "investigating"

    edge = client.post(
        f"{path}/lineage",
        json={
            "upstream_dataset_id": first["id"],
            "downstream_dataset_id": second["id"],
            "transformation": "contract projection",
        },
    )
    if edge.status_code == 409:
        first, second = datasets[-2], datasets[-1]
        edge = client.post(
            f"{path}/lineage",
            json={
                "upstream_dataset_id": first["id"],
                "downstream_dataset_id": second["id"],
                "transformation": "contract projection",
            },
        )
    assert edge.status_code == 201
    impact = client.get(f"{path}/lineage/{first['id']}/impact").json()
    assert second["id"] in impact["downstream_dataset_ids"]

    slo = client.post(
        f"{path}/slos",
        json={
            "dataset_id": first["id"],
            "name": "Fresh data",
            "freshness_minutes": 45,
            "success_rate_target": 0.99,
            "window_days": 7,
        },
    )
    assert slo.status_code == 201
    evaluated = client.post(
        f"{path}/slos/{slo.json()['id']}/evaluation", json={"current_success_rate": 0.8}
    )
    assert evaluated.json()["status"] == "breached"
    cost = client.post(
        f"{path}/costs",
        json={
            "dataset_id": first["id"],
            "period_start": "2026-08-01",
            "period_end": "2026-08-31",
            "amount_usd": 99.5,
            "query_count": 45,
            "scanned_bytes": 1000,
            "trend": "stable",
        },
    )
    assert cost.status_code == 201


def test_structured_domain_errors(client: TestClient, state: ApplicationState) -> None:
    response = client.patch(
        f"{workspace_path(state)}/datasets/missing/status",
        headers={"X-Request-ID": "error-trace"},
        json={"status": "healthy"},
    )
    assert response.status_code == 404
    assert response.json() == {
        "code": "not_found",
        "message": "dataset not found",
        "request_id": "error-trace",
    }
