import { AlertCircle, LoaderCircle, RefreshCw } from 'lucide-react'
import { useState, type ReactNode } from 'react'

import './App.css'
import { AppShell } from './components/AppShell'
import { useObservatoryData } from './hooks/useObservatoryData'
import type { ViewKey } from './types'
import { DatasetsView } from './views/DatasetsView'
import { IncidentsView } from './views/IncidentsView'
import { LineageView } from './views/LineageView'
import { OverviewView } from './views/OverviewView'
import { QualityView } from './views/QualityView'
import { ReliabilityView } from './views/ReliabilityView'

function App() {
  const [activeView, setActiveView] = useState<ViewKey>('overview')
  const state = useObservatoryData()

  if (state.status === 'loading') {
    return <main className="state-page"><LoaderCircle className="spin" /><h1>Loading observatory</h1><p>Collecting the latest quality and reliability signals.</p></main>
  }

  if (state.status === 'error') {
    return <main className="state-page"><AlertCircle /><h1>Unable to reach StreamSentry</h1><p>{state.error}</p><button className="primary-button" onClick={state.refresh}><RefreshCw size={17} />Try again</button></main>
  }

  const data = state.data
  const views: Record<ViewKey, ReactNode> = {
    overview: <OverviewView data={data} onOpenIncidents={() => setActiveView('incidents')} />,
    datasets: <DatasetsView data={data} />,
    quality: <QualityView data={data} />,
    incidents: <IncidentsView data={data} />,
    lineage: <LineageView data={data} />,
    reliability: <ReliabilityView data={data} />,
  }

  return <AppShell activeView={activeView} workspaceName={data.workspace.name} onNavigate={setActiveView} onRefresh={state.refresh}>{views[activeView]}</AppShell>
}

export default App
