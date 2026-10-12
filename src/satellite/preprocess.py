
"""Validation utilities for satellite flood imagery."""

import rasterio


def validate_raster_pair(
    pre_event_path: str,
    post_event_path: str,
) -> dict:
    """Check whether two raster images are aligned for comparison.

    This function validates the raster grids; it does not detect floods
    or perform reprojection.
    """
    with rasterio.open(pre_event_path) as before, rasterio.open(
        post_event_path
    ) as after:
        checks = {
            "same_crs": before.crs == after.crs,
            "same_dimensions": (
                before.width == after.width
                and before.height == after.height
            ),
            "same_transform": before.transform == after.transform,
            "same_band_count": before.count == after.count,
        }

        return {
            "compatible": all(checks.values()),
            "checks": checks,
            "pre_event": {
                "width": before.width,
                "height": before.height,
                "crs": str(before.crs),
                "bands": before.count,
            },
            "post_event": {
                "width": after.width,
                "height": after.height,
                "crs": str(after.crs),
                "bands": after.count,
            },
        }
