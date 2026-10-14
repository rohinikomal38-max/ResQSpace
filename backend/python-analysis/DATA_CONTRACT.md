# ResQSpace Python Analysis — Data Contract

**Contract version:** 0.1.0 (provisional)

## 1. Flood Detection Inputs

The flood-detection module plans to provide:

- `flood_extent.geojson`
- `flood_summary.json`
- `flood_extent.tif` (optional for downstream processing, pending confirmation)

### `flood_extent.geojson`

Expected structure:
- GeoJSON FeatureCollection.
- Polygon geometries representing detected potential-change areas.
- Feature properties include `event_id` and `classification`.
- Current classification value: `potential_change`.
- Intended CRS: EPSG:4326 (WGS84), subject to confirmation that the exporter correctly reprojects geometries.

**Important:** Potential-change areas must not be treated as confirmed flooded or damaged areas.

### `flood_summary.json`

The provisional summary contains:
- `schema_version`
- `event_id`
- `processing_status`
- `source`
- `method`
- `threshold`
- `valid_pixel_count`
- `changed_pixel_count`
- `change_fraction`
- `classification_note`
- `uncertainty_notes`

The final field definitions and types remain subject to confirmation by Member 1.

## 2. Infrastructure Input

The infrastructure input should be a readable GeoJSON file containing asset geometries and, where available, asset identifiers, categories, and source information.

The current exposure function compares asset geometries with the supplied flood polygons using geometric intersection.

Exposure means potential geometric overlap with a potential-change area. It does not confirm flooding, damage, or service disruption.

## 3. Road Network Input

The road input should contain road-segment geometries in a readable GeoJSON file with a defined CRS.

The current road assessment flags segments intersecting the supplied polygons as `potential_closure`. This is a potential-impact flag, not a verified closure.

Connectivity analysis also requires a prepared graph and mappings for settlement and destination nodes. Building this graph automatically from geographic road data is not yet implemented.

## 4. Output Conventions

- Intended GeoJSON output CRS: EPSG:4326.
- Summary files use JSON.
- Shared metadata schema version: `0.1.0` (provisional).
- Source, event date, processing status, and uncertainty should be recorded where available.
- Missing or invalid measurements must not be presented as confirmed values.
- Potential exposure, road closures, and isolation must not be described as confirmed outcomes.

## 5. Integration Checklist

Before integration testing, confirm:
- Final flood output files and field types.
- Whether GeoJSON geometries are actually reprojected to EPSG:4326.
- Geometry validity and handling of empty inputs.
- Infrastructure and road data sources.
- Settlement and destination identifiers.
- Output filenames and API expectations.
- Compatible Python and dependency versions.
- Representative flood outputs from Member 1.

The contract remains provisional until both modules are tested together and the team agrees on the final schema.

## Agreed API Integration Paths

The Express API expects these four analysis outputs under
`backend/data/outputs/`:

| File | Purpose |
|---|---|
| `infrastructure_exposure.geojson` | Infrastructure assets with potential exposure classifications |
| `infrastructure_summary.json` | Infrastructure exposure counts and metadata |
| `road_connectivity.geojson` | Road segments with potential closure classifications |
| `connectivity_summary.json` | Settlement reachability and isolation summary |

The input paths are:

- `backend/data/outputs/flood_extent.geojson`
- `backend/data/inputs/infrastructure_assets.geojson`
- `backend/data/inputs/road_segments.geojson`

Connectivity analysis also requires a prepared NetworkX graph, settlement-to-node mappings, and destination node IDs. Their file format and exact paths must be agreed with the API teammate before integration.

All GeoJSON outputs should use EPSG:4326. Summary JSON files must include `schema_version` and a supported `processing_status`.

**Important:** Potential exposure, potential road closure, and potential isolation are analytical flags, not confirmation of real-world damage or access conditions.

This contract is provisional until tested against representative input files and the Express API.

## Connectivity Graph Input Format

The connectivity module will use three JSON inputs. Proposed paths are
provisional and must be confirmed with the API teammate.

### 1. Road graph: `road_graph.json`

Expected structure:

```json
{
  "nodes": [
    {"id": "node-1"},
    {"id": "node-2"},
    {"id": "node-3"}
  ],
  "edges": [
    {"source": "node-1", "target": "node-2"},
    {"source": "node-2", "target": "node-3"}
  ]
}
```

- Each node ID must be unique.
- Each edge must reference existing node IDs.
- The initial graph is undirected.
- This graph represents the prepared road network. Road closures must be
  applied to the graph before calculating post-event accessibility.

### 2. Settlement mapping: `settlement_nodes.json`

Expected structure:

```json
{
  "settlement-1": "node-1",
  "settlement-2": "node-3"
}
```

Each key is a settlement ID and each value is its corresponding road-graph
node ID.

### 3. Destination nodes: `destination_nodes.json`

Expected structure:

```json
{
  "destinations": [
    {"id": "hospital-1", "node_id": "node-2"},
    {"id": "shelter-1", "node_id": "node-3"}
  ]
}
```

Each destination must map to a node in the road graph.


## Connectivity Input Files — v0.1.0

The following JSON formats are the agreed provisional integration
contract for connectivity analysis.

Proposed directory:
`backend/data/inputs/`

### 1. road_graph.json

Required structure:


{
  "nodes": [
    {"id": "node-1"},
    {"id": "node-2"},
    {"id": "node-3"}
  ],
  "edges": [
    {
      "source": "node-1",
      "target": "node-2",
      "road_id": "road-1"
    },
    {
      "source": "node-2",
      "target": "node-3",
      "road_id": "road-2"
    }
  ]
}


Required fields:

- `nodes`: array of graph nodes.
- `nodes[].id`: non-empty string; unique within the graph.
- `edges`: array of road-network edges.
- `edges[].source`: ID of an existing node.
- `edges[].target`: ID of an existing node.

Rules:
- Every edge must include a non-empty `road_id` matching the corresponding road segment in `road_segments.geojson`.
- `road_type` and `length_m` are optional attributes.
- Road IDs must be unique in the road-segment GeoJSON and must map consistently to graph edges.

### 2. settlement_nodes.json

Required structure:

```json
{
  "settlement-1": "node-1",
  "settlement-2": "node-3"
}
```

Required fields and rules:

- Each object key is a non-empty settlement ID.
- Each value is a non-empty road-graph node ID.
- Settlement IDs must be unique JSON object keys.
- Every mapped node should exist in `road_graph.json`.
- If a settlement maps to a missing node, its result must be marked
  `uncertain`, not `potentially_isolated`.

### 3. destination_nodes.json

Required structure:

```json
{
  "destinations": [
    {"id": "hospital-1", "node_id": "node-2"},
    {"id": "shelter-1", "node_id": "node-3"}
  ]
}
```

Required fields and rules:

- `destinations`: array of destination records.
- `destinations[].id`: non-empty, unique destination ID.
- `destinations[].node_id`: non-empty graph node ID.
- Every destination node should exist in `road_graph.json`.
- Missing destination nodes must be reported as uncertain or invalid input;
  they must not silently produce a false isolation result.
- An empty destination list must not be interpreted as proof of isolation.

### Input validation and connectivity assumptions

- All three files must be valid JSON with the structures described above.
- Invalid JSON, missing required fields, duplicate IDs, or invalid edge
  references must produce a clear validation error.
- Missing input files must be reported as unavailable; do not fabricate
  replacement datasets.
- The initial graph is undirected and represents the supplied road network.
- Reachability means connected in the supplied graph; it does not prove
  that a road is safe or passable in the real world.
- To assess post-event accessibility, potential road closures must be
  applied to the graph before reachability is calculated.
- These input files have not yet been supplied. Full analysis and integration
  testing remain pending until representative datasets are available.
  
  ## Road-to-Graph Mapping

Each road segment in `backend/data/inputs/road_segments.geojson` must have a unique `road_id` property.

Each edge in `backend/data/inputs/road_graph.json` must include:
- `source`: ID of the starting graph node
- `target`: ID of the ending graph node
- `road_id`: ID matching the corresponding road segment

The `road_id` value must match between the GeoJSON feature and graph edge. Graph edges are undirected.

Road segments flagged as `potential_closure` must not be treated as confirmed closures. Connectivity analysis must document whether potential closures were applied to the graph or whether the graph represents baseline connectivity.


