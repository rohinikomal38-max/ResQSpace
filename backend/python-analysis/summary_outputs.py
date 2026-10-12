
import json
from pathlib import Path

from output_schema import build_metadata


def write_json(output_path, data):
    """Write a JSON object to a file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        file.write("\n")


def write_infrastructure_summary(
    output_path,
    total_assets,
    exposure_counts,
    event_id=None,
    source=None,
):
    """Write infrastructure exposure statistics."""
    summary = build_metadata(
        event_id=event_id,
        processing_status="completed",
        source=source,
        uncertainty_notes=[
            "Exposure indicates geometric intersection, not confirmed damage."
        ],
    )

    summary.update({
        "total_assets": total_assets,
        "exposure_counts": exposure_counts,
    })

    write_json(output_path, summary)
    return summary


def write_connectivity_summary(
    output_path,
    settlement_results,
    destination_id=None,
    event_id=None,
    source=None,
):
    """Write settlement connectivity statistics."""
    statuses = [
        result.get("isolation_status", "not_assessed")
        for result in settlement_results.values()
    ]

    summary = build_metadata(
        event_id=event_id,
        processing_status="completed",
        source=source,
        uncertainty_notes=[
            "Isolation is estimated using the supplied road graph.",
            "Results depend on road-closure and destination assumptions.",
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
