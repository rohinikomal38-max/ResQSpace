
import unittest

from infrastructure import assess_exposure


class MockGeometry:
    def __init__(self, intersects_result=False, empty=False):
        self.intersects_result = intersects_result
        self.is_empty = empty

    def intersects(self, other):
        return self.intersects_result


class TestInfrastructureExposure(unittest.TestCase):
    def test_intersecting_asset_is_exposed(self):
        asset = MockGeometry(intersects_result=True)
        flood = MockGeometry()

        self.assertTrue(assess_exposure(asset, flood))

    def test_non_intersecting_asset_is_not_exposed(self):
        asset = MockGeometry(intersects_result=False)
        flood = MockGeometry()

        self.assertFalse(assess_exposure(asset, flood))

    def test_missing_geometry_returns_none(self):
        self.assertIsNone(assess_exposure(None, MockGeometry()))

    def test_empty_geometry_returns_none(self):
        asset = MockGeometry(empty=True)
        flood = MockGeometry()

        self.assertIsNone(assess_exposure(asset, flood))


if __name__ == "__main__":
    unittest.main()
