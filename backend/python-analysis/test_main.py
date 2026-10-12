
import json
import subprocess
import sys
import unittest
from pathlib import Path


class TestMain(unittest.TestCase):
    def test_main_outputs_valid_status_json(self):
        script = Path(__file__).with_name("main.py")

        result = subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            check=True,
        )

        output = json.loads(result.stdout)

        self.assertEqual(output["project"], "ResQSpace")
        self.assertEqual(output["module"], "infrastructure-connectivity")
        self.assertEqual(output["schema_version"], "0.1.0")
        self.assertEqual(output["processing_status"], "pending")


if __name__ == "__main__":
    unittest.main()
