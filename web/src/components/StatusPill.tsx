import { titleCase } from '../lib/format'

interface StatusPillProps {
  value: string
}

export function StatusPill({ value }: StatusPillProps) {
  return <span className={`status-pill status-${value}`}>{titleCase(value)}</span>
}
