# ResQSpace Python Analysis — Data Contract

**Contract version:** 0.1.0 (provisional)

## 1. Flood Extent Input

**Expected filename:** `flood_extent.geojson`

Requirements:
- Must be a valid, readable GeoJSON FeatureCollection.
- Must contain polygon or multipolygon flood geometries.
- Must have a defined CRS that can be interpreted by GeoPandas.
- Geometries should be valid and represent the flood extent for the relevant event.
- Event date, source, and uncertainty should be documented when available.

This is the proposed primary input from the flood-detection module. Confirm the actual filename and structure with Member 1 before integration.

## 2. Infrastructure Input

The infrastructure input should be a readable GeoJSON file containing asset geometries and, where available, asset identifiers, categories, and source information.

The current exposure function compares asset geometries with the flood extent using geometric intersection.

## 3. Road Network Input

The road input should contain road-segment geometries in a readable GeoJSON file with a defined CRS.

The current road assessment flags segments intersecting the flood extent as `potential_closure`. This is an analytical flag, not a verified closure.

The connectivity analysis also requires a prepared graph and mappings for settlement and destination nodes. Building this graph from geographic road data is not yet implemented.

## 4. Output Conventions

- GeoJSON outputs use EPSG:4326.
- Summary files use JSON.
- Metadata includes the provisional schema version, processing status, source, event date, generation timestamp, CRS, and uncertainty notes.
- Missing or invalid measurements should not be presented as confirmed values.
- Potential exposure and isolation must not be described as confirmed damage or actual isolation.

## 5. Integration Checklist

Before connecting the modules, confirm:
- Final flood input filename and field structure.
- CRS and geometry types.
- Infrastructure and road data sources.
- Settlement and destination identifiers.
- Output filenames and API expectations.
- Compatible Python and dependency versions.

This contract documents current expectations; it does not replace testing with the actual team outputs.
