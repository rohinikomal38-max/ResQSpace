
import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import './App.css'

const API_URL = 'http://localhost:3000/api/results'

function StatusBadge({ status }) {
  const labels = {
    available: 'Available',
    unavailable: 'Awaiting data',
    invalid: 'Invalid data',
    error: 'Read error',
    ready: 'Ready',
    partial: 'Partial',
  }

  return (
    <span className={`status status-${status || 'unknown'}`}>
      {labels[status] || status || 'Unknown'}
    </span>
  )
}

function FitGeoJSON({ data }) {
  const map = useMap()

  useEffect(() => {
    if (!data?.features?.length) return

    const layer = L.geoJSON(data)
    const bounds = layer.getBounds()

    if (bounds.isValid()) {
      map.fitBounds(bounds, { padding: [24, 24] })
    }
  }, [data, map])

  return null
}

function MapPanel({ floodData }) {
  return (
    <section className="panel map-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">GEOSPATIAL VIEW</p>
          <h2>Flood extent map</h2>
        </div>
        <span className="map-key"><i /> Potential flood extent</span>
      </div>

      <div className="map-frame">
        <MapContainer
          center={[20.5937, 78.9629]}
          zoom={5}
          scrollWheelZoom
          className="leaflet-map"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {floodData && (
            <>
              <GeoJSON
                data={floodData}
                style={{
                  color: '#e45e50',
                  weight: 2,
                  fillColor: '#f27662',
                  fillOpacity: 0.4,
                }}
              />
              <FitGeoJSON data={floodData} />
            </>
          )}
        </MapContainer>

        {!floodData && (
          <div className="map-empty">
            <div className="map-empty-icon">⌖</div>
            <h3>Waiting for flood layer</h3>
            <p>
              The map will display flood polygons when
              flood_extent.geojson becomes available.
            </p>
          </div>
        )}
      </div>
      <p className="panel-footnote">
        Map centered on India by default. No flood extent is inferred when
        source data is unavailable.
      </p>
    </section>
  )
}

function MetricCard({ label, value, note, accent }) {
  return (
    <article className={`metric-card ${accent || ''}`}>
      <p className="metric-label">{label}</p>
      <div className="metric-value">{value}</div>
      <p className="metric-note">{note}</p>
    </article>
  )
}

function OutputRow({ label, file }) {
  return (
    <div className="output-row">
      <div className="output-info">
        <span className="file-dot" />
        <div>
          <p>{label}</p>
          <small>{file?.status === 'available' ? 'Loaded successfully' : file?.message || 'Waiting for pipeline output'}</small>
        </div>
      </div>
      <StatusBadge status={file?.status} />
    </div>
  )
}

export default function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadResults() {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(API_URL)
      if (!response.ok) throw new Error(`API returned HTTP ${response.status}`)
      setResults(await response.json())
    } catch {
      setError('Cannot reach the backend. Make sure the Express server is running on port 3000.')
    } finally {
      setLoading(false)
    }
  }
 useEffect(() => {
  let cancelled = false

  async function fetchResults() {
    setError('')

    try {
      const response = await fetch(API_URL)

      if (!response.ok) {
        throw new Error(`API returned HTTP ${response.status}`)
      }

      const data = await response.json()

      if (!cancelled) {
        setResults(data)
      }
    } catch {
      if (!cancelled) {
        setError(
          'Cannot reach the backend. Make sure the Express server is running on port 3000.'
        )
      }
    } finally {
      if (!cancelled) {
        setLoading(false)
      }
    }
  }

  fetchResults()

  return () => {
    cancelled = true
  }
}, [])
  
  const files = results?.files || {}
  const floodSummary = files.floodSummary?.data
  const infrastructureSummary = files.infrastructureSummary?.data
  const connectivitySummary = files.connectivitySummary?.data
  const floodData = files.floodExtent?.status === 'available'
    ? files.floodExtent.data
    : null

  const floodedArea = floodSummary?.flooded_area_m2
  const areaText = typeof floodedArea === 'number'
    ? `${(floodedArea / 1_000_000).toLocaleString(undefined, { maximumFractionDigits: 2 })} km²`
    : '—'

  const infrastructureCount =
    infrastructureSummary?.exposed_asset_count ??
    infrastructureSummary?.exposed_count ??
    null

  const isolatedCount =
    connectivitySummary?.isolated_settlement_count ??
    connectivitySummary?.isolated_count ??
    null

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#overview">
          <span className="brand-mark">R</span>
          <span>ResQ<span className="brand-light">Space</span></span>
        </a>

        <p className="nav-label">WORKSPACE</p>
        <a className="nav-item active" href="#overview"><span>▦</span> Overview</a>
        <a className="nav-item" href="#map"><span>⌖</span> Flood mapping</a>
        <a className="nav-item" href="#infrastructure"><span>⌂</span> Infrastructure</a>
        <a className="nav-item" href="#connectivity"><span>⇄</span> Connectivity</a>
        <a className="nav-item" href="#outputs"><span>▤</span> Data outputs</a>

        <div className="sidebar-bottom">
          <span className="live-indicator" />
          <div>
            <strong>Analysis workspace</strong>
            <small>Multimodal AI · Track B</small>
          </div>
        </div>
      </aside>

      <section className="main-content" id="overview">
        <header className="topbar">
          <div className="breadcrumb">Workspace <span>/</span> Overview</div>
          <div className="topbar-right">
            <span className="environment-label">DEVELOPMENT</span>
            <button className="refresh-button" onClick={loadResults} disabled={loading}>
              <span>{loading ? '↻' : '⟳'}</span> {loading ? 'Loading…' : 'Refresh data'}
            </button>
          </div>
        </header>

        <section className="welcome-section">
          <div>
            <p className="eyebrow">DISASTER INTELLIGENCE PLATFORM</p>
            <h1>Flood response overview<span>.</span></h1>
            <p className="welcome-copy">
              Satellite-derived flood mapping and infrastructure intelligence
              in one operational workspace.
            </p>
          </div>
          <div className="status-summary">
            <span className={`pulse ${results?.integrationStatus === 'ready' ? 'pulse-ready' : ''}`} />
            <div>
              <strong>{loading ? 'Connecting to pipeline' : error ? 'Backend disconnected' : results?.integrationStatus === 'ready' ? 'All outputs ready' : 'Data pipeline status'}</strong>
              <small>{loading ? 'Fetching analysis outputs' : error ? 'Check your backend server' : `${Object.values(files).filter(f => f.status === 'available').length} of 7 outputs available`}</small>
            </div>
          </div>
        </section>

        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button onClick={loadResults}>Retry</button>
          </div>
        )}

        <section className="metrics-grid" aria-label="Flood response metrics">
          <MetricCard
            label="FLOODED AREA"
            value={areaText}
            note={floodSummary ? 'From flood summary' : 'Awaiting validated measurements'}
            accent="metric-coral"
          />
          <MetricCard
            label="EXPOSED INFRASTRUCTURE"
            value={infrastructureCount ?? '—'}
            note={infrastructureCount == null ? 'Awaiting infrastructure summary' : 'Reported by analysis output'}
            accent="metric-amber"
          />
          <MetricCard
            label="POTENTIALLY ISOLATED"
            value={isolatedCount ?? '—'}
            note={isolatedCount == null ? 'Awaiting connectivity summary' : 'Potential isolation, not confirmed'}
            accent="metric-blue"
          />
          <MetricCard
            label="OUTPUTS AVAILABLE"
            value={`${Object.values(files).filter(f => f.status === 'available').length}/7`}
            note={loading ? 'Checking output files' : 'Pipeline output availability'}
            accent="metric-green"
          />
        </section>

        <div id="map" className="dashboard-grid">
          <MapPanel floodData={floodData} />

          <section className="panel analysis-panel" id="infrastructure">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">ANALYSIS STATUS</p>
                <h2>Operational layers</h2>
              </div>
            </div>
            <div className="layer-list">
              <div className="layer-item">
                <span className="layer-icon flood-icon">≈</span>
                <div className="layer-copy"><strong>Flood extent</strong><small>Satellite-derived polygons</small></div>
                <StatusBadge status={files.floodExtent?.status} />
              </div>
              <div className="layer-item">
                <span className="layer-icon infra-icon">⌂</span>
                <div className="layer-copy"><strong>Infrastructure exposure</strong><small>Potential asset exposure</small></div>
                <StatusBadge status={files.infrastructureExposure?.status} />
              </div>
              <div className="layer-item" id="connectivity">
                <span className="layer-icon road-icon">⇄</span>
                <div className="layer-copy"><strong>Road connectivity</strong><small>Potential access disruption</small></div>
                <StatusBadge status={files.roadConnectivity?.status} />
              </div>
            </div>
            <div className="uncertainty-note">
              <strong>Interpretation note</strong>
              <p>Exposure and isolation are potential analytical outcomes, not verified damage or confirmed road closures.</p>
            </div>
          </section>
        </div>

        <section className="panel outputs-panel" id="outputs">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">BACKEND INTEGRATION</p>
              <h2>Analysis outputs</h2>
            </div>
            <span className="schema-tag">Schema {results?.schemaVersion || '0.1.0'}</span>
          </div>
          <div className="outputs-grid">
            <OutputRow label="Flood extent" file={files.floodExtent} />
            <OutputRow label="Flood summary" file={files.floodSummary} />
            <OutputRow label="Infrastructure exposure" file={files.infrastructureExposure} />
            <OutputRow label="Infrastructure summary" file={files.infrastructureSummary} />
            <OutputRow label="Road connectivity" file={files.roadConnectivity} />
            <OutputRow label="Connectivity summary" file={files.connectivitySummary} />
            <OutputRow label="Analysis metadata" file={files.analysisMetadata} />
          </div>
          <div className="outputs-footer">
            <span>{results?.warnings?.length ?? 7} output notice(s)</span>
            <span>{loading ? 'Refreshing…' : 'Last checked just now'}</span>
          </div>
        </section>

        <footer className="page-footer">
          <span>ResQSpace · Disaster intelligence for informed response</span>
          <span>Potential outcomes are not ground-truth confirmations.</span>
        </footer>
      </section>
    </main>
  )
}
