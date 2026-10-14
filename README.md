<div align="center">

# 🌊 ResQ Space

### Mapping Flood Impact from Space. Guiding Response on the Ground.

**Satellite-Powered Flood Mapping & Disaster Response Intelligence**

Turning satellite-derived flood information into actionable geospatial insights to help responders identify potentially affected areas, assess infrastructure exposure, and understand where communities could become isolated.

<br/>

[![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge\&logo=react\&logoColor=black)](https://react.dev/)
[![Node.js](https://img.shields.io/badge/Backend-Node.js-339933?style=for-the-badge\&logo=nodedotjs\&logoColor=white)](https://nodejs.org/)
[![Express](https://img.shields.io/badge/API-Express-000000?style=for-the-badge\&logo=express\&logoColor=white)](https://expressjs.com/)
[![Python](https://img.shields.io/badge/Processing-Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![Geospatial](https://img.shields.io/badge/Geospatial-GeoJSON-2E8B57?style=for-the-badge)](#-how-it-works)

<br/>

**Hackathon Project · Multimodal AI Hackathon 2026 · Track B**

*Mapping Flood Damage from Space*

</div>

---

# ResQSpace

## 🌐 Live Demo
**Live Website:** https://res-q-space-7l7w5jg59-nityajha54-6094s-projects.vercel.app/

## About the Project
...
## 🚨 The Problem

When severe flooding occurs, roads become inaccessible, infrastructure is damaged, and entire communities can become difficult to reach.

Emergency responders need more than a map showing where water might be. They need to understand:

* 🌊 **Where could flooding be occurring?**
* 🏗️ **Which critical infrastructure may be exposed?**
* 🛣️ **Could flooded road segments disconnect communities?**
* 📍 **Which areas may require further investigation and prioritised response?**

Traditional ground-based assessments can be delayed when roads, communication networks, and access routes are disrupted.

**The challenge is to turn remote-sensing information into useful, location-based intelligence before responders can inspect every affected area on the ground.**

## 💡 Our Solution

ResQ Space is a geospatial disaster-response prototype that connects satellite-derived flood analysis with a backend API and an interactive mapping dashboard.

Instead of treating flood mapping as the final result, ResQ Space is designed to connect potential flood extent with infrastructure exposure, road connectivity, and concise analysis summaries.

### 🎯 What ResQ Space Aims to Deliver

| Capability                         | Purpose                                                                          |
| ---------------------------------- | -------------------------------------------------------------------------------- |
| 🛰️ Satellite-based flood analysis | Identify potential flood-affected areas from processed geospatial data.          |
| 🗺️ Interactive flood map          | Visualise available flood-analysis outputs in a dashboard.                       |
| 🏗️ Infrastructure exposure        | Identify infrastructure features that may intersect with potential flood extent. |
| 🛣️ Road connectivity analysis     | Assess whether potential flood impacts could disrupt road access.                |
| 🏘️ Community isolation insights   | Help identify settlements that may become disconnected from accessible routes.   |
| 📊 Analysis summaries              | Present available outputs and their processing status in a readable format.      |

> **Current implementation status:** The dashboard and results API are working, and the frontend production build and lint checks pass. Infrastructure exposure, road connectivity, and full end-to-end analysis execution still require verification where applicable. See [Project Status](#-project-status) for details.

---

## 🛰️ Why ResQ Space?

### From satellite data to response intelligence

A flood map is useful. Understanding what that flood might affect is even more valuable.

ResQ Space focuses on the next analytical steps:

**Potential flood extent → Infrastructure exposure → Road accessibility → Response planning**

The goal is to help decision-makers move from *"Where might the water be?"* towards *"What could be affected, and where should we investigate first?"*

### 🌍 Designed Around Real-World Disaster Challenges

* **Geospatial-first:** Uses geographic data and spatial relationships to analyse potential impacts.
* **Connected workflow:** Brings satellite-processing outputs into a backend API and an interactive frontend.
* **Action-oriented:** Focuses on infrastructure and accessibility, not only flood visualisation.
* **Transparent:** Distinguishes available outputs from missing, pending, or unverified analysis.
* **Extensible:** Provides a foundation for adding additional datasets, analysis methods, and response-planning capabilities.

---

## ⚙️ How It Works

```text
        SATELLITE / GEOSPATIAL INPUTS
                     │
                     ▼
        ┌─────────────────────────┐
        │  Satellite Processing   │
        │  & Flood Analysis       │
        │       Python            │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   Geospatial Outputs    │
        │                         │
        │   • Flood extent        │
        │   • Analysis summary    │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   Express REST API      │
        │                         │
        │   • Health status       │
        │   • Analysis execution  │
        │   • Results delivery    │
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   React Dashboard      │
        │                         │
        │   • Interactive map     │
        │   • Analysis results    │
        │   • Output availability │
        └─────────────────────────┘
```

### Workflow

1. **Process geospatial data:** The satellite-processing module produces flood-analysis outputs.
2. **Export analytical results:** Available results are represented using geospatial formats such as GeoJSON and structured summary files.
3. **Expose results through the backend:** The Express API provides endpoints for health checks and accessing analysis results.
4. **Visualise the outputs:** The React dashboard retrieves available results and displays the flood extent on an interactive map.
5. **Extend the analysis:** Infrastructure exposure and road-connectivity analysis can build upon the flood-extent output when the necessary input datasets are available.

---

## 🗺️ Technology Stack

<table>
<tr>
<th>Layer</th>
<th>Technology</th>
<th>Purpose</th>
</tr>
<tr>
<td>Frontend</td>
<td>React, Vite, JavaScript</td>
<td>Interactive disaster-response dashboard</td>
</tr>
<tr>
<td>Mapping</td>
<td>Leaflet, React Leaflet</td>
<td>Geospatial map visualisation</td>
</tr>
<tr>
<td>Backend</td>
<td>Node.js, Express.js</td>
<td>REST API and results integration</td>
</tr>
<tr>
<td>Satellite processing</td>
<td>Python</td>
<td>Flood analysis and geospatial processing</td>
</tr>
<tr>
<td>Geospatial data</td>
<td>GeoJSON</td>
<td>Representing geographic features and analysis outputs</td>
</tr>
<tr>
<td>Version control</td>
<td>Git, GitHub</td>
<td>Collaboration and source-code management</td>
</tr>
</table>

---

## 📊 Project Status

ResQ Space is an active hackathon prototype. The following status reflects the current verified implementation rather than the full intended roadmap.

| Component                                     | Status                                             |
| --------------------------------------------- | -------------------------------------------------- |
| React dashboard                               | ✅ Working                                          |
| Interactive map integration                   | ✅ Implemented                                      |
| Frontend production build                     | ✅ Passing                                          |
| Frontend lint checks                          | ✅ Passing                                          |
| Backend health endpoint                       | ✅ Verified                                         |
| Results API (`GET /api/results`)              | ✅ Verified returning HTTP 200                      |
| Flood extent and summary outputs              | 🟡 Available for analysis display                  |
| Analysis execution (`POST /api/analysis/run`) | 🟡 End-to-end verification pending                 |
| Infrastructure exposure                       | 🟡 Requires verification with the necessary inputs |
| Road connectivity analysis                    | 🟡 Requires verification with the necessary inputs |
| Full end-to-end workflow                      | 🟡 Awaiting integration-test confirmation          |

**Legend:** ✅ Verified · 🟡 Pending verification or dependent on available inputs

The project should not be interpreted as a fully operational emergency-response system. Its current outputs are analytical estimates that require appropriate validation.

---

## 🧰 Getting Started

Follow these instructions to run the frontend and backend locally.

### Prerequisites

Install the following before starting:

* [Node.js and npm](https://nodejs.org/)
* [Git](https://git-scm.com/)
* Python and the dependencies required by the satellite-processing module, if you intend to run that module.

### 1. Clone the Repository

```bash
git clone https://github.com/rohinikomal38-max/ResQSpace.git
cd ResQSpace
```

### 2. Start the Backend

Open a terminal:

```bash
cd backend
npm install
npm start
```

The backend is configured to listen on port `3000` by default.

Health-check endpoint:

```text
http://localhost:3000/api/health
```

Results endpoint:

```text
http://localhost:3000/api/results
```

The health endpoint should return a successful response when the backend is running.

### 3. Start the Frontend

Open a **second terminal** from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Vite prints the local frontend URL in the terminal. Open that URL in your browser.

If port `5173` is already occupied, Vite may select another available port.

### 4. Verify the Frontend

From the `frontend` directory, run:

```bash
npm run build
npm run lint
```

Both commands have passed in the current development environment.

> **Note:** Starting the frontend and backend does not by itself verify the complete satellite-analysis execution workflow. The analysis endpoint and its resulting outputs must also be tested end to end.

---

## 🔌 Backend API

The current integration includes the following endpoints:

| Method | Endpoint            | Purpose                                                            |
| ------ | ------------------- | ------------------------------------------------------------------ |
| `GET`  | `/api/health`       | Check backend availability                                         |
| `GET`  | `/api/results`      | Retrieve available analysis results                                |
| `POST` | `/api/analysis/run` | Initiate the analysis workflow; end-to-end verification is pending |

### Health Check Example

Request:

```http
GET /api/health
```

Example successful response:

```json
{
  "status": "ok",
  "service": "resqspace-backend"
}
```

### Results API

The results endpoint exposes available analysis outputs and their status.

Depending on the data available, these may include:

* Flood extent GeoJSON
* Flood summary
* Infrastructure exposure results
* Infrastructure summary
* Road-connectivity results
* Connectivity summary
* Analysis metadata

Not every output is guaranteed to be available in every run. Missing inputs or incomplete processing may leave some results unavailable.

---

## 🧪 Testing and Validation

The following checks have been completed during development:

* [x] Frontend production build
* [x] Frontend ESLint checks
* [x] Backend health endpoint verification
* [x] Results endpoint returning HTTP 200
* [x] Dashboard rendering in the browser
* [ ] End-to-end verification of `POST /api/analysis/run`
* [ ] Confirmation that all dependent outputs are generated and returned correctly

### Recommended End-to-End Validation

Before considering the complete workflow verified:

1. Start the backend and confirm `/api/health` responds successfully.
2. Execute `POST /api/analysis/run` using the request format expected by the backend.
3. Confirm that the processing operation completes and produces the expected output files.
4. Retrieve `/api/results` and verify that the returned summaries and GeoJSON correspond to the latest run.
5. Confirm that the frontend displays the available results without browser-console errors.
6. Check how missing inputs and failed processing are reported.

---

## 🛣️ Roadmap

The following improvements represent future work and verification goals, not claims that every capability is already complete.

* [ ] Complete end-to-end analysis execution and results verification.
* [ ] Validate infrastructure exposure outputs against the required infrastructure datasets.
* [ ] Validate road-network disruption and connectivity calculations.
* [ ] Improve handling of missing inputs and failed processing.
* [ ] Add a sample-data workflow for easier demonstrations.
* [ ] Add dashboard screenshots and a recorded project walkthrough.
* [ ] Document validated satellite data sources and processing methodology.
* [ ] Evaluate the results against independent reference data.
* [ ] Prepare a deployment configuration for a public demonstration.

---

## ⚠️ Limitations and Responsible Use

ResQ Space is an educational and hackathon prototype.

* **Potential flooding is not confirmed flooding.** Satellite-derived and geospatial outputs may contain uncertainty and require validation.
* **Exposure is not confirmed damage.** A feature intersecting a potential flood extent does not prove that it has been damaged.
* **Potential disconnection is not confirmed isolation.** Road-network analysis depends on the completeness and quality of its input data and assumptions.
* **Missing data affects results.** Infrastructure and connectivity outputs may remain unavailable if required datasets or processing steps are missing.
* **Emergency decisions require verification.** Results should be reviewed alongside authoritative information, ground assessments, and guidance from qualified disaster-response personnel.

ResQ Space is intended to support situational awareness and further investigation—not replace official emergency-management systems or professional judgement.

---

## 👥 Team and Contributions

ResQ Space is a collaborative hackathon project.

The work brings together satellite processing, geospatial analysis, backend integration, and frontend visualisation.

Team members and their contributions should be credited here:

| Team member          | Contribution                                 |
| -------------------- | -------------------------------------------- |
| Add team member name | Satellite processing and geospatial analysis |
| Add team member name | Backend API and integration                  |
| Add team member name | Frontend dashboard and mapping               |

*Update the names and responsibilities to reflect your actual team before submission.*

---

## 🌟 Our Vision

We believe satellite data becomes more valuable when it helps answer practical questions on the ground.

ResQ Space aims to bridge the gap between **observing a potential disaster and understanding its possible consequences**—helping responders investigate affected infrastructure, assess accessibility, and make better-informed plans.

### From Space to Situational Awareness.

**ResQ Space — Mapping impact. Informing response.**

---

## 📄 License

No license has been specified here. Add a license file and update this section once the team has agreed on the terms under which the project may be used and distributed.
