# Repo 2.0 gate (SDD-15)

**Date:** 2026-09-16  
**Stage:** Modernized (structure) · **Nature:** SDD-aligned · **Specs:** structured · **Controls:** traceability + gates · **Validation:** spec-aligned · **Outcome:** improved repo

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Playbook SDD-15; transformation SDD-15; SDD-01…14 artifacts under `participant/work/sdd_15/`; `tests/test_known_legacy_defects.py` (3 xfail); `src/ot_command/api.py` GET-only; `src/ot_command/__init__.py` still `0.1.0`.

### Assumptions
Layout is the increment. Packaging `__version__` left at `0.1.0` (OPEN-010) so the documented conflict remains evidence.

### Unknowns
OPEN-001…010, 012…029, OPEN-RISK-01/05/11. OPEN-011 closed (root `specs/01_mandate.md` now exists).

### Did not conclude
Did not implement modern engines. Did not bump `__init__.py`. Did not clean CSVs.

## OM 1–13 essential artifacts

| Check | Path | OK |
|---|---|---|
| Mandate | `specs/01_mandate.md` | yes |
| Current state | `specs/02_current_state.md` | yes |
| 96-cell forensics pointer | `specs/03_forensics_96.md` + matrix.csv | yes |
| SCQA / CTQs | `specs/04_problem_value.md` | yes |
| Use case | `specs/05_use_case.md` | yes |
| Domain | `specs/06_domain.md` | yes |
| Data | `specs/07_data_knowledge.md` | yes |
| Evals | `specs/08_evals_risks.md` + `evals/golden_cases.jsonl` EVAL-001…031 | yes |
| Options frozen | `specs/09_options.md` | yes |
| Info arch | `specs/10_information_architecture.md` | yes |
| App arch | `specs/11_ai_app_architecture.md` | yes |
| Agentic | `specs/12_agentic.md` | yes |
| Security | `specs/13_security_guardrails.md` | yes |
| Delivery + TRACEABILITY | `specs/14_delivery_spec.md` + `traceability/TRACEABILITY.csv` | yes |
| ADR index | `adrs/ADR-00-index.md` ADR-KG, ADR-01…16 | yes |
| Coverage 96 | `participant/work/FDE_96_COVERAGE.csv` | yes |
| Gate script | `scripts/check_sdd_gates.py` | yes |

## Confirmations
- **No live OT write surface added.** API remains GET `/health` and `/diagnostics`. `modern/` has README only.
- **`data/` contradictions were not cleaned.** Seeded alias collisions, state conflicts, dirty telemetry, CURRENT-backup rows remain.
- **`legacy_*` behavior unchanged.** XFAIL tests remain strict.
- **`__init__.py` version not bumped** (OPEN-010). pyproject still 2.0.0.
- **verify_repo.py:** VERIFY_OK. One SDD-03 matrix cell used a restricted-role substring; wording changed to “war-room chair” (OPEN-001 unchanged). `data/` not touched.

## ENH remediations queued
ENH-01 identity (FR-001) · ENH-02 telemetry (FR-002) · ENH-03 contextual risk (FR-003) · ENH-04 safety (FR-004) · ENH-05 recovery (FR-005) · ENH-06 graph slice (FR-006) · ENH-07 agent allowlist (FR-012) · ENH-08 red team · ENH-09 harness + assurance · ENH-10 observability / SBOM / FinOps.

Next prompt: **ENH-01**.
