from ot_command.core.policy import requires_human_approval
from ot_command.diagnostics import run_diagnostics

def test_diagnostics_detect_seeded_imperfections():
    d=run_diagnostics()
    assert d['alias_collisions'] > 0
    assert d['undocumented_network_paths'] > 0
    assert d['duplicate_telemetry_packets'] > 0

def test_safety_critical_actions_require_human_approval():
    assert requires_human_approval('write_plc_logic')
    assert requires_human_approval('modify_sis')
    assert not requires_human_approval('summarize')

def test_recovery_gaps_exist():
    d=run_diagnostics()
    assert d['recovery_unverified_dependencies'] > 0
