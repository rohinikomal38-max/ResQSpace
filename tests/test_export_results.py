"""Tests for ResQSpace result exports."""

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from src.satellite.export_results import export_change_results


class TestExportChangeResults(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)
        self.reference_path = self.folder / "reference.tif"
        self.output_dir = self.folder / "outputs"

        with rasterio.open(
            self.reference_path,
            "w",
            driver="GTiff",
            height=2,
            width=2,
            count=1,
            dtype="uint8",
            crs="EPSG:4326",
            transform=from_origin(80, 30, 0.01, 0.01),
        ) as dataset:
            dataset.write(np.zeros((2, 2), dtype="uint8"), 1)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_exports_all_three_files(self):
        mask = np.array([[False, True], [False, True]])

        result = export_change_results(
            str(self.reference_path),
            mask,
            str(self.output_dir),
            "test-event",
            0.15,
        )

        self.assertTrue(Path(result["raster"]).exists())
        self.assertTrue(Path(result["geojson"]).exists())
        self.assertTrue(Path(result["summary"]).exists())
        self.assertEqual(result["feature_count"], 1)

    def test_summary_and_geojson_contents(self):
        mask = np.array([[True, False], [False, False]])

        result = export_change_results(
            str(self.reference_path),
            mask,
            str(self.output_dir),
            "test-event",
            0.15,
        )

        with open(result["summary"], encoding="utf-8") as file:
            summary = json.load(file)

        with open(result["geojson"], encoding="utf-8") as file:
            geojson = json.load(file)

        self.assertEqual(summary["event_id"], "test-event")
        self.assertEqual(summary["changed_pixel_count"], 1)
        self.assertEqual(len(geojson["features"]), 1)
        self.assertEqual(
            geojson["features"][0]["properties"]["classification"],
            "potential_change",
        )

    def test_summary_includes_contract_metadata_and_valid_count(self):
        mask = np.array([[True, False], [False, False]])

        result = export_change_results(
            str(self.reference_path),
            mask,
            str(self.output_dir),
            "metadata-test-event",
            0.15,
            valid_pixel_count=3,
        )

        with open(result["summary"], encoding="utf-8") as file:
            summary = json.load(file)

        self.assertEqual(summary["schema_version"], "0.1.0")
        self.assertEqual(summary["event_id"], "metadata-test-event")
        self.assertEqual(summary["processing_status"], "completed")
        self.assertEqual(summary["valid_pixel_count"], 3)
        self.assertEqual(summary["changed_pixel_count"], 1)
        self.assertAlmostEqual(summary["change_fraction"], 1 / 3)
        self.assertEqual(summary["crs"], "EPSG:4326")
        self.assertIsNone(summary["event_date"])
        self.assertTrue(summary["generated_at"])
        self.assertIsInstance(summary["uncertainty_notes"], list)


    def test_rejects_wrong_mask_dimensions(self):
        with self.assertRaises(ValueError):
            export_change_results(
                str(self.reference_path),
                np.zeros((3, 3), dtype=bool),
                str(self.output_dir),
                "test-event",
                0.15,
            )


if __name__ == "__main__":
    unittest.main()
