import { Search } from 'lucide-react'
import { useMemo, useState } from 'react'

import { StatusPill } from '../components/StatusPill'
import { formatBytes, formatCompactNumber, formatDateTime, titleCase } from '../lib/format'
import type { Dataset, ObservatoryData } from '../types'

interface DatasetsViewProps { data: ObservatoryData }

export function DatasetsView({ data }: DatasetsViewProps) {
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('all')
  const [selected, setSelected] = useState<Dataset | null>(null)
  const ownerName = new Map(data.owners.map((owner) => [owner.id, owner.name]))
  const filtered = useMemo(() => data.datasets.filter((dataset) => {
    const matchesSearch = `${dataset.name} ${dataset.fully_qualified_name} ${dataset.tags.join(' ')}`.toLowerCase().includes(search.toLowerCase())
    return matchesSearch && (status === 'all' || dataset.status === status)
  }), [data.datasets, search, status])

  return (
    <div className="view-stack">
      <section className="toolbar panel">
        <label className="search-field"><span>Search datasets</span><div><Search size={17} /><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Name, table, or tag" /></div></label>
        <label><span>Health state</span><select value={status} onChange={(event) => setStatus(event.target.value)}><option value="all">All states</option><option value="healthy">Healthy</option><option value="degraded">Degraded</option><option value="failing">Failing</option><option value="paused">Paused</option></select></label>
        <div className="result-count"><strong>{filtered.length}</strong><span>datasets matched</span></div>
      </section>
      <section className="panel">
        <div className="section-heading"><div><h2>Dataset inventory</h2><p>Ownership, scale, freshness, and reliability state.</p></div></div>
        <div className="table-wrap"><table><thead><tr><th>Dataset</th><th>Platform</th><th>Owner</th><th>Tier</th><th>Rows</th><th>Observed</th><th>State</th></tr></thead><tbody>
          {filtered.map((dataset) => <tr className="clickable-row" key={dataset.id} onClick={() => setSelected(dataset)}><td><strong>{dataset.name}</strong><small>{dataset.fully_qualified_name}</small></td><td>{dataset.platform}</td><td>{ownerName.get(dataset.owner_id)}</td><td>{titleCase(dataset.tier)}</td><td>{formatCompactNumber(dataset.row_count)}</td><td>{formatDateTime(dataset.last_observed_at)}</td><td><StatusPill value={dataset.status} /></td></tr>)}
        </tbody></table></div>
      </section>
      {selected && <div className="drawer-backdrop" onMouseDown={() => setSelected(null)}><aside className="detail-drawer" onMouseDown={(event) => event.stopPropagation()} aria-label="Dataset details"><button className="drawer-close" onClick={() => setSelected(null)} aria-label="Close details">×</button><span className="eyebrow">{selected.platform} · {titleCase(selected.tier)}</span><h2>{selected.name}</h2><code>{selected.fully_qualified_name}</code><p>{selected.description}</p><dl><div><dt>Owner</dt><dd>{ownerName.get(selected.owner_id)}</dd></div><div><dt>Health</dt><dd><StatusPill value={selected.status} /></dd></div><div><dt>Rows</dt><dd>{formatCompactNumber(selected.row_count)}</dd></div><div><dt>Storage</dt><dd>{formatBytes(selected.size_bytes)}</dd></div><div><dt>Last observed</dt><dd>{formatDateTime(selected.last_observed_at)}</dd></div></dl><div className="tag-list">{selected.tags.map((tag) => <span key={tag}>{tag}</span>)}</div></aside></div>}
    </div>
  )
}
