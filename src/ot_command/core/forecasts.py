"""Deterministic advisory forecasts (Moonshot) and template captions (AI ON).

No LLM ranker. Engines remain authoritative. execute is always false.
UNKNOWN process_context is not permission to isolate.
"""

from __future__ import annotations

from functools import lru_cache

from ot_command.core.policy import ACTION_TIERS
from ot_command.core.data_layer import (
    derived_alerts_by_id,
    derived_alerts_by_plant,
    derived_assets_by_id,
    derived_assets_by_plant,
    derived_plants_by_id,
    derived_recovery_by_plant,
    derived_vendor_session_anomalies,
    load_safety_barriers,
    load_vulnerabilities,
    source_path,
)
from ot_command.repository import rows

BANNER = "ADVISORY FORECAST — NOT A CONTROL ACTION"
ALLOWED_ACTIONS = frozenset({"MONITOR", "RECOMMEND_CONTAINMENT_REVIEW", "ABSTAIN"})
TWIN_ACTIONS = frozenset({"do_nothing", "isolate_preview", "increase_logging", "open_ticket"})
WRITE_LIKE = frozenset({"UNEXPECTED_WRITE", "CONFIG_DRIFT"})
SAFETY_AGING_TYPES = frozenset({"SIS_TRIP", "PERMISSIVE"})
RESTORE_TEST_ROT_DAYS = 90
HIGH_CRIT = frozenset({"HIGH", "CRITICAL"})
HIGH_PLANTS = frozenset({"HIGH", "CRITICAL"})

TAGS_PATH = "data/reference/tags.csv"
UNITS_PATH = "data/raw/process_units.csv"
NETWORK_PATH = "data/raw/network_edges.csv"
BARRIERS_PATH = source_path("safety_barriers")
ALERTS_PATH = source_path("cyber_alerts")
SESSIONS_PATH = source_path("vendor_sessions")
ASSETS_PATH = source_path("assets")
VULNS_PATH = source_path("vulnerabilities")
RECOVERY_PATH = source_path("recovery_readiness")
PLANTS_PATH = "data/reference/plants.csv"

CATEGORY_PRIORITY = {
    "UNKNOWN_PROCESS_CONTEXT": 0,
    "SAFETY_BYPASS_AGING": 1,
    "VENDOR_SESSION_PLUS_WRITE_ALERT": 2,
    "UNDOCUMENTED_PATH_ON_CRITICAL_UNIT": 3,
    "IDENTITY_CONFLICT_REACHABLE": 4,
    "RESTORE_TEST_ROT": 5,
}


@lru_cache(maxsize=1)
def _units_by_id() -> dict[str, dict]:
    return {r["unit_id"]: dict(r) for r in rows(UNITS_PATH)}


@lru_cache(maxsize=1)
def _unit_for_asset() -> dict[str, str]:
    mapping: dict[str, str] = {}
    for tag in rows(TAGS_PATH):
        mapping.setdefault(tag["asset_id"], tag["unit_id"])
    return mapping


@lru_cache(maxsize=1)
def _network_edges() -> tuple[dict, ...]:
    return tuple(rows(NETWORK_PATH))


def _plant_or_404(plant_id: str) -> dict:
    plant = derived_plants_by_id().get(plant_id)
    if not plant:
        raise KeyError(plant_id)
    return plant


def _forecast_id(plant_id: str, seq: int) -> str:
    compact = plant_id.replace("-", "")
    return f"FC-{compact}-{seq:02d}"


def _parse_plant_from_forecast_id(forecast_id: str) -> str | None:
    if not forecast_id.startswith("FC-PLT"):
        return None
    rest = forecast_id[len("FC-") :]
    parts = rest.split("-")
    if len(parts) < 2:
        return None
    token = parts[0]
    if token.startswith("PLT") and token[3:].isdigit():
        return f"PLT-{token[3:]}"
    return None


def _role_for_category(category: str) -> str:
    if category in {"SAFETY_BYPASS_AGING", "UNKNOWN_PROCESS_CONTEXT"}:
        return "PROCESS_ENGINEER"
    if category == "RESTORE_TEST_ROT":
        return "PROCESS_ENGINEER"
    return "PROCESS_ENGINEER"


def _layer_for_category(category: str) -> str:
    return {
        "VENDOR_SESSION_PLUS_WRITE_ALERT": "CYBER",
        "SAFETY_BYPASS_AGING": "SAFETY",
        "RESTORE_TEST_ROT": "RECOVERY",
        "IDENTITY_CONFLICT_REACHABLE": "CYBER",
        "UNDOCUMENTED_PATH_ON_CRITICAL_UNIT": "CYBER",
        "UNKNOWN_PROCESS_CONTEXT": "PROCESS",
    }.get(category, "CYBER")


def _twin_scenario_for_category(category: str, plant_id: str) -> str:
    if category in {"VENDOR_SESSION_PLUS_WRITE_ALERT", "SAFETY_BYPASS_AGING", "UNKNOWN_PROCESS_CONTEXT"} and plant_id == "PLT-10":
        return "cascade_001"
    if category == "IDENTITY_CONFLICT_REACHABLE":
        return "inject_01"
    if category == "RESTORE_TEST_ROT":
        return "inject_05"
    return "nominal"


def _clamp_action(*, process_context: str | None, intended: str) -> str:
    if process_context == "UNKNOWN":
        return "ABSTAIN" if intended != "MONITOR" else "MONITOR"
    if intended not in ALLOWED_ACTIONS:
        return "ABSTAIN"
    return intended


def _base_forecast(
    *,
    forecast_id: str,
    plant_id: str,
    asset_id: str | None,
    category: str,
    evidence_ids: list[str],
    missing_evidence: list[str],
    abstain_reason: str | None,
    recommended_action: str,
    process_context: str | None = None,
    extra: dict | None = None,
) -> dict:
    action = _clamp_action(process_context=process_context, intended=recommended_action)
    row = {
        "forecast_id": forecast_id,
        "plant_id": plant_id,
        "asset_id": asset_id,
        "category": category,
        "layer": _layer_for_category(category),
        "horizon_days": 7,
        "confidence": "LOW" if process_context == "UNKNOWN" or missing_evidence else "MEDIUM",
        "recommended_action": action,
        "required_role": _role_for_category(category),
        "action_tier": min(ACTION_TIERS["recommend"], 1),
        "twin_scenario_id": _twin_scenario_for_category(category, plant_id),
        "evidence_ids": evidence_ids,
        "missing_evidence": missing_evidence,
        "abstain_reason": abstain_reason,
        "execute": False,
    }
    if extra:
        row.update(extra)
    return row


def _vendor_plus_write(
    *,
    plant_id: str,
    alert_id: str | None,
    asset_id: str | None,
) -> dict | None:
    alerts = list(derived_alerts_by_plant().get(plant_id, []))
    sessions = [s for s in derived_vendor_session_anomalies() if s.get("plant_id") == plant_id and "unapproved_window" in s.get("anomaly_flags", [])]
    if not sessions:
        return None

    write_alerts = [
        a
        for a in alerts
        if a.get("type") in WRITE_LIKE and a.get("severity") in HIGH_CRIT
    ]
    if not write_alerts:
        return None

    chosen_alert = None
    if alert_id:
        chosen_alert = next((a for a in write_alerts if a["alert_id"] == alert_id), None)
    if chosen_alert is None and asset_id:
        chosen_alert = next((a for a in write_alerts if a.get("asset_id") == asset_id), None)
    if chosen_alert is None:
        # Prefer CASCADE seed ALT-002783 when present.
        chosen_alert = next((a for a in write_alerts if a["alert_id"] == "ALT-002783"), write_alerts[0])

    session = next((s for s in sessions if s.get("asset_id") == chosen_alert.get("asset_id")), None)
    if session is None:
        session = next((s for s in sessions if s.get("session_id") == "RA-00025"), sessions[0])

    ctx = chosen_alert.get("process_context") or "UNKNOWN"
    unit_id = _unit_for_asset().get(chosen_alert.get("asset_id") or "")
    unit = _units_by_id().get(unit_id or "")
    safe_state = unit.get("safe_state") if unit else None
    barriers = [
        b
        for b in load_safety_barriers()
        if b.get("plant_id") == plant_id and b.get("unit_id") == unit_id and b.get("state") == "BYPASSED"
    ]
    barrier = next((b for b in barriers if b.get("barrier_id") == "PLT-10-SAFE-07"), barriers[0] if barriers else None)

    evidence = [chosen_alert["alert_id"], session["session_id"]]
    if barrier:
        evidence.append(barrier["barrier_id"])
    missing = []
    if ctx == "UNKNOWN":
        missing.append("process_context")
    reason = None
    if ctx == "UNKNOWN":
        parts = [f"process_context={ctx}"]
        if barrier and barrier.get("bypass_authorized") == "NO":
            parts.append(f"barrier {barrier['state']} unauthorized")
        if safe_state:
            parts.append(f"safe_state={safe_state}")
        reason = "; ".join(parts)

    return _base_forecast(
        forecast_id="",
        plant_id=plant_id,
        asset_id=chosen_alert.get("asset_id"),
        category="VENDOR_SESSION_PLUS_WRITE_ALERT",
        evidence_ids=evidence,
        missing_evidence=missing,
        abstain_reason=reason,
        recommended_action="ABSTAIN" if ctx == "UNKNOWN" else "RECOMMEND_CONTAINMENT_REVIEW",
        process_context=ctx,
        extra={"alert_id": chosen_alert["alert_id"], "session_id": session["session_id"]},
    )


def _safety_bypass_aging(*, plant_id: str, asset_id: str | None) -> list[dict]:
    unit_id = _unit_for_asset().get(asset_id or "") if asset_id else None
    rows_out: list[dict] = []
    seen: set[str] = set()
    for barrier in load_safety_barriers():
        if barrier.get("plant_id") != plant_id:
            continue
        aging_type = barrier.get("barrier_type") in SAFETY_AGING_TYPES and barrier.get("state") != "ACTIVE"
        unauthorized_bypass = barrier.get("state") == "BYPASSED" and barrier.get("bypass_authorized") == "NO"
        if not (aging_type or unauthorized_bypass):
            continue
        bid = barrier["barrier_id"]
        if bid in seen:
            continue
        seen.add(bid)
        unit = _units_by_id().get(barrier.get("unit_id") or "")
        asset_for_unit = None
        if asset_id and _unit_for_asset().get(asset_id) == barrier.get("unit_id"):
            asset_for_unit = asset_id
        min_load = bool(unit and unit.get("safe_state") == "MIN_LOAD")
        reason = (
            f"barrier_type={barrier.get('barrier_type')} state={barrier.get('state')} "
            f"bypass_authorized={barrier.get('bypass_authorized')}"
        )
        if min_load:
            reason += f"; safe_state={unit['safe_state']}"
        rows_out.append(
            _base_forecast(
                forecast_id="",
                plant_id=plant_id,
                asset_id=asset_for_unit,
                category="SAFETY_BYPASS_AGING",
                evidence_ids=[bid],
                missing_evidence=[],
                abstain_reason=reason if (unauthorized_bypass or min_load) else None,
                recommended_action="ABSTAIN" if unauthorized_bypass or min_load else "MONITOR",
                process_context="UNKNOWN" if unauthorized_bypass else None,
                extra={"barrier_id": bid, "unit_id": barrier.get("unit_id"), "preferred": bid == "PLT-10-SAFE-07" or (unit_id and barrier.get("unit_id") == unit_id)},
            )
        )
    rows_out.sort(key=lambda r: (0 if r.get("preferred") else 1, r.get("barrier_id") or ""))
    for row in rows_out:
        row.pop("preferred", None)
    return rows_out[:3]


def _restore_test_rot(*, plant_id: str) -> list[dict]:
    found: list[dict] = []
    for rec in derived_recovery_by_plant().get(plant_id, []):
        if rec.get("backup_status") != "CURRENT":
            continue
        try:
            days = int(rec.get("last_restore_test_days") or 0)
        except (TypeError, ValueError):
            continue
        if days <= RESTORE_TEST_ROT_DAYS:
            continue
        component = rec.get("component") or "UNKNOWN"
        found.append(
            _base_forecast(
                forecast_id="",
                plant_id=plant_id,
                asset_id=None,
                category="RESTORE_TEST_ROT",
                evidence_ids=[f"{plant_id}:{component}"],
                missing_evidence=[],
                abstain_reason=None,
                recommended_action="MONITOR",
                extra={"component": component, "last_restore_test_days": days, "preferred": component == "IDENTITY"},
            )
        )
    found.sort(key=lambda r: (0 if r.get("preferred") else 1, -int(r.get("last_restore_test_days") or 0)))
    for row in found:
        row.pop("preferred", None)
    return found[:2]


def _identity_conflict_reachable(*, plant_id: str, asset_id: str | None) -> list[dict]:
    assets = derived_assets_by_plant().get(plant_id, [])
    vulns_by_asset: dict[str, list[dict]] = {}
    for v in load_vulnerabilities():
        vulns_by_asset.setdefault(v["asset_id"], []).append(v)

    found: list[dict] = []
    for asset in assets:
        registered = asset.get("registered_state")
        observed = asset.get("observed_state")
        conflict = (registered == "ACTIVE" and observed in {"OFFLINE", "UNSEEN"}) or (
            registered == "RETIRED" and observed == "ONLINE"
        )
        if not conflict:
            continue
        aid = asset["asset_id"]
        if asset_id and aid != asset_id:
            continue
        open_reachable = [
            v
            for v in vulns_by_asset.get(aid, [])
            if v.get("status") == "OPEN" and (v.get("network_reachable") or v.get("reachable")) == "YES"
        ]
        if not open_reachable:
            continue
        vuln = max(open_reachable, key=lambda v: float(v.get("cvss") or 0))
        reachable = vuln.get("network_reachable") or vuln.get("reachable") or "UNKNOWN"
        cvss = float(vuln.get("cvss") or 0)
        crit = asset.get("criticality") or "UNKNOWN"
        unreachable_high = reachable == "NO" and cvss >= 9.0
        reachable_open_crit = reachable == "YES" and vuln.get("status") == "OPEN" and crit in HIGH_CRIT
        found.append(
            _base_forecast(
                forecast_id="",
                plant_id=plant_id,
                asset_id=aid,
                category="IDENTITY_CONFLICT_REACHABLE",
                evidence_ids=[aid, vuln.get("finding_id") or ""],
                missing_evidence=[],
                abstain_reason=None,
                recommended_action="RECOMMEND_CONTAINMENT_REVIEW",
                extra={
                    "registered_state": registered,
                    "observed_state": observed,
                    "finding_id": vuln.get("finding_id"),
                    "cvss": cvss,
                    "reachable": reachable,
                    "_unreachable_cvss9": unreachable_high,
                    "_reachable_open_crit": reachable_open_crit,
                    "preferred": aid == "OT-00528",
                },
            )
        )
    found.sort(key=lambda r: (0 if r.get("preferred") else 1, 0 if r.get("_reachable_open_crit") else 1, r.get("asset_id") or ""))
    for row in found:
        row.pop("preferred", None)
    return found[:3]


def _undocumented_path(*, plant_id: str, asset_id: str | None) -> dict | None:
    plant = derived_plants_by_id().get(plant_id) or {}
    if plant.get("criticality") not in HIGH_PLANTS:
        return None
    edges = [
        e
        for e in _network_edges()
        if e.get("plant_id") == plant_id and e.get("documented") == "NO" and e.get("observed_last_24h") == "YES"
    ]
    if not edges:
        return None
    chosen = None
    if asset_id:
        chosen = next((e for e in edges if e.get("source_asset") == asset_id or e.get("target_asset") == asset_id), None)
    chosen = chosen or edges[0]
    aid = asset_id if asset_id in {chosen.get("source_asset"), chosen.get("target_asset")} else chosen.get("target_asset")
    return _base_forecast(
        forecast_id="",
        plant_id=plant_id,
        asset_id=aid,
        category="UNDOCUMENTED_PATH_ON_CRITICAL_UNIT",
        evidence_ids=[chosen.get("source_asset") or "", chosen.get("target_asset") or ""],
        missing_evidence=[],
        abstain_reason=None,
        recommended_action="MONITOR",
        extra={
            "source_asset": chosen.get("source_asset"),
            "target_asset": chosen.get("target_asset"),
            "protocol": chosen.get("protocol"),
        },
    )


def _unknown_process_context(*, plant_id: str, alert_id: str | None, asset_id: str | None) -> dict | None:
    alerts = list(derived_alerts_by_plant().get(plant_id, []))
    candidates = [
        a
        for a in alerts
        if a.get("severity") in HIGH_CRIT and (a.get("process_context") or "UNKNOWN") == "UNKNOWN"
    ]
    if not candidates:
        return None
    chosen = None
    if alert_id:
        pinned = derived_alerts_by_id().get(alert_id)
        if (
            pinned
            and pinned.get("plant_id") == plant_id
            and pinned.get("severity") in HIGH_CRIT
            and (pinned.get("process_context") or "UNKNOWN") == "UNKNOWN"
        ):
            chosen = pinned
        else:
            chosen = next((a for a in candidates if a["alert_id"] == alert_id), None)
    if chosen is None and asset_id:
        chosen = next((a for a in candidates if a.get("asset_id") == asset_id), None)
    if chosen is None:
        chosen = next((a for a in candidates if a["alert_id"] == "ALT-002783"), candidates[0])

    unit_id = _unit_for_asset().get(chosen.get("asset_id") or "")
    unit = _units_by_id().get(unit_id or "")
    safe_state = unit.get("safe_state") if unit else None
    reason = "process_context=UNKNOWN"
    if safe_state:
        reason += f"; safe_state={safe_state}"
    return _base_forecast(
        forecast_id="",
        plant_id=plant_id,
        asset_id=chosen.get("asset_id"),
        category="UNKNOWN_PROCESS_CONTEXT",
        evidence_ids=[chosen["alert_id"]],
        missing_evidence=["process_context"],
        abstain_reason=reason,
        recommended_action="ABSTAIN",
        process_context="UNKNOWN",
        extra={"alert_id": chosen["alert_id"]},
    )


def _assign_ids(plant_id: str, forecasts: list[dict]) -> list[dict]:
    out = []
    for i, row in enumerate(forecasts, start=1):
        item = dict(row)
        item["forecast_id"] = _forecast_id(plant_id, i)
        if item.get("recommended_action") not in ALLOWED_ACTIONS:
            item["recommended_action"] = "ABSTAIN"
        item["execute"] = False
        item["action_tier"] = min(int(item.get("action_tier") or 1), 1)
        out.append(item)
    return out


def _rank_forecasts(forecasts: list[dict]) -> list[dict]:
    """Unreachable CVSS ≥9.0 must not rank above reachable OPEN on CRITICAL/HIGH."""

    def key(row: dict) -> tuple:
        unreachable = 1 if row.get("_unreachable_cvss9") else 0
        reachable_open_crit = 0 if row.get("_reachable_open_crit") else 1
        category = CATEGORY_PRIORITY.get(row.get("category") or "", 99)
        return (category, unreachable, reachable_open_crit, row.get("asset_id") or "")

    ranked = sorted(forecasts, key=key)
    for row in ranked:
        row.pop("_unreachable_cvss9", None)
        row.pop("_reachable_open_crit", None)
    return ranked


def list_forecasts(
    *,
    plant_id: str,
    asset_id: str | None = None,
    alert_id: str | None = None,
    as_of: str = "workshop-static",
) -> dict:
    del as_of
    _plant_or_404(plant_id)
    collected: list[dict] = []

    vendor = _vendor_plus_write(plant_id=plant_id, alert_id=alert_id, asset_id=asset_id)
    if vendor:
        collected.append(vendor)
    collected.extend(_safety_bypass_aging(plant_id=plant_id, asset_id=asset_id))
    collected.extend(_restore_test_rot(plant_id=plant_id))
    collected.extend(_identity_conflict_reachable(plant_id=plant_id, asset_id=asset_id))
    undoc = _undocumented_path(plant_id=plant_id, asset_id=asset_id)
    if undoc:
        collected.append(undoc)
    unknown = _unknown_process_context(plant_id=plant_id, alert_id=alert_id, asset_id=asset_id)
    if unknown:
        collected.append(unknown)

    if alert_id:
        collected = [
            c
            for c in collected
            if c.get("alert_id") in {None, alert_id} or c.get("category") not in {"VENDOR_SESSION_PLUS_WRITE_ALERT", "UNKNOWN_PROCESS_CONTEXT"}
        ]

    ranked = _rank_forecasts(collected)
    numbered = _assign_ids(plant_id, ranked)
    return {
        "mode": "moonshot",
        "banner": BANNER,
        "execute": False,
        "plant_id": plant_id,
        "asset_id": asset_id,
        "alert_id": alert_id,
        "forecasts": numbered,
        "note": "Deterministic CSV joins — not a model ranker. Engines remain authoritative.",
    }


def get_forecast(forecast_id: str) -> dict | None:
    plant_id = _parse_plant_from_forecast_id(forecast_id)
    if not plant_id:
        return None
    try:
        payload = list_forecasts(plant_id=plant_id)
    except KeyError:
        return None
    return next((f for f in payload["forecasts"] if f["forecast_id"] == forecast_id), None)


def explain_slice(
    *,
    plant_id: str,
    asset_id: str | None = None,
    alert_id: str | None = None,
) -> dict:
    plant = _plant_or_404(plant_id)
    forecast_payload = list_forecasts(plant_id=plant_id, asset_id=asset_id, alert_id=alert_id)
    forecasts = forecast_payload["forecasts"]
    alert = derived_alerts_by_id().get(alert_id or "")
    asset = derived_assets_by_id().get(asset_id or (alert.get("asset_id") if alert else "") or "")
    unit_id = _unit_for_asset().get((asset or {}).get("asset_id") or "")
    unit = _units_by_id().get(unit_id or "")

    evidence_ids: list[str] = []
    source_files = {PLANTS_PATH, ALERTS_PATH, ASSETS_PATH, BARRIERS_PATH, SESSIONS_PATH}
    sentences: list[str] = []

    sentences.append(
        f"Plant {plant_id} is {plant.get('criticality', 'UNKNOWN')} criticality ({plant.get('plant_type', 'unknown type')}, {plant.get('region', 'UNKNOWN')})."
    )
    if alert:
        evidence_ids.append(alert["alert_id"])
        sentences.append(
            f"Alert {alert['alert_id']} on {(asset or {}).get('asset_id') or alert.get('asset_id')} is {alert.get('severity')} {alert.get('type')} with process_context={alert.get('process_context') or 'UNKNOWN'}."
        )
        if (alert.get("process_context") or "UNKNOWN") == "UNKNOWN":
            sentences.append("UNKNOWN process context is not permission to isolate; the engine packet must ABSTAIN or MONITOR.")
    elif asset:
        evidence_ids.append(asset["asset_id"])
        sentences.append(
            f"Asset {asset['asset_id']} is registered {asset.get('registered_state')} and observed {asset.get('observed_state')} (criticality {asset.get('criticality')})."
        )
    if unit:
        source_files.add(UNITS_PATH)
        sentences.append(
            f"Unit {unit_id} production_criticality={unit.get('production_criticality')} with safe_state={unit.get('safe_state')}."
        )

    vendor = next((f for f in forecasts if f["category"] == "VENDOR_SESSION_PLUS_WRITE_ALERT"), None)
    if vendor:
        evidence_ids.extend(vendor.get("evidence_ids") or [])
        sentences.append(
            f"Unapproved vendor session plus write-like alert is joined on this plant; recommended_action={vendor['recommended_action']} (execute=false)."
        )
    safety = next((f for f in forecasts if f["category"] == "SAFETY_BYPASS_AGING"), None)
    if safety:
        evidence_ids.extend(safety.get("evidence_ids") or [])
        sentences.append(
            f"Safety barrier {safety['evidence_ids'][0] if safety.get('evidence_ids') else 'degraded'} is not a live ACTIVE protection — isolate_preview is not a control action."
        )
    unknown = next((f for f in forecasts if f["category"] == "UNKNOWN_PROCESS_CONTEXT"), None)
    if unknown:
        evidence_ids.extend(unknown.get("evidence_ids") or [])
        if unknown.get("abstain_reason"):
            sentences.append(f"Abstain reason: {unknown['abstain_reason']}.")
    restore = next((f for f in forecasts if f["category"] == "RESTORE_TEST_ROT"), None)
    if restore and len(sentences) < 7:
        evidence_ids.extend(restore.get("evidence_ids") or [])
        source_files.add(RECOVERY_PATH)
        sentences.append(
            f"Backup CURRENT with restore-test rot on {restore.get('component')} is not RecoveryReady."
        )
    identity = next((f for f in forecasts if f["category"] == "IDENTITY_CONFLICT_REACHABLE"), None)
    if identity and len(sentences) < 7:
        evidence_ids.extend(identity.get("evidence_ids") or [])
        source_files.add(VULNS_PATH)
        sentences.append(
            f"Identity conflict {identity.get('asset_id')} with reachable OPEN vulnerability is ranked by operational context, not raw CVSS."
        )
    undoc = next((f for f in forecasts if f["category"] == "UNDOCUMENTED_PATH_ON_CRITICAL_UNIT"), None)
    if undoc and len(sentences) < 7:
        evidence_ids.extend(undoc.get("evidence_ids") or [])
        source_files.add(NETWORK_PATH)
        sentences.append("A live undocumented network edge is observed on this HIGH plant; blast radius may be unknown.")

    pad = [
        "This caption is a deterministic template filled from the same CSV joins as diagnostics, safety, recovery, and sessions.",
        "Engines remain authoritative; a later model must not change ACTION_TIERS or the draft packet (ADR-13).",
        "execute remains false — isolate_endpoint is not an executable from this surface.",
    ]
    for extra in pad:
        if len(sentences) >= 6:
            break
        sentences.append(extra)
    sentences = sentences[:8]
    if len(sentences) < 4:
        sentences.extend(pad[: 4 - len(sentences)])

    uniq_evidence = []
    for eid in evidence_ids:
        if eid and eid not in uniq_evidence:
            uniq_evidence.append(eid)

    return {
        "mode": "on",
        "plant_id": plant_id,
        "asset_id": asset_id or (asset.get("asset_id") if asset else None),
        "alert_id": alert_id or (alert.get("alert_id") if alert else None),
        "caption": " ".join(sentences),
        "sentence_count": len(sentences),
        "evidence_ids": uniq_evidence,
        "source_files": sorted(source_files),
        "engine_authoritative": True,
        "explainer": "template_v1",
        "execute": False,
        "note": "Deterministic template — not a model ranker. If a later explainer disagrees, keep the engine packet.",
    }


def twin_preview(
    *,
    scenario_id: str | None = None,
    forecast_id: str | None = None,
    proposed_action: str = "do_nothing",
) -> dict:
    if proposed_action not in TWIN_ACTIONS:
        raise ValueError(f"proposed_action must be one of {sorted(TWIN_ACTIONS)}")

    forecast = get_forecast(forecast_id) if forecast_id else None
    twin_scenario = scenario_id or (forecast.get("twin_scenario_id") if forecast else None) or "nominal"
    cascade = twin_scenario == "cascade_001"
    unknown = bool(
        (forecast and forecast.get("category") == "UNKNOWN_PROCESS_CONTEXT")
        or (forecast and (forecast.get("abstain_reason") or "").startswith("process_context=UNKNOWN"))
    )

    if proposed_action == "isolate_preview":
        if cascade:
            lab = "UNSAFE_ISOLATION"
            detail = "CASCADE isolate_preview at 08:50 MIN_LOAD with unauthorized barrier bypass — unsafe. Recommendation Gate remains DO_NOT_ISOLATE / ABSTAIN."
        elif unknown:
            lab = "INSUFFICIENT_EVIDENCE"
            detail = "process_context=UNKNOWN — isolate_preview cannot be justified. UNKNOWN is not permission."
        else:
            lab = "CONSEQUENCE_SKETCHED"
            detail = "Lab sketch only. No write to PLC, SIS, setpoint, or interlock."
    elif proposed_action == "do_nothing":
        lab = "CONSEQUENCE_SKETCHED" if cascade else "NO_MATERIAL_CHANGE"
        detail = "No plant change. Advisory rehearsal only."
    else:
        lab = "NO_MATERIAL_CHANGE"
        detail = f"{proposed_action} is tier-2 recommendable in policy.py and is not executed from this lab."

    return {
        "mode": "moonshot",
        "banner": BANNER,
        "execute": False,
        "apply_to_plant": False,
        "scenario_id": twin_scenario,
        "forecast_id": forecast_id,
        "forecast": forecast,
        "proposed_action": proposed_action,
        "lab_result": lab,
        "detail": detail,
        "create_approval_packet": {
            "method": "POST",
            "path": "/recommend",
            "execute": False,
            "note": "Existing recommendation gate. Packet remains the engine.",
        },
        "forbidden": [
            "write_plc_logic",
            "modify_sis",
            "change_setpoint",
            "bypass_interlock",
            "isolate_endpoint execute",
        ],
        "note": "Twin is a consequence sketch — not a physics/SIS-certified simulator and not a control action.",
    }
