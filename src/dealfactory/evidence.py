from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any


def receipt(payload: dict[str, Any]) -> dict[str, Any]:
    envelope = {"schema": "ma.integration.evidence.v1", "evidence_class": "simulated", "generated_at": datetime.now(timezone.utc).isoformat(), "payload": payload}
    canonical = json.dumps(envelope, sort_keys=True, separators=(",", ":")).encode()
    envelope["sha256"] = hashlib.sha256(canonical).hexdigest()
    envelope["integrity_note"] = "Digest detects envelope changes; it does not prove deal-room completeness, identity, custody or realized synergy."
    return envelope

