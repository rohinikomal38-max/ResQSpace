"""Baseline raster change detection for ResQSpace."""

import numpy as np
import rasterio

from src.satellite.preprocess import validate_raster_pair


def detect_changes(
    pre_event_path: str,
    post_event_path: str,
    threshold: float = 0.15,
) -> dict:
    """Flag pixels with large relative changes between two rasters.

    This is a change-detection baseline, not a validated flood classifier.
    Inputs must be comparable, aligned, single-band rasters.
    """
    if threshold <= 0:
        raise ValueError("threshold must be greater than zero")

    validation = validate_raster_pair(pre_event_path, post_event_path)

    if not validation["compatible"]:
        raise ValueError(
            "Raster grids are incompatible. Align both rasters first."
        )

    with rasterio.open(pre_event_path) as before, rasterio.open(
        post_event_path
    ) as after:
        if before.count != 1 or after.count != 1:
            raise ValueError("Detection requires single-band rasters")

        pre = before.read(1, masked=True).astype("float32")
        post = after.read(1, masked=True).astype("float32")

        valid = ~(
            np.ma.getmaskarray(pre) | np.ma.getmaskarray(post)
        )
        pre_data = np.asarray(pre.filled(np.nan))
        post_data = np.asarray(post.filled(np.nan))
        valid &= np.isfinite(pre_data) & np.isfinite(post_data)

        if not np.any(valid):
            raise ValueError("No valid overlapping pixels found")

        denominator = np.maximum(
            (np.abs(pre_data) + np.abs(post_data)) / 2,
            1e-6,
        )
        relative_change = np.abs(post_data - pre_data) / denominator
        changed = valid & (relative_change >= threshold)

    return {
        "changed_pixel_count": int(np.count_nonzero(changed)),
        "valid_pixel_count": int(np.count_nonzero(valid)),
        "threshold": threshold,
        "method": "symmetric_relative_change_baseline",
        "changed_mask": changed,
        "warning": (
            "Changed pixels are not confirmed flooded areas. "
            "Validate with suitable Sentinel-1 processing and reference data."
        ),
    }
