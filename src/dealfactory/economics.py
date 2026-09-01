from __future__ import annotations

from dataclasses import dataclass

from .models import Asset, DealCosts
from .tsa import TSAExposure


@dataclass(frozen=True)
class DealEconomics:
    annual_standalone_cost_usd: float
    annual_run_rate_delta_usd: float
    tsa_forecast_cost_usd: float
    one_time_cost_usd: float
    three_year_net_value_usd: float
    synergy_realization_ratio: float

    def as_dict(self) -> dict[str, float]:
        return self.__dict__.copy()


def calculate(assets: list[Asset], costs: DealCosts, tsa: list[TSAExposure]) -> DealEconomics:
    standalone = sum(asset.standalone_cost_usd for asset in assets) + costs.annual_standalone_shared_cost_usd
    delta = costs.annual_parent_run_cost_usd - standalone
    tsa_cost = sum(item.forecast_cost_usd for item in tsa)
    one_time = costs.one_time_program_cost_usd + costs.disruption_contingency_usd + tsa_cost
    net = delta * 3 - one_time
    realized = max(0.0, min(1.0, delta / costs.purchase_case_synergy_usd)) if costs.purchase_case_synergy_usd else 0.0
    return DealEconomics(round(standalone, 2), round(delta, 2), round(tsa_cost, 2), round(one_time, 2), round(net, 2), round(realized, 4))

