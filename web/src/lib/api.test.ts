import { afterEach, describe, expect, it, vi } from 'vitest'

import { ApiError, fetchObservatoryData } from './api'

const workspace = {
  id: 'workspace_1',
  slug: 'northstar',
  name: 'Northstar',
  created_at: '2026-08-18T12:00:00Z',
}

afterEach(() => vi.restoreAllMocks())

describe('observatory API client', () => {
  it('loads the workspace resources concurrently', async () => {
    const responseByPath: Record<string, unknown> = {
      '/api/v1/workspaces': [workspace],
      '/owners': [],
      '/datasets': [],
      '/checks': [],
      '/runs': [],
      '/incidents': [],
      '/lineage': [],
      '/slos': [],
      '/costs': [],
      '/dashboard': {
        datasets: 0,
        failing_datasets: 0,
        open_incidents: 0,
        failed_runs: 0,
        slo_breaches: 0,
        warehouse_cost_usd: 0,
        reliability_score: 100,
      },
    }
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation((input) => {
      const url = String(input)
      const key = Object.keys(responseByPath).find((path) => url.endsWith(path))
      return Promise.resolve(
        new Response(JSON.stringify(key ? responseByPath[key] : null), { status: 200 }),
      )
    })
    const result = await fetchObservatoryData()
    expect(result.workspace.name).toBe('Northstar')
    expect(result.metrics.reliability_score).toBe(100)
    expect(fetchMock).toHaveBeenCalledTimes(10)
  })

  it('rejects a missing workspace', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('[]', { status: 200 }))
    await expect(fetchObservatoryData()).rejects.toEqual(
      new ApiError('No workspace is available', 404),
    )
  })

  it('returns the failed HTTP status', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('{}', { status: 503 }))
    await expect(fetchObservatoryData()).rejects.toMatchObject({ status: 503 })
  })
})
