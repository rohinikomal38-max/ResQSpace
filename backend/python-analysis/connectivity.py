
import os
import tempfile
from pathlib import Path

import geopandas as gpd
import networkx as nx

from graph_loader import (
    load_destination_nodes,
    load_road_graph,
    load_settlement_nodes,
    validate_node_mappings,
)


def write_geojson_atomically(dataframe, output_path):
    """Write GeoJSON to a temporary file, then replace the destination."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.stem}.",
            suffix=".geojson",
            delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)

        dataframe.to_file(temp_path, driver="GeoJSON")
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def assess_road_closures(roads_path, flood_path, output_path):
    """
    Flag road segments intersecting potential-change areas.

    These are potential closures, not verified road closures.
    """
    roads = gpd.read_file(roads_path)
    flood = gpd.read_file(flood_path)

    if roads.crs is None or flood.crs is None:
        raise ValueError("Both input files must have a defined CRS.")

    if roads.empty or flood.empty:
        raise ValueError(
            "Road and potential-change files must not be empty."
        )

    roads = roads.to_crs("EPSG:4326")
    flood = flood.to_crs("EPSG:4326")

    flood_geometry = flood.geometry.union_all()

    def classify_road(geometry):
        if geometry is None or geometry.is_empty:
            return "uncertain"

        if not geometry.is_valid:
            return "uncertain"

        if geometry.intersects(flood_geometry):
            return "potential_closure"

        return "not_flagged"

    roads["closure_status"] = roads.geometry.apply(classify_road)
    roads["closure_method"] = "strict_intersection"
    roads["closure_verified"] = False

    write_geojson_atomically(roads, output_path)

    return {
        "total_road_segments": len(roads),
        "potential_closures": int(
            (roads["closure_status"] == "potential_closure").sum()
        ),
        "uncertain_segments": int(
            (roads["closure_status"] == "uncertain").sum()
        ),
        "closure_method": "strict_intersection",
        "closure_verified": False,
        "output_file": str(output_path),
        "crs": "EPSG:4326",
        "classification_note": (
            "Road intersections indicate potential closures only; "
            "closures have not been independently verified."
        ),
    }



def analyze_connectivity(graph, settlement_nodes, destination_nodes):
    """
    Assess reachability on an already-prepared road graph.

    Missing settlement nodes or unavailable destinations produce
    uncertain results rather than unsupported isolation claims.
    """
    results = {}

    available_destinations = [
        node for node in destination_nodes if node in graph
    ]

    for settlement_id, node in settlement_nodes.items():
        if node not in graph:
            results[settlement_id] = {
                "reachable": None,
                "isolation_status": "uncertain",
                "reason": "Settlement node is missing from the road graph",
                "reachable_destination_id": None,
            }
            continue

        if not available_destinations:
            results[settlement_id] = {
                "reachable": None,
                "isolation_status": "uncertain",
                "reason": "No valid destination nodes are available",
                "reachable_destination_id": None,
            }
            continue

        reachable_destination = next(
            (
                destination
                for destination in available_destinations
                if nx.has_path(graph, node, destination)
            ),
            None,
        )

        results[settlement_id] = {
            "reachable": reachable_destination is not None,
            "isolation_status": (
                "connected"
                if reachable_destination is not None
                else "potentially_isolated"
            ),
            "reason": (
                None
                if reachable_destination is not None
                else "No path to any available destination in the supplied graph"
            ),
            "reachable_destination_id": reachable_destination,
        }

    return results

def analyze_connectivity_from_files(
    graph_path,
    settlement_path,
    destination_path,
):
    """Load validated connectivity inputs and analyze reachability."""
    graph = load_road_graph(graph_path)
    settlement_nodes = load_settlement_nodes(settlement_path)
    destination_mapping = load_destination_nodes(destination_path)

    validate_node_mappings(
        graph,
        settlement_nodes,
        destination_mapping,
    )

    destination_node_ids = list(destination_mapping.values())

    return analyze_connectivity(
        graph,
        settlement_nodes,
        destination_node_ids,
    )

