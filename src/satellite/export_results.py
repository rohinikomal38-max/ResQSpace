"""Export baseline change-detection results for ResQSpace."""

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import shapes
from rasterio.warp import transform_geom
from shapely.geometry import mapping


def export_change_results(
    reference_raster_path: str,
    changed_mask: np.ndarray,
    output_dir: str,
    event_id: str,
    threshold: float,
    method: str = "symmetric_relative_change_baseline",
    valid_pixel_count: int | None = None,
) -> dict:
    """Export a change mask as GeoTIFF, GeoJSON, and a JSON summary."""
    if not event_id.strip():
        raise ValueError("event_id must not be empty")

    if threshold <= 0:
        raise ValueError("threshold must be greater than zero")

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    with rasterio.open(reference_raster_path) as source:
        mask = np.asarray(changed_mask, dtype=bool)

        if mask.shape != (source.height, source.width):
            raise ValueError("Mask dimensions must match the reference raster")

        profile = source.profile.copy()
        profile.update(driver="GTiff", count=1, dtype="uint8", nodata=255)

        raster_path = output / "flood_extent.tif"
        with rasterio.open(raster_path, "w", **profile) as destination:
            destination.write(mask.astype("uint8"), 1)

        features = []
        for geometry, value in shapes(
            mask.astype("uint8"),
            mask=mask,
            transform=source.transform,
        ):
            if value == 1:
                features.append(
                    {
                        "type": "Feature",
                         "geometry": transform_geom(
                            source.crs, "EPSG:4326", geometry
                        ),
                        "properties": {
                            "event_id": event_id,
                            "classification": "potential_change",
                        },
                    }
                )

        geojson_path = output / "flood_extent.geojson"
        geojson_path.write_text(
            json.dumps(
                {
                    "type": "FeatureCollection",
                    "name": "ResQSpace potential change extent",
                    "features": features,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        changed_count = int(np.count_nonzero(mask))
        total_count = (
            int(valid_pixel_count)
            if valid_pixel_count is not None
            else int(mask.size)
        )

        if total_count < changed_count or total_count > mask.size:
            raise ValueError(
                "valid_pixel_count must be between changed pixels "
                "and total mask pixels"
            )

        summary = {
            "schema_version": "0.1.0",
            "event_id": event_id,
            "processing_status": "completed",
            "source": Path(reference_raster_path).name,
            "event_date": None,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "crs": "EPSG:4326",
            "method": method,
            "threshold": threshold,
            "valid_pixel_count": total_count,
            "changed_pixel_count": changed_count,
            "change_fraction": (
                changed_count / total_count if total_count else None
            ),
            "classification_note": (
                "Potential changes only; not confirmed flooded areas."
            ),
            "uncertainty_notes": [
                "Results depend on raster quality and preprocessing.",
                "The baseline has not been validated as a flood classifier.",
            ],
        }


        summary_path = output / "flood_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    return {
        "raster": str(raster_path),
        "geojson": str(geojson_path),
        "summary": str(summary_path),
        "feature_count": len(features),
    }
