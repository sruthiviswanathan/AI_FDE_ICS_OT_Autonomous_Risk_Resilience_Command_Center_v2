import pytest

from ot_command.core import guardrails
from ot_command.core.policy import ACTION_TIERS, requires_human_approval
from tests.helpers.golden import get_golden_case


FORBIDDEN = (
    "write_plc_logic",
    "change_setpoint",
    "modify_sis",
    "bypass_interlock",
)


def test_policy_requires_human_for_plc_sis_setpoint_bypass():
    for action in FORBIDDEN:
        assert requires_human_approval(action) is True
        assert ACTION_TIERS[action] == 4


def test_guardrails_refuse_tier4_control_actions():
    for action in FORBIDDEN:
        result = guardrails.refuse_control_action(action)
        assert result["refused"] is True
        assert result["tier"] == 4


def test_eval_014_refuses_sis_and_plc_demand():
    case = get_golden_case("EVAL-014")
    for action in case["must_not"]:
        if action in ACTION_TIERS:
            result = guardrails.refuse_control_action(action)
            assert result["refused"] is True


def test_eval_023_tool_trace_rejects_execute_tools():
    allowed = get_golden_case("EVAL-023")["fixture"]["allowed_names"]
    trace = allowed + ["isolate_endpoint"]
    with pytest.raises(Exception):
        guardrails.assert_tool_trace_safe(trace)


def test_forbidden_execute_actions_frozen_set():
    assert "write_plc_logic" in guardrails.FORBIDDEN_EXECUTE_ACTIONS
    assert "modify_sis" in guardrails.FORBIDDEN_EXECUTE_ACTIONS
    assert "bypass_interlock" in guardrails.FORBIDDEN_EXECUTE_ACTIONS
