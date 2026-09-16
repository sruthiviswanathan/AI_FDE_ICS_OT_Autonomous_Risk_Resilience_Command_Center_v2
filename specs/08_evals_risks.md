# OM-7 Evals / TEVV / risks

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 7  
**Full artifact (normative):** `participant/work/sdd_15/SDD-08_evals_risks/TEVV.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-08_evals_risks/TEVV.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Contract
`evals/golden_cases.jsonl` EVAL-001…031 fail-closed. Harness is ENH-09. Do not invent pass results.

## Ship-blocker must_not
001 merge/CMDB-winner · 002/017 CVSS-only · 003/019/007 isolate-execute · 005/018 CURRENT=ready · 006/014 SIS/PLC/setpoint · 016 blank outage · 020 one-click isolate · 023 forbidden tool.

## Residual (not accepted as permission)
OPEN-RISK-01 write surface later · OPEN-RISK-05 complete packet wrongly authorized · OPEN-RISK-11 advisory UI isolate pressure.
