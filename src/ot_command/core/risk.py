"""Contextual operational risk (ADR-03, FR-003). CVSS is an input, not the sort key."""

from __future__ import annotations

from typing import Any

from ..repository import rows

VULNS_PATH = "data/raw/vulnerabilities.csv"
ASSETS_PATH = "data/raw/assets.csv"
TAGS_PATH = "data/reference/tags.csv"
UNITS_PATH = "data/raw/process_units.csv"
BARRIERS_PATH = "data/raw/safety_barriers.csv"
RECOVERY_PATH = "data/raw/recovery_readiness.csv"

CRIT_ORD = {"CRITICAL": 3, "HIGH": 2, "MEDIUM": 1, "LOW": 0}
REACH_ORD = {"YES": 2, "UNKNOWN": 1, "NO": 0}
REDUCING_CONTROLS = {"SEGMENTED", "ALLOWLIST", "MONITORED"}
DEGRADED_SAFETY = {"BYPASSED", "DEGRADED"}

_CACHE: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    vulns = {r["finding_id"]: r for r in rows(VULNS_PATH)}
    assets = {r["asset_id"]: r for r in rows(ASSETS_PATH)}
    units = {r["unit_id"]: r for r in rows(UNITS_PATH)}
    tags_by_asset: dict[str, list[dict]] = {}
    for tag in rows(TAGS_PATH):
        tags_by_asset.setdefault(tag["asset_id"], []).append(tag)
    barriers_by_unit: dict[str, list[dict]] = {}
    for bar in rows(BARRIERS_PATH):
        barriers_by_unit.setdefault(bar["unit_id"], []).append(bar)
    recovery_by_plant: dict[str, list[dict]] = {}
    for rec in rows(RECOVERY_PATH):
        recovery_by_plant.setdefault(rec["plant_id"], []).append(rec)
    _CACHE = {
        "vulns": vulns,
        "assets": assets,
        "units": units,
        "tags_by_asset": tags_by_asset,
        "barriers_by_unit": barriers_by_unit,
        "recovery_by_plant": recovery_by_plant,
    }
    return _CACHE


def _norm_reach(value: Any) -> str:
    if value in (True, "YES", "yes"):
        return "YES"
    if value in (False, "NO", "no"):
        return "NO"
    if value in (None, "", "UNKNOWN"):
        return "UNKNOWN"
    return str(value).upper() if str(value).upper() in REACH_ORD else "UNKNOWN"


def _norm_crit(value: Any) -> str:
    if not value:
        return "UNKNOWN"
    text = str(value).upper()
    return text if text in CRIT_ORD else "UNKNOWN"


def _from_vuln_row(finding: dict) -> dict:
    data = _load()
    fid = finding.get("finding_id") or finding.get("id")
    row = data["vulns"].get(fid) if fid else None
    if not row:
        return {}
    return {
        "finding_id": row["finding_id"],
        "asset_id": row["asset_id"],
        "cvss": float(row["cvss"]),
        "network_reachable": row["network_reachable"],
        "compensating_control": row["compensating_control"],
        "severity": row["severity"],
        "status": row["status"],
    }


def rank_factors(finding: dict) -> dict:
    data = _load()
    merged = {**_from_vuln_row(finding), **{k: v for k, v in finding.items() if v is not None and v != ""}}
    asset_id = merged.get("asset_id")
    asset = data["assets"].get(asset_id) if asset_id else None
    reach = _norm_reach(
        merged.get("reachable") if merged.get("reachable") is not None else merged.get("network_reachable")
    )
    asset_crit = _norm_crit(merged.get("criticality") or (asset["criticality"] if asset else None))
    tags = data["tags_by_asset"].get(asset_id or "", [])
    unit_ids = []
    if merged.get("unit"):
        unit_ids.append(merged["unit"])
    unit_ids.extend(t["unit_id"] for t in tags if t.get("unit_id"))
    unit_ids = list(dict.fromkeys(unit_ids))
    process_join_missing = not unit_ids
    unit_crits = []
    safe_states = []
    for uid in unit_ids:
        unit = data["units"].get(uid)
        if unit:
            unit_crits.append(_norm_crit(unit.get("production_criticality")))
            safe_states.append(unit.get("safe_state"))
    if merged.get("safe_state"):
        safe_states.append(merged["safe_state"])
    process_criticality = asset_crit
    for crit in unit_crits:
        if CRIT_ORD.get(crit, -1) > CRIT_ORD.get(process_criticality, -1):
            process_criticality = crit
    barriers = []
    for uid in unit_ids:
        barriers.extend(data["barriers_by_unit"].get(uid, []))
    barrier_hint = str(merged.get("barrier") or "")
    states = [b.get("state") for b in barriers]
    if "BYPASSED" in barrier_hint.upper():
        states.append("BYPASSED")
    if any(s in DEGRADED_SAFETY for s in states):
        safety_state = next(s for s in states if s in DEGRADED_SAFETY)
        safety_pressure = 2
    elif states:
        safety_state = states[0]
        safety_pressure = 0
    else:
        safety_state = "UNKNOWN"
        safety_pressure = 1
    control = merged.get("compensating_control") or "UNKNOWN"
    control_credit = 1 if str(control).upper() in REDUCING_CONTROLS else 0
    plant_id = asset["plant_id"] if asset else merged.get("plant_id")
    rec_rows = data["recovery_by_plant"].get(plant_id or "", [])
    recovery_ready = False
    recovery_reason = "join_missing"
    if rec_rows:
        blockers = []
        for rec in rec_rows:
            if rec.get("runbook_status") != "CURRENT" or rec.get("dependency_verified") != "YES":
                blockers.append(f"{rec.get('component')}:runbook/deps")
            if rec.get("backup_status") != "CURRENT":
                blockers.append(f"{rec.get('component')}:backup")
        recovery_reason = (
            ";".join(blockers[:6])
            if blockers
            else "ADR-05 CURRENT backup is not RecoveryReady; ENH-06 owns the public predicate"
        )
    elif merged.get("recovery_ready") is False:
        recovery_reason = "supplied_false"
    recovery_gap = 1 if recovery_ready is not True else 0
    freshness = merged.get("evidence_freshness") or "UNKNOWN"
    factors = {
        "reachability": reach,
        "process_criticality": process_criticality,
        "process criticality": process_criticality,
        "safety": {
            "barrier_state": safety_state,
            "safe_state": safe_states[0] if safe_states else None,
            "pressure": safety_pressure,
        },
        "controls": {
            "compensating_control": control,
            "reducing": bool(control_credit),
        },
        "recovery": {
            "recovery_ready": recovery_ready,
            "reason": recovery_reason,
            "gap": recovery_gap,
        },
        "evidence_freshness": freshness,
        "cvss": float(merged["cvss"]) if merged.get("cvss") not in (None, "") else None,
        "cvss_is_sort_key": False,
    }
    uncertainty = {
        "process_join_missing": process_join_missing,
        "recovery_join_missing": not rec_rows,
        "evidence_freshness": freshness,
        "safety_unknown": safety_state == "UNKNOWN",
    }
    return {
        **factors,
        "uncertainty": uncertainty,
        "asset_id": asset_id,
        "unit_ids": unit_ids,
        "finding_id": merged.get("finding_id") or merged.get("id"),
    }


def _sort_tuple(factors: dict) -> tuple:
    reach = REACH_ORD.get(factors.get("reachability"), 0)
    crit = CRIT_ORD.get(factors.get("process_criticality"), 0)
    safety = (factors.get("safety") or {}).get("pressure") or 0
    control_credit = 1 if (factors.get("controls") or {}).get("reducing") else 0
    recovery_gap = (factors.get("recovery") or {}).get("gap") or 0
    return (-reach, -crit, -safety, control_credit, -recovery_gap)


def contextual_rank(findings: list[dict]) -> list[dict]:
    ranked = []
    for finding in findings:
        factors = rank_factors(finding)
        fid = finding.get("id") or finding.get("finding_id") or factors.get("finding_id")
        row = dict(finding)
        row["id"] = fid
        row["finding_id"] = finding.get("finding_id") or fid
        row["factors"] = factors
        row["uncertainty"] = factors.get("uncertainty")
        row["_sort"] = _sort_tuple(factors)
        ranked.append(row)
    ranked.sort(key=lambda r: (r["_sort"], str(r.get("id") or "")))
    for row in ranked:
        row.pop("_sort", None)
    return ranked


def rank_all(limit: int = 50) -> dict:
    data = _load()
    findings = list(data["vulns"].values())
    ordered = contextual_rank(findings)
    cap = min(max(int(limit), 1), 200)
    return {
        "order": "contextual",
        "sort_key": "reachability,process_criticality,safety,controls,recovery",
        "cvss_is_sort_key": False,
        "llm_rerank": False,
        "returned": min(len(ordered), cap),
        "available": len(ordered),
        "items": ordered[:cap],
        "uncertainty": {"estate_wide": True, "process_join_missing_possible": True},
    }
