# OM-2 Current state

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 2  
**Full artifact (normative):** `participant/work/sdd_15/SDD-02_current_state/CURRENT_STATE.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-02_current_state/CURRENT_STATE.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Freeze (as-is, not to-be)
- Landscape: Purdue-like documented stack **plus** 779 undocumented observed edges (`network_edges.csv`).
- Identity: 2016 assets; 200 ACTIVE vs OFFLINE/UNSEEN; 5 PASSIVE alias collisions; shadow spreadsheet 220 rows, **0** field diffs vs CMDB (OPEN-015).
- Telemetry: 31224 events; 4094 not GOOD; 120 duplicates; 47 F-on-TEMP.
- Safety: 61 barriers not ACTIVE; 73 proof not CURRENT; 860 HIGH/CRIT alerts would ISOLATE under `legacy_isolation_recommendation`.
- Recovery: `legacy_recovery_ready` is true iff backup CURRENT; 113/119 CURRENT rows are weak on restore/runbook/deps.
- Process mining is **file mining** (enterprise_events 6500; correlation_id empty 3251/6500 — OPEN-012).
- Shift email is **untrusted content**. Shadow inventory is **evidence**, not a new CMDB.

## C4 as-is
CLI + FastAPI `GET /health` + `GET /diagnostics` (14 collapsed ints). `legacy/risk.py` is the risk/recovery/isolate shim. No gold identity/risk/safety/recovery APIs.
