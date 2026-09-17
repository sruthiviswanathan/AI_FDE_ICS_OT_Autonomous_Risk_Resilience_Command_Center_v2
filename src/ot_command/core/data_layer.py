"""Runtime data abstraction layer (APP-01).

Loads workshop estate sources at runtime and builds derived views.
UI and product API must consume engines/API — not acceptance-test fixtures.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path

from ot_command.repository import jsonl, rows

ROOT = Path(__file__).resolve().parents[3]

# Playbook logical names → repo paths (do not rewrite data/ contradictions).
CANONICAL_SOURCES: dict[str, dict[str, str]] = {
    "plants": {
        "logical_name": "plants.csv",
        "path": "data/reference/plants.csv",
        "format": "csv",
        "grain": "plant_id",
    },
    "assets": {
        "logical_name": "assets.csv",
        "path": "data/raw/assets.csv",
        "format": "csv",
        "grain": "asset_id",
    },
    "telemetry": {
        "logical_name": "telemetry.jsonl",
        "path": "data/telemetry/tag_telemetry.jsonl",
        "format": "jsonl",
        "grain": "event_id",
    },
    "vulnerabilities": {
        "logical_name": "vulnerabilities.csv",
        "path": "data/raw/vulnerabilities.csv",
        "format": "csv",
        "grain": "vuln_id",
    },
    "safety_barriers": {
        "logical_name": "safety_barriers.csv",
        "path": "data/raw/safety_barriers.csv",
        "format": "csv",
        "grain": "barrier_id",
    },
    "recovery_readiness": {
        "logical_name": "recovery_readiness.csv",
        "path": "data/raw/recovery_readiness.csv",
        "format": "csv",
        "grain": "plant_id+component",
    },
    "vendor_sessions": {
        "logical_name": "vendor_sessions.csv",
        "path": "data/raw/remote_access_sessions.csv",
        "format": "csv",
        "grain": "session_id",
    },
    "cyber_alerts": {
        "logical_name": "cyber_alerts.csv",
        "path": "data/raw/cyber_alerts.csv",
        "format": "csv",
        "grain": "alert_id",
    },
}


def _resolve_path(rel: str) -> Path:
    override = __import__("os").environ.get("OT_DATA_ROOT")
    base = Path(override) if override else ROOT
    return base / rel


def source_path(key: str) -> str:
    return CANONICAL_SOURCES[key]["path"]


def clear_cache() -> None:
    """Drop cached raw/derived views (tests or hot reload)."""
    for fn in (
        load_plants,
        load_assets,
        load_telemetry,
        load_vulnerabilities,
        load_safety_barriers,
        load_recovery_readiness,
        load_vendor_sessions,
        load_cyber_alerts,
        derived_plants_by_id,
        derived_assets_by_id,
        derived_assets_by_plant,
        derived_alerts_by_id,
        derived_alerts_by_asset,
        derived_alerts_by_plant,
        derived_vulnerabilities,
        derived_safety_barriers_by_unit,
        derived_degraded_barriers_by_unit,
        derived_recovery_by_plant,
        derived_vendor_sessions_by_asset,
        derived_vendor_session_anomalies,
        derived_telemetry_quality_keys,
    ):
        fn.cache_clear()


@lru_cache(maxsize=1)
def load_plants() -> tuple[dict, ...]:
    return tuple(rows(source_path("plants")))


@lru_cache(maxsize=1)
def load_assets() -> tuple[dict, ...]:
    return tuple(rows(source_path("assets")))


@lru_cache(maxsize=1)
def load_cyber_alerts() -> tuple[dict, ...]:
    return tuple(rows(source_path("cyber_alerts")))


@lru_cache(maxsize=1)
def load_telemetry() -> tuple[dict, ...]:
    return tuple(jsonl(source_path("telemetry")))


@lru_cache(maxsize=1)
def load_vulnerabilities() -> tuple[dict, ...]:
    return tuple(rows(source_path("vulnerabilities")))


@lru_cache(maxsize=1)
def load_safety_barriers() -> tuple[dict, ...]:
    return tuple(rows(source_path("safety_barriers")))


@lru_cache(maxsize=1)
def load_recovery_readiness() -> tuple[dict, ...]:
    return tuple(rows(source_path("recovery_readiness")))


@lru_cache(maxsize=1)
def load_vendor_sessions() -> tuple[dict, ...]:
    return tuple(rows(source_path("vendor_sessions")))


@lru_cache(maxsize=1)
def derived_plants_by_id() -> dict[str, dict]:
    return {r["plant_id"]: dict(r) for r in load_plants()}


@lru_cache(maxsize=1)
def derived_assets_by_id() -> dict[str, dict]:
    return {r["asset_id"]: dict(r) for r in load_assets()}


@lru_cache(maxsize=1)
def derived_assets_by_plant() -> dict[str, list[dict]]:
    by_plant: dict[str, list[dict]] = defaultdict(list)
    for row in load_assets():
        by_plant[row["plant_id"]].append(dict(row))
    for plant_id in by_plant:
        by_plant[plant_id].sort(key=lambda r: r["asset_id"])
    return dict(by_plant)


@lru_cache(maxsize=1)
def derived_alerts_by_id() -> dict[str, dict]:
    return {r["alert_id"]: dict(r) for r in load_cyber_alerts()}


@lru_cache(maxsize=1)
def derived_alerts_by_asset() -> dict[str, list[dict]]:
    by_asset: dict[str, list[dict]] = defaultdict(list)
    for row in load_cyber_alerts():
        by_asset[row["asset_id"]].append(dict(row))
    for asset_id in by_asset:
        by_asset[asset_id].sort(key=lambda r: r["alert_id"], reverse=True)
    return dict(by_asset)


@lru_cache(maxsize=1)
def derived_alerts_by_plant() -> dict[str, list[dict]]:
    by_plant: dict[str, list[dict]] = defaultdict(list)
    for row in load_cyber_alerts():
        by_plant[row["plant_id"]].append(dict(row))
    for plant_id in by_plant:
        by_plant[plant_id].sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return dict(by_plant)


def _asset_state_conflict(asset: dict) -> bool:
    return asset["registered_state"] == "ACTIVE" and asset["observed_state"] in {"OFFLINE", "UNSEEN"}


def _barrier_degraded(barrier: dict) -> bool:
    return barrier["state"] != "ACTIVE" or barrier.get("bypass_authorized", "NO") != "NO"


def _severity_at_least(severity: str, minimum: str | None) -> bool:
    if not minimum:
        return True
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sev = severity.upper()
    floor = minimum.upper()
    return order.get(sev, 99) <= order.get(floor, 99)


def _alert_summary_fields(alert: dict) -> dict:
    return {
        "alert_id": alert["alert_id"],
        "asset_id": alert["asset_id"],
        "severity": alert.get("severity", ""),
        "type": alert.get("type", ""),
        "timestamp": alert.get("timestamp", ""),
        "soc_status": alert.get("soc_status", ""),
        "process_context": alert.get("process_context", ""),
    }


def _pick_top_alerts(alerts: list[dict], limit: int) -> list[dict]:
    candidates = [
        a
        for a in alerts
        if a.get("severity", "").upper() in {"HIGH", "CRITICAL"}
        and a.get("soc_status", "").upper() in {"OPEN", "TRIAGED"}
    ]
    candidates.sort(key=lambda a: a.get("timestamp", ""), reverse=True)
    return [_alert_summary_fields(a) for a in candidates[:limit]]


def _count_by_field(rows: list[dict], field: str) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in rows:
        counts[row.get(field, "UNKNOWN") or "UNKNOWN"] += 1
    return dict(sorted(counts.items()))


def _top_assets_by_alerts(plant_id: str, assets: list[dict], *, limit: int = 10) -> list[dict]:
    by_asset = derived_alerts_by_asset()
    ranked: list[dict] = []
    for asset in assets:
        aid = asset["asset_id"]
        alert_count = len(by_asset.get(aid, []))
        if alert_count > 0:
            ranked.append({"asset_id": aid, "alert_count": alert_count})
    ranked.sort(key=lambda r: (-r["alert_count"], r["asset_id"]))
    return ranked[:limit]


def _estate_asset_status_summary() -> dict:
    assets = load_assets()
    by_registered = _count_by_field(list(assets), "registered_state")
    by_observed = _count_by_field(list(assets), "observed_state")
    conflicts = sum(1 for a in assets if _asset_state_conflict(a))
    pairs: dict[str, int] = defaultdict(int)
    for a in assets:
        key = f"{a['registered_state']}/{a['observed_state']}"
        pairs[key] += 1
    top_pairs = sorted(pairs.items(), key=lambda x: (-x[1], x[0]))[:12]
    return {
        "total_assets": len(assets),
        "by_registered_state": by_registered,
        "by_observed_state": by_observed,
        "state_conflicts": conflicts,
        "registered_observed_pairs": [{"pair": k, "count": v} for k, v in top_pairs],
    }


def _degraded_unit_count_for_plant(plant_id: str) -> int:
    units: set[str] = set()
    for barrier in load_safety_barriers():
        if barrier["plant_id"] == plant_id and _barrier_degraded(barrier):
            units.add(barrier["unit_id"])
    return len(units)


_ELEVATION_RULE_TEXT = (
    "elevated when any of: asset_state_conflicts>0, safety_degraded_units>0, "
    "recovery_stale>0, or alerts_high_critical_open>0 (HIGH/CRITICAL + OPEN/TRIAGED + process_context≠UNKNOWN)"
)

_POSTURE_MOTTO = "cyber ≠ operational ≠ safety ≠ recovery — composite OK only when all layers are OK"

_LAYER_OK = "ok"
_LAYER_AMBER = "amber"
_LAYER_RED = "red"


def _layer(status: str, reason: str, *, count: int = 0) -> dict:
    return {"status": status, "reason": reason, "count": count}


def _composite_posture(*statuses: str) -> str:
    if _LAYER_RED in statuses:
        return _LAYER_RED
    if _LAYER_AMBER in statuses:
        return _LAYER_AMBER
    return _LAYER_OK


def _safety_barrier_flags_for_plant(plant_id: str) -> tuple[int, int]:
    """Returns (degraded_units, bypass_authorized_or_unknown_barriers)."""
    units: set[str] = set()
    bypass_flags = 0
    for barrier in load_safety_barriers():
        if barrier["plant_id"] != plant_id:
            continue
        if _barrier_degraded(barrier):
            units.add(barrier["unit_id"])
        if barrier.get("bypass_authorized", "NO") in {"YES", "UNKNOWN"}:
            bypass_flags += 1
    return len(units), bypass_flags


def _compute_plant_posture_layers(
    plant_id: str,
    assets: list[dict],
    alerts: list[dict],
    recovery_rows: list[dict],
) -> tuple[dict, str]:
    """Five-layer posture — red on any layer blocks composite OK (playbook: cyber ≠ ops ≠ safety ≠ recovery)."""
    alerts_hc = [a for a in alerts if a.get("severity", "").upper() in {"HIGH", "CRITICAL"}]
    alerts_hc_open = [
        a for a in alerts_hc if a.get("soc_status", "").upper() in {"OPEN", "TRIAGED"}
    ]
    alerts_hc_crit_open = [a for a in alerts_hc_open if a.get("severity", "").upper() == "CRITICAL"]
    hc_degraded = [a for a in alerts_hc_open if a.get("process_context", "") == "DEGRADED"]
    hc_unknown = [a for a in alerts_hc_open if a.get("process_context", "UNKNOWN") == "UNKNOWN"]

    if alerts_hc_crit_open:
        cyber = _layer(
            _LAYER_RED,
            "CRITICAL alerts OPEN/TRIAGED (SOC queue)",
            count=len(alerts_hc_crit_open),
        )
    elif alerts_hc_open:
        cyber = _layer(
            _LAYER_AMBER,
            "HIGH alerts OPEN/TRIAGED (inventory — not contextual rank)",
            count=len(alerts_hc_open),
        )
    else:
        cyber = _layer(_LAYER_OK, "No OPEN/TRIAGED HIGH/CRITICAL alerts")

    if hc_degraded:
        process_ops = _layer(
            _LAYER_RED,
            "HC alerts with DEGRADED process context (ops disagreement signal)",
            count=len(hc_degraded),
        )
    elif hc_unknown:
        process_ops = _layer(
            _LAYER_AMBER,
            "HC alerts with UNKNOWN process context (soc vs ops unresolved)",
            count=len(hc_unknown),
        )
    else:
        process_ops = _layer(_LAYER_OK, "No HC alert process-context conflicts")

    degraded_units, bypass_flags = _safety_barrier_flags_for_plant(plant_id)
    if degraded_units > 0:
        safety = _layer(
            _LAYER_RED,
            "Degraded or unauthorized safety barrier on unit",
            count=degraded_units,
        )
    elif bypass_flags > 0:
        safety = _layer(
            _LAYER_AMBER,
            "Barrier bypass authorized or unknown — verify safety owner",
            count=bypass_flags,
        )
    else:
        safety = _layer(_LAYER_OK, "Safety barriers ACTIVE without bypass flags")

    stale = sum(1 for r in recovery_rows if r.get("backup_status") != "CURRENT")
    runbook_gap = sum(1 for r in recovery_rows if r.get("runbook_status") != "CURRENT")
    dep_gap = sum(1 for r in recovery_rows if r.get("dependency_verified") != "YES")
    if stale > 0 or runbook_gap > 0:
        recovery = _layer(
            _LAYER_RED,
            "Stale backup or runbook gap for recovery component",
            count=stale + runbook_gap,
        )
    elif dep_gap > 0:
        recovery = _layer(
            _LAYER_AMBER,
            "Recovery dependency not verified",
            count=dep_gap,
        )
    else:
        recovery = _layer(_LAYER_OK, "Recovery records current with verified deps")

    conflicts = sum(1 for a in assets if _asset_state_conflict(a))
    if conflicts > 0:
        evidence = _layer(
            _LAYER_RED,
            "Registered vs observed asset state conflict",
            count=conflicts,
        )
    else:
        evidence = _layer(_LAYER_OK, "No asset identity/state conflicts in catalog")

    layers = {
        "cyber_exposure": cyber,
        "process_ops_disagreement": process_ops,
        "safety_posture": safety,
        "recovery_credibility": recovery,
        "evidence_quality": evidence,
    }
    composite = _composite_posture(*(layer["status"] for layer in layers.values()))
    return layers, composite


def estate_by_plant_view(*, include_top_alerts: int = 3, severity_min: str | None = None) -> dict:
    """Per-plant estate aggregates for the Home dashboard (read-only inventory signals)."""
    cap = min(max(include_top_alerts, 0), 10)
    plants_meta = derived_plants_by_id()
    assets_by_plant = derived_assets_by_plant()
    alerts_by_plant = derived_alerts_by_plant()
    recovery_by_plant = derived_recovery_by_plant()

    plant_rows: list[dict] = []
    for plant_id in sorted(plants_meta):
        meta = plants_meta[plant_id]
        assets = assets_by_plant.get(plant_id, [])
        alerts = alerts_by_plant.get(plant_id, [])
        if severity_min:
            alerts = [a for a in alerts if _severity_at_least(a.get("severity", ""), severity_min)]

        asset_conflicts = sum(1 for a in assets if _asset_state_conflict(a))
        recovery_rows = recovery_by_plant.get(plant_id, [])
        recovery_stale = sum(1 for r in recovery_rows if r.get("backup_status") != "CURRENT")
        safety_degraded_units = _degraded_unit_count_for_plant(plant_id)

        alerts_hc = [a for a in alerts if a.get("severity", "").upper() in {"HIGH", "CRITICAL"}]
        alerts_open_triaged = [a for a in alerts if a.get("soc_status", "").upper() in {"OPEN", "TRIAGED"}]
        alerts_hc_open = [
            a
            for a in alerts_hc
            if a.get("soc_status", "").upper() in {"OPEN", "TRIAGED"}
            and a.get("process_context", "UNKNOWN") != "UNKNOWN"
        ]

        elevation_reasons: list[str] = []
        if asset_conflicts > 0:
            elevation_reasons.append("asset_state_conflicts")
        if safety_degraded_units > 0:
            elevation_reasons.append("safety_degraded_units")
        if recovery_stale > 0:
            elevation_reasons.append("recovery_stale")
        if len(alerts_hc_open) > 0:
            elevation_reasons.append("alerts_high_critical_open")

        posture_layers, posture_composite = _compute_plant_posture_layers(
            plant_id, assets, alerts, recovery_rows
        )

        plant_rows.append(
            {
                "plant_id": plant_id,
                "region": meta.get("region", ""),
                "country": meta.get("country", ""),
                "plant_type": meta.get("plant_type", ""),
                "criticality": meta.get("criticality", ""),
                "counts": {
                    "assets": len(assets),
                    "alerts_total": len(alerts),
                    "alerts_high_critical": len(alerts_hc),
                    "alerts_open_or_triaged": len(alerts_open_triaged),
                    "alerts_high_critical_open": len(alerts_hc_open),
                    "asset_state_conflicts": asset_conflicts,
                    "safety_degraded_units": safety_degraded_units,
                    "recovery_stale": recovery_stale,
                },
                "signals": {
                    "elevated": posture_composite != _LAYER_OK,
                    "elevation_reasons": elevation_reasons,
                    "posture_composite": posture_composite,
                },
                "posture_layers": posture_layers,
                "top_alerts": _pick_top_alerts(alerts_by_plant.get(plant_id, []), cap),
                "assets_by_registered_state": _count_by_field(assets, "registered_state"),
                "assets_by_observed_state": _count_by_field(assets, "observed_state"),
                "top_assets_by_alerts": _top_assets_by_alerts(plant_id, assets),
            }
        )

    total_alerts = sum(len(v) for v in alerts_by_plant.values())

    return {
        "provenance": "runtime-derived",
        "freshness": "workshop-static",
        "plant_count": len(plant_rows),
        "total_alerts": total_alerts,
        "asset_status_summary": _estate_asset_status_summary(),
        "plants": plant_rows,
        "methodology": {
            "elevated_rule": _ELEVATION_RULE_TEXT,
            "posture_motto": _POSTURE_MOTTO,
            "posture_composite_rule": (
                "Composite OK only when all five layers are OK. "
                "Any red layer blocks green/OK; amber layers show caution."
            ),
            "not_operational_risk_rank": (
                "Alert counts are inventory signals, not contextual risk rank. Use /risk/contextual for findings."
            ),
        },
    }


def list_plants() -> list[dict]:
    return sorted(derived_plants_by_id().values(), key=lambda r: r["plant_id"])


def list_assets_for_plant(plant_id: str, *, limit: int = 100, q: str | None = None) -> list[dict]:
    assets = derived_assets_by_plant().get(plant_id, [])
    if q:
        prefix = q.strip().upper()
        assets = [a for a in assets if a["asset_id"].upper().startswith(prefix)]
    by_asset = derived_alerts_by_asset()
    enriched = []
    for a in assets[:limit]:
        row = dict(a)
        row["alert_count"] = len(by_asset.get(a["asset_id"], []))
        enriched.append(row)
    return enriched


def list_alerts_for_asset(
    asset_id: str, *, limit: int = 50, severity: str | None = None
) -> list[dict]:
    alerts = list(derived_alerts_by_asset().get(asset_id, []))
    if severity:
        sev = severity.strip().upper()
        alerts = [a for a in alerts if a.get("severity", "").upper() == sev]
    return alerts[:limit]


@lru_cache(maxsize=1)
def derived_vulnerabilities() -> tuple[dict, ...]:
    return load_vulnerabilities()


@lru_cache(maxsize=1)
def derived_safety_barriers_by_unit() -> dict[str, list[dict]]:
    by_unit: dict[str, list[dict]] = defaultdict(list)
    for row in load_safety_barriers():
        by_unit[row["unit_id"]].append(dict(row))
    return dict(by_unit)


@lru_cache(maxsize=1)
def derived_degraded_barriers_by_unit() -> dict[str, list[dict]]:
    by_unit: dict[str, list[dict]] = defaultdict(list)
    for row in load_safety_barriers():
        if row["state"] != "ACTIVE" or row.get("bypass_authorized", "NO") != "NO":
            by_unit[row["unit_id"]].append(dict(row))
    return dict(by_unit)


@lru_cache(maxsize=1)
def derived_recovery_by_plant() -> dict[str, list[dict]]:
    by_plant: dict[str, list[dict]] = defaultdict(list)
    for row in load_recovery_readiness():
        by_plant[row["plant_id"]].append(dict(row))
    return dict(by_plant)


@lru_cache(maxsize=1)
def derived_vendor_sessions_by_asset() -> dict[str, list[dict]]:
    by_asset: dict[str, list[dict]] = defaultdict(list)
    for row in load_vendor_sessions():
        by_asset[row["asset_id"]].append(dict(row))
    return dict(by_asset)


@lru_cache(maxsize=1)
def derived_vendor_session_anomalies() -> list[dict]:
    anomalies: list[dict] = []
    for row in load_vendor_sessions():
        flags = []
        if row.get("approved_window") != "YES":
            flags.append("unapproved_window")
        if row.get("mfa") != "YES":
            flags.append("mfa_not_confirmed")
        if row.get("identity") in (None, "", "unknown"):
            flags.append("unknown_identity")
        if flags:
            item = dict(row)
            item["anomaly_flags"] = flags
            item["provenance"] = {
                "source_path": source_path("vendor_sessions"),
                "record_id": row["session_id"],
                "freshness": "workshop-static",
            }
            anomalies.append(item)
    return anomalies


@lru_cache(maxsize=1)
def derived_telemetry_quality_keys() -> Counter:
    tele = load_telemetry()
    return Counter((x["tag_id"], x["event_time"], str(x["value"]), x["unit"]) for x in tele)


def sources_catalog() -> dict:
    """Introspection for UI/API — canonical sources only."""
    entries = []
    loaders = {
        "plants": load_plants,
        "assets": load_assets,
        "telemetry": load_telemetry,
        "vulnerabilities": load_vulnerabilities,
        "safety_barriers": load_safety_barriers,
        "recovery_readiness": load_recovery_readiness,
        "vendor_sessions": load_vendor_sessions,
        "cyber_alerts": load_cyber_alerts,
    }
    for key, meta in CANONICAL_SOURCES.items():
        path = meta["path"]
        resolved = _resolve_path(path)
        count = len(loaders[key]())
        entries.append(
            {
                "source_key": key,
                "logical_name": meta["logical_name"],
                "path": path,
                "format": meta["format"],
                "grain": meta["grain"],
                "record_count": count,
                "exists": resolved.is_file(),
                "freshness": "workshop-static",
                "fixture_dependent": False,
            }
        )
    return {
        "mode": "runtime-derived",
        "note": "UI must not depend on acceptance-test fixtures; load canonical estate files only.",
        "sources": entries,
    }


def estate_derived_view() -> dict:
    """Live derived estate summary built from canonical sources at runtime."""
    assets = load_assets()
    tele = load_telemetry()
    barriers = load_safety_barriers()
    recovery = load_recovery_readiness()
    sessions = load_vendor_sessions()
    packet_keys = derived_telemetry_quality_keys()

    alias_collisions = 0  # aliases are supplementary; counted in identity engine

    return {
        "provenance": "runtime-derived",
        "freshness": "workshop-static",
        "counts": {
            "assets": len(assets),
            "telemetry_events": len(tele),
            "vulnerabilities": len(load_vulnerabilities()),
            "safety_barriers": len(barriers),
            "recovery_records": len(recovery),
            "vendor_sessions": len(sessions),
        },
        "derived_signals": {
            "asset_state_conflicts": sum(
                1
                for a in assets
                if a["registered_state"] == "ACTIVE" and a["observed_state"] in {"OFFLINE", "UNSEEN"}
            ),
            "telemetry_bad_or_uncertain": sum(1 for x in tele if x["quality"] != "GOOD"),
            "duplicate_telemetry_packets": sum(v - 1 for v in packet_keys.values() if v > 1),
            "safety_bypassed_or_degraded": sum(s["state"] != "ACTIVE" for s in barriers),
            "recovery_stale_or_unknown_backup": sum(x["backup_status"] != "CURRENT" for x in recovery),
            "unapproved_vendor_sessions": sum(x["approved_window"] != "YES" for x in sessions),
            "vendor_sessions_without_confirmed_mfa": sum(x["mfa"] != "YES" for x in sessions),
            "vendor_session_anomalies": len(derived_vendor_session_anomalies()),
        },
        "alias_collisions_note": "Alias collisions require asset_aliases.csv via identity engine",
        "alias_collisions_placeholder": alias_collisions,
    }
