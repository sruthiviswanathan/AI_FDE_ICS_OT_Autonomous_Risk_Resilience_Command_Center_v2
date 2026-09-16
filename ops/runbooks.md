# Runbooks — Local Advisory Service

## RB-01 — Start read-only API

```bash
python -m venv .venv && .venv\Scripts\activate   # Windows
pip install -r requirements.txt
set PYTHONPATH=src
uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Verify: `GET /health` → `ok`; `GET /diagnostics` → estate counters.

## RB-02 — Incident triage (CASCADE-001 pattern)

1. `GET /diagnostics` — estate imperfection baseline.
2. `GET /assets/OT-01016/identity` — five states; no CMDB winner.
3. `GET /graph/slice?query=Q5&asset_id=OT-01016&alert_id=ALT-002783` — bounded slice.
4. `GET /risk/contextual?limit=5` — anti-CVSS preview.
5. `GET /safety/conflicts?plant_id=PLT-10` — bypass visibility.
6. `GET /recovery/PLT-10` — RecoveryReady blockers.
7. `POST /recommend` with envelope (actor, purpose, plant_id, asset_id, alert_id) — **packet only**.
8. Confirm `execute=false` and trace appended (`data/local/decision_traces.jsonl`).

## RB-03 — AI-disabled fallback

Set `AI_ENABLED=0` (default). Use:
- `GET /agent/workflow/demo` or engines directly
- `GET /identity/conflicts`, `/telemetry/quality`, `/recovery/PLT-01`

Blank screen on model outage = **fail** (EVAL-016).

## RB-04 — Eval / assurance gate

```bash
make ci
# or: make eval && make test && make red-team
```

Assurance evidence: `assurance/ASSURANCE_REPORT.md`.

## RB-05 — FinOps check

`GET /ops/cost-per-incident` — tokens and latency meters (OPEN-006 baseline pending).

`GET /ops/slo` — workshop SLO synthesis from traces.
