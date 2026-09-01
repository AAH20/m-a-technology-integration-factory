from __future__ import annotations

import json
from pathlib import Path

from .models import Asset, DealCosts, IdentityFinding, TSAService


def load_case(path: str | Path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    assets = []
    for item in data["assets"]:
        row = dict(item)
        row["dependencies"] = tuple(row.get("dependencies", []))
        assets.append(Asset(**row))
    services = []
    for item in data["tsa_services"]:
        row = dict(item)
        row["dependency_assets"] = tuple(row.get("dependency_assets", []))
        services.append(TSAService(**row))
    identities = [IdentityFinding(**item) for item in data["identity_findings"]]
    return assets, services, identities, DealCosts(**data["costs"]), set(data.get("evidence_ready", []))

