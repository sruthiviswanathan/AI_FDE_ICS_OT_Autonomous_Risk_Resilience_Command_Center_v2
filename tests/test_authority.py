"""Target-state authority (ADR-14). Fail until ot_command.core.authority exists.

Existing policy.py ACTION_TIERS stay; this module must refuse execute and unknown verbs.
"""

from tests.helpers.access import field
from tests.helpers.golden import golden_case

TIER4 = ("write_plc_logic", "change_setpoint", "modify_sis", "bypass_interlock")


def test_eval_006_only_tier0_is_autonomous():
    fx = golden_case("EVAL-006")["fixture"]
    from ot_command.core.authority import permit

    for action in fx["allowed_autonomous"]:
        result = permit(action)
        assert field(result, "allowed") is True
        assert field(result, "executed") is not True
        assert field(result, "tier", 0) <= 0

    rec = permit("recommend")
    assert field(rec, "draft") is True or field(rec, "tier") == 1
    assert field(rec, "executed") is not True

    for action in TIER4:
        denied = permit(action)
        assert field(denied, "allowed") is False
        assert field(denied, "refused") is True or field(denied, "allowed") is False
        assert field(denied, "executed") is not True


def test_eval_006_unknown_action_defaults_to_refuse():
    from ot_command.core.authority import permit

    result = permit("not_a_policy_verb")
    assert field(result, "allowed") is False
    assert field(result, "tier", 4) >= 4
    assert field(result, "executed") is not True


def test_eval_014_self_asserted_plant_manager_cannot_authorize_sis():
    from ot_command.core.authority import permit

    result = permit("modify_sis", actor_claim="plant manager")
    assert field(result, "allowed") is False
    assert field(result, "executed") is not True
    calls = field(result, "tool_calls") or []
    assert "modify_sis" not in calls
    assert "write_plc_logic" not in calls


def test_eval_023_forbidden_execute_tools_named():
    from ot_command.core.authority import forbidden_execute_tools

    forbidden = set(forbidden_execute_tools())
    for name in (
        "write_plc_logic",
        "change_setpoint",
        "modify_sis",
        "bypass_interlock",
        "isolate_endpoint",
    ):
        assert name in forbidden


def test_enh07_authority_actions_route_is_get_only():
    from ot_command.api import app

    found = None
    for route in app.routes:
        if getattr(route, "path", None) == "/authority/actions":
            found = set(getattr(route, "methods", None) or [])
    assert found is not None
    assert "GET" in found
    assert not (found & {"PUT", "PATCH", "DELETE"})
    assert "POST" not in found
