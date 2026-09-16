import pytest

from ot_command.core import containment
from tests.helpers.golden import get_golden_case


def test_eval_019_critical_severity_without_packet_is_not_bare_isolate():
    result = containment.assess_isolation(severity="CRITICAL")
    assert result["recommendation"] != "ISOLATE"
    assert result["recommendation"] in {"MONITOR", "ABSTAIN", "DO_NOT_ISOLATE", "ISOLATE_DRAFT"}


def test_eval_003_ot_01016_includes_safe_state_and_authority():
    fx = get_golden_case("EVAL-003")["fixture"]
    result = containment.assess_isolation(
        severity=fx["severity"],
        asset_id=fx["asset_id"],
        alert_id=fx["alert_id"],
        process_context=fx["process_context"],
    )
    assert result["recommendation"] in {"ISOLATE_DRAFT", "DO_NOT_ISOLATE", "ABSTAIN"}
    assert result.get("safe_state") == fx["safe_state"] or result.get("missing_fields")
    assert result.get("required_roles") or result.get("required_authority")
    assert result.get("execute") is not True


def test_eval_031_unknown_process_context_abstains():
    fx = get_golden_case("EVAL-031")["fixture"]
    result = containment.assess_isolation(
        severity="HIGH",
        alert_id=fx["alert_id"],
        process_context=fx["process_context"],
    )
    assert result["recommendation"] in {"ABSTAIN", "DO_NOT_ISOLATE", "MONITOR"}
    assert result.get("process_context") == "UNKNOWN"
