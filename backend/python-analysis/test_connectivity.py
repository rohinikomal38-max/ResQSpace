
import unittest

import networkx as nx

from connectivity import analyze_connectivity


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


if __name__ == "__main__":
    unittest.main()
