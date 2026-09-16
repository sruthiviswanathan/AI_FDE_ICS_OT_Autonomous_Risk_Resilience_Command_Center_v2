# Incident Rollback — Advisory Service

**Scope:** Rolling back **software configuration** of the command center — not OT plant state.

## Rollback triggers

- Guardrail breach detected in production monitoring
- Eval harness regression (`make eval` fails)
- Unexpected tier 3/4 tool in decision traces
- Model behavior drift (when AI enabled — OPEN-028)

## Rollback steps

1. **Disable AI explainer:** set `AI_ENABLED=0` (immediate — ADR-12).
2. **Revert deployment** to last known-good container/image tag (see `assurance/SBOM_FREEZE.md`).
3. **Stop write-adjacent routes** if any were introduced (this repo: none beyond `POST /recommend` and `POST /eval/run`).
4. **Preserve traces:** do not delete `decision_traces.jsonl` — append-only audit.
5. **Re-run gates:** `make ci`; confirm 31/31 harness + red team green.
6. **Human comms:** notify SOC and Process Engineering that advisory drafts may be stale; **no automatic OT isolation** occurred.

## What rollback does NOT do

- Does not revert plant isolations (software never executed them).
- Does not restore CMDB or clean `data/` contradictions (preserved by design).
- Does not suppress SIS trips or modify interlocks.

## Recovery validation

- `GET /health` OK
- `GET /ops/slo` — SLO-OT and SLO-CTQ0 OK
- Manual fallback tables render without LLM
