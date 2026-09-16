"""Golden-case loader. Does not mark evals passed."""

from tests.helpers.golden import GOLDEN_PATH, load_golden_cases


def test_golden_jsonl_contains_eval_001_through_031():
    cases = load_golden_cases()
    missing = [f"EVAL-{i:03d}" for i in range(1, 32) if f"EVAL-{i:03d}" not in cases]
    assert missing == []
    assert GOLDEN_PATH.exists()
    assert cases["EVAL-001"]["must_not"]
    assert cases["EVAL-006"]["must_not"]
