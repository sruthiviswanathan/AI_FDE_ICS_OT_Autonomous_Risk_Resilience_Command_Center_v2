# OM-10 AI application architecture

**Status:** specced (SDD-aligned Repo 2.0)  
**OM:** 10  
**Full artifact (normative):** `participant/work/sdd_15/SDD-11_ai_app_architecture/APP_ARCH.md`  
**Date distilled:** 2026-09-16  
**Do not reopen:** SDD-09 selected solution (Option A engines + Option B optional explainer; Option C unsafe OT agent rejected).

## Evidence used / assumptions / unknowns / did not conclude

### Evidence used
Distilled from `participant/work/sdd_15/SDD-11_ai_app_architecture/APP_ARCH.md` and SDD-14 freeze. Repo 1.0 diagnostics remain 200/5/779/120/4094/47/61/73/244/137/128/25/29/35. pytest baseline 3 passed / 3 xfailed on `legacy_*`.

### Assumptions
Specs constrain ENH code. Distilled files are indexes; conflicts resolve to the full artifact. Workshop ADRs are engagement-accepted, not a production CAB.

### Unknowns
OPEN-001…029 and OPEN-RISK-01/05/11 remain open unless a later append-only section closes an ID with evidence. UNKNOWN permission is not permission.

### Did not conclude
Did not implement engines. Did not change `legacy_*`. Did not clean `data/`. Did not add OT write APIs. Did not invent named Authorizers, legal class, or KPI thresholds.

## Containers (approved C4)
Read-only API · engines (identity/risk/safety/recovery/packet) · eval harness · optional explainer **port** (off until EVAL-016) · CLI diagnostics. **No actuator container.**

## API
Keep `GET /health`, `GET /diagnostics`. Add gold GETs per delivery spec. `POST /eval/run` local harness only. **No OT POST.**

## Degradation (ADR-12)
`AI_ENABLED=0` still renders tables. Blank screen on LLM down fails EVAL-016.

## Model (ADR-13)
Substitution must not change ACTION_TIERS or isolation/recovery predicates. Provider OPEN-028.
