# ResQSpace Python Analysis

This module contains the Python analysis components for infrastructure exposure and road connectivity assessment.

## Current Components

- `main.py` — Generates initial analysis metadata.
- `output_schema.py` — Defines shared metadata fields and schema version.
- `infrastructure.py` — Assesses infrastructure exposure to a supplied flood extent.
- `connectivity.py` — Flags potentially affected road segments and analyzes connectivity on a supplied road graph.
- `summary_outputs.py` — Writes infrastructure and connectivity summary JSON files.
- `requirements.txt` — Lists Python dependencies.
- `test_main.py` — Tests metadata output from the main script.
- `test_output_schema.py` — Tests shared metadata validation.
- `test_infrastructure.py` — Tests infrastructure exposure classification.
- `test_connectivity.py` — Tests road-network connectivity logic.
- `test_summary_outputs.py` — Tests summary JSON writers.

## Data and Output Conventions

- GeoJSON outputs use EPSG:4326.
- Flood intersection indicates potential exposure, not confirmed damage.
- Road intersections indicate potential closures, not verified road closures.
- Connectivity results depend on the supplied graph, settlement nodes, and destination nodes.
- Missing or invalid inputs should be reported as uncertain or not assessed where appropriate.
- The shared metadata schema is currently version `0.1.0` and remains provisional pending team integration.

## Dependencies

Install dependencies from this directory with:

```bash
python -m pip install -r requirements.txt
```

## Running Tests

Run the test suite from this directory with:

```bash
python -m unittest discover -v
```

These commands have not yet been verified in the project environment.

## Integration Status

This module is under development. Integration with the flood-detection outputs and the backend API, as well as local execution and testing, are still required.

## Connectivity JSON Loader

`graph_loader.py` loads and validates the connectivity inputs:

- `road_graph.json` — road-network nodes and edges.
- `settlement_nodes.json` — settlement IDs mapped to graph nodes.
- `destination_nodes.json` — hospital or shelter IDs mapped to graph nodes.

The `connectivity.py` function `analyze_connectivity_from_files()`
loads these inputs, validates the node mappings, and calculates
settlement reachability using NetworkX.

Example usage:

```python
from connectivity import analyze_connectivity_from_files

results = analyze_connectivity_from_files(
    "backend/data/inputs/road_graph.json",
    "backend/data/inputs/settlement_nodes.json",
    "backend/data/inputs/destination_nodes.json",
)

print(results)
```

The example assumes the files exist at the supplied paths. The input
datasets have not yet been confirmed available.

Invalid JSON, missing files, and mappings to nonexistent graph nodes
raise errors. The calling pipeline must handle those errors and report
the input as invalid or unavailable.

These results describe connectivity in the supplied graph only.
Flood-related road closures must be incorporated before interpreting
the results as post-event accessibility.

## Testing Status

Unit and integration test cases have been added, but they have not yet
been executed. Local test execution and integration testing with
representative datasets remain pending.
```
