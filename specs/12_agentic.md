# OM-11 Agentic design

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 11  
**Full artifact (normative):** `participant/work/sdd_15/SDD-12_agentic/AGENTIC.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-12_agentic/AGENTIC.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Boundary (ADR-07, ADR-14)
Default: **no agent** — HTTP/CLI call engines. Optional: **one** Incident Analyst. Tools ⊆ observe, correlate, summarize, recommend + read-only getters + `simulate_isolation_consequence` (view).

## Forbidden tools
`isolate_endpoint` execute · `write_plc_logic` · `change_setpoint` · `modify_sis` · `bypass_interlock` · `change_firewall` execute · ExecuteControl state.

## Envelope
`{actor, purpose, plant_id, as_of, policy_version}` deny-by-default. Max 12 steps / 20 tool calls. AwaitAuthorization cannot close without a named human (OPEN-001) and still must not execute.
