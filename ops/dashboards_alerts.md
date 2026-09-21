# Dashboards and alerts design — advisory ops

**REL-01** · C65, C67 · As-built meters: `GET /ops/slo`, `GET /ops/cost-per-incident`, `GET /diagnostics`.  
**Not a deployed Grafana stack.** This is the workshop dashboard *design* a shift lead can reconstruct from APIs and the Command Center UI.

## Panels (what to look at)

| Panel | Source | What “good” looks like | What “bad” looks like |
|-------|--------|------------------------|-----------------------|
| Service health | `GET /health` | `status=ok`, `mode=synthetic-read-only` | API down; wrong `api_version` on proxy |
| Estate imperfections | `GET /diagnostics` + Estate Dashboard | Conflicts **visible** (200+ state conflicts, undocumented paths, etc.) | Counts dropped because someone cleaned `data/` |
| Named SLOs | `GET /ops/slo` | SLO-OT / SLO-CTQ0 **OK** | `execute` in traces; new POST write route |
| Packet latency | `GET /ops/slo` SLO-LAT | p95 present and &lt; 8000 ms **with joins** | p95 green because joins skipped (forbidden) |
| FinOps | `GET /ops/cost-per-incident` | tokens=0 while AI off | token spike with AI on; cheaper CVSS-only rank (EVAL-026) |
| Agent-loop | `GET /ops/slo` `agent_loop_alerts` | 0 over cap (12 steps / 20 tools) | loop_hits &gt; 0 |
| AI mode | UI header badge | `AI-DISABLED` default; `ai_outage` forces OFF | Blank screen; Moonshot with Execute button (must not exist) |
| Recovery honesty | `GET /recovery/PLT-01` | IDENTITY `recovery_ready=false` despite CURRENT | UI saying “ready” from backup_status alone |
| Decision audit | Audit page / `data/local/decision_traces.jsonl` | `execute=false`; tool_trace allowlisted | Hidden CoT used as authority; isolate tool |

Command Center screens that already surface these: Control Tower, Estate, KPI, Audit, Simulation (eval harness), Recovery Graph.

## Alerts (recommended — not wired to a pager)

| ID | Condition | Severity | Response |
|----|-----------|----------|----------|
| ALT-OT-EXEC | Trace `execute=true` or forbidden POST appears | S1 | [incident_rollback.md](incident_rollback.md); SLO-OT breach |
| ALT-LOOP | `workflow_steps` &gt; 12 or `tool_call_count` &gt; 20 | S1 | Abort agent; `AI_ENABLED=0`; [ai_incident_response.md](ai_incident_response.md) |
| ALT-INJECT | Prompt/tool-misuse pattern on envelope | S1/S2 | Guardrail refuse; keep packet ABSTAIN |
| ALT-EVAL | `make eval` not 31/31 | S2 | Block release |
| ALT-AI-DOWN | Model timeout / `AI_ENABLED` forced 0 | S3 | Tables must remain (EVAL-016); caption/Moonshot hide |
| ALT-COST | tokens p95 &gt; 2× prior when AI enabled | S4 | Throttle explainer; OPEN-006 still pending dollars |
| ALT-FAST-WRONG | Latency down **and** EVAL-002/017 fail | S2 | Do not celebrate speed |
| ALT-DATA-CLEAN | Diagnostics counters collapse vs `VERIFICATION.md` baseline | S2 | Reject change; restore bronze `data/` |

There is **no** alert that pages Plant OT to isolate a controller from this app.

## Agent-loop signal

Caps are code, not a dashboard widget: `MAX_AGENT_STEPS=12`, `MAX_TOOL_CALLS=20` in `src/ot_command/core/guardrails.py`. `GET /ops/slo` reports `agent_loop_alerts` over the last 500 traces.

## AI-disabled drill (dashboard expectation)

Scenario rail **AI outage** (`ai_outage`, EVAL-016): header control disabled, badge `AI-DISABLED`, caption and forecast list **hidden**, estate pills and draft packet **still render**. If the screen is blank, the drill failed.

## Related

- Cost panel detail: [finops_cost_dashboard.md](finops_cost_dashboard.md)
- SLO definitions: [named_slos.md](named_slos.md)
