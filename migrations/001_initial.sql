CREATE TABLE workspaces (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(160) NOT NULL,
    slug VARCHAR(120) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE owners (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name VARCHAR(160) NOT NULL,
    email VARCHAR(255) NOT NULL,
    team VARCHAR(160) NOT NULL,
    UNIQUE (workspace_id, email)
);

CREATE TABLE datasets (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    owner_id VARCHAR(64) NOT NULL REFERENCES owners(id),
    name VARCHAR(160) NOT NULL,
    fully_qualified_name VARCHAR(320) NOT NULL,
    platform VARCHAR(80) NOT NULL,
    tier VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    tags JSON NOT NULL,
    last_observed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE (workspace_id, fully_qualified_name)
);

CREATE INDEX idx_datasets_workspace_status ON datasets (workspace_id, status);
CREATE INDEX idx_datasets_workspace_owner ON datasets (workspace_id, owner_id);

CREATE TABLE quality_checks (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    check_type VARCHAR(40) NOT NULL,
    severity VARCHAR(32) NOT NULL,
    configuration JSON NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_checks_workspace_dataset ON quality_checks (workspace_id, dataset_id);

CREATE TABLE quality_runs (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    check_id VARCHAR(64) NOT NULL REFERENCES quality_checks(id) ON DELETE CASCADE,
    dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    status VARCHAR(32) NOT NULL,
    observed_value JSON,
    expected_value JSON,
    message TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_runs_workspace_completed ON quality_runs (workspace_id, completed_at DESC);
CREATE INDEX idx_runs_dataset_status ON quality_runs (dataset_id, status);

CREATE TABLE incidents (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id),
    check_id VARCHAR(64) REFERENCES quality_checks(id),
    owner_id VARCHAR(64) REFERENCES owners(id),
    title VARCHAR(240) NOT NULL,
    summary TEXT NOT NULL,
    severity VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP
);

CREATE INDEX idx_incidents_workspace_status ON incidents (workspace_id, status);
CREATE INDEX idx_incidents_dataset_created ON incidents (dataset_id, created_at DESC);

CREATE TABLE lineage_edges (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    upstream_dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    downstream_dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    transformation VARCHAR(240) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    UNIQUE (workspace_id, upstream_dataset_id, downstream_dataset_id)
);

CREATE TABLE service_level_objectives (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    freshness_minutes INTEGER NOT NULL CHECK (freshness_minutes > 0),
    success_rate_target NUMERIC(6, 5) NOT NULL,
    current_success_rate NUMERIC(6, 5) NOT NULL,
    window_days INTEGER NOT NULL CHECK (window_days > 0),
    status VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE cost_signals (
    id VARCHAR(64) PRIMARY KEY,
    workspace_id VARCHAR(64) NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    dataset_id VARCHAR(64) NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    amount_usd NUMERIC(14, 2) NOT NULL,
    query_count INTEGER NOT NULL,
    scanned_bytes BIGINT NOT NULL,
    trend VARCHAR(32) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    UNIQUE (dataset_id, period_start, period_end)
);

CREATE INDEX idx_costs_workspace_period ON cost_signals (workspace_id, period_end DESC);
