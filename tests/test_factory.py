import unittest

from dealfactory.factory import DealFactory
from dealfactory.models import Asset, DealCosts, IdentityFinding, TSAService


def asset(identifier, dependencies=(), day1=False, shared=False, criticality="standard"):
    return Asset(identifier, identifier, "cloud", "owner", "newco", "hosting", criticality, 100, 80, "internal", shared, day1, dependencies)


class DealFactoryTests(unittest.TestCase):
    def setUp(self):
        self.assets = [asset("identity", day1=True, shared=True, criticality="critical"), asset("erp", ("identity",), day1=True, criticality="critical")]
        self.services = [TSAService("tsa", "identity service", 1000, 500, 6, 6, ("identity",), True, "owner")]
        self.identities = [IdentityFinding("admin", "entra", "shared", True, True, False)]
        self.costs = DealCosts(1000, 2000, 10000, 1000, 500)

    def test_day1_blocker_and_identity_criticality(self):
        result = DealFactory().analyze(self.assets, self.services, self.identities, self.costs, {"identity"})
        self.assertEqual(result["payload"]["day1"]["blockers"], ["erp"])
        self.assertEqual(result["payload"]["identity"][0]["severity"], "critical")
        self.assertEqual(result["payload"]["execution_waves"], [["identity"], ["erp"]])

    def test_tsa_extension_when_dependency_missing(self):
        result = DealFactory().analyze(self.assets, self.services, self.identities, self.costs, set())
        tsa = result["payload"]["tsa"][0]
        self.assertFalse(tsa["on_time"])
        self.assertEqual(tsa["months_extended"], 1)

    def test_receipt_is_explicitly_simulated(self):
        result = DealFactory().analyze(self.assets, self.services, self.identities, self.costs, {"identity", "erp"})
        self.assertEqual(result["evidence_class"], "simulated")
        self.assertEqual(len(result["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()

