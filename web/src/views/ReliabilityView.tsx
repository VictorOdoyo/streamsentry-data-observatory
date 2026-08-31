import { ArrowDownRight, ArrowRight, ArrowUpRight, CircleDollarSign, Target } from 'lucide-react'

import { StatusPill } from '../components/StatusPill'
import { formatBytes, formatCurrency, formatDateTime } from '../lib/format'
import type { ObservatoryData } from '../types'

interface ReliabilityViewProps { data: ObservatoryData }

const trendIcon = { down: ArrowDownRight, stable: ArrowRight, up: ArrowUpRight }

export function ReliabilityView({ data }: ReliabilityViewProps) {
  const datasetName = new Map(data.datasets.map((dataset) => [dataset.id, dataset.name]))
  return <div className="view-stack"><section className="panel"><div className="section-heading"><div><h2>Service level objectives</h2><p>Freshness and successful run targets for critical data products.</p></div></div><div className="slo-grid">{data.slos.map((slo) => { const percentage = Math.round(slo.current_success_rate * 1000) / 10; return <article className="slo-card" key={slo.id}><div><Target /><StatusPill value={slo.status} /></div><h3>{slo.name}</h3><p>{datasetName.get(slo.dataset_id)}</p><div className="progress-track"><span style={{ width: `${percentage}%` }} /></div><div className="slo-values"><strong>{percentage}%</strong><span>Target {(slo.success_rate_target * 100).toFixed(1)}%</span></div><small>{slo.freshness_minutes} min freshness · {slo.window_days} day window · evaluated {formatDateTime(slo.evaluated_at)}</small></article>})}</div></section><section className="panel"><div className="section-heading"><div><h2>Warehouse cost signals</h2><p>Observed query spend, scan volume, and directional movement.</p></div></div><div className="table-wrap"><table><thead><tr><th>Dataset</th><th>Period</th><th>Spend</th><th>Queries</th><th>Scanned</th><th>Trend</th></tr></thead><tbody>{data.costs.map((cost) => { const TrendIcon = trendIcon[cost.trend]; return <tr key={cost.id}><td><strong>{datasetName.get(cost.dataset_id)}</strong></td><td>{cost.period_start} to {cost.period_end}</td><td><strong>{formatCurrency(cost.amount_usd)}</strong></td><td>{cost.query_count.toLocaleString()}</td><td>{formatBytes(cost.scanned_bytes)}</td><td><span className={`trend trend-${cost.trend}`}><TrendIcon size={16} />{cost.trend}</span></td></tr>})}</tbody></table></div><div className="cost-note"><CircleDollarSign /><span><strong>Cost is a reliability signal.</strong> Sudden spend changes often reveal runaway jobs, reprocessing, or upstream schema churn before users report a problem.</span></div></section></div>
}
