
import geopandas as gpd
import networkx as nx


def assess_road_closures(roads_path, flood_path, output_path):
    """Flag road segments intersecting a flood extent as potential closures."""
    roads = gpd.read_file(roads_path)
    flood = gpd.read_file(flood_path)

    if roads.crs is None or flood.crs is None:
        raise ValueError("Both input files must have a defined CRS.")

    if roads.empty or flood.empty:
        raise ValueError("Road and flood files must not be empty.")

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

    roads.to_file(output_path, driver="GeoJSON")

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
        "output_file": output_path,
        "crs": "EPSG:4326",
    }


def analyze_connectivity(graph, settlement_nodes, destination_nodes):
    """Assess settlement reachability on an already-prepared road graph."""
    results = {}

    available_destinations = [
        node for node in destination_nodes if node in graph
    ]

    for settlement_id, node in settlement_nodes.items():
        if node not in graph or not available_destinations:
            results[settlement_id] = {
                "reachable": None,
                "isolation_status": "uncertain",
                "reason": "Missing network node or destination",
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
            "reason": None,
            "reachable_destination_id": reachable_destination,
        }

    return results

