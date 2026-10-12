"""End-to-end tests for the ResQSpace pipeline."""

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from src.satellite.run_pipeline import run_pipeline


class TestRunPipeline(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)
        self.pre_path = self.folder / "pre.tif"
        self.post_path = self.folder / "post.tif"
        self.output_dir = self.folder / "outputs"

        self.write_raster(self.pre_path, [[10, 10], [10, 10]])
        self.write_raster(self.post_path, [[10, 20], [10, 30]])

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_raster(self, path, values):
        with rasterio.open(
            path,
            "w",
            driver="GTiff",
            height=2,
            width=2,
            count=1,
            dtype="float32",
            crs="EPSG:4326",
            transform=from_origin(80, 30, 0.01, 0.01),
        ) as dataset:
            dataset.write(np.array(values, dtype="float32"), 1)

    def test_pipeline_creates_all_outputs(self):
        result = run_pipeline(
            str(self.pre_path),
            str(self.post_path),
            str(self.output_dir),
            event_id="synthetic-test-event",
            threshold=0.5,
        )

        self.assertEqual(result["processing_status"], "completed")
        self.assertEqual(result["detection"]["changed_pixel_count"], 2)

        self.assertTrue((self.output_dir / "flood_extent.tif").exists())
        self.assertTrue((self.output_dir / "flood_extent.geojson").exists())
        self.assertTrue((self.output_dir / "flood_summary.json").exists())

        with open(
            self.output_dir / "flood_summary.json",
            encoding="utf-8",
        ) as file:
            summary = json.load(file)

        self.assertEqual(summary["event_id"], "synthetic-test-event")
        self.assertEqual(summary["changed_pixel_count"], 2)

    def test_pipeline_rejects_missing_input(self):
        with self.assertRaises(FileNotFoundError):
            run_pipeline(
                str(self.folder / "missing.tif"),
                str(self.post_path),
                str(self.output_dir),
                event_id="missing-input-test",
            )


if __name__ == "__main__":
    unittest.main()
