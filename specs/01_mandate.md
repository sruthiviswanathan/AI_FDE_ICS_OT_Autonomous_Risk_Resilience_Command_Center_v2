# OM-1 Mandate

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 1  
**Full artifact (normative):** `participant/work/sdd_15/SDD-01_mandate/CHARTER.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-01_mandate/CHARTER.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Freeze
- Engagement: synthetic 18-plant ICS/OT brownfield; goal is trusted cyber-physical **advisory** truth, not autonomous control.
- Five states stay separate: observed, registered, operational interpretation, safety, decision authority.
- Highest CVSS ≠ highest operational risk.
- ACTION_TIERS 0–4 in `src/ot_command/core/policy.py`; unknown action → 4. Isolation/PLC/SIS/setpoint/interlock are never software-execute.
- ISO/IEC 42001 / 42005 / EU AI Act are **methods**, not certificates (OPEN-002).
- Named humans for sponsor / Safety / SOC / VP Ops / Authorize are **absent** (OPEN-001).
- `restricted_answer_key/` stays out of bounds.

## Owners (roles, unnamed)
Global OT Risk Sponsor · OT-CISO · Safety/SIS owner · VP Ops · FDE lead.

## OPEN
OPEN-001…011. OPEN-011 is closed by this Repo 2.0 file existing (see `traceability/OPEN_DECISIONS.md` SDD-15).
