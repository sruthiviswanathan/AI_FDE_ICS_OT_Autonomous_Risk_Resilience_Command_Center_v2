# FinOps — cost per analyzed incident (design)

KPI from `docs/05_kpis_baseline.md`: **AI cost per analyzed incident / avoided escalation**. Formula and dollar threshold are **OPEN-006 BASELINE_PENDING**. This dashboard must not treat a cheaper CVSS-only rank as a win (EVAL-026).

## Tiles (workshop)

| Tile | Source | Notes |
|---|---|---|
| Incidents analyzed | `trace_count` | `data/local/decision_traces.jsonl` |
| Tokens / call | `trace.tokens` | Placeholder `len//4` until OPEN-028 |
| USD | **null** | Do not invent a unit price |
| Latency | last CASCADE AI-disabled ms | Completeness > speed; SLO-LAT p95 <8s without dropping joins |
| Error budget SLO-OT | 0 | Any execute tool is a budget breach |
| Avoided escalation | not measured | Counter-metric: false-positive isolate drafts |

API: `GET /ops/cost-per-incident`.

Explainer off (`AI_ENABLED=0`) is a cost of **0 tokens**, not a failed product.
