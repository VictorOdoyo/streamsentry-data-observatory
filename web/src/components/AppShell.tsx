import {
  Activity,
  BellRing,
  Boxes,
  Database,
  Gauge,
  Menu,
  Network,
  RefreshCw,
  ShieldAlert,
  X,
} from 'lucide-react'
import { useState, type ReactNode } from 'react'

import type { ViewKey } from '../types'

const navigation: Array<{ key: ViewKey; label: string; icon: typeof Gauge }> = [
  { key: 'overview', label: 'Overview', icon: Gauge },
  { key: 'datasets', label: 'Datasets', icon: Database },
  { key: 'quality', label: 'Quality monitor', icon: Activity },
  { key: 'incidents', label: 'Incidents', icon: ShieldAlert },
  { key: 'lineage', label: 'Lineage', icon: Network },
  { key: 'reliability', label: 'Reliability & cost', icon: Boxes },
]

interface AppShellProps {
  activeView: ViewKey
  children: ReactNode
  workspaceName: string
  onNavigate: (view: ViewKey) => void
  onRefresh: () => void
}

export function AppShell({
  activeView,
  children,
  workspaceName,
  onNavigate,
  onRefresh,
}: AppShellProps) {
  const [menuOpen, setMenuOpen] = useState(false)
  const activeLabel = navigation.find((item) => item.key === activeView)?.label ?? 'Overview'

  const navigate = (view: ViewKey) => {
    onNavigate(view)
    setMenuOpen(false)
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${menuOpen ? 'sidebar-open' : ''}`}>
        <div className="brand">
          <span className="brand-mark"><Activity size={21} /></span>
          <span><strong>StreamSentry</strong><small>Data observatory</small></span>
        </div>
        <nav aria-label="Primary navigation">
          {navigation.map(({ key, label, icon: Icon }) => (
            <button
              className={activeView === key ? 'nav-item active' : 'nav-item'}
              key={key}
              onClick={() => navigate(key)}
              type="button"
            >
              <Icon size={18} />
              <span>{label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <BellRing size={17} />
          <span><strong>Telemetry live</strong><small>9 monitors reporting</small></span>
        </div>
      </aside>
      {menuOpen && <button className="sidebar-scrim" aria-label="Close menu" onClick={() => setMenuOpen(false)} />}
      <main className="main-content">
        <header className="topbar">
          <button className="icon-button menu-button" aria-label="Open menu" onClick={() => setMenuOpen(true)}>
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <div>
            <span className="eyebrow">{workspaceName}</span>
            <h1>{activeLabel}</h1>
          </div>
          <button className="secondary-button" onClick={onRefresh} type="button">
            <RefreshCw size={16} /> Refresh
          </button>
        </header>
        <div className="view-content">{children}</div>
      </main>
    </div>
  )
}
