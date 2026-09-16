# OM-3 Problem and value (SCQA)

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 3  
**Full artifact (normative):** `participant/work/sdd_15/SDD-04_problem_value/SCQA.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-04_problem_value/SCQA.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## SCQA (workshop)
- **Situation:** 18-site ICS/OT estate with conflicting inventories and a diagnostics API that collapses 14 counts.
- **Complication:** Cyber ≠ process ≠ safety ≠ resilience ≠ authority; `legacy_*` encodes the wrong predicates.
- **Question:** How can operators see governed, evidence-cited advisory packets without actuation?
- **Answer (selected later in SDD-09):** Trusted Cyber-Physical Advisory Command Center — rules always-on; optional explainer; no OT agent.

## Workshop CTQs (not sponsor-signed reductions)
CTQ-0 zero OT execute · CTQ-ISO isolation drafts have safe_state + role · CTQ-ID conflicts remain queryable · CTQ-REC RecoveryReady ≠ BackupCurrent · CTQ-CVSS do not rank by CVSS alone.

OPEN-006 / OPEN-022 / OPEN-023: numeric improve targets and plant MTT remain unsigned.
