"""Tests for baseline raster change detection."""

import tempfile
import unittest
from pathlib import Path

import numpy as np
import rasterio
from rasterio.transform import from_origin

from src.satellite.detect_flood import detect_changes


class TestDetectChanges(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp_dir.name)

        self.pre_path = self.folder / "pre.tif"
        self.post_path = self.folder / "post.tif"

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

    def test_detects_large_changes(self):
        self.write_raster(self.pre_path, [[10, 10], [10, 10]])
        self.write_raster(self.post_path, [[10, 20], [10, 30]])

        result = detect_changes(
            str(self.pre_path),
            str(self.post_path),
            threshold=0.5,
        )

        self.assertEqual(result["changed_pixel_count"], 2)
        self.assertEqual(result["valid_pixel_count"], 4)

    def test_identical_rasters_have_no_changes(self):
        values = [[10, 20], [30, 40]]
        self.write_raster(self.pre_path, values)
        self.write_raster(self.post_path, values)

        result = detect_changes(str(self.pre_path), str(self.post_path))

        self.assertEqual(result["changed_pixel_count"], 0)

    def test_handles_zero_change(self):
        self.write_raster(
            self.pre_path,
            [[10, 10], [10, 10]],
        )
        self.write_raster(
            self.post_path,
            [[10, 10], [10, 10]],
        )

        result = detect_changes(
            str(self.pre_path),
            str(self.post_path),
        )

        self.assertEqual(result["changed_pixel_count"], 0)

    def test_handles_near_zero_values(self):
        self.write_raster(
            self.pre_path,
            [[0, 1e-8], [1e-7, 1e-6]],
        )
        self.write_raster(
            self.post_path,
            [[1e-8, 2e-8], [2e-7, 2e-6]],
        )

        result = detect_changes(
            str(self.pre_path),
            str(self.post_path),
            threshold=0.15,
        )

        self.assertEqual(result["valid_pixel_count"], 4)
        self.assertGreaterEqual(result["changed_pixel_count"], 0)
        self.assertLessEqual(
            result["changed_pixel_count"],
            result["valid_pixel_count"],
        )
        self.assertEqual(
            result["method"],
            "symmetric_relative_change_baseline",
        )




    def test_rejects_zero_threshold(self):
        self.write_raster(self.pre_path, [[10, 10], [10, 10]])
        self.write_raster(self.post_path, [[10, 10], [10, 10]])

        with self.assertRaises(ValueError):
            detect_changes(
                str(self.pre_path),
                str(self.post_path),
                threshold=0,
            )


if __name__ == "__main__":
    unittest.main()
