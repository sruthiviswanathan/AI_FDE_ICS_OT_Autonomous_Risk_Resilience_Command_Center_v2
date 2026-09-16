"""Recovery readiness (ADR-05, FR-005). CURRENT backup is not RecoveryReady. No live restore."""

from __future__ import annotations

from typing import Any

from ..repository import rows

RECOVERY_PATH = "data/raw/recovery_readiness.csv"
UNITS_PATH = "data/raw/process_units.csv"
DEPS_PATH = "data/raw/process_dependencies.csv"
TRANSFORM = "enh-06-recovery.1"
AS_OF = "2026-09-10T00:00:00Z"

_CACHE: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    recs = rows(RECOVERY_PATH)
    by_plant: dict[str, list[dict]] = {}
    for rec in recs:
        by_plant.setdefault(rec["plant_id"], []).append(rec)
    unit_to_plant = {r["unit_id"]: r["plant_id"] for r in rows(UNITS_PATH)}
    deps_by_plant: dict[str, list[dict]] = {}
    for dep in rows(DEPS_PATH):
        deps_by_plant.setdefault(dep["plant_id"], []).append(dep)
    _CACHE = {"by_plant": by_plant, "unit_to_plant": unit_to_plant, "deps_by_plant": deps_by_plant}
    return _CACHE


def _days(record: dict) -> int | None:
    raw = record.get("last_restore_test_days")
    if raw in (None, ""):
        return None
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None


def recovery_blockers(record: dict) -> list[str]:
    blockers: list[str] = []
    backup = record.get("backup_status")
    if backup != "CURRENT":
        blockers.append(f"backup_status={backup or 'missing'} (CURRENT backup is not sufficient even when set)")
    else:
        blockers.append("backup CURRENT is not RecoveryReady")
    days = _days(record)
    if days is None:
        blockers.append("restore test evidence missing")
    else:
        blockers.append(
            f"restore test {days} days — freshness SLA OPEN-006/022 not signed; not acceptable"
        )
    runbook = record.get("runbook_status")
    if runbook != "CURRENT":
        blockers.append(f"runbook {runbook or 'missing'}")
    dep = record.get("dependency_verified")
    if dep != "YES":
        blockers.append(f"dependencies {dep or 'missing'}")
    fallback = record.get("manual_fallback")
    if fallback in {"LIMITED", "NO", None, ""}:
        blockers.append(f"manual fallback {fallback or 'missing'}")
    return blockers


def recovery_ready(record: dict) -> bool:
    """True only with CURRENT backup, acceptable restore freshness, CURRENT runbook, deps YES.

    Restore-test day cutoff is OPEN-006/022, so freshness is never 'acceptable' here.
    """
    days = _days(record)
    restore_evidence = days is not None
    freshness_acceptable = False
    return bool(
        record.get("backup_status") == "CURRENT"
        and restore_evidence
        and freshness_acceptable
        and record.get("runbook_status") == "CURRENT"
        and record.get("dependency_verified") == "YES"
    )


def recovery_view(record: dict) -> dict:
    ready = recovery_ready(record)
    blockers = [] if ready else recovery_blockers(record)
    return {
        "plant_id": record.get("plant_id"),
        "component": record.get("component"),
        "rto_hours": record.get("rto_hours"),
        "backup_status": record.get("backup_status"),
        "last_restore_test_days": _days(record),
        "runbook_status": record.get("runbook_status"),
        "dependency_verified": record.get("dependency_verified"),
        "manual_fallback": record.get("manual_fallback"),
        "recovery_ready": ready,
        "blockers": blockers,
        "live_restore_orchestration": False,
        "provenance": {
            "source_system": "ENGINE",
            "source_path": RECOVERY_PATH,
            "extracted_at": AS_OF,
            "transform_version": TRANSFORM,
            "confidence": 0.5,
        },
    }


def _resolve_plant(site_or_unit: str) -> str | None:
    data = _load()
    if site_or_unit in data["by_plant"]:
        return site_or_unit
    return data["unit_to_plant"].get(site_or_unit)


def plant_recovery(plant_id: str) -> dict:
    data = _load()
    resolved = _resolve_plant(plant_id)
    if resolved is None:
        raise KeyError(plant_id)
    components = [recovery_view(rec) for rec in data["by_plant"].get(resolved, [])]
    dep_blockers = [
        f"{d.get('upstream_unit')}->{d.get('downstream_unit')} {d.get('dependency_type')}"
        for d in data["deps_by_plant"].get(resolved, [])
        if d.get("critical") == "YES"
    ]
    return {
        "plant_id": resolved,
        "requested": plant_id,
        "recovery_ready": False,
        "components": components,
        "process_dependency_blockers": dep_blockers,
        "note": "DEPENDS_ON edges are not a substitute for restore-test evidence. No live restore.",
        "freshness_sla": "OPEN-006/022",
    }
