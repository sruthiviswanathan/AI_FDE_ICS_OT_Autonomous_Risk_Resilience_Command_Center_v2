# Evals / TEVV

Evaluate identity correctness, evidence grounding, temporal correctness, unit correctness, process-context correctness, safety-policy compliance, authority enforcement, tool trajectory, side effects, uncertainty communication, recovery reasoning, latency and cost.

`golden_cases.jsonl` holds EVAL-001…031. Scenario map: `scenarios.md`.

**Harness:** `evals/harness.py` (ENH-09). Pytest: `tests/test_eval_golden.py`. Do not invent pass results. XFAIL tests on `legacy_*` remain. Assurance write-up: `assurance/ASSURANCE_REPORT.md`.
