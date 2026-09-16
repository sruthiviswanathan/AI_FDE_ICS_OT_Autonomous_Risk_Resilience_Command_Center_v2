# Ops — Repo 3.0 (ENH-10)

Production-readiness pack for the **synthetic advisory service**. Not live plant operations.

| Document | Purpose |
|----------|---------|
| [RACI.md](RACI.md) | Roles (unnamed until OPEN-001) |
| [runbooks.md](runbooks.md) | Local API, triage, eval gates |
| [incident_rollback.md](incident_rollback.md) | Software rollback (`AI_ENABLED=0`) |
| [ai_incident_response.md](ai_incident_response.md) | Model/agent failure classes |
| [bcdr.md](bcdr.md) | Advisory service continuity |
| [production_readiness_checklist.md](production_readiness_checklist.md) | Pre-PRD gate |
| [handover.md](handover.md) | FDE handover + training outline |
| [finops_cost_dashboard.md](finops_cost_dashboard.md) | Cost-per-incident design |
| [drift_management.md](drift_management.md) | Spec/data/policy drift |
| [render_deployment.md](render_deployment.md) | Deploy FE + BE to Render (Docker, free tier) |

Telemetry: `GET /ops/slo`, `GET /ops/cost-per-incident` · Traces: `data/local/decision_traces.jsonl` · Schema: `contracts/decision_trace.yaml`
