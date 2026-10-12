
import json
import tempfile
import unittest
from pathlib import Path

import networkx as nx

from graph_loader import (
    load_destination_nodes,
    load_road_graph,
    load_settlement_nodes,
    validate_node_mappings,
)


class TestGraphLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.directory = Path(self.temp_dir.name)

    def write_json(self, filename, data):
        path = self.directory / filename
        path.write_text(json.dumps(data), encoding="utf-8")
        return path

    def test_load_valid_road_graph(self):
        path = self.write_json(
            "road_graph.json",
            {
                "nodes": [
                    {"id": "node-1"},
                    {"id": "node-2"},
                ],
                "edges": [
                    {"source": "node-1", "target": "node-2"}
                ],
            },
        )

        graph = load_road_graph(path)

        self.assertIsInstance(graph, nx.Graph)
        self.assertEqual(graph.number_of_nodes(), 2)
        self.assertTrue(graph.has_edge("node-1", "node-2"))

    def test_duplicate_node_is_rejected(self):
        path = self.write_json(
            "road_graph.json",
            {
                "nodes": [
                    {"id": "node-1"},
                    {"id": "node-1"},
                ],
                "edges": [],
            },
        )

        with self.assertRaisesRegex(ValueError, "Duplicate node ID"):
            load_road_graph(path)

    def test_edge_with_missing_node_is_rejected(self):
        path = self.write_json(
            "road_graph.json",
            {
                "nodes": [{"id": "node-1"}],
                "edges": [
                    {"source": "node-1", "target": "missing-node"}
                ],
            },
        )

        with self.assertRaisesRegex(ValueError, "missing node"):
            load_road_graph(path)

    def test_self_loop_is_rejected(self):
        path = self.write_json(
            "road_graph.json",
            {
                "nodes": [{"id": "node-1"}],
                "edges": [
                    {"source": "node-1", "target": "node-1"}
                ],
            },
        )

        with self.assertRaisesRegex(ValueError, "Self-loops"):
            load_road_graph(path)

    def test_missing_file_is_reported(self):
        with self.assertRaises(FileNotFoundError):
            load_road_graph(self.directory / "missing.json")

    def test_load_settlement_mapping(self):
        path = self.write_json(
            "settlement_nodes.json",
            {"settlement-1": "node-1"},
        )

        self.assertEqual(
            load_settlement_nodes(path),
            {"settlement-1": "node-1"},
        )

    def test_load_destination_mapping(self):
        path = self.write_json(
            "destination_nodes.json",
            {
                "destinations": [
                    {"id": "hospital-1", "node_id": "node-2"}
                ]
            },
        )

        self.assertEqual(
            load_destination_nodes(path),
            {"hospital-1": "node-2"},
        )

    def test_duplicate_destination_id_is_rejected(self):
        path = self.write_json(
            "destination_nodes.json",
            {
                "destinations": [
                    {"id": "hospital-1", "node_id": "node-1"},
                    {"id": "hospital-1", "node_id": "node-2"},
                ]
            },
        )

        with self.assertRaisesRegex(ValueError, "Duplicate destination"):
            load_destination_nodes(path)

    def test_missing_mapped_graph_node_is_rejected(self):
        graph = nx.Graph()
        graph.add_node("node-1")

        with self.assertRaisesRegex(ValueError, "missing graph nodes"):
            validate_node_mappings(
                graph,
                {"settlement-1": "missing-node"},
                {"hospital-1": "node-1"},
            )

    def test_valid_node_mappings_are_accepted(self):
        graph = nx.Graph()
        graph.add_nodes_from(["node-1", "node-2"])

        validate_node_mappings(
            graph,
            {"settlement-1": "node-1"},
            {"hospital-1": "node-2"},
            
    def test_invalid_json_is_reported(self):
        path = self.directory / "invalid.json"
        path.write_text("{invalid json}", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "Invalid JSON"):
            load_road_graph(path)
        )
        
    def test_duplicate_edge_in_reverse_direction_is_rejected(self):
        path = self.write_json(
            "road_graph.json",
            {
                "nodes": [
                    {"id": "node-1"},
                    {"id": "node-2"},
                ],
                "edges": [
                    {"source": "node-1", "target": "node-2"},
                    {"source": "node-2", "target": "node-1"},
                ],
            },
        )

        with self.assertRaisesRegex(ValueError, "Duplicate edge"):
            load_road_graph(path)


if __name__ == "__main__":
    unittest.main()
