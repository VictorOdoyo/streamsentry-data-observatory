import { useCallback, useEffect, useState } from 'react'

import { fetchObservatoryData } from '../lib/api'
import type { ObservatoryData } from '../types'

type DataState =
  | { status: 'loading'; data: null; error: null }
  | { status: 'ready'; data: ObservatoryData; error: null }
  | { status: 'error'; data: null; error: string }

export function useObservatoryData() {
  const [state, setState] = useState<DataState>({ status: 'loading', data: null, error: null })
  const [refreshKey, setRefreshKey] = useState(0)

  const refresh = useCallback(() => {
    setState({ status: 'loading', data: null, error: null })
    setRefreshKey((value) => value + 1)
  }, [])

  useEffect(() => {
    const controller = new AbortController()
    fetchObservatoryData(controller.signal)
      .then((data) => setState({ status: 'ready', data, error: null }))
      .catch((error: unknown) => {
        if (controller.signal.aborted) return
        const message = error instanceof Error ? error.message : 'Unable to load observability data'
        setState({ status: 'error', data: null, error: message })
      })
    return () => controller.abort()
  }, [refreshKey])

  return { ...state, refresh }
}
