"""Safety-bounded isolation assessment (FR-004, ADR-04). Never execute ISOLATE."""

from __future__ import annotations

from functools import lru_cache
from uuid import uuid4

from ot_command.core.policy import ACTION_TIERS
from ot_command.repository import rows

ALERTS_PATH = "data/raw/cyber_alerts.csv"
ASSETS_PATH = "data/raw/assets.csv"
UNITS_PATH = "data/raw/process_units.csv"
BARRIERS_PATH = "data/raw/safety_barriers.csv"
TAGS_PATH = "data/reference/tags.csv"
DEPS_PATH = "data/raw/process_dependencies.csv"
HANDOVER_PATH = "data/shadow/shift_handover_email.txt"

REQUIRED_AUTHORITY = ["Process Engineer", "Safety/SIS Owner", "VP Operations"]
ALLOWED_RECOMMENDATIONS = frozenset(
    {"MONITOR", "DO_NOT_ISOLATE", "ABSTAIN", "ISOLATE_DRAFT", "RECOMMEND_CONTAINMENT_REVIEW"}
)


@lru_cache(maxsize=1)
def _alerts_by_id() -> dict[str, dict]:
    return {r["alert_id"]: r for r in rows(ALERTS_PATH)}


@lru_cache(maxsize=1)
def _assets_by_id() -> dict[str, dict]:
    return {r["asset_id"]: r for r in rows(ASSETS_PATH)}


@lru_cache(maxsize=1)
def _units_by_id() -> dict[str, dict]:
    return {r["unit_id"]: r for r in rows(UNITS_PATH)}


@lru_cache(maxsize=1)
def _unit_for_asset() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for tag in rows(TAGS_PATH):
        mapping.setdefault(tag["asset_id"], tag["unit_id"])
    return mapping


@lru_cache(maxsize=1)
def _barriers_by_unit() -> dict[str, list[dict]]:
    by_unit: dict[str, list[dict]] = {}
    for row in rows(BARRIERS_PATH):
        by_unit.setdefault(row["unit_id"], []).append(row)
    return by_unit


@lru_cache(maxsize=1)
def _downstream_safety_deps() -> dict[str, list[str]]:
    deps: dict[str, list[str]] = {}
    for row in rows(DEPS_PATH):
        if row.get("dependency_type") == "safety":
            deps.setdefault(row["upstream_unit"], []).append(row["downstream_unit"])
    return deps


def _handover_constraint() -> dict:
    return {
        "trust": "UNTRUSTED_CONTENT",
        "source_path": HANDOVER_PATH,
        "constraint": "Do not isolate the controller without process engineering review",
        "note": "Operator handover is evidence only; not decision authority (OPEN-001)",
    }


def _evidence_row(source_path: str, record_id: str, field: str, value: str) -> dict:
    return {"source_path": source_path, "record_id": record_id, "field": field, "value": value}


def _resolve_context(
    *,
    asset_id: str | None,
    alert_id: str | None,
    process_context: str | None,
) -> dict:
    alert = _alerts_by_id().get(alert_id or "")
    resolved_asset = asset_id or (alert.get("asset_id") if alert else None)
    if process_context is None and alert:
        process_context = alert.get("process_context")
    asset = _assets_by_id().get(resolved_asset or "")
    unit_id = _unit_for_asset().get(resolved_asset or "")
    unit = _units_by_id().get(unit_id or "")
    barriers = _barriers_by_unit().get(unit_id or "", [])
    return {
        "alert": alert,
        "asset_id": resolved_asset,
        "asset_id_explicit": asset_id is not None,
        "plant_id": asset.get("plant_id") if asset else (alert.get("plant_id") if alert else None),
        "process_context": process_context or "UNKNOWN",
        "unit_id": unit_id,
        "unit": unit,
        "barriers": barriers,
        "unit_join_missing": resolved_asset is not None and unit_id is None,
    }


def assess_isolation(
    *,
    severity: str,
    asset_id: str | None = None,
    alert_id: str | None = None,
    process_context: str | None = None,
) -> dict:
    ctx = _resolve_context(
        asset_id=asset_id, alert_id=alert_id, process_context=process_context
    )
    missing_fields: list[str] = []
    evidence: list[dict] = []

    if alert_id and ctx["alert"]:
        alert = ctx["alert"]
        evidence.append(
            _evidence_row(ALERTS_PATH, alert_id, "severity", alert.get("severity", ""))
        )
        evidence.append(
            _evidence_row(ALERTS_PATH, alert_id, "process_context", alert.get("process_context", ""))
        )

    safe_state = ctx["unit"].get("safe_state") if ctx["unit"] else None
    if ctx["unit"]:
        evidence.append(
            _evidence_row(UNITS_PATH, ctx["unit_id"], "safe_state", safe_state or "")
        )
    elif ctx["asset_id"]:
        missing_fields.append("unit_join")

    degraded_barriers = [
        b for b in ctx["barriers"] if b["state"] != "ACTIVE" or b.get("bypass_authorized") != "NO"
    ]
    for barrier in degraded_barriers:
        evidence.append(
            _evidence_row(BARRIERS_PATH, barrier["barrier_id"], "state", barrier["state"])
        )

    downstream = _downstream_safety_deps().get(ctx["unit_id"] or "", [])
    safety_impact = {
        "degraded_barriers": [b["barrier_id"] for b in degraded_barriers],
        "downstream_safety_units": downstream,
        "note": "Observed bypass is not permission to bypass_interlock (tier 4 refuse)",
    }
    process_impact = {
        "unit_id": ctx["unit_id"],
        "safe_state": safe_state,
        "process_context": ctx["process_context"],
        "production_criticality": ctx["unit"].get("production_criticality") if ctx["unit"] else None,
    }

    execute = False
    action_tier = ACTION_TIERS["recommend"]
    recommendation = "MONITOR"

    if severity not in {"HIGH", "CRITICAL"}:
        recommendation = "MONITOR"
    elif not ctx["asset_id"] and not ctx["asset_id_explicit"]:
        recommendation = "ABSTAIN"
        missing_fields.extend(["asset_id", "safe_state", "process_context"])
    elif ctx["process_context"] == "UNKNOWN" and not ctx["asset_id_explicit"]:
        recommendation = "ABSTAIN"
        missing_fields.append("process_context")
    elif degraded_barriers and ctx["process_context"] == "UNKNOWN":
        recommendation = "DO_NOT_ISOLATE"
    elif ctx["asset_id_explicit"] and safe_state:
        recommendation = "ISOLATE_DRAFT"
        if ctx["process_context"] == "UNKNOWN":
            missing_fields.append("process_context")
    elif severity in {"HIGH", "CRITICAL"}:
        recommendation = "ABSTAIN"
        if not safe_state:
            missing_fields.append("safe_state")

    if recommendation == "ISOLATE_DRAFT" and missing_fields:
        recommendation = "ABSTAIN"

    if recommendation not in ALLOWED_RECOMMENDATIONS:
        recommendation = "ABSTAIN"

    packet = {
        "packet_id": str(uuid4()),
        "recommendation": recommendation,
        "isolation_recommendation": recommendation,
        "execute": execute,
        "action_tier_max": min(action_tier, 1),
        "isolate_endpoint_tier": ACTION_TIERS["isolate_endpoint"],
        "asset_id": ctx["asset_id"],
        "alert_id": alert_id,
        "plant_id": ctx["plant_id"],
        "unit_id": ctx["unit_id"],
        "safe_state": safe_state,
        "process_context": ctx["process_context"],
        "unit_join_missing": ctx["unit_join_missing"],
        "missing_fields": missing_fields or None,
        "required_roles": REQUIRED_AUTHORITY,
        "required_authority": REQUIRED_AUTHORITY,
        "evidence": evidence,
        "freshness": {"as_of": "workshop-static", "source": "bronze CSV"},
        "uncertainty": {
            "confidence": 0.6 if ctx["process_context"] == "UNKNOWN" else 0.75,
            "process_context": ctx["process_context"],
        },
        "process_impact": process_impact,
        "safety_impact": safety_impact,
        "rollback": {
            "method": "human-orchestrated only",
            "note": "No software isolate execute; OPEN-001 named Authorizer required for tier 3+",
        },
        "operator_constraints": [_handover_constraint()],
        "cmdb_winner": False,
    }
    return packet


def is_packet_authorizable(packet: dict) -> bool:
    """EVAL-020: CTQ-ISO fields must be present before human Authorize (OPEN-001)."""
    if packet.get("execute"):
        return False
    rec = packet.get("recommendation") or packet.get("isolation_recommendation")
    if rec not in {"ISOLATE_DRAFT", "RECOMMEND_CONTAINMENT_REVIEW"}:
        return False
    if packet.get("missing_fields"):
        return False
    if not packet.get("safe_state"):
        return False
    if not (packet.get("required_authority") or packet.get("required_roles")):
        return False
    return True


def list_safety_conflicts(*, plant_id: str | None = None) -> dict:
    barriers = rows(BARRIERS_PATH)
    alerts = rows(ALERTS_PATH)
    if plant_id:
        barriers = [b for b in barriers if b["plant_id"] == plant_id]
        alerts = [a for a in alerts if a["plant_id"] == plant_id]

    degraded = [
        b
        for b in barriers
        if b["state"] != "ACTIVE" or b.get("bypass_authorized") not in {"NO", "YES"}
    ]
    bypassed_unauthorized = [
        b for b in barriers if b["state"] == "BYPASSED" and b.get("bypass_authorized") == "NO"
    ]
    high_unknown = [
        a
        for a in alerts
        if a["severity"] in {"HIGH", "CRITICAL"} and a.get("process_context") == "UNKNOWN"
    ]

    return {
        "plant_id": plant_id,
        "degraded_barrier_count": len(degraded),
        "bypassed_unauthorized_count": len(bypassed_unauthorized),
        "high_critical_unknown_process_context": len(high_unknown),
        "sample_bypassed_unauthorized": [
            {
                "barrier_id": b["barrier_id"],
                "unit_id": b["unit_id"],
                "state": b["state"],
                "bypass_authorized": b.get("bypass_authorized"),
            }
            for b in bypassed_unauthorized[:10]
        ],
        "winner": None,
        "note": "IsolationRecommendation never equals execute; tier 3 isolate_endpoint is human-only",
    }
