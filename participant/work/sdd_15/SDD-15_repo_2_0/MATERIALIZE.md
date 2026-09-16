# SDD-15 — Materialize Repo 2.0

**Prompt:** SDD-15 | MATERIALIZE REPO 2.0  
**Depends on:** SDD-01…14 freeze  
**Date:** 2026-09-16  
**FDE capabilities evidenced:** C17, C32; coverage of C01–C96 as specced|pending  
**Not this prompt:** product engines; UI; OT writes; cleaning CSVs; deleting XFAIL.

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Playbook SDD-15 file list; transformation prompt `specs/adrs/` + `FDE_96_COVERAGE.csv`; SDD-14 delivery increment table; ADR register Accepted ADR-KG and ADR-01…16; expanded golden cases EVAL-001…031; `policy.py` ACTION_TIERS; `api.py` two GETs.

### Assumptions
Repo 2.0 = navigable SDD structure. Repo 3.0 = ENH behavior on a parallel modern path. Distilled specs do not replace long-form on conflict.

### Unknowns
Same OPEN register as SDD-14 except OPEN-011 closed by `specs/01_mandate.md`. OPEN-010 left open (`__init__.py` 0.1.0 vs pyproject 2.0.0).

### Did not conclude
Did not implement identity/risk/safety/recovery engines. Did not reopen SDD-09. Did not name Authorizers.

## Layout produced
`specs/` · `adrs/` · `specs/adrs/` (copies) · `evals/golden_cases.jsonl` expanded · `evals/scenarios.md` · `traceability/` · `.cursor/rules/sdd.mdc` · `scripts/check_sdd_gates.py` · `src/ot_command/modern/README.md` · `assurance/README.md` · `ops/README.md` · `participant/work/FDE_96_COVERAGE.csv` · `specs/REPO_2_0_GATE.md`

## Ban observed
No `legacy_*` edits · no XFAIL deleted · no CSV clean · no OT write API · no UI.
