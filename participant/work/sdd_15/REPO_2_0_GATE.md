# SDD-15 — Repo 2.0 gate

**Prompt:** SDD-15 | Materialize Repo 2.0  
**Date:** 2026-09-16  
**FDE capabilities:** C17, C32 + coverage rows C01–C96  
**Not this prompt:** implement engines (ENH-01); change `legacy_*`; UI.

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
- `analysis-artefacts/CAPSTONE_PLAYBOOK.md` SDD-15 layout
- `analysis-artefacts/transformation-prompts/REPO_2.0_SDD_09_TO_15.md` (specs/adrs, coverage columns, REPO_2_0_GATE)
- `analysis-artefacts/FDE_96_TO_OM21_MAP.md` master table C01–C96
- Frozen SDD-01…14 under `participant/work/sdd_15/`
- `evals/golden_cases.jsonl` expanded in place from `SDD-08_evals_risks/golden_cases_expanded.jsonl` (EVAL-001…006 retained)
- `src/ot_command/legacy/risk.py` untouched
- `src/ot_command/api.py` still two GETs
- `src/ot_command/__init__.py` `__version__ = "0.1.0"` (OPEN-010 left open)

### Assumptions
1. Distilled `specs/*.md` point at long-form artifacts; long-form remains normative on conflict.
2. `pending` in coverage ≠ `missing`. Missing would fail the gate; pending waits on ENH/REL with an owner in OPEN_DECISIONS or the map’s prompt column.
3. Packaging version alignment is optional and was **not** done.

### Unknowns
OPEN-001…010, 012…029, OPEN-RISK-01/05/11 unchanged. OPEN-011 closed because `specs/01_mandate.md` exists.

### Did not conclude
Did not implement FR-001…014 code. Did not select LLM provider. Did not authorize isolation.

## Comparison vs SDD slide (Repo 1.0 → 2.0)

| Dimension | Repo 1.0 (before) | Repo 2.0 (this prompt) |
|---|---|---|
| Stage | Brownfield simulation | **Modernized** (structure only) |
| Nature | Runnable diagnostics + seeded defects | **SDD-aligned** |
| Specs | Participant worktree only | **Structured** `specs/01`…`14` + `adrs/` |
| Controls | AGENTS.md + ot-fde.mdc | **Traceability + gates** (`TRACEABILITY.csv`, `check_sdd_gates.py`, `sdd.mdc`) |
| Validation | 3 passed / 3 xfailed | **Spec-aligned** (same legacy tests + structural gate test) |
| Outcome | Discoverable mess | **Improved repo** ready for ENH-01 |

## Confirmations
| Claim | Evidence |
|---|---|
| No OT write surface added | No new routes in `api.py`; `modern/` README only |
| Data contradictions not cleaned | `data/raw` and `data/shadow` not rewritten |
| Legacy behavior preserved | `tests/test_known_legacy_defects.py` still strict xfail |
| EVAL-001…006 kept | Present in expanded `evals/golden_cases.jsonl` |
| 96 coverage rows | `participant/work/FDE_96_COVERAGE.csv` |

## ENH queue
ENH-01…10 as `specs/14_delivery_spec.md` / TRACEABILITY.csv.

**Gate:** PASS. `scripts/check_sdd_gates.py` → SDD_GATE_OK (48 paths, 31 eval cases). pytest **4 passed / 3 xfailed**. `verify_repo.py` → VERIFY_OK. Coverage 96 rows (72 specced, 24 pending ENH/REL, 0 missing).

**Next:** ENH-01
