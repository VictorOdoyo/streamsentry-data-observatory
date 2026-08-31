import { AlertOctagon, Clock3, UserRoundCheck } from 'lucide-react'
import { useState } from 'react'

import { StatusPill } from '../components/StatusPill'
import { formatDateTime } from '../lib/format'
import type { Incident, ObservatoryData } from '../types'

interface IncidentsViewProps { data: ObservatoryData }

export function IncidentsView({ data }: IncidentsViewProps) {
  const [selected, setSelected] = useState<Incident | null>(data.incidents[0] ?? null)
  const datasetName = new Map(data.datasets.map((dataset) => [dataset.id, dataset.name]))
  const ownerName = new Map(data.owners.map((owner) => [owner.id, owner.name]))
  return <div className="incident-layout">
    <section className="panel incident-queue"><div className="section-heading"><div><h2>Incident queue</h2><p>Reliability events ordered by current urgency.</p></div><span className="count-badge">{data.incidents.length}</span></div><div className="queue-list">{data.incidents.map((incident) => <button className={selected?.id === incident.id ? 'queue-item selected' : 'queue-item'} key={incident.id} onClick={() => setSelected(incident)}><span className={`severity-bar status-${incident.severity}`} /><span className="grow"><span><StatusPill value={incident.severity} /><StatusPill value={incident.status} /></span><strong>{incident.title}</strong><small>{datasetName.get(incident.dataset_id)} · {formatDateTime(incident.updated_at)}</small></span></button>)}</div></section>
    <section className="panel incident-detail">{selected ? <><div className="incident-detail-heading"><div><span className="eyebrow">Incident {selected.id.slice(-6).toUpperCase()}</span><h2>{selected.title}</h2></div><StatusPill value={selected.status} /></div><p className="detail-summary">{selected.summary}</p><div className="detail-facts"><div><AlertOctagon /><span><small>Affected dataset</small><strong>{datasetName.get(selected.dataset_id)}</strong></span></div><div><UserRoundCheck /><span><small>Incident owner</small><strong>{selected.assignee_id ? ownerName.get(selected.assignee_id) : 'Unassigned'}</strong></span></div><div><Clock3 /><span><small>Last updated</small><strong>{formatDateTime(selected.updated_at)}</strong></span></div></div><div className="timeline"><div><span /><article><small>{formatDateTime(selected.created_at)}</small><strong>Incident detected</strong><p>StreamSentry opened this incident from a failed quality observation.</p></article></div>{selected.assignee_id && <div><span /><article><small>Response milestone</small><strong>Owner assigned</strong><p>{ownerName.get(selected.assignee_id)} is coordinating the response.</p></article></div>}{selected.resolved_at && <div><span /><article><small>{formatDateTime(selected.resolved_at)}</small><strong>Reliability restored</strong><p>The incident was resolved after monitor recovery.</p></article></div>}</div></> : <div className="empty-state"><AlertOctagon /><strong>Select an incident</strong><span>Choose an event to inspect its response timeline.</span></div>}</section>
  </div>
}
