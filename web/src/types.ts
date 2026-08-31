export type DatasetStatus = 'healthy' | 'degraded' | 'failing' | 'paused'
export type DatasetTier = 'critical' | 'standard' | 'experimental'
export type RunStatus = 'passed' | 'failed' | 'skipped'
export type IncidentStatus = 'open' | 'investigating' | 'monitoring' | 'resolved'
export type IncidentSeverity = 'sev1' | 'sev2' | 'sev3'
export type SloStatus = 'meeting' | 'at_risk' | 'breached'

export interface Workspace {
  id: string
  slug: string
  name: string
  created_at: string
}

export interface Owner {
  id: string
  workspace_id: string
  name: string
  email: string
  team: string
  created_at: string
}

export interface Dataset {
  id: string
  workspace_id: string
  name: string
  fully_qualified_name: string
  platform: string
  tier: DatasetTier
  status: DatasetStatus
  owner_id: string
  description: string
  tags: string[]
  last_observed_at: string
  row_count: number
  size_bytes: number
  created_at: string
}

export interface QualityCheck {
  id: string
  workspace_id: string
  dataset_id: string
  name: string
  check_type: string
  severity: 'info' | 'warning' | 'critical'
  enabled: boolean
  configuration: Record<string, unknown>
  created_at: string
}

export interface QualityRun {
  id: string
  workspace_id: string
  dataset_id: string
  check_id: string
  status: RunStatus
  observed_value: number | string | null
  expected_value: number | string | null
  message: string
  metrics: Record<string, unknown>
  started_at: string
  finished_at: string
}

export interface Incident {
  id: string
  workspace_id: string
  dataset_id: string
  check_id: string | null
  title: string
  summary: string
  severity: IncidentSeverity
  status: IncidentStatus
  assignee_id: string | null
  created_at: string
  updated_at: string
  resolved_at: string | null
}

export interface LineageEdge {
  id: string
  workspace_id: string
  upstream_dataset_id: string
  downstream_dataset_id: string
  transformation: string
  observed_at: string
}

export interface ServiceLevelObjective {
  id: string
  workspace_id: string
  dataset_id: string
  name: string
  freshness_minutes: number
  success_rate_target: number
  current_success_rate: number
  status: SloStatus
  window_days: number
  evaluated_at: string
}

export interface CostSignal {
  id: string
  workspace_id: string
  dataset_id: string
  period_start: string
  period_end: string
  amount_usd: number
  query_count: number
  scanned_bytes: number
  trend: 'up' | 'stable' | 'down'
  observed_at: string
}

export interface DashboardMetrics {
  datasets: number
  failing_datasets: number
  open_incidents: number
  failed_runs: number
  slo_breaches: number
  warehouse_cost_usd: number
  reliability_score: number
}

export interface ObservatoryData {
  workspace: Workspace
  owners: Owner[]
  datasets: Dataset[]
  checks: QualityCheck[]
  runs: QualityRun[]
  incidents: Incident[]
  lineage: LineageEdge[]
  slos: ServiceLevelObjective[]
  costs: CostSignal[]
  metrics: DashboardMetrics
}

export type ViewKey = 'overview' | 'datasets' | 'quality' | 'incidents' | 'lineage' | 'reliability'
