
import json
import os
import tempfile
from pathlib import Path

from output_schema import build_metadata


def write_json(output_path, data):
    """Write JSON atomically by replacing the destination after writing."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            temp_path = Path(file.name)
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def write_infrastructure_summary(
    output_path,
    total_assets,
    exposure_counts,
    event_id=None,
    source=None,
    processing_status="completed",
):
    """Write infrastructure potential-impact statistics."""
    summary = build_metadata(
        event_id=event_id,
        processing_status=processing_status,
        source=source,
        uncertainty_notes=[
            "Potentially affected assets overlap potential-change areas.",
            "Overlap does not confirm flooding or infrastructure damage.",
            "Results depend on input geometry quality and CRS information.",
        ],
    )

    summary.update({
        "total_assets": total_assets,
        "exposure_counts": exposure_counts,
        "classification_note": (
            "potentially_affected means geometric overlap with a "
            "potential-change area; not_flagged does not confirm safety."
        ),
    })

    write_json(output_path, summary)
    return summary


def write_connectivity_summary(
    output_path,
    settlement_results,
    destination_id=None,
    event_id=None,
    source=None,
    processing_status="completed",
):
    """Write estimated settlement connectivity statistics."""
    statuses = [
        result.get("isolation_status", "not_assessed")
        for result in settlement_results.values()
    ]

    summary = build_metadata(
        event_id=event_id,
       processing_status=processing_status,
        source=source,
        uncertainty_notes=[
            "Connectivity is estimated using the supplied road graph.",
            "Results depend on road-closure and destination assumptions.",
            "Potential isolation is not a confirmed service disruption.",
        ],
    )

    summary.update({
        "destination_id": destination_id,
        "settlements": {
            "total": len(settlement_results),
            "connected": statuses.count("connected"),
            "potentially_isolated": statuses.count("potentially_isolated"),
            "uncertain": statuses.count("uncertain"),
            "not_assessed": statuses.count("not_assessed"),
        },
        "results": settlement_results,
    })

    write_json(output_path, summary)
    return summary
