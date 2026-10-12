
import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestMain(unittest.TestCase):
    def test_main_outputs_valid_metadata_json(self):
        script_dir = Path(__file__).resolve().parent

        result = subprocess.run(
            [sys.executable, str(script_dir / "main.py")],
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)

        self.assertEqual(data["schema_version"], "0.1.0")
        self.assertEqual(data["processing_status"], "pending")
        self.assertEqual(data["crs"], "EPSG:4326")
        self.assertIn("uncertainty_notes", data)


if __name__ == "__main__":
    unittest.main()

