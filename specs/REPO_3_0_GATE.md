# Repo 3.0 gate (ENH-10)

**Date:** 2026-09-16  
**Stage:** Modernized (engines + ops) · **Nature:** production-oriented synthetic · **Specs:** refined + as-built C4 · **Controls:** traceability + gates + guardrails + traces + SBOM freeze · **Validation:** readiness-focused (harness + assurance) · **Outcome:** PRD + App ready

Not a live-plant go-live. OM 14–16 engineering + assurance complete. REL / PRD / APP remain for adoption, value, lifecycle, and UI.

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Playbook ENH-10; `REPO_3.0_ENH_01_TO_10.md`; `evals/harness.py` 31/31; `assurance/ASSURANCE_REPORT.md`; gold GETs including `/graph/slice`; `GET /ops/slo`; `GET /ops/cost-per-incident`; `ops/production_readiness_checklist.md`; `specs/as_built_c4.md`; `contracts/decision_trace.yaml`.

### Assumptions
Repo 3.0 is the advisory increment that can generate a PRD and App. Packaging `__version__` stays `0.1.0` (OPEN-010). Dollar cost remains null (OPEN-006).

### Unknowns
OPEN-001 named Authorizer; OPEN-002 legal class; OPEN-006 KPI formulas; OPEN-024 unsigned SBOM; OPEN-028 model; OPEN-029 API authn; OPEN-RISK-01/05/11 residual.

### Did not conclude
Customer UI; live OT canary; signed SBOM; isolate execute; named people in RACI.

## Comparison table (SDD slide)

| Dimension | Repo 1.0 | Repo 2.0 | Repo 3.0 |
|---|---|---|---|
| Stage | Baseline | Modernized (structure) | Modernized (engines + ops) |
| Nature | Brownfield simulation | SDD-aligned | Production-oriented synthetic |
| Specs | `docs/` scattered | structured `specs/` | refined + as-built C4 |
| Controls | AGENTS.md + ot-fde.mdc | traceability + gates | + guardrails + decision traces + SBOM freeze |
| Validation | 3 pass / 3 xfail | spec-aligned | readiness-focused (harness + assurance + ops) |
| Outcome | messy discoverable repo | improved repo | **PRD + App ready** |

## Gate checks

| Check | Evidence | OK |
|---|---|---|
| Target engines pass | pytest ENH-01…10; 73 passed / 3 xfail only on `legacy_*` | yes |
| API read-only of OT | POST `/recommend` is a packet; no isolate/PLC/SIS routes | yes |
| Guardrails tested | `tests/red_team/`; ENH-08 | yes |
| Assurance report exists | `assurance/ASSURANCE_REPORT.md` | yes |
| As-built C4 exists | `specs/as_built_c4.md` | yes |
| Specs refined | hop-capped graph; traces contract; ops pack | yes |
| Ready to generate PRD + App | this gate; UI not built | yes |

**Next:** PRD-01
