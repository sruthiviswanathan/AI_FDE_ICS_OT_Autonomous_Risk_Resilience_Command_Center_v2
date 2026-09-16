import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = ROOT / "evals" / "golden_cases.jsonl"


def load_golden_cases(*, case_set: str | None = None) -> list[dict]:
    cases = []
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            case = json.loads(line)
            if case_set is None or case.get("set") == case_set:
                cases.append(case)
    return cases


def get_golden_case(case_id: str) -> dict:
    for case in load_golden_cases():
        if case["case_id"] == case_id:
            return case
    raise KeyError(f"golden case not found: {case_id}")
