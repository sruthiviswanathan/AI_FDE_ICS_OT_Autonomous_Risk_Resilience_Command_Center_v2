# Technical documentation — shift-lead operating notes

**REL-01** · Companion to [runbooks.md](runbooks.md). Architecture pictures: `specs/as_built_c4.md`.

## What this system is

A **synthetic-read-only** Command Center: FastAPI (`src/ot_command/api.py` v3.0.0) + React UI (`apps/command_center`). Engines in `src/ot_command/core/`. Legacy defects remain in `src/ot_command/legacy/` for XFAIL contrast.

## Start (local)

See RB-01. Required: Python 3.11+, Node 18+ for UI. `AI_ENABLED=0` default.

Health: `GET /health` → `{ "status": "ok", "mode": "synthetic-read-only", "api_version": "3.0.0" }`  
There is **no** `ai_enabled` field on `/health` (AI mode is a UI query param `ai=`; backend explainer stays off unless a fork sets the env flag).

## Gold read API (shift-lead map)

| Method | Path | Use |
|--------|------|-----|
| GET | `/health` `/diagnostics` | Liveness / estate counters |
| GET | `/plants` `/plants/{id}/assets` `/assets/{id}/alerts` | Inventory browse |
| GET | `/assets/{id}/identity` `/identity/conflicts` | FR-001 |
| GET | `/telemetry/quality` `/telemetry/timeline?order=event_time` | FR-002 |
| GET | `/risk/contextual` | FR-003 anti-CVSS |
| GET | `/safety/conflicts` | FR-004 |
| GET | `/recovery/{site_or_unit}` | FR-005 |
| GET | `/graph/slice` | FR-006 hop cap 8 |
| GET | `/authority/actions` | Catalog; not execute |
| GET | `/ops/slo` `/ops/cost-per-incident` | Named SLOs / FinOps |
| GET | `/scenarios/catalog` `/scenarios/{id}` | Demo rail |
| GET | `/forecasts` `/explain` `/twin/preview` | Advisory AI ON / Moonshot / lab |
| GET | `/audit/traces` `/agent/workflow/demo` | Audit; EVAL-016 envelope |
| POST | `/recommend` | Draft packet only |
| POST | `/eval/run` | Local harness — no OT I/O |

Forbidden: `/isolate`, `/plc`, `/sis`, `/setpoint`, `/bypass`, `/firewall` POST. Twin `proposed_action` is `do_nothing | isolate_preview | increase_logging | open_ticket` — **lab_result only**.

OpenAPI export: `contracts/openapi_command_center.yaml` (`scripts/export_openapi.py`).

## UI flags (query string)

| Param | Values | Notes |
|-------|--------|-------|
| `persona` | full, fde, soc_analyst, process_engineer, safety_owner, executive | View filter, not authority |
| `scenario` | nominal, cascade_001, inject_01…06, ai_outage | Loads plant/asset/alert |
| `ai` | off, on, moonshot | `ai_outage` forces off; Moonshot hidden for executive |

Demo: `/estate?persona=full&ai=off` · `/estate?persona=full&scenario=cascade_001&ai=moonshot` · `/simulation?persona=full&scenario=cascade_001&ai=moonshot`

## Policy pin

Envelopes should carry `"policy_version": "policy.py:ACTION_TIERS"`. Unknown verbs = tier 4 refuse.

## Data

Do not rewrite `data/raw` or promote `data/shadow`. Diagnostics integers in `VERIFICATION.md` / `run_diagnostics()` are the quantitative baseline unless re-measured.

## Build / gates

```text
make ci          # sdd-gates, verify, test, eval, red-team
make eval        # EVAL-001…031
```

Dockerfile: multi-stage UI + API. Demo hosting: [render_deployment.md](render_deployment.md) (no auth).

## Support tiers (functions)

- L1: SOC — tables + packet  
- L2: FDE — harness, API, traces  
- L3: Safety / Process — authorization **outside** this app (OPEN-001)
