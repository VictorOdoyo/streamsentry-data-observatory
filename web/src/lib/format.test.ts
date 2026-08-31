import { describe, expect, it } from 'vitest'

import { formatBytes, formatCompactNumber, formatCurrency, titleCase } from './format'

describe('operator formatters', () => {
  it('formats reliability values for compact scanning', () => {
    expect(formatCompactNumber(1_250_000)).toBe('1.3M')
    expect(formatCurrency(4521.25)).toBe('$4,521')
    expect(formatBytes(1024 ** 3)).toBe('1.0 GB')
    expect(formatBytes(0)).toBe('0 B')
  })

  it('normalizes status labels', () => {
    expect(titleCase('at_risk')).toBe('At Risk')
  })
})
