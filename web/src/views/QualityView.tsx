import { CircleCheck, CircleX, PauseCircle } from 'lucide-react'

import { StatusPill } from '../components/StatusPill'
import { formatDateTime, titleCase } from '../lib/format'
import type { ObservatoryData } from '../types'

interface QualityViewProps { data: ObservatoryData }

export function QualityView({ data }: QualityViewProps) {
  const datasetName = new Map(data.datasets.map((dataset) => [dataset.id, dataset.name]))
  const checkName = new Map(data.checks.map((check) => [check.id, check.name]))
  const passed = data.runs.filter((run) => run.status === 'passed').length
  const failed = data.runs.filter((run) => run.status === 'failed').length
  const skipped = data.runs.filter((run) => run.status === 'skipped').length
  return <div className="view-stack">
    <section className="quality-summary">
      <article><CircleCheck className="good" /><span>Passed runs</span><strong>{passed}</strong></article>
      <article><CircleX className="bad" /><span>Failed runs</span><strong>{failed}</strong></article>
      <article><PauseCircle className="muted" /><span>Skipped runs</span><strong>{skipped}</strong></article>
    </section>
    <section className="panel"><div className="section-heading"><div><h2>Check registry</h2><p>Active quality policies by dataset and severity.</p></div></div><div className="check-grid">{data.checks.map((check) => <article className="check-card" key={check.id}><div><StatusPill value={check.severity} /><StatusPill value={check.enabled ? 'enabled' : 'disabled'} /></div><h3>{check.name}</h3><p>{datasetName.get(check.dataset_id)}</p><small>{titleCase(check.check_type)} policy</small></article>)}</div></section>
    <section className="panel"><div className="section-heading"><div><h2>Execution history</h2><p>Observed and expected values from recent runs.</p></div></div><div className="table-wrap"><table><thead><tr><th>Check</th><th>Dataset</th><th>Result</th><th>Observed</th><th>Expected</th><th>Finished</th></tr></thead><tbody>{data.runs.map((run) => <tr key={run.id}><td><strong>{checkName.get(run.check_id)}</strong><small>{run.message}</small></td><td>{datasetName.get(run.dataset_id)}</td><td><StatusPill value={run.status} /></td><td>{String(run.observed_value ?? '—')}</td><td>{String(run.expected_value ?? '—')}</td><td>{formatDateTime(run.finished_at)}</td></tr>)}</tbody></table></div></section>
  </div>
}
