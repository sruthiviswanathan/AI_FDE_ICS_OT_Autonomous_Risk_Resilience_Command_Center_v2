"""Harness execution for EVAL-001…031. Fail closed on must_not. No invented pass."""

from evals.harness import load_cases, run_all


def test_golden_harness_executes_eval_001_through_031():
    report = run_all()
    assert report["n"] == 31
    assert report["invented_pass"] is False
    ids = [r["case_id"] for r in report["results"]]
    assert ids == [f"EVAL-{i:03d}" for i in range(1, 32)]
    assert report["fail"] == 0, report["fails"]


def test_harness_loads_same_golden_file_as_loader():
    from tests.helpers.golden import load_golden_cases

    assert set(load_cases()) == set(load_golden_cases())
