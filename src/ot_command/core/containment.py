"""Safety-aware containment policy (ADR-04, FR-004). Recommend only. Never execute isolate."""

from __future__ import annotations

from typing import Any

from .policy import ACTION_TIERS
from ..repository import rows

ALERTS_PATH = "data/raw/cyber_alerts.csv"
ASSETS_PATH = "data/raw/assets.csv"
TAGS_PATH = "data/reference/tags.csv"
UNITS_PATH = "data/raw/process_units.csv"
BARRIERS_PATH = "data/raw/safety_barriers.csv"
DEPS_PATH = "data/raw/process_dependencies.csv"
HANDOVER_PATH = "data/shadow/shift_handover_email.txt"
TRANSFORM = "enh-05-containment.1"
AS_OF = "2026-09-10T00:00:00Z"
UNSAFE_SAFE_STATES = {"MIN_LOAD"}
REVIEW_ROLES = ["Process Eng", "Safety/SIS owner", "VP Ops"]

_CACHE: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    alerts = {r["alert_id"]: r for r in rows(ALERTS_PATH)}
    assets = {r["asset_id"]: r for r in rows(ASSETS_PATH)}
    units = {r["unit_id"]: r for r in rows(UNITS_PATH)}
    tags_by_asset: dict[str, list[dict]] = {}
    for tag in rows(TAGS_PATH):
        tags_by_asset.setdefault(tag["asset_id"], []).append(tag)
    barriers_by_unit: dict[str, list[dict]] = {}
    for bar in rows(BARRIERS_PATH):
        barriers_by_unit.setdefault(bar["unit_id"], []).append(bar)
    deps_from: dict[str, list[dict]] = {}
    for dep in rows(DEPS_PATH):
        deps_from.setdefault(dep["upstream_unit"], []).append(dep)
    _CACHE = {
        "alerts": alerts,
        "assets": assets,
        "units": units,
        "tags_by_asset": tags_by_asset,
        "barriers_by_unit": barriers_by_unit,
        "deps_from": deps_from,
    }
    return _CACHE


def _ev(source_path: str, field: str, record_id: str) -> dict:
    return {"source_path": source_path, "field": field, "record_id": record_id}


def isolation_recommendation(alert: dict) -> dict:
    """Return a recommend-only packet. isolate_endpoint is ACTION_TIERS 3 and is never executed."""
    data = _load()
    merged = dict(alert)
    alert_id = merged.get("alert_id")
    if alert_id and alert_id in data["alerts"]:
        for key, val in data["alerts"][alert_id].items():
            merged.setdefault(key, val)
    asset_id = merged.get("asset_id")
    asset = data["assets"].get(asset_id) if asset_id else None
    plant_id = merged.get("plant_id") or (asset["plant_id"] if asset else None)
    unit_ids = []
    if merged.get("unit"):
        unit_ids.append(merged["unit"])
    if asset_id:
        unit_ids.extend(t["unit_id"] for t in data["tags_by_asset"].get(asset_id, []) if t.get("unit_id"))
    unit_ids = list(dict.fromkeys(uid for uid in unit_ids if uid))
    unit_join_missing = not unit_ids
    units = [data["units"][uid] for uid in unit_ids if uid in data["units"]]
    safe_state = merged.get("safe_state")
    if safe_state is None and units:
        safe_state = units[0].get("safe_state")
    barriers = []
    for uid in unit_ids:
        barriers.extend(data["barriers_by_unit"].get(uid, []))
    downstream = []
    for uid in unit_ids:
        downstream.extend(data["deps_from"].get(uid, []))
    process_context = merged.get("process_context") or "UNKNOWN"
    severity = (merged.get("severity") or "").upper()
    high_crit = severity in {"HIGH", "CRITICAL"}
    pe_warning = bool(merged.get("process_engineer_warning"))
    soc_isolate = bool(merged.get("soc_requests_isolate"))
    user_prompt = str(merged.get("user_prompt") or merged.get("prompt") or "")
    override = any(
        tok in user_prompt.lower()
        for tok in ("isolate", "ignore safety", "bypass the sis", "write plc")
    )
    handover_constraint = bool(merged.get("cascade") or merged.get("scenario"))
    unsafe_state = safe_state in UNSAFE_SAFE_STATES
    critical_dep = any(d.get("critical") == "YES" or d.get("dependency_type") == "safety" for d in downstream)
    missing_ctq = high_crit and not safe_state
    unknown_ctx = str(process_context).upper() == "UNKNOWN"

    abstain = bool(
        unknown_ctx
        or unsafe_state
        or pe_warning
        or (soc_isolate and pe_warning)
        or override
        or handover_constraint
        or missing_ctq
        or (high_crit and unit_join_missing)
        or critical_dep
    )
    if abstain:
        rec = "ABSTAIN"
    elif high_crit and safe_state and not unit_join_missing:
        rec = "RECOMMEND_CONTAINMENT_REVIEW"
    else:
        rec = "MONITOR"

    evidence = [
        _ev("src/ot_command/core/policy.py", "ACTION_TIERS.isolate_endpoint", "3"),
        _ev("src/ot_command/core/policy.py", "ACTION_TIERS.recommend", "1"),
    ]
    if alert_id:
        evidence.append(_ev(ALERTS_PATH, "alert_id", str(alert_id)))
    if asset_id:
        evidence.append(_ev(ASSETS_PATH, "asset_id", str(asset_id)))
    if unit_ids:
        evidence.append(_ev(UNITS_PATH, "unit_id", unit_ids[0]))
    if barriers:
        evidence.append(_ev(BARRIERS_PATH, "barrier_id", barriers[0]["barrier_id"]))
    if handover_constraint or override or pe_warning:
        evidence.append(_ev(HANDOVER_PATH, "operator_constraint", "untrusted"))

    bypassed = [b for b in barriers if b.get("state") in {"BYPASSED", "DEGRADED"}]
    packet = {
        "packet_id": f"pkt-{alert_id or asset_id or 'adhoc'}",
        "subject_asset_uid": asset_id,
        "plant_id": plant_id,
        "isolation_recommendation": rec,
        "recommendation": rec,
        "safe_state": safe_state,
        "unit_id": unit_ids[0] if unit_ids else None,
        "unit_join_missing": unit_join_missing,
        "process_context": process_context,
        "executed": False,
        "authorizable": False,
        "one_click_isolate": False,
        "action_tier_max": 1,
        "permitted_action": "recommend" if rec != "MONITOR" else "observe",
        "forbidden_action": "isolate_endpoint",
        "isolate_endpoint_tier": ACTION_TIERS["isolate_endpoint"],
        "required_role": list(REVIEW_ROLES),
        "required_authority": list(REVIEW_ROLES),
        "evidence": evidence,
        "freshness": {"as_of": AS_OF, "alert_timestamp": merged.get("timestamp") or merged.get("time")},
        "uncertainty": {
            "confidence": 0.4 if unknown_ctx or unit_join_missing else 0.6,
            "process_context": process_context,
            "open_001_named_authorizer": True,
        },
        "process_impact": {
            "safe_state": safe_state,
            "downstream_units": [d.get("downstream_unit") for d in downstream],
            "critical_dependency": critical_dep,
        },
        "safety_impact": {
            "bypassed_or_degraded_barriers": [b["barrier_id"] for b in bypassed],
            "observe_existing_bypass_is_not_bypass_interlock": True,
        },
        "rollback": {"software": "none — no OT write was issued", "human": "war-room / process restart authority OPEN-001"},
        "vector_used": False,
        "transform_version": TRANSFORM,
    }
    return packet


def safety_conflicts(limit: int = 50) -> dict:
    data = _load()
    items = []
    unknown_high = 0
    for alert in data["alerts"].values():
        if alert.get("severity") not in {"HIGH", "CRITICAL"}:
            continue
        if str(alert.get("process_context", "")).upper() == "UNKNOWN":
            unknown_high += 1
        if len(items) < limit:
            packet = isolation_recommendation(alert)
            items.append(
                {
                    "alert_id": alert["alert_id"],
                    "asset_id": alert["asset_id"],
                    "severity": alert["severity"],
                    "process_context": alert["process_context"],
                    "isolation_recommendation": packet["isolation_recommendation"],
                    "executed": False,
                }
            )
    bypassed = [
        {"barrier_id": b["barrier_id"], "unit_id": b["unit_id"], "state": b["state"], "bypass_authorized": b["bypass_authorized"]}
        for rows_ in data["barriers_by_unit"].values()
        for b in rows_
        if b.get("state") in {"BYPASSED", "DEGRADED"}
    ]
    return {
        "unknown_process_context_high_crit_count": unknown_high,
        "alerts": items,
        "bypassed_or_degraded_barriers": bypassed[:limit],
        "executed": False,
        "isolate_execute": False,
        "note": "Observe existing bypass ≠ bypass_interlock. Isolation is never execute.",
    }


def recommendation_packet(incident_id: str) -> dict:
    data = _load()
    if incident_id in data["alerts"]:
        return isolation_recommendation(data["alerts"][incident_id])
    if incident_id in data["assets"]:
        return isolation_recommendation({"asset_id": incident_id})
    raise KeyError(incident_id)
