# OM-9 Information architecture

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 9  
**Full artifact (normative):** `participant/work/sdd_15/SDD-10_information_architecture/INFO_ARCH.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-10_information_architecture/INFO_ARCH.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Layers
bronze (`data/`) → silver (joins, quality flags) → gold (identity/risk/safety/recovery/recommendation packets).

## Five graph queries (ADR-KG)
1 Identity lineage · 2 Undocumented path to HIGH/CRIT unit · 3 Safety–cyber join · 4 Recovery blockers · 5 CASCADE-001 slice. Hop cap 8. Missing tag→unit stays missing (1834 assets).

## Persistence (ADR-09)
Typed JSON / JSONL views. Not RDF. Not Neo4j-now.

## Anticorruption (ADR-10)
v1 `operationalState` is a **side-field**, not ObservedState (OPEN-009).

Schemas: `participant/work/sdd_15/SDD-10_information_architecture/schemas/`.
