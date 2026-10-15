
import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import './App.css'

const API_URL = 'http://localhost:3000/api/results'

function LandingPage({ onLaunch }) {
return ( <div className="landing-page"> <nav className="landing-nav"> <div className="landing-brand"> <span className="landing-brand-mark">R</span> <span>
ResQ<span className="landing-brand-light">Space</span> </span> </div> <span className="landing-nav-label">DISASTER INTELLIGENCE PLATFORM</span> </nav>

  <section className="landing-hero">
    <div className="landing-hero-content">
      <p className="landing-eyebrow">
        SATELLITE-POWERED DISASTER INTELLIGENCE
      </p>

      <h1>
        When floods strike,
        <br />
        <span>every second matters.</span>
      </h1>

      <p className="landing-description">
        ResQ Space transforms geospatial flood data into interactive
        visual insights to help emergency responders understand
        potentially affected areas and support disaster-response planning.
      </p>

      <div className="landing-actions">
        <button
          className="landing-button landing-button-primary"
          onClick={onLaunch}
        >
          Launch Dashboard &rarr;
        </button>

        <a
          className="landing-button landing-button-secondary"
          href="#how-it-works"
        >
          Discover How It Works
        </a>
      </div>
    </div>
  </section>

  <section className="landing-section">
    <div className="landing-section-heading">
      <p className="landing-eyebrow">BUILT FOR DISASTER RESPONSE</p>
      <h2>From geospatial data to actionable insights.</h2>
      <p>
        Explore potential flood impacts through a unified geospatial
        analysis workspace.
      </p>
    </div>

    <div className="landing-features">
      <article className="landing-feature-card">
        <div className="landing-feature-icon">🛰️</div>
        <h3>Flood Mapping</h3>
        <p>
          Visualize available flood-extent data on an interactive map
          to understand potentially affected geographic areas.
        </p>
      </article>

      <article className="landing-feature-card">
        <div className="landing-feature-icon">🏗️</div>
        <h3>Infrastructure Exposure</h3>
        <p>
          Organize infrastructure-exposure analysis outputs to support
          assessment of potentially affected assets.
        </p>
      </article>

      <article className="landing-feature-card">
        <div className="landing-feature-icon">🛣️</div>
        <h3>Connectivity Insights</h3>
        <p>
          Present available road-connectivity analysis outputs to help
          assess possible access disruptions.
        </p>
      </article>
    </div>
  </section>

  <section className="landing-section" id="how-it-works">
    <div className="landing-section-heading">
      <p className="landing-eyebrow">HOW IT WORKS</p>
      <h2>A clearer picture of flood impact.</h2>
      <p>
        ResQ Space brings geospatial processing and interactive
        visualization together in one workspace.
      </p>
    </div>

    <div className="landing-process">
      <article className="landing-process-step">
        <span className="landing-step-number">01</span>
        <h3>Geospatial Data</h3>
        <p>Start with available satellite-derived and geographic inputs.</p>
      </article>

      <article className="landing-process-step">
        <span className="landing-step-number">02</span>
        <h3>Flood Analysis</h3>
        <p>Process available inputs into geospatial analysis outputs.</p>
      </article>

      <article className="landing-process-step">
        <span className="landing-step-number">03</span>
        <h3>Visualize Results</h3>
        <p>Present available geographic results and summary metrics.</p>
      </article>

      <article className="landing-process-step">
        <span className="landing-step-number">04</span>
        <h3>Explore Insights</h3>
        <p>Review output availability and potential impacts in the dashboard.</p>
      </article>
    </div>
  </section>

  <section className="landing-cta">
    <h2>Explore the map. Understand the impact.</h2>
    <p>
      Open the ResQ Space workspace to explore available flood data,
      analysis summaries, and geospatial outputs.
    </p>

    <button
      className="landing-button landing-button-primary"
      onClick={onLaunch}
    >
      Explore ResQ Space &rarr;
    </button>
  </section>

  <footer className="landing-footer">
    <div>ResQ Space · Mapping potential flood impacts from space</div>
    <div>
      Analysis outputs support assessment and are not confirmation of
      ground-truth damage or road closures.
    </div>
  </footer>
</div>


)
}


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
  const [showDashboard, setShowDashboard] = useState(false)
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

  if (!showDashboard) {
  return <LandingPage onLaunch={() => setShowDashboard(true)} />
}

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
