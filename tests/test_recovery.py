import pytest

from ot_command.core import recovery
from tests.helpers.golden import get_golden_case


def test_eval_018_current_backup_status_alone_is_not_ready():
    assert recovery.recovery_ready(backup_status="CURRENT") is False


def test_eval_005_plt_01_identity_not_ready():
    fx = get_golden_case("EVAL-005")["fixture"]
    assert (
        recovery.recovery_ready(
            plant_id=fx["plant_id"],
            component=fx["component"],
            record={
                "backup_status": fx["backup_status"],
                "last_restore_test_days": fx["last_restore_test_days"],
                "runbook_status": fx["runbook_status"],
                "dependency_verified": fx["dependency_verified"],
                "manual_fallback": fx["manual_fallback"],
            },
        )
        is False
    )


def test_recovery_ready_requires_restore_runbook_deps():
    record = {
        "backup_status": "CURRENT",
        "last_restore_test_days": 30,
        "runbook_status": "CURRENT",
        "dependency_verified": "YES",
        "manual_fallback": "YES",
    }
    assert recovery.recovery_ready(record=record) is True
