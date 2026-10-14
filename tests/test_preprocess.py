"""Tests for satellite raster preprocessing."""

import unittest

import numpy as np
import rasterio
from rasterio.io import MemoryFile
from rasterio.transform import from_origin

from src.satellite.preprocess import validate_raster_pair


def create_test_raster():
    """Create a small in-memory raster for testing."""
    memory_file = MemoryFile()
    dataset = memory_file.open(
        driver="GTiff",
        height=10,
        width=10,
        count=1,
        dtype="uint8",
        crs="EPSG:4326",
        transform=from_origin(80, 30, 0.01, 0.01),
    )
    dataset.write(np.zeros((1, 10, 10), dtype="uint8"))
    dataset.close()
    return memory_file


class TestValidateRasterPair(unittest.TestCase):
    def test_matching_rasters_are_compatible(self):
        first = create_test_raster()
        second = create_test_raster()

        try:
            result = validate_raster_pair(first.name, second.name)
            self.assertTrue(result["compatible"])
            self.assertTrue(all(result["checks"].values()))
        finally:
            first.close()
            second.close()

    def test_different_dimensions_are_incompatible(self):
        first = create_test_raster()
        second_file = MemoryFile()
        second = second_file.open(
            driver="GTiff",
            height=8,
            width=10,
            count=1,
            dtype="uint8",
            crs="EPSG:4326",
            transform=from_origin(80, 30, 0.01, 0.01),
        )
        second.write(np.zeros((1, 8, 10), dtype="uint8"))
        second.close()

        try:
            result = validate_raster_pair(first.name, second_file.name)
            self.assertFalse(result["compatible"])
            self.assertFalse(result["checks"]["same_dimensions"])
        finally:
            first.close()
            second_file.close()


if __name__ == "__main__":
    unittest.main()
