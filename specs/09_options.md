# OM-8 Options and selected solution

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 8  
**Full artifact (normative):** `participant/work/sdd_15/SDD-09_options/OPTIONS.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-09_options/OPTIONS.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Selected
**Trusted Cyber-Physical Advisory Command Center.** Option **A** (deterministic engines) is always-on. Option **B** optional explainer after facts. AI-disabled = A.

## Rejected (do not implement)
Option C unsafe OT agent · autonomous isolation · multi-agent default · digital twin · decorative KG · buy-GRC as substitute for joins.

## ADR-KG
Bounded evidence-graph **view** (five queries). Persistence decided in SDD-10 (typed JSON). Vector = untrusted memory only.

**Do not reopen this selection in ENH.**
