
import json
import tempfile
import unittest
from pathlib import Path

from summary_outputs import (
    write_connectivity_summary,
    write_infrastructure_summary,
)


class TestSummaryOutputs(unittest.TestCase):
    def test_infrastructure_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "infrastructure_summary.json"

            write_infrastructure_summary(
                output_path=output,
                total_assets=10,
                exposure_counts={
                    "potentially_affected": 3,
                    "not_flagged": 7,
                },
            )

            with output.open(encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["total_assets"], 10)
            self.assertEqual(
                data["exposure_counts"]["potentially_affected"], 3
            )
            self.assertEqual(
                data["exposure_counts"]["not_flagged"], 7
            )
            self.assertEqual(data["schema_version"], "0.1.0")

    def test_connectivity_summary(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "connectivity_summary.json"

            results = {
                "settlement-1": {
                    "reachable": True,
                    "isolation_status": "connected",
                },
                "settlement-2": {
                    "reachable": False,
                    "isolation_status": "potentially_isolated",
                },
            }

            write_connectivity_summary(
                output_path=output,
                settlement_results=results,
                destination_id="hospital-1",
            )

            with output.open(encoding="utf-8") as file:
                data = json.load(file)

            self.assertEqual(data["settlements"]["total"], 2)
            self.assertEqual(data["settlements"]["connected"], 1)
            self.assertEqual(
                data["settlements"]["potentially_isolated"], 1
            )
            self.assertEqual(data["destination_id"], "hospital-1")


if __name__ == "__main__":
    unittest.main()
