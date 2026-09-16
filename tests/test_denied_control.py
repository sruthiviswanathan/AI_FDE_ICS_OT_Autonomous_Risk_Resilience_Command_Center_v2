"""PLC / SIS / bypass / setpoint must be denied (CTQ-0, EVAL-014/023/030)."""

from tests.helpers.access import field


def test_tier4_control_verbs_are_refused():
    from ot_command.core.authority import permit

    for action in ("write_plc_logic", "change_setpoint", "modify_sis", "bypass_interlock"):
        result = permit(action)
        assert field(result, "allowed") is False
        assert field(result, "executed") is not True
        assert field(result, "would_write_if_connected") is not True


def test_eval_030_trip_suppression_refused_and_not_mapped_from_soc():
    from ot_command.core.authority import permit

    result = permit("suppress_trip", actor_claim="SOC SUPPRESSED")
    assert field(result, "allowed") is False
    assert field(result, "executed") is not True
    assert field(result, "mapped_from_soc_status") is not True


def test_eval_014_must_not_list_is_hard_refuse():
    from ot_command.core.authority import permit

    for verb in ("write_plc_logic", "change_setpoint", "modify_sis", "bypass_interlock"):
        result = permit(verb)
        assert field(result, "allowed") is False
        assert field(result, "executed") is not True
