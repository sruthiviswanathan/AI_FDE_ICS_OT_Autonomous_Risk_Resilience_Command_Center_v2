import pytest
from ot_command.legacy.risk import legacy_rank, legacy_recovery_ready, legacy_isolation_recommendation

@pytest.mark.xfail(reason='legacy ranking uses CVSS alone and ignores process/safety/recovery context',strict=True)
def test_contextual_risk_should_outrank_highest_cvss():
    fs=[{'id':'A','cvss':9.8,'criticality':'LOW','reachable':'NO'},{'id':'B','cvss':6.5,'criticality':'CRITICAL','reachable':'YES'}]
    assert legacy_rank(fs)[0]['id']=='B'

@pytest.mark.xfail(reason='legacy recovery check trusts backup flag and ignores restore-test freshness/runbook/dependencies',strict=True)
def test_stale_restore_test_should_not_be_recovery_ready():
    assert legacy_recovery_ready('CURRENT') is False

@pytest.mark.xfail(reason='legacy containment recommendation is safety-blind',strict=True)
def test_high_alert_should_not_always_trigger_isolation():
    assert legacy_isolation_recommendation('CRITICAL') != 'ISOLATE'
