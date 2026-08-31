export const formatCompactNumber = (value: number) =>
  new Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 }).format(value)

export const formatCurrency = (value: number) =>
  new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  }).format(value)

export const formatDateTime = (value: string) =>
  new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  }).format(new Date(value))

export const formatBytes = (value: number) => {
  if (value === 0) return '0 B'
  const unit = Math.floor(Math.log(value) / Math.log(1024))
  const units = ['B', 'KB', 'MB', 'GB', 'TB']
  return `${(value / 1024 ** unit).toFixed(unit > 2 ? 1 : 0)} ${units[unit]}`
}

export const titleCase = (value: string) =>
  value.replaceAll('_', ' ').replace(/\b\w/g, (character) => character.toUpperCase())
