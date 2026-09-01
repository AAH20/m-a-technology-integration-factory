from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .day1 import assess_day1
from .economics import calculate
from .evidence import receipt
from .graph import AssetGraph
from .identity import score_identity
from .models import Asset, DealCosts, IdentityFinding, TSAService
from .tsa import forecast


class DealFactory:
    def analyze(self, assets: list[Asset], services: list[TSAService], identities: list[IdentityFinding], costs: DealCosts, evidence_ready: set[str]) -> dict[str, Any]:
        if not assets:
            raise ValueError("assets are required")
        graph = AssetGraph(assets)
        day1 = assess_day1(assets, evidence_ready)
        tsa = [forecast(service, evidence_ready) for service in services]
        identity = [score_identity(finding) for finding in identities]
        economics = calculate(assets, costs, tsa)
        payload = {
            "deal_scope": {"assets": len(assets), "tsa_services": len(services), "identity_findings": len(identities)},
            "day1": day1.as_dict(),
            "tsa": [item.as_dict() for item in tsa],
            "identity": identity,
            "execution_waves": graph.waves(),
            "shared_critical_assets": [asset.id for asset in assets if asset.shared_with_parent and (asset.criticality == "critical" or graph.blast_radius(asset.id) >= 5)],
            "economics": economics.as_dict(),
            "cost_inputs": asdict(costs),
            "decision_boundary": "analysis is advisory; owners, legal counsel and authorized change governance approve execution",
        }
        return receipt(payload)

