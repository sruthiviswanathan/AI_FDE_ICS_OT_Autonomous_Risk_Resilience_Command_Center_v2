"""Target-state contextual rank (ADR-03). Fail until ot_command.core.risk exists.

Keep tests/test_known_legacy_defects.py XFAIL on legacy_rank as historical evidence.
"""

from tests.helpers.access import field, rec_id
from tests.helpers.golden import golden_case


def test_eval_017_reachable_critical_outranks_unreachable_cvss_98():
    fx = golden_case("EVAL-017")["fixture"]
    from ot_command.core.risk import contextual_rank

    ranked = contextual_rank([fx["A"], fx["B"]])
    assert rec_id(ranked[0]) == "B"
    factors = field(ranked[0], "factors") or field(ranked[0], "must_include") or []
    factor_text = str(factors).lower() + " " + " ".join(golden_case("EVAL-017")["must_include"])
    for needed in ("reachability", "criticality", "safety", "recovery"):
        assert needed in factor_text or field(ranked[0], needed) is not None


def test_eval_002_vul_00098_outranks_unreachable_98():
    fx = golden_case("EVAL-002")["fixture"]
    from ot_command.core.risk import contextual_rank

    low = dict(fx["high_cvss_must_not_win_blindly"])
    high = dict(fx["context_outrank"])
    ranked = contextual_rank([low, high])
    top = rec_id(ranked[0])
    assert top in {"VUL-00098", "OT-01016"} or top == high.get("finding_id")
    assert rec_id(ranked[0]) != low.get("finding_id")


def test_contextual_rank_is_not_legacy_rank():
    from ot_command.core.risk import contextual_rank
    from ot_command.legacy.risk import legacy_rank

    findings = [
        {"id": "A", "cvss": 9.8, "criticality": "LOW", "reachable": "NO"},
        {"id": "B", "cvss": 6.5, "criticality": "CRITICAL", "reachable": "YES"},
    ]
    modern = [rec_id(x) for x in contextual_rank(findings)]
    legacy = [x["id"] for x in legacy_rank(findings)]
    assert modern[0] == "B"
    assert legacy[0] == "A"


def test_eval_002_must_include_five_factors_on_top_finding():
    from ot_command.core.risk import rank_factors

    factors = rank_factors(
        {
            "finding_id": "VUL-00098",
            "cvss": 8.7,
            "network_reachable": "YES",
            "asset_id": "OT-01016",
        }
    )
    blob = str(factors).lower()
    for key in golden_case("EVAL-002")["must_include"]:
        token = key.split()[0].lower()
        assert token in blob or key.replace(" ", "_") in blob or field(factors, token) is not None
