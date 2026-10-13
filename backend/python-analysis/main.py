
import json
from pathlib import Path

from output_schema import build_metadata
from infrastructure import process_asset_file
from connectivity import (
    analyze_connectivity_from_files,
    assess_road_closures,
)
from summary_outputs import (
    write_connectivity_summary,
    write_infrastructure_summary,
)


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
INPUT_DIR = DATA_DIR / "inputs"
OUTPUT_DIR = DATA_DIR / "outputs"

REQUIRED_INPUTS = {
    "flood_extent": OUTPUT_DIR / "flood_extent.geojson",
    "infrastructure_assets": INPUT_DIR / "infrastructure_assets.geojson",
    "road_segments": INPUT_DIR / "road_segments.geojson",
    "road_graph": INPUT_DIR / "road_graph.json",
    "settlement_nodes": INPUT_DIR / "settlement_nodes.json",
    "destination_nodes": INPUT_DIR / "destination_nodes.json",
}


def main():
    # Ensure the output directory exists.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Check whether the required input files exist.
    available_inputs = {
        name: path.is_file()
        for name, path in REQUIRED_INPUTS.items()
    }

    missing_inputs = [
        name
        for name, available in available_inputs.items()
        if not available
    ]

    # Determine the preflight status.
    if missing_inputs:
        processing_status = "pending"
        input_note = (
            "Required input files are missing: "
            + ", ".join(missing_inputs)
        )
    else:
        processing_status = "processing"
        input_note = (
            "All required input files are present; "
            "their contents have not yet been validated."
        )

    # Build shared metadata.
    result = build_metadata(
        processing_status=processing_status,
        uncertainty_notes=[
            "The complete analysis pipeline has not run yet.",
            input_note,
        ],
    )

    # Print a JSON report.
    report = {
        "metadata": result,
        "paths": {
            "input_dir": str(INPUT_DIR),
            "output_dir": str(OUTPUT_DIR),
        },
        "available_inputs": available_inputs,
        "missing_inputs": missing_inputs,
    }

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
