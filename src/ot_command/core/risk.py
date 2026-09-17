"""Contextual operational risk (FR-003, ADR-03). CVSS is input, not the sort key."""

from __future__ import annotations

from functools import lru_cache

from ot_command.core.data_layer import (
    derived_assets_by_id,
    derived_degraded_barriers_by_unit,
    derived_recovery_by_plant,
    derived_vulnerabilities,
    source_path,
)

VULNERABILITIES_PATH = source_path("vulnerabilities")
ASSETS_PATH = source_path("assets")
RECOVERY_PATH = source_path("recovery_readiness")
SAFETY_PATH = source_path("safety_barriers")

CRITICALITY_WEIGHT = {"CRITICAL": 40, "HIGH": 30, "MEDIUM": 20, "LOW": 10, "UNKNOWN": 5}
REACHABILITY_WEIGHT = {"YES": 35, "UNKNOWN": 12, "NO": 5}
COMPENSATING_ADJ = {
    "NONE": 0,
    "ALLOWLIST": -3,
    "MONITORED": -2,
    "SEGMENTED": -2,
    "UNKNOWN": 0,
}
CVSS_WEIGHT = 2.0


@lru_cache(maxsize=1)
def _assets_by_id() -> dict[str, dict]:
    return derived_assets_by_id()


@lru_cache(maxsize=1)
def _recovery_by_plant() -> dict[str, list[dict]]:
    return derived_recovery_by_plant()


@lru_cache(maxsize=1)
def _degraded_barriers_by_unit() -> dict[str, list[dict]]:
    return derived_degraded_barriers_by_unit()


def _normalize_finding(finding: dict) -> dict:
    row = dict(finding)
    asset_id = row.get("asset_id")
    asset = _assets_by_id().get(asset_id or "")
    if asset:
        row.setdefault("criticality", asset["criticality"])
        row.setdefault("plant_id", asset["plant_id"])
        row.setdefault("observed_state", asset["observed_state"])
    row["reachable"] = row.get("reachable") or row.get("network_reachable") or "UNKNOWN"
    row.setdefault("compensating_control", row.get("compensating_control", "UNKNOWN"))
    return row


def _recovery_penalty(plant_id: str | None) -> tuple[float, dict]:
    if not plant_id:
        return 0.0, {"status": "UNKNOWN", "note": "plant_id missing"}
    rows_for_plant = _recovery_by_plant().get(plant_id, [])
    if not rows_for_plant:
        return 5.0, {"status": "UNKNOWN", "note": "no recovery rows for plant"}
    weak = [
        r
        for r in rows_for_plant
        if r["backup_status"] == "CURRENT"
        and (
            int(r["last_restore_test_days"]) > 180
            or r["runbook_status"] != "CURRENT"
            or r["dependency_verified"] != "YES"
            or r["manual_fallback"] not in {"YES", "CURRENT"}
        )
    ]
    if weak:
        return 8.0, {
            "status": "DEGRADED",
            "components": [r["component"] for r in weak[:3]],
            "note": "CURRENT backup alone is not RecoveryReady (ADR-05)",
        }
    return 0.0, {"status": "ACCEPTABLE", "note": "no weak CURRENT-only rows detected in sample"}


def _safety_adjustment(finding: dict) -> tuple[float, dict]:
    barrier_text = str(finding.get("barrier", "")).upper()
    unit_id = finding.get("unit")
    degraded = _degraded_barriers_by_unit().get(unit_id or "", [])
    score = 0.0
    evidence = []
    if "BYPASSED" in barrier_text:
        score += 15.0
        evidence.append({"source": "fixture", "note": finding.get("barrier")})
    for barrier in degraded:
        score += 10.0
        evidence.append(
            {
                "source_path": SAFETY_PATH,
                "record_id": barrier["barrier_id"],
                "state": barrier["state"],
                "bypass_authorized": barrier.get("bypass_authorized"),
            }
        )
        break
    return score, {"adjustment": score, "evidence": evidence}


def _score_finding(finding: dict) -> tuple[float, dict]:
    normalized = _normalize_finding(finding)
    criticality = normalized.get("criticality", "UNKNOWN")
    reachable = normalized.get("reachable", "UNKNOWN")
    cvss = float(normalized.get("cvss", 0))

    crit_pts = CRITICALITY_WEIGHT.get(criticality, 5)
    reach_pts = REACHABILITY_WEIGHT.get(reachable, 12)
    cvss_pts = cvss * CVSS_WEIGHT
    comp_pts = COMPENSATING_ADJ.get(normalized.get("compensating_control", "UNKNOWN"), 0)
    safety_pts, safety_detail = _safety_adjustment(normalized)
    recovery_pts, recovery_detail = _recovery_penalty(normalized.get("plant_id"))

    total = crit_pts + reach_pts + cvss_pts + comp_pts + safety_pts + recovery_pts
    breakdown = {
        "process_criticality": {"value": criticality, "points": crit_pts},
        "reachability": {"value": reachable, "points": reach_pts},
        "cvss_input": {"value": cvss, "points": cvss_pts, "note": "input only — not sort key"},
        "compensating_control": {
            "value": normalized.get("compensating_control"),
            "points": comp_pts,
        },
        "safety": {**safety_detail, "points": safety_pts},
        "recovery": {**recovery_detail, "points": recovery_pts},
        "contextual_score": round(total, 2),
    }
    evidence = [
        {"factor": "reachability", "value": reachable},
        {"factor": "process_criticality", "value": criticality},
        {"factor": "cvss", "value": cvss},
    ]
    if safety_detail.get("evidence"):
        evidence.extend(safety_detail["evidence"])
    return total, {"factor_breakdown": breakdown, "evidence": evidence}


def contextual_rank(findings: list, *, context: dict | None = None) -> list:
    del context  # reserved for future scoped ranking; engines remain deterministic
    scored = []
    for finding in findings:
        total, meta = _score_finding(finding)
        row = dict(finding)
        row.update(meta)
        row["_sort_score"] = total
        scored.append(row)
    scored.sort(key=lambda x: x["_sort_score"], reverse=True)
    for row in scored:
        row.pop("_sort_score", None)
    return scored


@lru_cache(maxsize=1)
def _all_vulnerabilities() -> tuple[dict, ...]:
    return derived_vulnerabilities()


def rank_corpus(
    *,
    limit: int = 20,
    asset_id: str | None = None,
    plant_id: str | None = None,
) -> dict:
    findings = [dict(row) for row in _all_vulnerabilities()]
    scope = {
        "requested": {"asset_id": asset_id, "plant_id": plant_id},
        "effective": {"asset_id": asset_id, "plant_id": plant_id},
    }
    if asset_id:
        findings = [f for f in findings if f.get("asset_id") == asset_id]
    elif plant_id:
        assets_in_plant = {
            aid for aid, asset in _assets_by_id().items() if asset.get("plant_id") == plant_id
        }
        findings = [f for f in findings if f.get("asset_id") in assets_in_plant]
    ranked = contextual_rank(findings)
    return {
        "count": len(ranked),
        "limit": limit,
        "rankings": ranked[:limit],
        "scope": scope,
        "method": "contextual_operational_risk",
        "note": "legacy_rank remains CVSS-only for contrast; LLM must not re-rank",
    }
