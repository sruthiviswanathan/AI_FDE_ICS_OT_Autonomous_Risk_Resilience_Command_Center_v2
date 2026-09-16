# OM-6 Data and knowledge

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 6  
**Full artifact (normative):** `participant/work/sdd_15/SDD-07_data_knowledge/DATA.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-07_data_knowledge/DATA.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Trust
| Source | Role |
|---|---|
| `data/raw/*` | Workshop files; operational-truth UNKNOWN (OPEN-003) |
| `data/shadow/ot_asset_inventory_FINAL_v8.csv` | Evidence overlay, not CMDB |
| `data/shadow/shift_handover_email.txt` | Untrusted memory |
| `data/ot_legacy.db` | Six tables set-equal to CSV; unread by diagnostics; lineage OPEN-007 |

## Datasheets
`participant/work/sdd_15/SDD-07_data_knowledge/datasheets/` DS-assets … DS-shift_email (12).

## Contracts
Keep root `contracts/*`. Canonical gold schemas live under SDD-10 `schemas/`. Telemetry schema omits ingest_time/source/asset_id present on records (OPEN-009).
