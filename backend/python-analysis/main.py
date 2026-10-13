
import json
from pathlib import Path

from output_schema import build_metadata


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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    available_inputs = {
        name: path.is_file()
        for name, path in REQUIRED_INPUTS.items()
    }

      if missing_inputs:
        processing_status = "pending"
    else:
        processing_status = "processing"
        
    result = build_metadata(
        processing_status=processing_status,
        uncertainty_notes=[
            "The complete analysis pipeline has not run yet.",
            (
                "Required input files are missing: "
                + ", ".join(missing_inputs)
                if missing_inputs
                else "All required input files are present; validity is not yet verified."
            ),
        ],
    )

    print(json.dumps({
        "metadata": result,
        "paths": {
            "input_dir": str(INPUT_DIR),
            "output_dir": str(OUTPUT_DIR),
        },
        "available_inputs": available_inputs,
    }, indent=2))


if __name__ == "__main__":
    main()
