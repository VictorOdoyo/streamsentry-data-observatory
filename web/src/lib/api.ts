import type {
  CostSignal,
  DashboardMetrics,
  Dataset,
  Incident,
  LineageEdge,
  ObservatoryData,
  Owner,
  QualityCheck,
  QualityRun,
  ServiceLevelObjective,
  Workspace,
} from '../types'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8080'

export class ApiError extends Error {
  readonly status: number

  constructor(message: string, status: number) {
    super(message)
    this.status = status
  }
}

async function request<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { Accept: 'application/json' },
    signal,
  })
  if (!response.ok) {
    throw new ApiError(`Request failed with status ${response.status}`, response.status)
  }
  return response.json() as Promise<T>
}

export async function fetchObservatoryData(signal?: AbortSignal): Promise<ObservatoryData> {
  const workspaces = await request<Workspace[]>('/api/v1/workspaces', signal)
  const workspace = workspaces[0]
  if (!workspace) throw new ApiError('No workspace is available', 404)
  const path = `/api/v1/workspaces/${workspace.id}`
  const [owners, datasets, checks, runs, incidents, lineage, slos, costs, metrics] =
    await Promise.all([
      request<Owner[]>(`${path}/owners`, signal),
      request<Dataset[]>(`${path}/datasets`, signal),
      request<QualityCheck[]>(`${path}/checks`, signal),
      request<QualityRun[]>(`${path}/runs`, signal),
      request<Incident[]>(`${path}/incidents`, signal),
      request<LineageEdge[]>(`${path}/lineage`, signal),
      request<ServiceLevelObjective[]>(`${path}/slos`, signal),
      request<CostSignal[]>(`${path}/costs`, signal),
      request<DashboardMetrics>(`${path}/dashboard`, signal),
    ])
  return { workspace, owners, datasets, checks, runs, incidents, lineage, slos, costs, metrics }
}
