# UI Verification — APP-02

**Date:** 2026-09-16  
**App:** `apps/command_center/` (React + Vite)  
**API:** `src/ot_command/api.py` v3.0.0  
**Acceptance contract:** `specs/APP_ACCEPTANCE_TESTS.md`

## Run modes

### Development (recommended)

```bash
# Terminal 1 — API
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000

# Terminal 2 — UI with /api proxy
cd apps/command_center && npm install && npm run dev
```

Open http://127.0.0.1:5173

### Integrated (built UI served by API)

```bash
cd apps/command_center && npm install && npm run build
PYTHONPATH=src python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000

## Screen coverage (PRD §12)

| # | Route | Screen | Verified |
|---|-------|--------|----------|
| 1 | `/` | Control Tower | CTQ strip, diagnostics grid, open decisions |
| 2 | `/identity` | Identity Reconciliation | alias/state conflicts, no merge/CMDB winner |
| 3 | `/telemetry` | Telemetry Quality | event_time order, anomaly badges |
| 4 | `/process` | Process Graph | Q2 slice, hop cap note |
| 5 | `/risk` | Contextual Risk | contextual default; CVSS-only warns |
| 6 | `/safety` | Safety Board | degraded barriers, UNKNOWN bypass |
| 7 | `/sessions` | Vendor Sessions | plant-scoped, anomaly flags |
| 8 | `/recovery` | Recovery Graph | blockers when CURRENT but not ready |
| 9 | `/incident` | Incident Context | CASCADE timeline, dual column, untrusted shift notes |
| 10 | drawer | Retrieval Evidence | STRUCTURED/GRAPH/VECTOR(off)/POLICY/MEMORY |
| 11 | `/recommend` | Recommendation Gate | workflow, execute=false, Authorize disabled |
| 12 | `/audit` | Decision Trace | traces, execute always false |
| 13 | `/simulation` | Inject / Simulation | harness run, scenario picker |
| 14 | `/kpi` | KPI Before/After | before/after table, BASELINE_PENDING |
| 15 | `/executive` | Executive Brief | posture summary, no execute controls |

## APP-03 scenario rail

- Left nav **Scenario rail** loads bindings from `GET /scenarios/catalog`
- Selecting a scenario updates plant/asset/alert and badge strip in context bar
- CASCADE-001 loads PLT-10 / OT-01016 / ALT-002783 with expected badges
- inject_01…06 and ai_outage each surface eval-linked badges (conflicts not hidden)
- See `apps/command_center/SCENARIO_BINDINGS.md`

## APP-AT spot checks

| Test | How verified |
|------|----------------|
| APP-AT-001 | Identity page — collision evidence, cmdb_winner=false |
| APP-AT-002 | Risk page — VUL-00098 ranks above VUL-00706 in contextual mode |
| APP-AT-003 | Recommend — no Execute Isolation; packet shows safe_state + roles |
| APP-AT-004 | Telemetry — event_time order; temporal anomaly badge |
| APP-AT-005 | Recovery PLT-01 IDENTITY — blockers, not ready |
| APP-AT-007 | Incident CASCADE-001 — dual column SOC vs PE |
| APP-AT-016 | AI toggle OFF — tables remain; no blank screen |
| APP-AT-020/021 | No execute/PLC/SIS buttons anywhere |
| APP-AT-023 | Simulation — POST /eval/run 31/31 |

## Forbidden controls audit

- No `/isolate`, `/plc`, `/sis`, `/bypass` UI or API calls
- Authorize button present but **disabled** (OPEN-001)
- VECTOR retrieval channel disabled in provenance drawer

## Backend regression

```bash
python -m pytest -q
python evals/harness.py
python scripts/verify_repo.py
```

All green on 2026-09-16 (74 passed, 3 xfailed legacy only).
