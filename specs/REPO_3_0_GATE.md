# Repo 3.0 gate (ENH-10)

**Date:** 2026-09-16  
**Stage:** Mature / production-oriented (synthetic) · **Outcome:** PRD + App ready

## SDD comparison table

| Dimension | Repo 1.0 (baseline) | Repo 2.0 (SDD-15) | Repo 3.0 (ENH-01…10) |
|-----------|---------------------|-------------------|----------------------|
| **Stage** | Immature discovery | Modernized structure | Production-oriented advisory increment |
| **Nature** | Brownfield simulation | SDD-aligned specs | Governed synthetic command center |
| **Specs** | Scattered docs | Structured `specs/` + ADRs | Refined + as-built C4 |
| **Controls** | Minimal tests | Traceability + SDD gates | Guardrails + harness + ops pack |
| **Validation** | 3 pass / 3 xfail legacy | Spec-aligned layout | Readiness-focused (31 evals + red team) |
| **Outcome** | Forensics complete | Improved repo | **PRD + App ready** (not customer UI) |

## Gate checks

| Check | Evidence | Status |
|-------|----------|--------|
| Modern engines pass | `tests/test_*`, `make eval` 31/31 | PASS |
| API read-only + gold GETs | `tests/test_api_readonly.py` | PASS |
| Graph slice FR-006 | `GET /graph/slice`, `core/graph_slice.py` | PASS |
| Guardrails tested | `tests/red_team` 17/17 | PASS |
| Assurance report | `assurance/ASSURANCE_REPORT.md` | PASS |
| As-built C4 | `specs/as_built_c4.md` | PASS |
| Ops pack | `ops/*.md` | PASS |
| Observability | traces + `GET /ops/slo`, `/ops/cost-per-incident` | PASS |
| Legacy XFAIL only on `legacy_*` | 3 xfail tests preserved | PASS |
| Data contradictions preserved | No CSV clean | PASS |
| `restricted_answer_key/` absent | verify_repo | PASS |

## OM coverage (14–16)

| OM | Deliverable | Location |
|----|-------------|----------|
| 14 | Modern engines ENH-01…06 | `src/ot_command/core/` |
| 14 | Agent ENH-07 | `core/agent.py` |
| 15 | Red team ENH-08 | `tests/red_team/` |
| 15 | Harness ENH-09 | `evals/harness.py` |
| 16 | Ops / FinOps / readiness ENH-10 | `ops/`, `core/ops.py` |

## Remaining for adoption (not Repo 3.0 blockers)

- **PRD-01** — product requirements document
- **APP-01/02** — customer application UI
- **REL-01…04** — live deployment, real auth (OPEN-029), model pin (OPEN-028)
- **Named Authorizer** (OPEN-001)

## Confirmations

- No live OT write surface. `execute=false` on all traces.
- AI disabled by default (ADR-12).
- Workshop only — not a certification or pentest sign-off.

**Next prompt:** PRD-01
