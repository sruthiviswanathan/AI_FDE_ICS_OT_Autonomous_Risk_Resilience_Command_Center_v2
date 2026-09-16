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
        load_assets,
        load_telemetry,
        load_vulnerabilities,
        load_safety_barriers,
        load_recovery_readiness,
        load_vendor_sessions,
        derived_assets_by_id,
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
def load_assets() -> tuple[dict, ...]:
    return tuple(rows(source_path("assets")))


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
def derived_assets_by_id() -> dict[str, dict]:
    return {r["asset_id"]: dict(r) for r in load_assets()}


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
        "assets": load_assets,
        "telemetry": load_telemetry,
        "vulnerabilities": load_vulnerabilities,
        "safety_barriers": load_safety_barriers,
        "recovery_readiness": load_recovery_readiness,
        "vendor_sessions": load_vendor_sessions,
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
