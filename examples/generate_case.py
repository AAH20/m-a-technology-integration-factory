from __future__ import annotations

import json
from pathlib import Path


domains = ["identity", "network", "erp", "crm", "data", "cloud", "endpoint", "security", "collaboration", "operations"]
capabilities = ["employee-access", "site-connectivity", "order-to-cash", "customer-service", "reporting", "hosting", "workplace", "incident-response", "communications", "service-management"]


def asset(index: int) -> dict[str, object]:
    domain = domains[index % len(domains)]
    core = index < 10
    return {
        "id": f"asset-{index:03d}",
        "name": f"{domain}-{index:03d}",
        "domain": domain,
        "owner": f"owner-{index % 14:02d}",
        "legal_entity": "newco-uk" if index % 3 else "newco-eu",
        "business_capability": capabilities[index % len(capabilities)],
        "criticality": "critical" if core or index % 17 == 0 else "standard",
        "annual_cost_usd": 18000.0 + (index % 8) * 6000.0,
        "standalone_cost_usd": 14000.0 + (index % 8) * 4800.0,
        "data_classification": "restricted" if domain in {"identity", "erp", "data"} else "internal",
        "shared_with_parent": core or index % 11 == 0,
        "day1_required": index < 25,
        "dependencies": [] if core else [f"asset-{index % 10:03d}"]
    }


assets = [asset(index) for index in range(120)]
tsa_services = []
for index in range(35):
    tsa_services.append({
        "id": f"tsa-{index:02d}",
        "name": f"{domains[index % 10]}-transition-service",
        "monthly_charge_usd": 12000.0 + (index % 6) * 4000.0,
        "extension_penalty_usd": 9000.0 + (index % 4) * 3000.0,
        "deadline_month": 9,
        "forecast_exit_month": 7 + (index % 4),
        "dependency_assets": [f"asset-{index % 25:03d}"],
        "acceptance_criteria_met": index % 7 != 0,
        "owner": f"workstream-{index % 8}"
    })

identity_findings = []
for index in range(40):
    identity_findings.append({
        "principal": f"principal-{index:03d}",
        "system": ["entra", "aws", "github", "sap", "salesforce"][index % 5],
        "finding_type": "shared-access",
        "privileged": index % 5 == 0,
        "former_parent_access": index % 4 == 0,
        "owner_confirmed": index % 6 != 0
    })

case = {
    "assets": assets,
    "tsa_services": tsa_services,
    "identity_findings": identity_findings,
    "costs": {
        "purchase_case_synergy_usd": 2400000.0,
        "one_time_program_cost_usd": 3800000.0,
        "annual_parent_run_cost_usd": 7200000.0,
        "annual_standalone_shared_cost_usd": 1500000.0,
        "disruption_contingency_usd": 650000.0
    },
    "evidence_ready": [f"asset-{index:03d}" for index in range(120) if index not in {2, 6, 19, 44, 77}]
}

Path(__file__).with_name("synthetic-international-carveout.json").write_text(json.dumps(case, indent=2) + "\n", encoding="utf-8")

