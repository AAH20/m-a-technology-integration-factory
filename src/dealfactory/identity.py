from __future__ import annotations

from .models import IdentityFinding


def score_identity(finding: IdentityFinding) -> dict[str, object]:
    score = 0
    reasons: list[str] = []
    if finding.former_parent_access:
        score += 50
        reasons.append("former-parent access remains")
    if finding.privileged:
        score += 30
        reasons.append("principal is privileged")
    if not finding.owner_confirmed:
        score += 20
        reasons.append("owner is unconfirmed")
    severity = "critical" if score >= 80 else "high" if score >= 50 else "medium" if score else "none"
    return {"principal": finding.principal, "system": finding.system, "score": score, "severity": severity, "reasons": reasons}

