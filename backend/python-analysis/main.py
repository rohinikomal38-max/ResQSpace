
import json

from output_schema import build_metadata


def main():
    result = build_metadata(
        processing_status="pending",
        uncertainty_notes=[
            "Flood input has not been loaded yet.",
            "Infrastructure and connectivity analysis has not run yet.",
        ],
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

