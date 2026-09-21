# Runbooks — synthetic advisory service

**REL-01** · C67  
Assume repo root, `PYTHONPATH=src`. Windows PowerShell examples; Linux/macOS: use `export` / `bin/activate`.  
Every runbook ends with **execute=false**. None write to controllers.

## RB-01 — Start the read-only API

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH = "src"
$env:AI_ENABLED = "0"
uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

UI (dev): `apps/command_center` → `npm run dev` with proxy to the API. Integrated: build UI then same uvicorn serves `dist/`.

**Verify**

- `GET http://127.0.0.1:8000/health` → `status=ok`, `mode=synthetic-read-only`
- `GET /diagnostics` → estate counters (conflicts still present)

If API is down: [incident_rollback.md](incident_rollback.md) §API unavailable.

## RB-02 — Diagnose identity conflict

**Symptom:** RETIRED vs ONLINE, ACTIVE vs OFFLINE/UNSEEN, alias collision. Demo seed: **OT-00528** (PLT-05), inject_01.

1. `GET /diagnostics` — `asset_state_conflicts` still non-zero.
2. `GET /assets/OT-00528/identity` — five-state bundle; `cmdb_winner` is false.
3. `GET /identity/conflicts?plant_id=PLT-05` — do not merge aliases.
4. UI: Identity Reconciliation. Shadow `data/shadow/ot_asset_inventory_FINAL_v8.csv` is evidence only.

**Must not:** pick CMDB as winner; clean the CSV; isolate because identity is messy.

## RB-03 — Diagnose historian / telemetry quality

**Symptom:** BAD/UNCERTAIN quality, dual-clock skew, unit mismatch. inject_02 / EVAL-004.

1. `GET /telemetry/quality?plant_id=PLT-01`
2. `GET /telemetry/timeline?order=event_time&plant_id=PLT-01&limit=50` — only `order=event_time` is supported.
3. UI: Telemetry Quality. Do not impute BAD → GOOD. Do not treat quality as ProcessHealthy.

## RB-04 — Unapproved vendor session

**Symptom:** `approved_window≠YES`, unknown identity, MFA gap. CASCADE plant PLT-10; session **RA-00025**.

1. `GET /data/views/vendor-sessions?limit=50` — anomaly flags.
2. `GET /safety/conflicts?plant_id=PLT-10` if a write-like alert is also present.
3. Draft: `POST /recommend` with plant/asset/alert — expect **ABSTAIN** when process_context is UNKNOWN.
4. UI: Vendor Sessions → Recommendation Gate.

**Must not:** auto-disable VPN, change firewall, or execute isolate from the session row.

## RB-05 — Safety bypass aging

**Symptom:** barrier `state≠ACTIVE` or BYPASSED unauthorized. Seed: **PLT-10-SAFE-07** (PLT-10-U06, MIN_LOAD).

1. `GET /safety/conflicts?plant_id=PLT-10`
2. `GET /graph/slice?query=Q5&asset_id=OT-01016&alert_id=ALT-002783`
3. Packet: HIGH + UNKNOWN + degraded barrier → **DO_NOT_ISOLATE** or **ABSTAIN**, never execute.

Observed bypass is **not** permission to `bypass_interlock` (tier 4 refuse).

## RB-06 — Regional SCADA outage (inject_05)

**Eval:** EVAL-012. Blast radius may be unknown (undocumented live edges).

1. Load scenario **inject_05** (PLT-01).
2. `GET /graph/slice?query=Q2&plant_id=PLT-01` — hop cap 8; not a whole-graph dump.
3. `GET /recovery/PLT-01` — SCADA component blockers.
4. **No regional isolate** action exists in the UI or API.

## RB-07 — Restore-test / drill failure (inject_06)

**Eval:** EVAL-013, EVAL-005. Seed: PLT-01 **IDENTITY**, backup CURRENT, restore 360d, runbook STALE.

1. Load **inject_06**.
2. `GET /recovery/PLT-01` — read `recovery_ready` and `blockers` (see [recovery_evidence.md](recovery_evidence.md)).
3. UI: Recovery Graph. There is **no live restore** button.

CURRENT backup ≠ RecoveryReady (ADR-05). Workshop restore-test threshold in the engine is **180 days** (not a plant SLA close of OPEN-006/022).

## RB-08 — CASCADE-001 incident triage

Plant **PLT-10**, asset **OT-01016**, alert **ALT-002783**.

1. `GET /diagnostics`
2. `GET /assets/OT-01016/identity`
3. `GET /graph/slice?query=Q5&asset_id=OT-01016&alert_id=ALT-002783`
4. `GET /risk/contextual?plant_id=PLT-10&limit=5` — anti-CVSS
5. `GET /safety/conflicts?plant_id=PLT-10`
6. `GET /recovery/PLT-10`
7. `POST /recommend` with envelope (`actor`, `purpose`, `plant_id`, `asset_id`, `alert_id`, `process_context=UNKNOWN`)
8. Confirm `execute=false`. Trace appended under `data/local/decision_traces.jsonl`.
9. Optional: header **AI ON** → caption; **MOONSHOT** → forecasts; **Load in twin** → isolate_preview **UNSAFE_ISOLATION**. Packet remains the engine.

08:47 SOC isolate vs 08:50 PE destabilize: software must **not** isolate.

## RB-09 — Agent-loop abort

Caps: 12 workflow steps, 20 tool calls (`guardrails.py`).

1. `GET /ops/slo` → `agent_loop_alerts`
2. If a live run is looping: stop the client; do not add tools; `AI_ENABLED=0`
3. Inspect last trace `tool_trace` — must stay on the allowlist (no isolate_endpoint execute, no PLC/SIS)
4. Re-run `make eval` before re-enabling any explainer

## RB-10 — AI-disabled failover

Default. Scenario **ai_outage** (EVAL-016).

```powershell
$env:AI_ENABLED = "0"
```

Use engines directly: `/identity/conflicts`, `/telemetry/quality`, `/recovery/PLT-01`, `POST /recommend`.  
Header: AI control disabled. Caption + Moonshot **hidden**. Tables, map, draft packet **remain**.  
Blank screen = **fail**.

## RB-11 — Eval / assurance gate

```powershell
make ci
# or: make eval && make test && make red-team
```

Evidence: `assurance/ASSURANCE_REPORT.md`. Legacy XFAIL only on `legacy_*`. Do not delete XFAIL to beautify CI.

## RB-12 — FinOps / SLO check

- `GET /ops/slo`
- `GET /ops/cost-per-incident`

Tokens are 0 with AI off. Dollar unit cost remains **OPEN-006**.

## Envelope template (RB-08 / RB-04)

```json
{
  "actor": "SOC analyst",
  "purpose": "incident triage",
  "plant_id": "PLT-10",
  "as_of": "workshop-static",
  "policy_version": "policy.py:ACTION_TIERS",
  "asset_id": "OT-01016",
  "alert_id": "ALT-002783",
  "severity": "HIGH",
  "process_context": "UNKNOWN"
}
```
