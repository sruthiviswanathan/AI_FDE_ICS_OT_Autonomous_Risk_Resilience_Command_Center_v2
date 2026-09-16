# Ops (ENH-10 / workshop)

Synthetic advisory operations pack. **No live OT.** Rollback = `AI_ENABLED=0` and no execute tools (there are none to disable behind a flag).

| Doc | Role |
|---|---|
| `RACI.md` | Roles (unnamed people — OPEN-001) |
| `runbooks.md` | Observe / recommend / abstain |
| `incident_rollback.md` | Feature-flag off; no plant rollback from this API |
| `ai_incident_response.md` | Agent-loop, prompt injection, model outage |
| `bcdr.md` | RecoveryReady ≠ backup CURRENT; tabletop only |
| `production_readiness_checklist.md` | Workshop gate |
| `handover.md` | Shift pack |
| `training_outline.md` | Enablement |
| `finops_cost_dashboard.md` | Cost per analyzed incident (OPEN-006) |
| `drift_management.md` | Prompt/policy/data drift |

SLOs: `specs/14_delivery_spec.md`. Traces: `data/local/decision_traces.jsonl` (gitignored). SBOM freeze: `src/ot_command/sbom_freeze.json`.
