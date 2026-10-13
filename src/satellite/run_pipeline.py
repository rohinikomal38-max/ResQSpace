"""Run the ResQSpace baseline change-detection pipeline."""

from pathlib import Path

from src.satellite.detect_flood import detect_changes
from src.satellite.export_results import export_change_results


def run_pipeline(
    pre_event_path: str,
    post_event_path: str,
    output_dir: str,
    event_id: str,
    threshold: float = 0.15,
) -> dict:
    """Detect potential raster changes and export the results."""
    pre_path = Path(pre_event_path)
    post_path = Path(post_event_path)

    if not pre_path.is_file():
        raise FileNotFoundError(f"Pre-event raster not found: {pre_path}")

    if not post_path.is_file():
        raise FileNotFoundError(f"Post-event raster not found: {post_path}")

    detection = detect_changes(
        str(pre_path),
        str(post_path),
        threshold=threshold,
    )

    exports = export_change_results(
        reference_raster_path=str(post_path),
        changed_mask=detection["changed_mask"],
        output_dir=output_dir,
        event_id=event_id,
        threshold=threshold,
    )

    return {
        "event_id": event_id,
        "processing_status": "completed",
        "detection": {
            "changed_pixel_count": detection["changed_pixel_count"],
            "valid_pixel_count": detection["valid_pixel_count"],
            "threshold": detection["threshold"],
            "method": detection["method"],
        },
        "exports": exports,
        "warning": detection["warning"],
    }
