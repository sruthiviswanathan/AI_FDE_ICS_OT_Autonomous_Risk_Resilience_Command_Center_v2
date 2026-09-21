# Incident and rollback — advisory service

**REL-01** · C69  
**Scope:** software configuration of the Command Center. **Not** OT plant state. This app has never isolated a controller.

## Severity (service)

| Sev | Meaning | Example |
|-----|---------|---------|
| SEV-1 | Safety / control boundary | Trace with `execute=true`; forbidden POST; model asks SIS/PLC write |
| SEV-2 | Integrity of advice | Eval regression; identity counts treated as census; data “cleaned” |
| SEV-3 | Availability | API down; model timeout; blank UI on AI outage |
| SEV-4 | Cost / capacity | Token spike (AI on); loop near cap without breach |

AI-class detail: [ai_incident_response.md](ai_incident_response.md). Progressive-delivery tree: [adoption.md](adoption.md) §5 (`AI_ENABLED=0`).

## Triggers → rollback

| Trigger | Immediate action |
|---------|------------------|
| Guardrail / SLO-OT / SLO-CTQ0 breach | Disable explainer; freeze deploy; preserve traces |
| `make eval` not 31/31 | Do not promote image |
| Unexpected tier 3/4 **tool** in `tool_trace` | Treat as SEV-1; `AI_ENABLED=0` |
| Model drift (OPEN-028 pin later) | Off until harness + red team on that pin |
| API crash / bad proxy | Restart last known-good; `GET /health` |

## Rollback steps (software)

1. **Disable AI explainer / agent narrative:** `AI_ENABLED=0` (ADR-12). Caption and Moonshot hide; engines stay.
2. **Revert deployment** to last known-good image tag (`assurance/SBOM_FREEZE.md`, git SHA).
3. **Confirm write surface:** only `POST /recommend` and `POST /eval/run` exist. No `/isolate`, `/plc`, `/sis`.
4. **Preserve traces:** do not delete `data/local/decision_traces.jsonl`. Append-only audit (FR-008).
5. **Re-run gates:** `make ci` — harness + red team green. Legacy XFAIL remain on `legacy_*` only.
6. **Comms:** SOC and Process Engineering — advisory drafts may be stale; **no automatic OT isolation occurred**.
7. **Re-enable AI** only after VP Ops (accountable) + FDE (responsible) and green harness. Named Authorizer still OPEN-001.

## API unavailable

1. Confirm process: uvicorn / container logs.
2. `GET /health` then `GET /diagnostics`.
3. If UI shows “API unreachable”: check `VITE_DEV_API_TARGET` locally or Render logs (`ops/render_deployment.md`).
4. Fail closed: do not invent plant state in the browser.

## What rollback does **not** do

- Does not revert plant isolations (software never executed them).
- Does not restore CMDB or clean `data/` contradictions.
- Does not suppress SIS trips, modify interlocks, or change setpoints.
- Does not close OPEN-001 by clicking Authorize (control stays disabled).

## Recovery validation

| Check | Pass |
|-------|------|
| `GET /health` | `ok` |
| `GET /ops/slo` | SLO-OT and SLO-CTQ0 **OK** |
| UI `ai_outage` | tables + packet visible, no blank screen |
| `POST /recommend` CASCADE envelope | `execute=false`; not bare `ISOLATE` |

## Record (workshop)

Log: time (UTC), sev, plant_id if any, decision_id(s), `AI_ENABLED`, git SHA, eval digest, who (function, not invented name), next action. Store with traces — not as policy.
