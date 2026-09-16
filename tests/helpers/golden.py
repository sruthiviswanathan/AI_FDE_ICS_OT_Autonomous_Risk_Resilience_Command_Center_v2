"""Load evals/golden_cases.jsonl. Does not execute engines or invent pass results."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "evals" / "golden_cases.jsonl"


def load_golden_cases(path: Path | None = None) -> dict[str, dict]:
    target = path or GOLDEN_PATH
    cases: dict[str, dict] = {}
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        cases[row["case_id"]] = row
    return cases


def golden_case(case_id: str, cases: dict[str, dict] | None = None) -> dict:
    table = cases if cases is not None else load_golden_cases()
    if case_id not in table:
        raise KeyError(f"missing {case_id} in {GOLDEN_PATH}")
    return table[case_id]
