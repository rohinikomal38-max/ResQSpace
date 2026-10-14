
import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestMain(unittest.TestCase):
    def test_main_outputs_valid_preflight_json(self):
        script_dir = Path(__file__).resolve().parent

        result = subprocess.run(
            [sys.executable, str(script_dir / "main.py")],
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)
        metadata = data["metadata"]

        self.assertEqual(metadata["schema_version"], "0.1.0")
        self.assertIn(
            metadata["processing_status"],
            {"pending", "processing"},
        )
        self.assertEqual(metadata["crs"], "EPSG:4326")
        self.assertIn("uncertainty_notes", metadata)

        self.assertIn("input_dir", data["paths"])
        self.assertIn("output_dir", data["paths"])
        self.assertIn("flood_extent", data["missing_inputs"])
        self.assertNotIn("flood_extent", data["available_inputs"])
        self.assertTrue(
            set(data["available_inputs"]).isdisjoint(
                data["missing_inputs"]
            )
        )
if __name__ == "__main__":
    unittest.main()
