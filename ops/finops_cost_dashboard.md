# FinOps — Cost Dashboard Design

**REL-01 companion.** Alert/panel placement: [dashboards_alerts.md](dashboards_alerts.md). Named latency SLO: [named_slos.md](named_slos.md).

**KPI:** AI cost per analyzed incident / avoided escalation (`docs/05_kpis_baseline.md`)  
**Status:** BASELINE_PENDING (OPEN-006) — meters implemented; dollar thresholds not set.

## Data sources

| Signal | Source | Field |
|--------|--------|-------|
| Tokens per incident | `data/local/decision_traces.jsonl` | `tokens` |
| Latency per incident | decision traces | `latency_ms` |
| Tool calls | decision traces | `tool_call_count` |
| AI on/off | decision traces | `ai_enabled` |
| Eval correctness | `make eval` | 31/31 gate |
| Legacy cost anti-pattern | EVAL-026 | CVSS-only shortcut invalidates cost win |

## API (implemented)

```
GET /ops/cost-per-incident
GET /ops/slo          # includes SLO-LAT p95 from traces
```

## Dashboard panels (design — not a deployed UI)

1. **Incidents analyzed (24h / 7d)** — count from traces
2. **Avg / p95 latency** — ms per `POST /recommend`
3. **Tokens per incident** — 0 when AI disabled; histogram when enabled
4. **Cost estimate** — `tokens × token_unit_cost` (placeholder 0 until OPEN-028 pricing)
5. **Counter-metric:** contextual rank correctness rate (link to eval harness)
6. **Error budget:** SLO-LAT vs 8s workshop target (`specs/14_delivery_spec.md`)

## Alerts (recommended)

| Alert | Condition |
|-------|-----------|
| Cost spike | tokens p95 > baseline × 2 when AI enabled |
| Fast-but-wrong | latency ↓ but EVAL-002 fails |
| Loop cap | workflow_steps > 12 or tool_call_count > 20 |

## Workshop note

Default deployment: **$0 model cost** (AI off). FinOps dashboard proves metering exists before model pin (OPEN-028).
