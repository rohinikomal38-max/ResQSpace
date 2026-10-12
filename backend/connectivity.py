
import networkx as nx


def analyze_connectivity(graph, settlement_nodes, destination_nodes):
    """
    Determine which settlements can reach at least one destination.

    graph: NetworkX graph of the road network.
    settlement_nodes: dict mapping settlement IDs to graph nodes.
    destination_nodes: iterable of destination graph nodes.

    Returns a dict keyed by settlement ID.
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
                "reason": "Settlement has no mapped road-network node",
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
