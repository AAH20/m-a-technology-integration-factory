from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Asset:
    id: str
    name: str
    domain: str
    owner: str
    legal_entity: str
    business_capability: str
    criticality: str
    annual_cost_usd: float
    standalone_cost_usd: float
    data_classification: str
    shared_with_parent: bool = False
    day1_required: bool = False
    dependencies: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TSAService:
    id: str
    name: str
    monthly_charge_usd: float
    extension_penalty_usd: float
    deadline_month: int
    forecast_exit_month: int
    dependency_assets: tuple[str, ...]
    acceptance_criteria_met: bool
    owner: str


@dataclass(frozen=True)
class IdentityFinding:
    principal: str
    system: str
    finding_type: str
    privileged: bool
    former_parent_access: bool
    owner_confirmed: bool


@dataclass(frozen=True)
class DealCosts:
    purchase_case_synergy_usd: float
    one_time_program_cost_usd: float
    annual_parent_run_cost_usd: float
    annual_standalone_shared_cost_usd: float
    disruption_contingency_usd: float

