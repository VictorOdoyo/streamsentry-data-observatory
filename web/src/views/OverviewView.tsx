import { AlertTriangle, CircleDollarSign, Database, ShieldCheck } from 'lucide-react'

import { StatusPill } from '../components/StatusPill'
import { formatCurrency, formatDateTime } from '../lib/format'
import type { ObservatoryData } from '../types'

interface OverviewViewProps {
  data: ObservatoryData
  onOpenIncidents: () => void
}

export function OverviewView({ data, onOpenIncidents }: OverviewViewProps) {
  const recentRuns = data.runs.slice(0, 5)
  const activeIncidents = data.incidents.filter((incident) => incident.status !== 'resolved')
  const datasetName = new Map(data.datasets.map((dataset) => [dataset.id, dataset.name]))

  return (
    <div className="view-stack">
      <section className="metric-grid" aria-label="Reliability metrics">
        <article className="metric-block"><Database /><span>Monitored datasets</span><strong>{data.metrics.datasets}</strong><small>{data.metrics.failing_datasets} currently failing</small></article>
        <article className="metric-block"><ShieldCheck /><span>Reliability score</span><strong>{data.metrics.reliability_score}%</strong><small>{data.metrics.failed_runs} failed recent runs</small></article>
        <article className="metric-block"><AlertTriangle /><span>Open incidents</span><strong>{data.metrics.open_incidents}</strong><small>{data.metrics.slo_breaches} SLO breaches</small></article>
        <article className="metric-block"><CircleDollarSign /><span>Observed spend</span><strong>{formatCurrency(data.metrics.warehouse_cost_usd)}</strong><small>Current reporting window</small></article>
      </section>

      <div className="overview-grid">
        <section className="panel">
          <div className="section-heading"><div><h2>Dataset health</h2><p>Current posture across monitored data products.</p></div></div>
          <div className="health-list">
            {data.datasets.map((dataset) => (
              <div className="health-row" key={dataset.id}>
                <span className={`health-dot status-${dataset.status}`} />
                <span className="grow"><strong>{dataset.name}</strong><small>{dataset.fully_qualified_name}</small></span>
                <StatusPill value={dataset.status} />
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="section-heading"><div><h2>Incident pressure</h2><p>Unresolved reliability events requiring attention.</p></div><button className="text-button" onClick={onOpenIncidents}>Open queue</button></div>
          {activeIncidents.length ? (
            <div className="incident-preview-list">
              {activeIncidents.map((incident) => (
                <article className="incident-preview" key={incident.id}>
                  <div><StatusPill value={incident.severity} /><StatusPill value={incident.status} /></div>
                  <h3>{incident.title}</h3>
                  <p>{incident.summary}</p>
                  <small>{datasetName.get(incident.dataset_id)} · {formatDateTime(incident.updated_at)}</small>
                </article>
              ))}
            </div>
          ) : <div className="empty-state"><ShieldCheck /><strong>No active incidents</strong><span>All monitored systems are within policy.</span></div>}
        </section>
      </div>

      <section className="panel">
        <div className="section-heading"><div><h2>Latest quality executions</h2><p>Most recent automated observations across all datasets.</p></div></div>
        <div className="table-wrap"><table><thead><tr><th>Dataset</th><th>Result</th><th>Observation</th><th>Finished</th></tr></thead><tbody>
          {recentRuns.map((run) => <tr key={run.id}><td><strong>{datasetName.get(run.dataset_id)}</strong></td><td><StatusPill value={run.status} /></td><td>{run.message}</td><td>{formatDateTime(run.finished_at)}</td></tr>)}
        </tbody></table></div>
      </section>
    </div>
  )
}
