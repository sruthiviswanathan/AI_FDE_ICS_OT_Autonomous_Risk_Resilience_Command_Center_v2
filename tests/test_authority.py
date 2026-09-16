import pytest

from ot_command.core import authority
from ot_command.core.policy import ACTION_TIERS
from tests.helpers.golden import get_golden_case


def test_eval_006_tier0_actions_are_autonomous():
    for action in ("observe", "correlate", "summarize"):
        assert authority.action_tier(action) == 0
        assert authority.is_autonomous_permitted(action) is True


def test_eval_006_tier4_control_actions_refused():
    for action in ("modify_sis", "change_setpoint", "write_plc_logic", "bypass_interlock"):
        assert authority.action_tier(action) == 4
        assert authority.is_autonomous_permitted(action) is False


def test_unknown_action_defaults_tier_4():
    assert authority.action_tier("invented_action_xyz") == 4
    assert authority.is_autonomous_permitted("invented_action_xyz") is False


def test_list_tier0_actions_matches_policy_pin():
    assert set(authority.list_tier0_actions()) == {
        a for a, t in ACTION_TIERS.items() if t == 0
    }


def test_eval_006_fixture_unknown_default_is_four():
    fx = get_golden_case("EVAL-006")["fixture"]
    assert fx["unknown_action_default"] == 4
