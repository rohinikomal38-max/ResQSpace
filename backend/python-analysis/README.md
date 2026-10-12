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
