
import unittest

from output_schema import (
    SCHEMA_VERSION,
    build_metadata,
)


class TestOutputSchema(unittest.TestCase):
    def test_metadata_contains_shared_fields(self):
        metadata = build_metadata(
            event_id="event-001",
            processing_status="completed",
            source="flood_extent.geojson",
            event_date="2026-10-12",
            uncertainty_notes=["Sample data only"],
        )

        self.assertEqual(metadata["schema_version"], SCHEMA_VERSION)
        self.assertEqual(metadata["event_id"], "event-001")
        self.assertEqual(metadata["processing_status"], "completed")
        self.assertEqual(metadata["source"], "flood_extent.geojson")
        self.assertEqual(metadata["crs"], "EPSG:4326")
        self.assertEqual(metadata["uncertainty_notes"], ["Sample data only"])
        self.assertIn("generated_at", metadata)

    def test_invalid_processing_status_is_rejected(self):
        with self.assertRaises(ValueError):
            build_metadata(processing_status="unknown_status")


if __name__ == "__main__":
    unittest.main()
