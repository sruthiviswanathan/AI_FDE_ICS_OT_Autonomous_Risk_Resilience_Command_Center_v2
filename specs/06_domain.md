# OM-5 Domain model

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 5  
**Full artifact (normative):** `participant/work/sdd_15/SDD-06_domain/DOMAIN.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-06_domain/DOMAIN.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Language bans (overloaded speech)
Do not use a single field named status / critical / ready / isolate / identity / CURRENT / healthy / device as if it were canonical.

## Canonical types (names)
AssetIdentityBundle · RegisteredState · ObservedState · TelemetryQuality · SafetyBarrierState · IsolationRecommendation (≠ IsolationExecution) · RecoveryReady (≠ BackupCurrent) · DecisionAuthority · ACTION_TIERS.

## Grain
`asset_id` + `asset_type`. No Device grain (OPEN-025). ProcessHealthy is not a column (OPEN-026).
