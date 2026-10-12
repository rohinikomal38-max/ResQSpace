
from datetime import datetime, timezone


SCHEMA_VERSION = "0.1.0"

VALID_PROCESSING_STATUSES = {
    "pending",
    "processing",
    "completed",
    "completed_with_warnings",
    "failed",
    "not_assessed",
}


def build_metadata(
    event_id=None,
    processing_status="pending",
    source=None,
    event_date=None,
    uncertainty_notes=None,
):
    """Build shared metadata for ResQSpace analysis outputs."""
    if processing_status not in VALID_PROCESSING_STATUSES:
        raise ValueError(
            f"Unsupported processing status: {processing_status}"
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "processing_status": processing_status,
        "source": source,
        "event_date": event_date,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "crs": "EPSG:4326",
        "uncertainty_notes": uncertainty_notes or [],
    }
