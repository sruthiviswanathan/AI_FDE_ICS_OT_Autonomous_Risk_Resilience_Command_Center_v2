# Production-readiness checklist — synthetic release (REL-01)

Use before calling the advisory Command Center **workshop-ready**.  
**Not** a live plant go-live, **not** an ISO certificate, **not** closure of OPEN-001 / 006 / 028 / 029.

Sign-off functions: FDE + OT Security + Safety (unnamed — OPEN-001).

## Engineering and assurance

- [ ] `make ci` green (sdd-gates, verify, test, eval, red-team)
- [ ] Golden harness EVAL-001…031 PASS (`make eval`)
- [ ] Red team A-01…A-10 PASS
- [ ] `assurance/ASSURANCE_REPORT.md` current enough to cite last executed run
- [ ] Legacy XFAIL only on `legacy_*` (do not delete)
- [ ] `restricted_answer_key/` not used

## Safety and authority

- [ ] No OT execute routes (`tests/test_api_readonly.py`)
- [ ] All recommend traces `execute=false`
- [ ] Guardrails: tier 4 refuse; loop caps 12 / 20
- [ ] `AI_ENABLED=0` default; `ai_outage` UI: tables + packet visible (EVAL-016)
- [ ] Authorize control disabled; OPEN-001 acknowledged
- [ ] Twin preview `apply_to_plant=false`; CASCADE isolate_preview = UNSAFE_ISOLATION
- [ ] Moonshot `recommended_action` ∈ MONITOR / RECOMMEND_CONTAINMENT_REVIEW / ABSTAIN only

## API and observability

- [ ] Gold GETs: identity, telemetry, risk, safety, recovery, authority, graph/slice
- [ ] Advisory GETs: `/forecasts`, `/explain`, `/twin/preview` (execute false)
- [ ] POST only `/recommend` and `/eval/run`
- [ ] `GET /ops/slo` and `GET /ops/cost-per-incident` respond
- [ ] Traces append with `contracts/decision_trace.yaml`
- [ ] Named SLOs documented (`ops/named_slos.md`); SLO-OT / SLO-CTQ0 error budget 0

## Data and drift

- [ ] `data/` contradictions still queryable
- [ ] Shadow inventory not promoted
- [ ] `ops/drift_management.md` followed (no silent clean)
- [ ] Pins: `assurance/SBOM_FREEZE.md`, `pyproject.toml`

## Operations pack (this REL-01)

- [ ] `ops/README.md` index complete
- [ ] RACI, runbooks, incident/rollback, AI IR, BC/DR
- [ ] Dashboards/alerts, named SLOs, SOPs/training, handover
- [ ] Recovery evidence (how to read `GET /recovery/{plant}`)
- [ ] AI-system record + transparency (no fake cert IDs)
- [ ] Technical documentation
- [ ] FinOps design + Render notes (demo, unauthenticated)

## Architecture

- [ ] `specs/as_built_c4.md`
- [ ] `traceability/TRACEABILITY.csv` reviewed; untraced modules not shipped
- [ ] SDD-09 not reopened (A + optional B; C rejected)

## Explicit exclusions (must remain unchecked as live claims)

- [ ] Live plant connectivity — **must stay absent**
- [ ] Production API auth — OPEN-029
- [ ] LLM vendor pin — OPEN-028
- [ ] Named Authorizer in software — OPEN-001
- [ ] Plant MTT / $ thresholds — OPEN-006
- [ ] Attested backup restore — OPEN-027

**Workshop ready** means: a shift lead can operate the synthetic system from `ops/` without the specs tree, and cannot execute OT from the product.
