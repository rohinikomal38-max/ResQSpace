
import json
from pathlib import Path

from output_schema import build_metadata


SCRIPT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = SCRIPT_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
INPUT_DIR = DATA_DIR / "inputs"
OUTPUT_DIR = DATA_DIR / "outputs"


def main():
    result = build_metadata(
        processing_status="pending",
        uncertainty_notes=[
            "Flood input has not been loaded yet.",
            "Infrastructure and connectivity analysis has not run yet.",
        ],
    )

    print(json.dumps({
        "metadata": result,
        "paths": {
            "input_dir": str(INPUT_DIR),
            "output_dir": str(OUTPUT_DIR),
        },
    }, indent=2))


if __name__ == "__main__":
    main()
