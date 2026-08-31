import { ArrowRight, Network } from 'lucide-react'
import { useState } from 'react'

import { StatusPill } from '../components/StatusPill'
import type { ObservatoryData } from '../types'

interface LineageViewProps { data: ObservatoryData }

export function LineageView({ data }: LineageViewProps) {
  const [focusId, setFocusId] = useState(data.datasets[0]?.id ?? '')
  const datasets = new Map(data.datasets.map((dataset) => [dataset.id, dataset]))
  const connected = data.lineage.filter((edge) => edge.upstream_dataset_id === focusId || edge.downstream_dataset_id === focusId)
  return <div className="view-stack"><section className="toolbar panel"><label><span>Focus dataset</span><select value={focusId} onChange={(event) => setFocusId(event.target.value)}>{data.datasets.map((dataset) => <option key={dataset.id} value={dataset.id}>{dataset.name}</option>)}</select></label><div className="result-count"><strong>{connected.length}</strong><span>direct dependencies</span></div></section><section className="panel lineage-canvas"><div className="section-heading"><div><h2>Dependency map</h2><p>Direct upstream and downstream relationships for impact analysis.</p></div></div>{connected.length ? <div className="lineage-list">{connected.map((edge) => { const upstream = datasets.get(edge.upstream_dataset_id); const downstream = datasets.get(edge.downstream_dataset_id); return <article className="lineage-edge" key={edge.id}><div className={edge.upstream_dataset_id === focusId ? 'lineage-node focus' : 'lineage-node'}><Network /><span><small>Upstream</small><strong>{upstream?.name}</strong><StatusPill value={upstream?.status ?? 'unknown'} /></span></div><div className="edge-label"><ArrowRight /><span>{edge.transformation}</span></div><div className={edge.downstream_dataset_id === focusId ? 'lineage-node focus' : 'lineage-node'}><Network /><span><small>Downstream</small><strong>{downstream?.name}</strong><StatusPill value={downstream?.status ?? 'unknown'} /></span></div></article>})}</div> : <div className="empty-state"><Network /><strong>No direct dependencies</strong><span>This dataset is currently isolated in the observed graph.</span></div>}</section></div>
}
