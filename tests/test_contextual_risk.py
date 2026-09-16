import pytest

from ot_command.core import risk
from tests.helpers.golden import get_golden_case


def test_eval_017_contextual_rank_puts_b_before_a():
    findings = [
        {"id": "A", "cvss": 9.8, "criticality": "LOW", "reachable": "NO"},
        {"id": "B", "cvss": 6.5, "criticality": "CRITICAL", "reachable": "YES"},
    ]
    ranked = risk.contextual_rank(findings)
    assert ranked[0]["id"] == "B"
    assert ranked[0].get("factor_breakdown") or ranked[0].get("evidence")


def test_eval_002_high_cvss_unreachable_low_does_not_win_blindly():
    case = get_golden_case("EVAL-002")
    high = case["fixture"]["high_cvss_must_not_win_blindly"]
    low = case["fixture"]["context_outrank"]
    ranked = risk.contextual_rank([high, low])
    assert ranked[0]["finding_id"] == low["finding_id"]


def test_contextual_rank_must_not_be_cvss_descending_only():
    findings = [
        {"id": "X", "cvss": 10.0, "criticality": "LOW", "reachable": "NO"},
        {"id": "Y", "cvss": 4.0, "criticality": "CRITICAL", "reachable": "YES"},
    ]
    ranked = risk.contextual_rank(findings)
    assert ranked[0]["id"] == "Y"
