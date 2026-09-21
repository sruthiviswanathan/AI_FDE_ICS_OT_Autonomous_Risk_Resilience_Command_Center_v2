# Transparency and oversight records

**REL-01** · C66 · ADR-06, ADR-08, ADR-12, ADR-15

A shift lead should know **what the system will admit it did**, and what it will **not** pretend to have logged.

## What exists (queryable)

| Record | Where | Use |
|--------|-------|------|
| Decision trace JSONL | `data/local/decision_traces.jsonl` | Audit page; `GET /audit/traces` |
| Trace schema | `contracts/decision_trace.yaml` | Required: decision_id, actor, purpose, plant_id, recommendation, execute=false |
| Workflow envelope | `POST /recommend` response `workflow_states` | Eight display states; timings |
| Tool trace | `tool_trace` on packet/trace | Allowlist only |
| Eval results | `make eval` / harness JSON | must_not gate |
| Red team | `tests/red_team/test_redteam_agent.py` | A-01…A-10 |
| Diagnostics | `GET /diagnostics` | Estate imperfections |
| SLO snapshot | `GET /ops/slo` | Named SLOs |
| Provenance drawer | UI STRUCTURED / GRAPH / POLICY / MEMORY | Citations to CSV paths |
| Scenario binding | `apps/command_center/scenario_bindings.json` | Expected badges; conflicts **shown** |
| Forecast / explain | `GET /forecasts`, `GET /explain` | Advisory; `engine_authoritative=true` |
| Twin sketch | `GET /twin/preview` | `apply_to_plant=false` |

`actor` is a role or service string — **not** a named Authorizer (OPEN-001).

## What is not logged (and must not be used as authority)

| Not logged / not authoritative | Why |
|--------------------------------|-----|
| Raw hidden chain-of-thought | ADR-08 — packet is the argument |
| VECTOR similarity as isolate/policy | ADR-06 — VECTOR only over labeled untrusted notes |
| Shift handover email as permission | `data/shadow/shift_handover_email.txt` UNTRUSTED; OPEN-018 unbound to plant |
| Shadow inventory as CMDB winner | ADR-01 |
| Model logits / weights | None in tree; OPEN-028 |
| Live OT sessions / historian taps | No connectors |
| Operator “I authorize” identity | OPEN-001; Authorize button disabled |

If a future explainer emits prose that is not in the packet, **the packet wins**.

## Oversight cadence (workshop)

| Activity | Who (function) | Record |
|----------|----------------|--------|
| Every PR | FDE | `make ci` |
| Before demo / release | FDE + SOC | checklist in [production_readiness_checklist.md](production_readiness_checklist.md) |
| After AI incident | FDE + VP Ops | [ai_incident_response.md](ai_incident_response.md) |
| Recovery honesty spot-check | Process | `GET /recovery/PLT-01` IDENTITY row |
| Management review of autonomy | REL-04 | remains recommend-only until then |

## Public demo note

Render (or any public URL) is **unauthenticated** (OPEN-029). Treat traces and estate files as workshop-sensitive. Do not paste plant-real data into this repo.
