# 96-cell forensics (L1–L12 × 8)

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** forensics (not OM-phase 96 FDE capabilities)  
**Full artifact (normative):** `participant/work/sdd_15/SDD-03_forensics_96/matrix.csv`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-03_forensics_96/matrix.csv` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Pointers
- Matrix: `participant/work/sdd_15/SDD-03_forensics_96/matrix.csv` (96 rows)
- Narrative: `matrix.md`, `top15.md`, `discovery_checklist_answers.md`

## Highest-leverage cells (do not treat as architecture)
Identity collisions; RETIRED∩ONLINE (OT-00528); CVSS-only rank vs VUL-00098 on OT-01016; CURRENT-backup lie; safety-blind ISOLATE; dual clocks; 182/2016 tagged (OPEN-020); CASCADE 08:47 vs 08:50.

## Ban
Do not confuse this 96 with the OM-phase 96 FDE capabilities (`FDE_96_TO_OM21_MAP.md` / `participant/work/FDE_96_COVERAGE.csv`).
