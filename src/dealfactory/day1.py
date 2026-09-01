from __future__ import annotations

from dataclasses import dataclass

from .models import Asset


@dataclass(frozen=True)
class Day1Readiness:
    required: int
    ready: int
    blocked: int
    readiness: float
    annual_revenue_at_risk_usd: float
    blockers: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {**self.__dict__, "blockers": list(self.blockers)}


def assess_day1(assets: list[Asset], evidence_ready: set[str]) -> Day1Readiness:
    required = [asset for asset in assets if asset.day1_required]
    blockers = tuple(sorted(asset.id for asset in required if asset.id not in evidence_ready))
    ready = len(required) - len(blockers)
    at_risk = sum(asset.annual_cost_usd * 4 for asset in required if asset.id in blockers and asset.criticality == "critical")
    return Day1Readiness(len(required), ready, len(blockers), round(ready / len(required), 4) if required else 1.0, round(at_risk, 2), blockers)

