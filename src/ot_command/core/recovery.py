"""Recovery readiness predicate (FR-005, ADR-05). CURRENT backup ≠ RecoveryReady."""

from __future__ import annotations

from functools import lru_cache

from ot_command.core.data_layer import load_recovery_readiness, source_path

RECOVERY_PATH = source_path("recovery_readiness")

# Workshop threshold — plant SLA days remain OPEN-006/022; absence ⇒ not ready.
RESTORE_TEST_MAX_DAYS = 180


def _provenance(record_id: str) -> dict:
    return {
        "source_path": RECOVERY_PATH,
        "record_id": record_id,
        "grain": "plant_id+component",
        "claim_type": "registered",
        "freshness": "workshop-static",
    }


@lru_cache(maxsize=1)
def _all_records() -> tuple[dict, ...]:
    return load_recovery_readiness()


def _record_key(plant_id: str, component: str) -> str:
    return f"{plant_id}:{component}"


def _find_record(plant_id: str, component: str) -> dict | None:
    for row in _all_records():
        if row["plant_id"] == plant_id and row["component"] == component:
            return dict(row)
    return None


def _evaluate_record(record: dict) -> tuple[bool, list[str]]:
    blockers: list[str] = []

    if record.get("backup_status") != "CURRENT":
        blockers.append(f"backup_status={record.get('backup_status', 'MISSING')}")

    restore_raw = record.get("last_restore_test_days")
    if restore_raw in (None, ""):
        blockers.append("restore_test_missing")
    else:
        restore_days = int(restore_raw)
        if restore_days > RESTORE_TEST_MAX_DAYS:
            blockers.append(f"restore_test_stale_{restore_days}d")

    if record.get("runbook_status") != "CURRENT":
        blockers.append(f"runbook_{str(record.get('runbook_status', 'MISSING')).lower()}")

    if record.get("dependency_verified") != "YES":
        blockers.append(f"dependency_{str(record.get('dependency_verified', 'MISSING')).lower()}")

    if record.get("manual_fallback") not in {"YES"}:
        blockers.append(f"manual_fallback_{str(record.get('manual_fallback', 'MISSING')).lower()}")

    return len(blockers) == 0, blockers


def recovery_ready(
    *,
    plant_id: str | None = None,
    component: str | None = None,
    backup_status: str | None = None,
    record: dict | None = None,
) -> bool:
    if record is None:
        if backup_status == "CURRENT" and plant_id is None and component is None:
            return False
        if plant_id and component:
            record = _find_record(plant_id, component)
            if record is None:
                return False
        else:
            return False

    rec = dict(record)
    if backup_status is not None:
        rec["backup_status"] = backup_status

    ready, _ = _evaluate_record(rec)
    return ready


def recovery_blockers(
    *,
    plant_id: str | None = None,
    component: str | None = None,
    record: dict | None = None,
) -> list[str]:
    rec = dict(record) if record else None
    if rec is None and plant_id and component:
        rec = _find_record(plant_id, component)
    if rec is None:
        return ["record_missing"]
    _, blockers = _evaluate_record(rec)
    return blockers


def get_plant_recovery_view(plant_id: str) -> dict:
    components = []
    for row in _all_records():
        if row["plant_id"] != plant_id:
            continue
        rec = dict(row)
        ready, blockers = _evaluate_record(rec)
        components.append(
            {
                "plant_id": rec["plant_id"],
                "component": rec["component"],
                "rto_hours": rec.get("rto_hours"),
                "backup_status": rec["backup_status"],
                "last_restore_test_days": int(rec["last_restore_test_days"]),
                "runbook_status": rec["runbook_status"],
                "dependency_verified": rec["dependency_verified"],
                "manual_fallback": rec["manual_fallback"],
                "recovery_ready": ready,
                "blockers": blockers,
                "provenance": _provenance(_record_key(rec["plant_id"], rec["component"])),
            }
        )

    if not components:
        raise KeyError(plant_id)

    return {
        "plant_id": plant_id,
        "component_count": len(components),
        "recovery_ready_count": sum(1 for c in components if c["recovery_ready"]),
        "components": components,
        "note": "RecoveryReady is derived; backup_status CURRENT alone is not sufficient (ADR-05)",
    }
