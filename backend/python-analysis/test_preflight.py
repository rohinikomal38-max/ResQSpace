
import unittest
from pathlib import Path

from main import REQUIRED_INPUTS


class TestPreflight(unittest.TestCase):
    def test_required_inputs_are_defined(self):
        expected_names = {
            "flood_extent",
            "infrastructure_assets",
            "road_segments",
            "road_graph",
            "settlement_nodes",
            "destination_nodes",
        }

        self.assertEqual(set(REQUIRED_INPUTS), expected_names)

    def test_input_paths_have_expected_extensions(self):
        self.assertEqual(
            REQUIRED_INPUTS["flood_extent"].suffix,
            ".geojson",
        )
        self.assertEqual(
            REQUIRED_INPUTS["road_graph"].suffix,
            ".json",
        )

    def test_input_paths_are_path_objects(self):
        for path in REQUIRED_INPUTS.values():
            self.assertIsInstance(path, Path)


if __name__ == "__main__":
    unittest.main()
