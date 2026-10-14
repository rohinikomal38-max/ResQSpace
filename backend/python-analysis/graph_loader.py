
import json
from pathlib import Path

import networkx as nx


def _read_json(path):
    """Read a JSON file and report clear input errors."""
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Required input file is unavailable: {file_path}"
        )

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {file_path}: {exc}"
        ) from exc


def load_road_graph(path):
    """Load and validate an undirected road graph from road_graph.json."""
    data = _read_json(path)

    if not isinstance(data, dict):
        raise ValueError("Road graph must be a JSON object.")

    nodes = data.get("nodes")
    edges = data.get("edges")

    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise ValueError("'nodes' and 'edges' must be arrays.")

    graph = nx.Graph()
    seen_nodes = set()

    for node in nodes:
        if not isinstance(node, dict):
            raise ValueError("Each node must be a JSON object.")

        node_id = node.get("id")

        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError("Every node needs a non-empty string ID.")

        if node_id in seen_nodes:
            raise ValueError(f"Duplicate node ID: {node_id}")

        seen_nodes.add(node_id)
        graph.add_node(node_id)

    seen_edges = set()

    for edge in edges:
        if not isinstance(edge, dict):
            raise ValueError("Each edge must be a JSON object.")

        source = edge.get("source")
        target = edge.get("target")

        if not isinstance(source, str) or not source.strip():
            raise ValueError("Every edge needs a source node ID.")

        if not isinstance(target, str) or not target.strip():
            raise ValueError("Every edge needs a target node ID.")

        if source not in graph or target not in graph:
            raise ValueError(
                f"Edge references a missing node: {source} -> {target}"
            )

        
        road_id = edge.get("road_id")

        if not isinstance(road_id, str) or not road_id.strip():
            raise ValueError(
                "Every edge needs a non-empty string road_id."
            )

        if source == target:
            raise ValueError(
                f"Self-loops are not permitted: {source}"
            )


        edge_key = frozenset((source, target))

        if edge_key in seen_edges:
            raise ValueError(
                f"Duplicate edge: {source} -- {target}"
            )

        seen_edges.add(edge_key)
        graph.add_edge(source, target, road_id=road_id)

    return graph


def load_settlement_nodes(path):
    """Load settlement IDs mapped to road-graph node IDs."""
    data = _read_json(path)

    if not isinstance(data, dict):
        raise ValueError("Settlement mapping must be a JSON object.")

    for settlement_id, node_id in data.items():
        if not isinstance(settlement_id, str) or not settlement_id.strip():
            raise ValueError("Settlement IDs must be non-empty strings.")

        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError(
                f"Invalid graph node mapping for {settlement_id}."
            )

    return data


def load_destination_nodes(path):
    """Load destination IDs and their road-graph node IDs."""
    data = _read_json(path)

    if not isinstance(data, dict):
        raise ValueError("Destination input must be a JSON object.")

    destinations = data.get("destinations")

    if not isinstance(destinations, list):
        raise ValueError("'destinations' must be an array.")

    destination_nodes = {}
    seen_ids = set()

    for destination in destinations:
        if not isinstance(destination, dict):
            raise ValueError("Each destination must be a JSON object.")

        destination_id = destination.get("id")
        node_id = destination.get("node_id")

        if not isinstance(destination_id, str) or not destination_id.strip():
            raise ValueError(
                "Every destination needs a non-empty string ID."
            )

        if destination_id in seen_ids:
            raise ValueError(
                f"Duplicate destination ID: {destination_id}"
            )

        if not isinstance(node_id, str) or not node_id.strip():
            raise ValueError(
                f"Invalid graph node mapping for {destination_id}."
            )

        seen_ids.add(destination_id)
        destination_nodes[destination_id] = node_id

    return destination_nodes


def validate_node_mappings(graph, settlement_nodes, destination_nodes):
    """Reject mappings that reference nodes absent from the graph."""
    missing_settlements = {
        settlement_id: node_id
        for settlement_id, node_id in settlement_nodes.items()
        if node_id not in graph
    }

    missing_destinations = {
        destination_id: node_id
        for destination_id, node_id in destination_nodes.items()
        if node_id not in graph
    }

    if missing_settlements or missing_destinations:
        raise ValueError(
            "Connectivity mappings reference missing graph nodes. "
            f"Settlements: {missing_settlements}; "
            f"destinations: {missing_destinations}"
        )
