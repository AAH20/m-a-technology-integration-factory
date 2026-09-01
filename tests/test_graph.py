import unittest

from dealfactory.graph import AssetGraph
from dealfactory.models import Asset


def asset(identifier, dependencies=()):
    return Asset(identifier, identifier, "x", "o", "e", "c", "standard", 1, 1, "internal", dependencies=dependencies)


class GraphTests(unittest.TestCase):
    def test_missing_asset_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing asset"):
            AssetGraph([asset("a", ("missing",))])

    def test_cycle_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "cycle"):
            AssetGraph([asset("a", ("b",)), asset("b", ("a",))])


if __name__ == "__main__":
    unittest.main()

