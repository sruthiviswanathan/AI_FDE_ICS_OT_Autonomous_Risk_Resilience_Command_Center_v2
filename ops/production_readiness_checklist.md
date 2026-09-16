# Production Readiness Checklist — Repo 3.0 (Synthetic)

Use before declaring **PRD+App ready**. Not a live plant go-live sign-off.

## Engineering & assurance

- [ ] `make ci` green (sdd-gates, verify, test, eval, red-team)
- [ ] Golden harness 31/31 PASS (`make eval`)
- [ ] Red team 17/17 PASS
- [ ] `assurance/ASSURANCE_REPORT.md` current
- [ ] Legacy XFAIL only on `legacy_*` functions (3 tests)
- [ ] `restricted_answer_key/` absent

## Safety & authority

- [ ] No OT execute routes (`tests/test_api_readonly.py`)
- [ ] `execute=false` on all decision traces
- [ ] Guardrails: tier 4 refuse; loop caps 12 steps / 20 tools
- [ ] `AI_ENABLED=0` default; manual fallback works (EVAL-016)
- [ ] OPEN-001 acknowledged: named Authorizer not implemented

## API & observability

- [ ] Gold GET routes wired (identity, telemetry, risk, safety, recovery, authority, graph/slice)
- [ ] `POST /recommend` and `POST /eval/run` local only
- [ ] `GET /ops/slo` and `GET /ops/cost-per-incident` respond
- [ ] Decision traces append with schema `contracts/decision_trace.yaml`
- [ ] Token and latency fields populated on new traces

## Data & drift

- [ ] `data/` contradictions **not** cleaned (alias collisions, state conflicts, etc.)
- [ ] Shadow inventory not promoted to CMDB
- [ ] Drift management process documented (`ops/drift_management.md`)
- [ ] Version pins documented (`assurance/SBOM_FREEZE.md`, `pyproject.toml`)

## Operations pack

- [ ] `ops/RACI.md`, runbooks, rollback, AI incident, BCDR present
- [ ] Handover + training outline (`ops/handover.md`)
- [ ] FinOps design (`ops/finops_cost_dashboard.md`)

## Architecture

- [ ] As-built C4 (`specs/as_built_c4.md`)
- [ ] TRACEABILITY.csv reviewed; OPEN-030 (core vs modern path) noted

## Explicit exclusions (workshop)

- [ ] No live plant connectivity
- [ ] No production API auth (OPEN-029)
- [ ] No LLM vendor selected (OPEN-028)
- [ ] No full customer UI (PRD-01 / APP-01 next)

**Sign-off role:** FDE + OT Security + Safety (unnamed — OPEN-001)
