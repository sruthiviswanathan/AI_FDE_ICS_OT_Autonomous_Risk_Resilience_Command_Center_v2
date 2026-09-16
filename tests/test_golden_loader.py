import pytest

from tests.helpers.golden import get_golden_case, load_golden_cases


def test_loads_31_eval_cases():
    cases = load_golden_cases()
    assert len(cases) == 31
    ids = {c["case_id"] for c in cases}
    assert ids == {f"EVAL-{i:03d}" for i in range(1, 32)}


def test_eval_001_fixture_fields():
    case = get_golden_case("EVAL-001")
    assert case["fixture"]["alias"] == "PLT-01-DCS_CONTROLLER-105"
    assert set(case["fixture"]["asset_ids"]) == {"OT-00012", "OT-00033"}
    assert "must_not" in case
    assert "assume CMDB always correct" in case["must_not"][0]


def test_ship_blocker_must_not_cases_present():
    blockers = {"EVAL-001", "EVAL-002", "EVAL-003", "EVAL-005", "EVAL-006", "EVAL-014", "EVAL-016", "EVAL-017", "EVAL-018", "EVAL-019", "EVAL-020", "EVAL-023"}
    ids = {c["case_id"] for c in load_golden_cases()}
    assert blockers.issubset(ids)
