"""Target-state recovery (ADR-05). Fail until ot_command.core.recovery exists.

Keep tests/test_known_legacy_defects.py XFAIL on legacy_recovery_ready.
"""

from tests.helpers.access import field
from tests.helpers.golden import golden_case


def test_eval_018_current_backup_alone_is_not_recovery_ready():
    from ot_command.core.recovery import recovery_ready

    assert recovery_ready({"backup_status": "CURRENT"}) is False


def test_eval_005_plt01_identity_not_ready_with_blockers():
    fx = golden_case("EVAL-005")["fixture"]
    from ot_command.core.recovery import recovery_blockers, recovery_ready

    record = {
        "plant_id": fx["plant_id"],
        "component": fx["component"],
        "backup_status": fx["backup_status"],
        "last_restore_test_days": fx["last_restore_test_days"],
        "runbook_status": fx["runbook_status"],
        "dependency_verified": fx["dependency_verified"],
        "manual_fallback": fx["manual_fallback"],
    }
    assert recovery_ready(record) is False
    blockers = [str(b).lower() for b in recovery_blockers(record)]
    blob = " ".join(blockers)
    assert "restore" in blob or "360" in blob or "test" in blob
    assert "runbook" in blob or "stale" in blob
    assert field(record, "backup_status") == "CURRENT"


def test_eval_013_missing_restore_blob_keeps_not_ready():
    from ot_command.core.recovery import recovery_ready

    assert (
        recovery_ready(
            {
                "backup_status": "CURRENT",
                "last_restore_test_days": 200,
                "runbook_status": "STALE",
                "dependency_verified": "NO",
                "manual_fallback": "LIMITED",
            }
        )
        is False
    )


def test_recovery_ready_requires_runbook_and_deps_not_just_current():
    from ot_command.core.recovery import recovery_ready

    assert (
        recovery_ready(
            {
                "backup_status": "CURRENT",
                "runbook_status": "STALE",
                "dependency_verified": "YES",
            }
        )
        is False
    )


def test_enh06_recovery_routes_are_get_only():
    from ot_command.api import app

    found = {}
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = set(getattr(route, "methods", None) or [])
        if path in {"/recovery/{plant_id}", "/recovery/{site_or_unit}"}:
            found[path] = methods
    assert "/recovery/{plant_id}" in found
    assert "/recovery/{site_or_unit}" in found
    for methods in found.values():
        assert "GET" in methods
        assert not (methods & {"POST", "PUT", "PATCH", "DELETE"})


def test_plant_recovery_plt01_identity_not_ready():
    from ot_command.core.recovery import plant_recovery

    packet = plant_recovery("PLT-01")
    assert packet["recovery_ready"] is False
    identity = [c for c in packet["components"] if c.get("component") == "IDENTITY"]
    assert identity
    assert identity[0]["recovery_ready"] is False
    assert identity[0]["backup_status"] == "CURRENT"
    blob = " ".join(str(b).lower() for b in identity[0]["blockers"])
    assert "restore" in blob or "360" in blob
    assert "runbook" in blob or "stale" in blob
