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
EVENT_ID = "resqspace-event"

FLOOD = OUTPUT_DIR / "flood_extent.geojson"
ASSETS = INPUT_DIR / "infrastructure_assets.geojson"
ROADS = INPUT_DIR / "road_segments.geojson"
GRAPH = INPUT_DIR / "road_graph.json"
SETTLEMENTS = INPUT_DIR / "settlement_nodes.json"
DESTINATIONS = INPUT_DIR / "destination_nodes.json"
REQUIRED_INPUTS = {
    "flood_extent": FLOOD,
    "infrastructure_assets": ASSETS,
    "road_segments": ROADS,
    "road_graph": GRAPH,
    "settlement_nodes": SETTLEMENTS,
    "destination_nodes": DESTINATIONS,
}

REQUIRED_INPUTS = {
    "flood_extent": FLOOD,
    "infrastructure_assets": ASSETS,
    "road_segments": ROADS,
    "road_graph": GRAPH,
    "settlement_nodes": SETTLEMENTS,
    "destination_nodes": DESTINATIONS,
}

INFRA = OUTPUT_DIR / "infrastructure_exposure.geojson"
INFRA_SUMMARY = OUTPUT_DIR / "infrastructure_summary.json"
ROAD_OUTPUT = OUTPUT_DIR / "road_connectivity.geojson"
CONNECTIVITY_SUMMARY = OUTPUT_DIR / "connectivity_summary.json"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    available = [
    name for name, path in REQUIRED_INPUTS.items()
    if path.is_file()
]
    
    required = REQUIRED_INPUTS

    missing = [
        name
        for name, path in REQUIRED_INPUTS.items()
        if not path.is_file()
    ]

    if missing:
        metadata = build_metadata(
            event_id=EVENT_ID,
            processing_status="pending",
            uncertainty_notes=[
                "Analysis did not run because required inputs are missing.",
                "Missing inputs: " + ", ".join(missing),
                "Potential flood changes and road closures are not confirmed.",
            ],
        )

        available_inputs = [
    name for name, path in REQUIRED_INPUTS.items()
    if path.is_file()
]
        print(json.dumps({
            "metadata": metadata,
            "paths": {
                "input_dir": str(INPUT_DIR),
                "output_dir": str(OUTPUT_DIR),
            },
            "available_inputs": available_inputs,
            "missing_inputs": missing,
            "available_inputs": available,
            "paths": {
                "input_dir": str(INPUT_DIR),
                "output_dir": str(OUTPUT_DIR),
            },
        }, indent=2))
        return

    try:
        infra_result = process_asset_file(
            ASSETS,
            FLOOD,
            INFRA,
        )

        closure_result = assess_road_closures(
            ROADS,
            FLOOD,
            ROAD_OUTPUT,
        )
        infra_result = process_asset_file(ASSETS, FLOOD, INFRA)
        closure_result = assess_road_closures(ROADS, FLOOD, ROAD_OUTPUT)

        settlement_results = analyze_connectivity_from_files(
            GRAPH,
            SETTLEMENTS,
            DESTINATIONS,
            ROAD_OUTPUT,
        )

        write_infrastructure_summary(
            INFRA_SUMMARY,
            infra_result["total_assets"],
            infra_result["exposure_counts"],
            event_id=EVENT_ID,
            source={"flood_extent": str(FLOOD)},
            processing_status="completed",
        )

        write_connectivity_summary(
            CONNECTIVITY_SUMMARY,
            settlement_results,
            event_id=EVENT_ID,
            source={
                "road_graph": str(GRAPH),
                "road_closures": str(ROAD_OUTPUT),
            },
            processing_status="partial",
        )

        print(json.dumps({
            "metadata": build_metadata(
                event_id=EVENT_ID,
                processing_status="partial",
                uncertainty_notes=[
                    "Road closure flags are potential, not verified.",
                    "Connectivity currently uses the supplied graph; "
                    "potential closures are not yet applied to graph edges.",
                ],
            ),
            "infrastructure": infra_result,
            "road_closures": closure_result,
            "settlements_analyzed": len(settlement_results),
            "outputs": [
                str(INFRA),
                str(INFRA_SUMMARY),
                str(ROAD_OUTPUT),
                str(CONNECTIVITY_SUMMARY),
            ],
        }, indent=2))
    except Exception as exc:
        print(json.dumps({
            "metadata": build_metadata(
                event_id=EVENT_ID,
                processing_status="failed",
                uncertainty_notes=[str(exc)],
            ),
            "error": str(exc),
        }, indent=2))
        raise


if __name__ == "__main__":
    main()
