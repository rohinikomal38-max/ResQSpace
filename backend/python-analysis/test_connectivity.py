
import json
import tempfile
import unittest
from pathlib import Path

import networkx as nx

from connectivity import (
    analyze_connectivity,
    analyze_connectivity_from_files,
)


class TestConnectivity(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.graph.add_edges_from([
            ("A", "B"),
            ("B", "C"),
            ("X", "Y"),
        ])

    def test_connected_settlement(self):
        results = analyze_connectivity(
            self.graph,
            {"settlement-1": "A"},
            ["C"],
        )

        self.assertEqual(
            results["settlement-1"]["isolation_status"],
            "connected",
        )
        self.assertTrue(results["settlement-1"]["reachable"])

    def test_disconnected_settlement(self):
        results = analyze_connectivity(
            self.graph,
            {"settlement-2": "X"},
            ["C"],
        )

        self.assertEqual(
            results["settlement-2"]["isolation_status"],
            "potentially_isolated",
        )
        self.assertFalse(results["settlement-2"]["reachable"])

    def test_missing_settlement_node_is_uncertain(self):
        results = analyze_connectivity(
            self.graph,
            {"settlement-3": "MISSING"},
            ["C"],
        )

        self.assertEqual(
            results["settlement-3"]["isolation_status"],
            "uncertain",
        )
        self.assertIsNone(results["settlement-3"]["reachable"])

    def test_missing_destination_nodes_are_uncertain(self):
        results = analyze_connectivity(
            self.graph,
            {"settlement-4": "A"},
            ["MISSING"],
        )

        self.assertEqual(
            results["settlement-4"]["isolation_status"],
            "uncertain",
        )
        self.assertIsNone(results["settlement-4"]["reachable"])

    def test_connectivity_from_json_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)

            graph_data = {
                "nodes": [
                    {"id": "A"},
                    {"id": "B"},
                    {"id": "C"},
                ],
                "edges": [
                    {"source": "A", "target": "B"},
                    {"source": "B", "target": "C"},
                ],
            }

            settlement_data = {
                "settlement-1": "A",
                "settlement-2": "C",
            }

            destination_data = {
                "destinations": [
                    {"id": "hospital-1", "node_id": "C"}
                ]
            }

            graph_path = directory / "road_graph.json"
            settlement_path = directory / "settlement_nodes.json"
            destination_path = directory / "destination_nodes.json"

            graph_path.write_text(
                json.dumps(graph_data),
                encoding="utf-8",
            )
            settlement_path.write_text(
                json.dumps(settlement_data),
                encoding="utf-8",
            )
            destination_path.write_text(
                json.dumps(destination_data),
                encoding="utf-8",
            )

            results = analyze_connectivity_from_files(
                graph_path,
                settlement_path,
                destination_path,
            )

            self.assertTrue(results["settlement-1"]["reachable"])
            self.assertTrue(results["settlement-2"]["reachable"])
            self.assertEqual(
                results["settlement-1"]["reachable_destination_id"],
                "C",
            )
            
    def test_file_integration_rejects_missing_destination_node(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)

            graph_path = directory / "road_graph.json"
            settlement_path = directory / "settlement_nodes.json"
            destination_path = directory / "destination_nodes.json"

            graph_path.write_text(
                json.dumps({
                    "nodes": [{"id": "A"}],
                    "edges": [],
                }),
                encoding="utf-8",
            )

            settlement_path.write_text(
                json.dumps({"settlement-1": "A"}),
                encoding="utf-8",
            )

            destination_path.write_text(
                json.dumps({
                    "destinations": [
                        {
                            "id": "hospital-1",
                            "node_id": "MISSING",
                        }
                    ]
                }),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError,
                "missing graph nodes",
            ):
                analyze_connectivity_from_files(
                    graph_path,
                    settlement_path,
                    destination_path,
                )


if __name__ == "__main__":
    unittest.main()
