# OM-13 Delivery specification

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 13  
**Full artifact (normative):** `participant/work/sdd_15/SDD-14_delivery_spec/DELIVERY_SPEC.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-14_delivery_spec/DELIVERY_SPEC.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Contract
`traceability/TRACEABILITY.csv` is C17. Untraced code is out of scope.

## Increments
| Increment | What | Must not |
|---|---|---|
| Repo 2.0 (this layout) | specs, ADRs, evals, gates, empty `modern/` | change `legacy_*`; clean data |
| Repo 3.0 / ENH-01…10 | parallel engines | OT writes; delete XFAIL until modern twins pass |

## SLOs (workshop; error budget 0 on safety)
SLO-OT 0 OT execute · SLO-CTQ0 0 write routes · SLO-ISO 100% drafts have safe_state+role · SLO-EVAL 100% must_not · SLO-LAT p95 <8s **without dropping joins**. Plant MTT OPEN-006.

## Backlog
ENH-01 identity · 02 telemetry · 03 risk · 04 safety · 05 recovery · 06 graph slice · 07 agent · 08 red team · 09 harness · 10 observability/SBOM/FinOps.
