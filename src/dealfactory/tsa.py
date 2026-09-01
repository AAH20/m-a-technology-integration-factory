from __future__ import annotations

from dataclasses import dataclass

from .models import TSAService


@dataclass(frozen=True)
class TSAExposure:
    service_id: str
    on_time: bool
    months_extended: int
    forecast_cost_usd: float
    blocker: str | None

    def as_dict(self) -> dict[str, object]:
        return self.__dict__.copy()


def forecast(service: TSAService, ready_assets: set[str]) -> TSAExposure:
    missing = sorted(set(service.dependency_assets) - ready_assets)
    criteria_ready = service.acceptance_criteria_met and not missing
    forecast_month = service.forecast_exit_month if criteria_ready else max(service.forecast_exit_month, service.deadline_month + 1)
    extension = max(0, forecast_month - service.deadline_month)
    cost = forecast_month * service.monthly_charge_usd + extension * service.extension_penalty_usd
    blocker = f"missing dependencies: {', '.join(missing)}" if missing else (None if service.acceptance_criteria_met else "acceptance criteria incomplete")
    return TSAExposure(service.id, extension == 0, extension, round(cost, 2), blocker)

