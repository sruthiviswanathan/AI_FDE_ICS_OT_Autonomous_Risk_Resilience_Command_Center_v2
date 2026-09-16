"""ENH-09 golden harness — EVAL-001…031 must pass via modern engines."""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def harness_report():
    from evals.harness import run_all

    return run_all()


def test_golden_cases_load_count():
    from tests.helpers.golden import load_golden_cases

    cases = load_golden_cases()
    assert len(cases) == 31
    assert cases[0]["case_id"] == "EVAL-001"
    assert cases[-1]["case_id"] == "EVAL-031"


def test_eval_harness_all_cases_pass(harness_report):
    failures = harness_report["failures"]
    assert harness_report["total"] == 31
    assert harness_report["passed"] == 31, json.dumps(failures, indent=2)
    assert harness_report["all_pass"] is True


def test_cascade_001_fixture_present():
    path = ROOT / "scenarios" / "cascade_001.json"
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["scenario_id"] == "CASCADE-001"
    times = {e["time"] for e in data["timeline"]}
    assert {"08:24", "08:38", "08:47", "08:50"}.issubset(times)
